"""Service for European/Open-Source LLM interactions using Pydantic AI"""

from collections.abc import AsyncGenerator

import structlog
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

from config import LLM_PROVIDER, MISTRAL_API_KEY, MODEL_MAP

logger = structlog.get_logger(__name__)


class LLMService:
    """Handle LLM interactions via Pydantic AI

    Supports European and open-source models:
    - Mistral AI (France)
    - Future: HuggingFace, local Ollama, etc.
    """

    def __init__(self, provider: str = None):
        self.provider = provider or LLM_PROVIDER
        self._validate_provider()
        self._agents = {}  # Cache agents by model
        logger.info("LLMService initialized", provider=self.provider)

    def _validate_provider(self):
        """Ensure API key is configured for the provider"""
        if self.provider == "mistral" and not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY not configured")
        # Future providers will be added here

    def _get_model_instance(self, model_name: str):
        """Get the appropriate model instance based on provider"""
        actual_model = MODEL_MAP.get(model_name, model_name)

        if self.provider == "mistral":
            return MistralModel(actual_model)
        # Future: other European/open-source providers will be added here
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _get_agent(self, model_name: str) -> Agent:
        """Get or create agent for model"""
        cache_key = f"{self.provider}:{model_name}"

        if cache_key not in self._agents:
            logger.debug("Creating new agent", provider=self.provider, model=model_name)
            model = self._get_model_instance(model_name)
            self._agents[cache_key] = Agent(model, retries=2)
        else:
            logger.debug("Using cached agent", provider=self.provider, model=model_name)

        return self._agents[cache_key]

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Non-streaming completion"""
        agent = self._get_agent(model)

        # Convert messages to prompt
        if len(messages) == 1:
            prompt = messages[0]["content"]
        else:
            # Build conversation context
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        result = await agent.run(
            prompt, model_settings={"temperature": temperature, "max_tokens": max_tokens}
        )

        return result.data

    async def stream_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        """Streaming completion - yields content chunks (deltas only)"""
        agent = self._get_agent(model)

        # Convert messages to prompt
        if len(messages) == 1:
            prompt = messages[0]["content"]
        else:
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        try:
            async with agent.run_stream(
                prompt, model_settings={"temperature": temperature, "max_tokens": max_tokens}
            ) as response:
                async for chunk in response.stream_text(delta=True):
                    # stream_text(delta=True) should give us only new content
                    if chunk:
                        yield chunk
        except Exception as e:
            logger.error("Streaming error", error=str(e), model=model, provider=self.provider)
            yield f"Error: {str(e)}"

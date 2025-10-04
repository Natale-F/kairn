"""Service for Mistral AI using Pydantic AI"""
from typing import List, Dict, AsyncGenerator
from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel

from config import MISTRAL_API_KEY, MODEL_MAP


class MistralService:
    """Handle all Mistral AI interactions via Pydantic AI"""
    
    def __init__(self):
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY not configured")
        
        self.api_key = MISTRAL_API_KEY
        self._agents = {}  # Cache agents by model
    
    def _get_agent(self, model_name: str) -> Agent:
        """Get or create agent for model"""
        mistral_model = MODEL_MAP.get(model_name, "mistral-small-latest")
        
        if mistral_model not in self._agents:
            # Pydantic AI lit automatically MISTRAL_API_KEY from the env
            self._agents[mistral_model] = Agent(
                MistralModel(mistral_model),
                retries=2
            )
        
        return self._agents[mistral_model]
    
    async def generate_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """Non-streaming completion"""
        agent = self._get_agent(model)
        
        # Convert messages to prompt (simple case)
        if len(messages) == 1:
            prompt = messages[0]["content"]
        else:
            # Build conversation context
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        result = await agent.run(
            prompt,
            model_settings={
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )
        
        return result.data
    
    async def stream_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
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
                prompt,
                model_settings={
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            ) as response:
                async for chunk in response.stream_text(delta=True):
                    # stream_text(delta=True) should give us only new content
                    if chunk:
                        yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"

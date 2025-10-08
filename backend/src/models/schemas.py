"""Pydantic models for request/response validation"""

from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message"""

    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class GenerateRequest(BaseModel):
    """Ollama /api/generate request"""

    model: str = Field(default="mistral-large", description="Model name")
    prompt: str = Field(..., description="Input prompt")
    stream: bool = Field(default=True, description="Stream response")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=32000)


class ChatRequest(BaseModel):
    """Ollama /api/chat request"""

    model: str = Field(default="mistral-large", description="Model name")
    messages: list[Message] = Field(..., description="Conversation history")
    stream: bool = Field(default=True, description="Stream response")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=32000)


class PullRequest(BaseModel):
    """Ollama /api/pull request"""

    name: str = Field(..., description="Model name to pull")


class OllamaResponse(BaseModel):
    """Standard Ollama response"""

    model: str
    created_at: str
    response: str | None = None
    message: dict[str, str] | None = None
    done: bool


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    service: str
    mistral_api_configured: bool


class ModelsResponse(BaseModel):
    """List of available models"""

    models: list[dict[str, Any]]

"""Pydantic models for request/response validation"""

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message"""

    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """OpenAI-compatible chat completions request"""

    model: str = Field(default="mistral-large", description="Model name")
    messages: list[Message] = Field(..., description="Conversation history")
    stream: bool = Field(default=True, description="Stream response")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=32000)


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    service: str
    mistral_api_configured: bool

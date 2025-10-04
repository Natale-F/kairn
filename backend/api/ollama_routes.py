"""Ollama-compatible API routes"""
import json
import time
from typing import AsyncGenerator
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse

from config import AVAILABLE_MODELS, MODEL_MAP
from models.schemas import (
    GenerateRequest,
    ChatRequest,
    PullRequest,
    ModelsResponse,
    OllamaResponse
)
from services.mistral_service import MistralService

router = APIRouter(prefix="/api", tags=["Ollama"])


@router.get("/tags", response_model=ModelsResponse)
async def list_models():
    """List available models (Ollama format)"""
    return {"models": AVAILABLE_MODELS}


@router.post("/generate")
async def generate(request: GenerateRequest):
    """Ollama-compatible /api/generate endpoint with streaming"""
    service = MistralService()
    
    # Convert prompt to messages
    messages = [{"role": "user", "content": request.prompt}]
    
    if not request.stream:
        # Non-streaming response
        content = await service.generate_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return OllamaResponse(
            model=request.model,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            response=content,
            done=True
        )
    
    # Streaming response
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            async for content in service.stream_completion(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                # Check if it's an error
                if content.startswith("{") and "error" in content:
                    yield content + "\n"
                    return
                
                # Send Ollama-format chunk
                yield json.dumps({
                    "model": request.model,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "response": content,
                    "done": False,
                }) + "\n"
            
            # Send final done message
            yield json.dumps({
                "model": request.model,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "response": "",
                "done": True,
            }) + "\n"
            
        except Exception as e:
            yield json.dumps({"error": f"Error: {str(e)}"}) + "\n"
    
    return StreamingResponse(generate_stream(), media_type="application/x-ndjson")


@router.post("/chat")
async def chat(request: ChatRequest):
    """Ollama-compatible /api/chat endpoint with streaming"""
    service = MistralService()
    
    # Convert Pydantic models to dict
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    if not request.stream:
        # Non-streaming response
        content = await service.generate_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return OllamaResponse(
            model=request.model,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            message={"role": "assistant", "content": content},
            done=True
        )
    
    # Streaming response
    async def chat_stream() -> AsyncGenerator[str, None]:
        try:
            async for content in service.stream_completion(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                # Check if it's an error
                if content.startswith("{") and "error" in content:
                    yield content + "\n"
                    return
                
                # Send Ollama-format chunk
                yield json.dumps({
                    "model": request.model,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "message": {"role": "assistant", "content": content},
                    "done": False,
                }) + "\n"
            
            # Send final done message
            yield json.dumps({
                "model": request.model,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "message": {"role": "assistant", "content": ""},
                "done": True,
            }) + "\n"
            
        except Exception as e:
            yield json.dumps({"error": f"Error: {str(e)}"}) + "\n"
    
    return StreamingResponse(chat_stream(), media_type="application/x-ndjson")


@router.post("/pull")
async def pull_model(request: PullRequest):
    """Mock /api/pull endpoint (models accessed via Mistral API)"""
    if request.name not in MODEL_MAP:
        return JSONResponse(
            status_code=404,
            content={"error": f"Model {request.name} not found"}
        )
    
    # Simulate success (no actual download)
    return JSONResponse({
        "status": "success",
        "digest": "sha256:abc123",
        "total": 1000000,
        "completed": 1000000,
    })

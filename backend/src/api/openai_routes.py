"""OpenAI-compatible API routes"""

import json
import time
from collections.abc import AsyncGenerator

import structlog
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from config import AVAILABLE_MODELS
from models.schemas import ChatRequest
from services.llm_service import LLMService

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["OpenAI"])


@router.get("/v1/models")
@router.get("/models")
async def list_openai_models():
    """List available models (OpenAI format)"""
    models = [
        {
            "id": model["name"],
            "object": "model",
            "created": int(time.time()),
            "owned_by": "mistral-ai",
        }
        for model in AVAILABLE_MODELS
    ]
    return {"data": models, "object": "list"}


@router.post("/v1/chat/completions")
@router.post("/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible /v1/chat/completions endpoint"""
    logger.debug(
        "Chat completions request",
        model=request.model,
        stream=request.stream,
        messages_count=len(request.messages),
    )
    service = LLMService()

    # Convert Pydantic models to dict
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

    if not request.stream:
        # Non-streaming response
        content = await service.generate_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }

    # Streaming response
    async def openai_stream() -> AsyncGenerator[str, None]:
        chunk_count = 0
        try:
            logger.info("Starting OpenAI stream", model=request.model)

            async for content in service.stream_completion(
                messages=messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                # Check if it's an error
                if content.startswith("{") and "error" in content:
                    logger.error("Stream error detected", error=content)
                    yield f"data: {content}\n\n"
                    yield "data: [DONE]\n\n"
                    return

                chunk_count += 1

                # Send OpenAI-format chunk
                chunk = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": request.model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"role": "assistant", "content": content},
                            "finish_reason": None,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk)}\n\n"

            # Send final done message
            logger.info("OpenAI stream completed", chunks=chunk_count)
            final_chunk = {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error("OpenAI stream exception", error=str(e), exc_info=True)
            error_data = {"error": {"message": str(e), "type": "server_error"}}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(openai_stream(), media_type="text/event-stream")


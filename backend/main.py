"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, MISTRAL_API_KEY
from api.ollama_routes import router as ollama_router

# Create FastAPI app
app = FastAPI(
    title="French Sovereign Chatbot Backend",
    description="Ollama-compatible API for Mistral AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ollama_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "French Sovereign Chatbot Backend (Ollama-compatible)",
        "version": "1.0.0",
        "mistral_api_configured": bool(MISTRAL_API_KEY),
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api": {
            "mistral": bool(MISTRAL_API_KEY)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""Configuration centralisée de l'application"""

import os

import structlog
from dotenv import load_dotenv

load_dotenv()

logger = structlog.get_logger(__name__)

# LLM Provider Configuration (European/Open-Source models)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral")  # Default: Mistral AI (France)

# API Configuration
MISTRAL_API_URL = "https://api.mistral.ai/v1"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
# Future providers:
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# CORS Origins (allow Open WebUI on various ports)
CORS_ORIGINS = [
    "http://localhost:3000",  # Open WebUI (mapped from 8080)
    "http://localhost:8080",  # Open WebUI (direct)
    "http://localhost:3001",
    FRONTEND_URL,
    "*",  # Allow all origins for Ollama compatibility
]

# Model Mapping (Mistral sovereign models)
MODEL_MAP = {
    "mistral-large": "mistral-large-latest",
    "mistral-large:latest": "mistral-large-latest",
    "mistral-medium": "mistral-medium-latest",
    "mistral-medium:latest": "mistral-medium-latest",
}

# Default models exposed to frontend (Ollama format)
AVAILABLE_MODELS = [
    {
        "name": "mistral-large",
        "model": "mistral-large",
        "modified_at": "2024-01-01T00:00:00Z",
        "size": 123456789,
        "digest": "sha256:abc123",
        "details": {
            "parent_model": "",
            "format": "mistral",
            "family": "mistral",
            "families": ["mistral"],
            "parameter_size": "70B",
            "quantization_level": "Q4_0",
        },
    },
    {
        "name": "mistral-medium",
        "model": "mistral-medium",
        "modified_at": "2024-01-01T00:00:00Z",
        "size": 67890123,
        "digest": "sha256:xyz789",
        "details": {
            "parent_model": "",
            "format": "mistral",
            "family": "mistral",
            "families": ["mistral"],
            "parameter_size": "22B",
            "quantization_level": "Q4_0",
        },
    },
]

# Validation
if not MISTRAL_API_KEY:
    logger.warning("MISTRAL_API_KEY not configured", env_file=".env")

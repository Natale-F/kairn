"""Configuration centralisée de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
MISTRAL_API_URL = "https://api.mistral.ai/v1"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# CORS Origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    FRONTEND_URL,
]

# Model Mapping (Mistral sovereign models)
MODEL_MAP = {
    "mistral-large": "mistral-large-latest",
    "mistral-medium": "mistral-medium-latest",
    "mistral-small": "mistral-small-latest",
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
            "quantization_level": "Q4_0"
        }
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
            "quantization_level": "Q4_0"
        }
    },
    {
        "name": "mistral-small",
        "model": "mistral-small",
        "modified_at": "2024-01-01T00:00:00Z",
        "size": 45678901,
        "digest": "sha256:def456",
        "details": {
            "parent_model": "",
            "format": "mistral",
            "family": "mistral",
            "families": ["mistral"],
            "parameter_size": "7B",
            "quantization_level": "Q4_0"
        }
    }
]

# Validation
if not MISTRAL_API_KEY:
    print("⚠️  WARNING: MISTRAL_API_KEY is not set in .env file")

# Backend - European/Open-Source Chatbot API

FastAPI backend with Ollama-compatible API supporting European and open-source LLM providers.

## 🌍 Supported Providers

Currently supported:
- **Mistral AI** 🇫🇷 (France) - Default provider

Planned:
- **HuggingFace** 
- **Ollama** (Local models)

## 🏗️ Architecture

```
backend/
├── api/                    # API Routes
│   └── ollama_routes.py   # Ollama-compatible endpoints
├── models/                 # Pydantic Models
│   └── schemas.py         # Request/Response validation
├── services/               # Business Logic
│   └── llm_service.py     # Generic LLM service (Pydantic AI)
├── config.py              # Centralized configuration
├── main.py                # FastAPI entry point
└── requirements.txt       # Python dependencies
```

## Quick Start

### With Docker (Recommended)

```bash
# From project root
docker-compose up -d backend
```

### Development Mode

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
export MISTRAL_API_KEY=your_key_here
export LLM_PROVIDER=mistral

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_PROVIDER` | LLM provider to use | `mistral` | ❌ |
| `MISTRAL_API_KEY` | Mistral AI API key | - | ✅ (if using Mistral) |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` | ❌ |

Get your Mistral API key: https://console.mistral.ai/

## API Endpoints

### Health Check
- `GET /` - Service status
- `GET /health` - Detailed health check

### Ollama-Compatible API
- `GET /api/tags` - List available models
- `POST /api/generate` - Text generation (streaming/non-streaming)
- `POST /api/chat` - Conversational chat (streaming/non-streaming)
- `POST /api/pull` - Mock endpoint (models via API)

**Interactive Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Automated Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
make test
# or
pytest tests

# Run with coverage report
make test-cov

# Run specific test suites
make test-unit    # Unit tests only
make test-api     # API tests only

# Code quality
make lint         # Check code with ruff
make format       # Format code with ruff
make check        # Lint + tests
```

**Test Coverage:**
- ✅ LLM Service (unit tests)
- ✅ API Endpoints (integration tests)
- ✅ Error handling and validation
- ✅ Streaming and non-streaming responses

See `tests/README.md` for detailed testing documentation.

### Manual Testing

```bash
# Health check
curl http://localhost:8000/

# List models
curl http://localhost:8000/api/tags

# Chat test (streaming)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large",
    "messages": [{"role": "user", "content": "Bonjour!"}],
    "stream": true
  }'

# Chat test (non-streaming)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

## Production

### Docker Build

```bash
docker build -t chatbot-backend .
docker run -d -p 8000:8000 \
  -e MISTRAL_API_KEY=your_key \
  -e LLM_PROVIDER=mistral \
  chatbot-backend
```

### Features
- **Multi-stage build** for smaller image size
- **Layer caching** optimization
- **Non-root user** for security
- **Health checks** configured

## Adding a New Provider

To add a new European/open-source provider:

1. **Add API key to `config.py`:**
```python
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
```

2. **Update `LLMService` in `services/llm_service.py`:**
```python
def _get_model_instance(self, model_name: str):
    if self.provider == "huggingface":
        from pydantic_ai.models.huggingface import HuggingFaceModel
        return HuggingFaceModel(actual_model)
```

3. **Set environment variable:**
```bash
export LLM_PROVIDER=huggingface
export HUGGINGFACE_API_KEY=your_key
```

## Performance

- **Async/await** throughout for high concurrency
- **Agent caching** per provider:model
- **Streaming support** for real-time responses
- **Pydantic AI** for provider abstraction

## Debugging

```bash
# Detailed logs
uvicorn main:app --log-level debug

# Auto-reload on changes
uvicorn main:app --reload

# Direct Python execution
python main.py
```

## Key Dependencies

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `pydantic-ai` - LLM provider abstraction
- `pydantic` - Data validation
- `python-dotenv` - Environment management

## Code Structure

1. **api/** - Route handlers only, no business logic
2. **services/** - Isolated business logic (LLM interactions)
3. **models/** - Pydantic schemas for validation
4. **config.py** - Single source of truth for configuration

## License

See LICENSE at project root.
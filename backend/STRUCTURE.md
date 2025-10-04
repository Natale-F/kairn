# 📂 Structure du Backend

## Arborescence

```
backend/
│
├── 📋 Configuration & Entry Point
│   ├── config.py              # Configuration centralisée (API keys, models, CORS)
│   ├── main.py                # Point d'entrée FastAPI (app, middlewares, routers)
│   └── run.py                 # Script de lancement dev (uvicorn --reload)
│
├── 🔌 API Routes
│   └── api/
│       ├── __init__.py
│       └── ollama_routes.py   # Routes Ollama-compatible (/api/tags, /api/chat, etc.)
│
├── 📦 Data Models
│   └── models/
│       ├── __init__.py
│       └── schemas.py         # Modèles Pydantic (validation + docs auto)
│
├── 🔧 Business Logic
│   └── services/
│       ├── __init__.py
│       └── mistral_service.py # Service Mistral AI (API calls, streaming)
│
├── 🐳 Docker
│   ├── Dockerfile             # Multi-stage optimisé (base + production)
│   └── .dockerignore          # Exclusions Docker
│
└── 📚 Documentation
    ├── README.md              # Documentation générale backend
    ├── API.md                 # Documentation API détaillée
    ├── STRUCTURE.md           # Ce fichier
    └── requirements.txt       # Dépendances Python
```

## 🎯 Responsabilités par fichier

### `config.py` - Configuration centralisée
```python
✓ Variables d'environnement (MISTRAL_API_KEY, etc.)
✓ Mapping des modèles (mistral-large → mistral-large-latest)
✓ Liste des modèles exposés (format Ollama)
✓ CORS origins
✗ Pas de logique métier
✗ Pas d'appels API
```

### `main.py` - Application FastAPI
```python
✓ Création de l'app FastAPI
✓ Configuration CORS middleware
✓ Enregistrement des routers
✓ Health check endpoint (/)
✗ Pas de routes métier
✗ Pas de logique dans les endpoints
```

### `api/ollama_routes.py` - Routes API
```python
✓ Définition des routes FastAPI
✓ Validation automatique (Pydantic)
✓ Délégation aux services
✓ Transformation de réponses
✗ Pas d'appels directs à Mistral
✗ Pas de logique complexe
```

### `models/schemas.py` - Validation
```python
✓ Modèles Pydantic (ChatRequest, GenerateRequest, etc.)
✓ Validation des types
✓ Documentation OpenAPI automatique
✓ Valeurs par défaut
✗ Pas de logique métier
✗ Pas d'appels externes
```

### `services/mistral_service.py` - Logique métier
```python
✓ Communication avec Mistral AI
✓ Gestion du streaming (SSE → NDJSON)
✓ Mapping des modèles
✓ Gestion des erreurs
✓ Logique métier isolée
✗ Pas de routes FastAPI
```

## 🔄 Flow d'une requête

```
1. Request arrives
   └─> main.py (FastAPI app)

2. Route matching
   └─> api/ollama_routes.py
       ├─> @router.post("/api/chat")
       └─> Validation automatique (Pydantic)

3. Request validated
   └─> models/schemas.py
       └─> ChatRequest(model, messages, stream, ...)

4. Business logic
   └─> services/mistral_service.py
       ├─> MistralService.stream_completion()
       ├─> Call Mistral API
       └─> Transform SSE → NDJSON

5. Response streamed
   └─> api/ollama_routes.py
       └─> StreamingResponse(chat_stream(), media_type="application/x-ndjson")

6. Client receives
   └─> NDJSON chunks
```

## 📊 Séparation des préoccupations

| Couche | Responsabilité | Dépendances |
|--------|---------------|-------------|
| **main.py** | Configuration app | FastAPI, config |
| **api/** | Routes HTTP | FastAPI, models, services |
| **models/** | Validation données | Pydantic |
| **services/** | Logique métier | httpx, config |
| **config.py** | Configuration | os, dotenv |

## 🧪 Testabilité

Chaque couche est testable indépendamment :

```python
# Test du service (mock httpx)
service = MistralService()
result = await service.generate_completion(messages, model)

# Test des routes (mock service)
response = client.post("/api/chat", json=payload)

# Test des modèles (validation)
request = ChatRequest(**data)
```

## 🔧 Extension

### Ajouter un nouveau modèle
```python
# config.py
MODEL_MAP["mistral-tiny"] = "mistral-tiny-latest"
AVAILABLE_MODELS.append({...})
```

### Ajouter une route
```python
# api/ollama_routes.py
@router.post("/api/new-endpoint")
async def new_endpoint(request: NewRequest):
    service = MistralService()
    result = await service.new_method()
    return result
```

### Ajouter un service
```python
# services/new_service.py
class NewService:
    def __init__(self):
        pass
    
    async def do_something(self):
        pass
```

## 📦 Dépendances

```
main.py
  ├── config.py
  └── api/ollama_routes.py
       ├── models/schemas.py
       └── services/mistral_service.py
            └── config.py
```

Pas de dépendances circulaires ✅

## 🚀 Démarrage

### Dev
```bash
python run.py
# ou
uvicorn main:app --reload
```

### Docker
```bash
docker build -t backend .
docker run -p 8000:8000 -e MISTRAL_API_KEY=xxx backend
```

### Tests
```bash
# Tests unitaires (à implémenter)
pytest tests/

# Tests d'intégration
curl http://localhost:8000/api/tags
```

## 📈 Métriques de qualité

- ✅ Séparation claire des responsabilités
- ✅ Pas de code dupliqué
- ✅ Configuration centralisée
- ✅ Validation automatique
- ✅ Gestion d'erreurs
- ✅ Async/await partout
- ✅ Type hints Python
- ✅ Documentation automatique (OpenAPI)

## 🔍 Points d'attention

### Sécurité
- ✅ Non-root user dans Docker
- ✅ Pas de secrets hardcodés
- ✅ CORS configuré
- ⚠️ Rate limiting (à implémenter)

### Performance
- ✅ Async I/O
- ✅ Streaming (pas de buffer)
- ⚠️ Caching (à implémenter)
- ⚠️ Connection pooling (httpx le fait)

### Monitoring
- ✅ Health check endpoint
- ⚠️ Logs structurés (à améliorer)
- ⚠️ Métriques Prometheus (à ajouter)

---

**Architecture propre ✨ Prête pour la production 🚀**

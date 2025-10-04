# Backend API Documentation

## 🎯 Overview

Ce backend FastAPI expose une **API compatible Ollama** qui traduit les requêtes vers Mistral AI.

## 🔗 Endpoints

### Health Check

```http
GET /
```

**Response:**
```json
{
  "status": "ok",
  "service": "French Sovereign Chatbot Backend (Ollama-compatible)",
  "mistral_api_configured": true
}
```

---

### List Models (Ollama-compatible)

```http
GET /api/tags
```

Liste les modèles disponibles au format Ollama.

**Response:**
```json
{
  "models": [
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
}
```

---

### Generate (Ollama-compatible)

```http
POST /api/generate
```

Génération de texte à partir d'un prompt (streaming ou non).

**Request Body:**
```json
{
  "model": "mistral-large",
  "prompt": "Explique-moi la souveraineté numérique",
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Response (streaming, NDJSON):**
```json
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","response":"La souveraineté","done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","response":" numérique","done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","response":"...","done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","response":"","done":true}
```

**Response (non-streaming):**
```json
{
  "model": "mistral-large",
  "created_at": "2024-01-01T12:00:00Z",
  "response": "La souveraineté numérique est...",
  "done": true
}
```

---

### Chat (Ollama-compatible)

```http
POST /api/chat
```

Chat conversationnel avec historique (streaming ou non).

**Request Body:**
```json
{
  "model": "mistral-large",
  "messages": [
    {
      "role": "system",
      "content": "Tu es un assistant spécialisé en souveraineté numérique."
    },
    {
      "role": "user",
      "content": "Pourquoi Mistral AI ?"
    }
  ],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 4096
}
```

**Response (streaming, NDJSON):**
```json
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","message":{"role":"assistant","content":"Mistral"},"done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","message":{"role":"assistant","content":" AI"},"done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","message":{"role":"assistant","content":"..."},"done":false}
{"model":"mistral-large","created_at":"2024-01-01T12:00:00Z","message":{"role":"assistant","content":""},"done":true}
```

**Response (non-streaming):**
```json
{
  "model": "mistral-large",
  "created_at": "2024-01-01T12:00:00Z",
  "message": {
    "role": "assistant",
    "content": "Mistral AI est un fournisseur français..."
  },
  "done": true
}
```

---

### Pull Model (Mock)

```http
POST /api/pull
```

Mock endpoint pour la compatibilité Ollama. Retourne succès immédiat (pas de téléchargement réel).

**Request Body:**
```json
{
  "name": "mistral-large"
}
```

**Response:**
```json
{
  "status": "success",
  "digest": "sha256:abc123",
  "total": 1000000,
  "completed": 1000000
}
```

---

## 🔄 Translation Flow

### Ollama Request → Mistral API

Le backend traduit automatiquement :

| Ollama Format | Mistral API Format |
|--------------|-------------------|
| `model: "mistral-large"` | `model: "mistral-large-latest"` |
| `model: "mistral-small"` | `model: "mistral-small-latest"` |
| `prompt: "text"` | `messages: [{"role": "user", "content": "text"}]` |
| NDJSON streaming | SSE streaming |

### Mistral API Response → Ollama Format

Streaming SSE de Mistral :
```
data: {"choices":[{"delta":{"content":"Hello"}}]}
data: [DONE]
```

Devient NDJSON Ollama :
```json
{"model":"mistral-large","response":"Hello","done":false}
{"model":"mistral-large","response":"","done":true}
```

---

## 🔐 Authentication

Le backend utilise `MISTRAL_API_KEY` depuis les variables d'environnement :

```bash
MISTRAL_API_KEY=votre_cle_api
```

Pas d'authentification exposée au frontend (le backend gère tout).

---

## 🚨 Error Handling

### 500 - API Key Missing
```json
{
  "detail": "MISTRAL_API_KEY not configured"
}
```

### 504 - Timeout
```json
{
  "detail": "Mistral API timeout"
}
```

### 500 - Mistral API Error
```json
{
  "detail": "Mistral API error: <error_message>"
}
```

---

## 🧪 Testing

### Test Health Check
```bash
curl http://localhost:8000/
```

### Test Models List
```bash
curl http://localhost:8000/api/tags
```

### Test Chat (streaming)
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": true
  }'
```

### Test Generate (non-streaming)
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large",
    "prompt": "Explique-moi Docker",
    "stream": false
  }'
```

---

## 📖 Interactive Docs

FastAPI génère automatiquement de la documentation interactive :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## 🔧 CORS Configuration

Le backend autorise les requêtes depuis :
- `http://localhost:3000` (dev)
- `http://localhost:3001`
- Variable `FRONTEND_URL` (custom)

Pour ajouter d'autres origines, modifiez `main.py` :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://votre-domaine.com",
    ],
    ...
)
```

---

## 📊 Performance

### Timeouts
- Requêtes HTTP vers Mistral : 60 secondes
- Streaming : pas de timeout (jusqu'à `[DONE]`)

### Rate Limiting
Géré par Mistral AI (voir [documentation](https://docs.mistral.ai/))

---

## 🆘 Troubleshooting

### Le backend ne démarre pas
```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Vérifier la clé API
echo $MISTRAL_API_KEY
```

### Erreurs 500
```bash
# Voir les logs détaillés
uvicorn main:app --reload --log-level debug
```

### Frontend ne reçoit pas de réponse
- Vérifier CORS (voir logs)
- Vérifier que `OLLAMA_URL` pointe vers le bon backend
- Tester l'endpoint directement avec `curl`

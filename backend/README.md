# Backend - French Sovereign Chatbot

Backend FastAPI avec API compatible Ollama pour Mistral AI.

## 🏗️ Architecture

```
backend/
├── api/                    # Routes API
│   ├── __init__.py
│   └── ollama_routes.py   # Routes Ollama-compatible
├── models/                 # Modèles Pydantic
│   ├── __init__.py
│   └── schemas.py         # Schémas de validation
├── services/               # Logique métier
│   ├── __init__.py
│   └── mistral_service.py # Service Mistral AI
├── config.py              # Configuration centralisée
├── main.py                # Point d'entrée FastAPI
├── requirements.txt       # Dépendances Python
└── Dockerfile            # Image Docker optimisée
```

## 🚀 Démarrage rapide

### Avec Docker (recommandé)

```bash
# Depuis la racine du projet
docker-compose up -d backend
```

### Mode développement

```bash
cd backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
export MISTRAL_API_KEY=your_key_here

# Lancer le serveur
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Variables d'environnement

| Variable | Description | Requis |
|----------|-------------|--------|
| `MISTRAL_API_KEY` | Clé API Mistral AI | ✅ Oui |
| `FRONTEND_URL` | URL du frontend pour CORS | ❌ Non (default: localhost:3000) |

## 🔌 Endpoints

### Health Check
- `GET /` - Status général
- `GET /health` - Health check détaillé

### Ollama-compatible API
- `GET /api/tags` - Liste des modèles
- `POST /api/generate` - Génération de texte
- `POST /api/chat` - Chat conversationnel
- `POST /api/pull` - Mock endpoint

**Documentation interactive** :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## 🧪 Tests

```bash
# Test de santé
curl http://localhost:8000/

# Liste des modèles
curl http://localhost:8000/api/tags

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

## 🏭 Production

### Dockerfile optimisé

Le Dockerfile utilise :
- **Multi-stage build** pour réduire la taille
- **Layer caching** optimal (requirements d'abord)
- **Non-root user** pour la sécurité
- **Health checks** configurés

### Build manuel

```bash
docker build -t chatbot-backend .
docker run -d -p 8000:8000 \
  -e MISTRAL_API_KEY=your_key \
  chatbot-backend
```

## 🔧 Configuration

Tous les paramètres sont centralisés dans `config.py` :
- URLs des APIs
- Mapping des modèles
- CORS origins
- Modèles disponibles

## 📊 Performance

- **Workers** : 1 par défaut (ajuster selon CPU)
- **Timeout** : 60s pour Mistral API
- **Streaming** : Support complet SSE → NDJSON

## 🐛 Debugging

```bash
# Logs détaillés
uvicorn main:app --log-level debug

# Recharger automatiquement
uvicorn main:app --reload

# Tester sans Docker
python main.py
```

## 📦 Dépendances principales

- `fastapi` - Framework web
- `uvicorn` - Serveur ASGI
- `httpx` - Client HTTP async
- `pydantic` - Validation de données
- `python-dotenv` - Variables d'environnement

## 🤝 Contribution

Structure à respecter :
1. **api/** - Routes uniquement, pas de logique
2. **services/** - Logique métier isolée
3. **models/** - Validation avec Pydantic
4. **config.py** - Configuration centralisée

## 📄 Licence

Voir LICENSE à la racine du projet.
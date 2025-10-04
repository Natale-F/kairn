# Kairn – The European Sovereign Cloud Assistant 🇪🇺

**Kairn** is an open-source AI assistant designed to **guide organizations in their transition toward sovereign and ethical cloud infrastructures**.  
Powered by **Mistral AI** (France) and deployable on **European providers such as OVHcloud, Infomaniak or Scaleway**, Kairn helps teams **understand, plan, and migrate** their workloads to **independent, privacy-focused, and open environments**.

Kairn promotes a vision of **transparent, self-hostable, and open technologies**—because sovereignty and innovation must go hand in hand.

---

## Why Kairn

Most AI and cloud tools today rely on U.S.-based infrastructures.  
**Kairn** proves that European technologies can deliver the same performance and reliability—without sacrificing independence or openness.  
It’s built for **organizations seeking to regain control of their data and infrastructure**, while contributing to a **more open, sustainable, and sovereign digital ecosystem**.

## Quick Start

### 1. Setup Environment

Create a `.env` file:
```bash
MISTRAL_API_KEY=your_mistral_api_key_here
```

Get your API key from [Mistral Console](https://console.mistral.ai/)

### 2. Launch

```bash
docker-compose up -d --build
```

Or use the script:
```bash
./start-docker.sh
```

### 3. Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What's Inside

- **Backend** (Python 3.12 + FastAPI) - Ollama-compatible API for Mistral AI
- **Frontend** (Next.js) - Modern chat UI based on [nextjs-ollama-llm-ui](https://github.com/jakobhoeg/nextjs-ollama-llm-ui)

Available models: `mistral-large`, `mistral-medium`,`mistral-small`

## Development

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

## Sovereignty

- French LLM provider (Mistral AI - Paris)
- No US dependencies
- Self-hostable on French infrastructure
- Complete data privacy

# Kairn – European Sovereign Cloud Assistant 🇪🇺

**Kairn** is an open-source AI chatbot that demonstrates how European technologies can power intelligent applications without relying on U.S. cloud infrastructure.

Built with **Mistral AI** (France 🇫🇷) and designed to run on **European cloud providers** (OVHcloud, Scaleway, Infomaniak), this project showcases a modern, privacy-focused approach to AI deployment.

**Tech Stack:** Python 3.12 · FastAPI · Next.js · Docker · Mistral AI · PostgreSQL with pgvector(scale)

---

## Why This Project

Most AI tools today depend on U.S.-based infrastructure. **Kairn** proves that European technologies can deliver the same capabilities while maintaining:

- **Data Sovereignty** – Full control over data location and processing
- **Privacy-First** – No third-party data sharing or tracking
- **Open Source** – Transparent, auditable, self-hostable
- **European Tech** – Supporting independent, sustainable digital ecosystems

Perfect for organizations exploring sovereign cloud strategies or developers interested in privacy-focused AI architectures.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Mistral AI API key ([get one here](https://console.mistral.ai/))

### Setup & Launch

1. **Create environment file**
```bash
echo "MISTRAL_API_KEY=your_actual_api_key_here" > .env
```

2. **Start the application**
```bash
./start-docker.sh
```

Or manually:
```bash
docker compose up -d --build
```

3. **Access the application**
- 💬 **Chat Interface:** http://localhost:3000
- 🔧 **API Backend:** http://localhost:8000
- 📚 **API Documentation:** http://localhost:8000/docs

---

## 🏗️ Architecture

### Backend
- **Python 3.12** with **FastAPI** framework
- Ollama-compatible API for seamless integration
- Direct integration with Mistral AI API
- Models: `mistral-large`, `mistral-medium`, `mistral-small`

### Frontend
- **Next.js** with modern React patterns
- Real-time chat interface
- Based on [nextjs-ollama-llm-ui](https://github.com/jakobhoeg/nextjs-ollama-llm-ui)
- Responsive design with Tailwind CSS

### Infrastructure
- Fully containerized with Docker
- Production-ready configuration
- Easily deployable on any European cloud provider

---

## Development

```bash
# View real-time logs
docker compose logs -f

# Restart services
docker compose restart

# Stop all services
docker compose down

# Rebuild after code changes
docker compose up -d --build
```

---

## European Sovereignty Features

- ✅ **French AI Provider** – Mistral AI (Paris, France)
- ✅ **No US Dependencies** – Complete operational independence
- ✅ **Self-Hostable** – Deploy on your own infrastructure
- ✅ **GDPR Compliant** – Built with European privacy standards
- ✅ **Open Source** – Full transparency and auditability

---

## License

This project demonstrates sovereign cloud principles and modern AI architectures. Feel free to explore, learn, and adapt for your own needs.

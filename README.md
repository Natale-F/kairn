# Kairn – European Sovereign Cloud Assistant 🇪🇺

**Kairn** is an open-source AI chatbot that demonstrates how European technologies can power intelligent applications without relying on U.S. cloud infrastructure.

Built with **Mistral AI** (France 🇫🇷) and designed to run on **European cloud providers** (OVHcloud, Scaleway, Infomaniak), this project showcases a modern, privacy-focused approach to AI deployment.

**Tech Stack:** Python 3.12 · FastAPI · Open WebUI · Docker · Mistral AI · PostgreSQL

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
cat > .env << EOF
# Backend Configuration
MISTRAL_API_KEY=your_mistral_api_key_here

# Database Configuration
POSTGRES_DB=openwebui
POSTGRES_USER=openwebui
POSTGRES_PASSWORD=change_this_secure_password

# Security (generate with: openssl rand -hex 32)
WEBUI_SECRET_KEY=change_this_secret_key_in_production
EOF
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
- 💬 **Chat Interface (Open WebUI):** http://localhost:3000
- 🔧 **API Backend:** http://localhost:8000
- 📚 **API Documentation:** http://localhost:8000/docs
- 🗄️ **Database:** PostgreSQL on port 5432 (internal)

4. **First login**
- On first access, Open WebUI will prompt you to create an admin account
- This account is stored locally in your PostgreSQL database

---

## 🏗️ Architecture

### Backend
- **Python 3.12** with **FastAPI** framework
- OpenAI-compatible API for seamless integration
- Direct integration with Mistral AI API
- Models: `mistral-large`, `mistral-medium`, `mistral-small`

### Frontend
- **Open WebUI** - Feature-rich, self-hosted AI interface
- User authentication and role-based access control
- Conversation history and sharing
- Modern, responsive interface
- Based on [Open WebUI](https://github.com/open-webui/open-webui)

### Database
- **PostgreSQL 16** for persistent storage
- Stores user accounts, conversations, and settings
- Fully containerized with data persistence

### Infrastructure
- Fully containerized with Docker Compose
- Production-ready configuration
- Health checks and automatic restarts
- Easily deployable on any European cloud provider

---

## Development

```bash
# View real-time logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Restart services
docker compose restart

# Stop all services
docker compose down

# Stop and remove all data (including database)
docker compose down -v

# Rebuild after code changes
docker compose up -d --build

# Access PostgreSQL database
docker exec -it chatbot-postgres psql -U openwebui -d openwebui
```

### Backend Development

The backend is a FastAPI application that exposes an OpenAI-compatible API. This means any tool that works with the OpenAI API format (like Open WebUI) can connect to it.

**Key endpoints:**
- `GET /v1/models` - List available models (OpenAI format)
- `POST /v1/chat/completions` - Chat completion (streaming and non-streaming)

**Your backend:**
- Exposes an OpenAI-compatible API
- Connects directly to Mistral AI
- Open WebUI connects to it using the OpenAI protocol
- Available at http://localhost:8000/docs for API documentation

### Frontend Customization

Open WebUI is highly configurable through environment variables in `docker-compose.yml`. See the [Open WebUI documentation](https://docs.openwebui.com/) for all available options.

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

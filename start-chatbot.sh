#!/bin/bash

set -e

echo "🚀 Starting Kairn - European Sovereign Cloud Assistant"
echo ""

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "   Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose installation
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "   Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo ""
    echo "Create a .env file with the following variables:"
    echo ""
    cat << 'EOF'
cat > .env << 'ENVFILE'
# Backend Configuration
MISTRAL_API_KEY=your_mistral_api_key_here

# Database Configuration
POSTGRES_DB=openwebui
POSTGRES_USER=openwebui
POSTGRES_PASSWORD=change_this_secure_password

# Security (generate with: openssl rand -hex 32)
WEBUI_SECRET_KEY=change_this_secret_key_in_production
ENVFILE
EOF
    echo ""
    echo "Get your Mistral API key from: https://console.mistral.ai/"
    exit 1
fi

# Check API key is configured
if grep -q "your_mistral_api_key_here" .env || grep -q "your_api_key_here" .env; then
    echo "❌ Error: MISTRAL_API_KEY not configured in .env file"
    echo "   Get your API key from: https://console.mistral.ai/"
    exit 1
fi

# Check database password is configured
if grep -q "change_this_secure_password" .env; then
    echo "⚠️  Warning: Using default database password"
    echo "   Consider changing POSTGRES_PASSWORD in .env for production"
    echo ""
fi

# Check secret key is configured
if grep -q "change_this_secret_key" .env; then
    echo "⚠️  Warning: Using default WEBUI_SECRET_KEY"
    echo "   Consider generating a secure key with: openssl rand -hex 32"
    echo ""
fi

echo "🏗️  Building Docker images..."
docker compose build

echo ""
echo "🚀 Starting services..."
docker compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access:"
echo "   - Open WebUI:  http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs:    http://localhost:8000/docs"
echo ""
echo "🔐 First Login:"
echo "   On first access to Open WebUI, you'll be prompted to create"
echo "   an admin account. This is stored locally in PostgreSQL."
echo ""
echo "📝 Commands:"
echo "   - View all logs:        docker compose logs -f"
echo "   - View backend logs:    docker compose logs -f backend"
echo "   - View frontend logs:   docker compose logs -f frontend"
echo "   - View database logs:   docker compose logs -f postgres"
echo "   - Stop services:        docker compose down"
echo "   - Stop and remove data: docker compose down -v"
echo "   - Restart services:     docker compose restart"
echo ""
echo "📚 Documentation:"
echo "   - Open WebUI docs:  https://docs.openwebui.com/"
echo "   - Mistral AI docs:  https://docs.mistral.ai/"
echo ""

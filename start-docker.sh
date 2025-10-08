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
    echo "Create a .env file with your Mistral API key:"
    echo "   MISTRAL_API_KEY=your_api_key_here"
    echo ""
    echo "Get your API key from: https://console.mistral.ai/"
    exit 1
fi

# Check API key is configured
if grep -q "your_mistral_api_key_here" .env || grep -q "your_api_key_here" .env; then
    echo "❌ Error: MISTRAL_API_KEY not configured in .env file"
    echo "   Get your API key from: https://console.mistral.ai/"
    exit 1
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
echo "   - Frontend: http://localhost:3000"
echo "   - Backend:  http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Commands:"
echo "   - View logs: docker compose logs -f"
echo "   - Stop:      docker compose down"
echo "   - Restart:   docker compose restart"
echo ""

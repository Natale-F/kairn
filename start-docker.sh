#!/bin/bash

# Script de démarrage Docker Compose pour le chatbot French Sovereign

set -e

echo "🚀 Démarrage du chatbot French Sovereign avec Docker Compose"
echo ""

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Installez Docker : https://docs.docker.com/get-docker/"
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Installez Docker Compose : https://docs.docker.com/compose/install/"
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé !"
    echo ""
    echo "Création d'un fichier .env de base..."
    cat > .env << 'EOF'
# ============================================================================
# MISTRAL API CONFIGURATION (Required)
# ============================================================================
# Your Mistral AI API key - Get it from https://console.mistral.ai/
MISTRAL_API_KEY=your_mistral_api_key_here

# ============================================================================
# BACKEND CONFIGURATION (Optional)
# ============================================================================
# Frontend URL for CORS (automatically set in Docker)
FRONTEND_URL=http://localhost:3000
EOF
    echo ""
    echo "📝 Fichier .env créé. MODIFIEZ-LE pour ajouter votre clé API Mistral !"
    echo ""
    echo "   nano .env"
    echo "   # ou"
    echo "   vim .env"
    echo ""
    read -p "Appuyez sur Entrée une fois la clé API configurée..."
fi

# Vérifier si la clé API est configurée
if grep -q "your_mistral_api_key_here" .env; then
    echo ""
    echo "⚠️  ATTENTION : Vous devez remplacer 'your_mistral_api_key_here' par votre vraie clé API Mistral !"
    echo ""
    echo "   Obtenez une clé sur : https://console.mistral.ai/"
    echo ""
    read -p "Continuer quand même ? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🏗️  Construction des images Docker..."
docker compose build

echo ""
echo "🚀 Démarrage des services..."
docker compose up -d

echo ""
echo "⏳ Attente du démarrage complet..."
sleep 5

# Vérifier le statut
echo ""
echo "📊 Statut des services :"
docker compose ps

echo ""
echo "✅ Démarrage terminé !"
echo ""
echo "📍 Accès aux services :"
echo "   - Frontend : http://localhost:3000"
echo "   - Backend  : http://localhost:8000"
echo "   - API Docs : http://localhost:8000/docs"
echo ""
echo "📝 Commandes utiles :"
echo "   - Voir les logs     : docker compose logs -f"
echo "   - Arrêter           : docker compose down"
echo "   - Redémarrer        : docker compose restart"
echo ""
echo "💡 Pour plus d'infos : cat README_DOCKER.md"
echo ""

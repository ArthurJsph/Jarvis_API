#!/bin/bash

# Quick start script for Jarvis Assistente API

echo "🚀 Jarvis Assistente API - Quick Start"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale Docker primeiro."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"
echo ""

# Create .env if doesn't exist
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e configure sua API_KEY antes de usar em produção!"
fi

# Build and start containers
echo ""
echo "🏗️  Construindo e iniciando containers..."
echo ""

docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Check if services are running
echo ""
echo "📊 Status dos serviços:"
docker-compose ps

echo ""
echo "✅ Jarvis Assistente API está rodando!"
echo ""
echo "🌐 Acesse:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs: docker-compose logs -f"
echo "   Parar: docker-compose stop"
echo "   Remover: docker-compose down"
echo ""

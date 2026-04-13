# Quick start script for Jarvis Assistente API (Windows PowerShell)

Write-Host "🚀 Jarvis Assistente API - Quick Start" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker encontrado e rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create .env if doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "📝 Criando arquivo .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANTE: Edite o arquivo .env e configure sua API_KEY antes de usar em produção!" -ForegroundColor Yellow
}

# Build and start containers
Write-Host ""
Write-Host "🏗️  Construindo e iniciando containers..." -ForegroundColor Cyan
Write-Host ""

docker-compose up -d --build

# Wait for services to be ready
Write-Host ""
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
Write-Host ""
Write-Host "📊 Status dos serviços:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "✅ Jarvis Assistente API está rodando!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesse:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📋 Comandos úteis:" -ForegroundColor Cyan
Write-Host "   Ver logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Parar: docker-compose stop" -ForegroundColor White
Write-Host "   Remover: docker-compose down" -ForegroundColor White
Write-Host ""

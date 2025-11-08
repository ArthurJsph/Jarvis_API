# 🚀 Jarvis Assistente API - Docker Setup

## 📋 Pré-requisitos

- Docker (20.10+)
- Docker Compose (1.29+)

## 🏗️ Estrutura do Projeto

```
jarvis_assistente_api/
├── frontend/              # React + Vite + Material-UI
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── services/     # Axios API service
│   │   ├── contexts/     # React contexts (Theme)
│   │   └── theme/        # Material-UI themes
│   ├── Dockerfile        # Multi-stage build
│   └── nginx.conf        # Nginx config
├── core/                 # Python backend modules
├── Dockerfile            # Python FastAPI backend
├── docker-compose.yml    # Orquestração dos serviços
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### 1. Configurar variáveis de ambiente (opcional)

```bash
# Criar arquivo .env na raiz
echo "API_KEY=sua-chave-secreta-aqui" > .env
```

### 2. Build e iniciar os containers

```bash
# Build e start em modo detached
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

### 3. Acessar a aplicação

- **Frontend**: http://localhost (porta 80)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🛠️ Comandos Úteis

### Gerenciamento de Containers

```bash
# Parar containers
docker-compose stop

# Parar e remover containers
docker-compose down

# Parar e remover containers + volumes
docker-compose down -v

# Rebuild sem cache
docker-compose build --no-cache

# Ver status dos containers
docker-compose ps

# Restart de um serviço específico
docker-compose restart backend
docker-compose restart frontend
```

### Debug e Logs

```bash
# Logs em tempo real
docker-compose logs -f

# Últimas 100 linhas de log
docker-compose logs --tail=100

# Executar comando dentro do container
docker-compose exec backend bash
docker-compose exec frontend sh

# Ver uso de recursos
docker stats
```

### Desenvolvimento

```bash
# Rebuild apenas um serviço
docker-compose up -d --build backend

# Forçar recreate dos containers
docker-compose up -d --force-recreate
```

## 🔧 Configurações Avançadas

### Portas Customizadas

Edite o `docker-compose.yml` para mudar as portas:

```yaml
services:
  frontend:
    ports:
      - "3000:80"  # Acesse em localhost:3000
  backend:
    ports:
      - "8080:8000"  # Acesse em localhost:8080
```

### Volumes Persistentes

Os dados são preservados em volumes Docker:

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect jarvis_assistente_api_data

# Backup de volume
docker run --rm -v jarvis_assistente_api_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz /data
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Backend
API_KEY=seu-api-key-seguro
PYTHONUNBUFFERED=1

# Frontend
VITE_API_URL=http://localhost:8000
```

## 📊 Monitoramento

### Health Checks

Os containers incluem health checks automáticos:

```bash
# Ver status de saúde
docker-compose ps

# Ver detalhes do health check
docker inspect --format='{{json .State.Health}}' jarvis-backend | jq
docker inspect --format='{{json .State.Health}}' jarvis-frontend | jq
```

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar se a porta está em uso
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problemas de permissão

```bash
# Linux: ajustar permissões
sudo chown -R $USER:$USER logs/ data/ documents/
```

### Frontend não conecta ao backend

1. Verifique se o backend está rodando: `docker-compose ps`
2. Teste a API diretamente: `curl http://localhost:8000/health`
3. Verifique a variável `VITE_API_URL` no container do frontend

## 🏭 Deploy em Produção

### Preparação

1. **Configure secrets apropriados**:
   ```bash
   # Gere uma API key segura
   openssl rand -hex 32
   ```

2. **Desabilite hot-reload no backend**:
   Edite o `Dockerfile` e remova `--reload` do CMD:
   ```dockerfile
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Configure HTTPS no Nginx** (recomendado):
   Use um proxy reverso como Traefik ou certbot

### Deploy com Docker Swarm

```bash
# Iniciar swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml jarvis

# Ver serviços
docker service ls
```

## 📝 Estrutura de Logs

```
logs/
├── jarvis.log          # Log principal
├── error.log           # Erros
└── access.log          # Acessos
```

## 🔐 Segurança

- ✅ API Key obrigatória para endpoints protegidos
- ✅ Headers de segurança no Nginx
- ✅ Health checks configurados
- ✅ Volumes isolados por container
- ⚠️ **IMPORTANTE**: Mude a API_KEY padrão em produção!

## 📚 Tecnologias

### Backend
- Python 3.11
- FastAPI
- Uvicorn
- Git integration
- Office document handling

### Frontend
- React 19
- TypeScript
- Vite
- Material-UI (MUI)
- Axios
- Emotion (styled components)

### DevOps
- Docker multi-stage builds
- Nginx (reverse proxy + static files)
- Docker Compose orchestration

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Pull Request

## 📄 Licença

MIT License - veja LICENSE para detalhes

---

**Desenvolvido com ❤️ usando Docker, React e FastAPI**

# Arquitetura do Projeto

## Objetivo

Organizar o projeto em camadas claras para backend, frontend, documentacao e operacao.

## Estrutura

```text
Jarvis_API/
|-- core/                  # Modulos backend (API, seguranca, gerenciadores)
|-- frontend/              # Aplicacao React + Vite
|-- templates/             # Templates para geracao de projetos/arquivos
|-- utils/                 # Utilitarios compartilhados
|-- docs/                  # Documentacao tecnica e historico de mudancas
|   |-- ARCHITECTURE.md
|   |-- DOCKER_README.md
|   |-- FRONTEND_UPDATES.md
|   `-- UPDATES.md
|-- scripts/               # Scripts de operacao e bootstrap
|   |-- README.md
|   |-- start.sh
|   `-- start.ps1
|-- main.py                # Entry point backend
|-- config.py              # Configuracoes centrais
|-- docker-compose.yml     # Stack local (frontend + backend)
|-- Dockerfile             # Build backend
`-- requirements.txt       # Dependencias Python
```

## Camadas

- API e dominio: concentrados em `core/`.
- Interface web: concentrada em `frontend/`.
- Operacao: concentrada em `scripts/`.
- Documentacao: concentrada em `docs/`.

## Convencoes

- Novos scripts operacionais devem ser adicionados em `scripts/`.
- Novos documentos tecnicos devem ser adicionados em `docs/`.
- Entrypoints de compatibilidade na raiz podem existir apenas como wrappers.
- Evitar logica de dominio fora de `core/`.

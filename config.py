"""Runtime configuration for Jarvis Remote Assistant (API-focused).

This file exposes a small set of configuration values used by the
server and other core modules. Values are read from environment
variables (see `.env.example`). Keep this file lightweight.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
WEB_DIR = BASE_DIR.parent / "web"
STATIC_DIR = WEB_DIR / "static"
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = os.getenv("LOG_FILE", str(LOGS_DIR / "jarvis.log"))

# App info
APP_NAME = os.getenv("APP_NAME", "Jarvis Remote Assistant")
APP_VERSION = os.getenv("APP_VERSION", "1.0")

# Defaults used by document managers
DEFAULT_ENCODING = os.getenv("DEFAULT_ENCODING", "utf-8")
DEFAULT_AUTHOR = os.getenv("DEFAULT_AUTHOR", "Jarvis")
DEFAULT_ORGANIZATION = os.getenv("DEFAULT_ORGANIZATION", "")

# Documents directory for Word/PPTX and other generated docs
DOCUMENTS_DIR = BASE_DIR / "documents"
DOCUMENTS_DIR.mkdir(exist_ok=True)

# NOTE: LLM backends removed in task-based assistant conversion. If you previously used LLMs,
# reintroduce configuration here (LLM_BACKEND, LLM_MODEL_PATH) and ensure the relevant
# packages are present in the environment.

# Security
API_KEY = os.getenv("API_KEY")
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Keep a small set of templates (if needed by generators); templates still live in templates/
FILE_TEMPLATES = {
    "py": '''"""
{filename}
Arquivo Python criado pelo Jarvis CLI
"""

def main():
    """Função principal"""
    print("Hello from {filename}")

if __name__ == "__main__":
    main()
''',
    
    "md": '''# {title}

Projeto criado pelo Jarvis CLI.

## Descrição

Descreva seu projeto aqui.

## Instalação

```bash
# Comandos de instalação
```

## Uso

```bash
# Exemplos de uso
```

## Contribuição

1. Fork o projeto
2. Crie uma branch
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

MIT
''',

    "js": '''// {filename}
// Arquivo JavaScript criado pelo Jarvis CLI

console.log("Hello from {filename}");

// Sua função principal aqui
function main() {{
    console.log("Executando {filename}");
}}

main();
''',

    "json": '''{{
  "name": "{name}",
  "version": "1.0.0",
  "description": "Projeto criado pelo Jarvis CLI",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js",
    "test": "echo \\"Error: no test specified\\" && exit 1"
  }},
  "keywords": ["jarvis", "cli"],
  "author": "Jarvis CLI",
  "license": "MIT"
}}
''',

    "html": '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Página criada pelo Jarvis CLI</p>
</body>
</html>
''',

    "css": '''/* {filename} */
/* Arquivo CSS criado pelo Jarvis CLI */

/* Reset básico */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}}

/* Adicione seus estilos aqui */
''',

    "txt": '''Arquivo de texto criado pelo Jarvis CLI
Data: {datetime}

Conteúdo do arquivo...
'''
}

# Dados falsos brasileiros
FAKE_DATA = {
    "nomes": [
        "Ana Silva", "João Santos", "Maria Oliveira", "Pedro Costa",
        "Carla Ferreira", "Bruno Lima", "Julia Rodrigues", "Rafael Almeida",
        "Fernanda Souza", "Lucas Pereira", "Camila Martins", "Gabriel Rocha",
        "Mariana Gomes", "Felipe Barbosa", "Larissa Cardoso", "Mateus Dias",
        "Isabella Castro", "Thiago Nascimento", "Beatriz Ribeiro", "Leonardo Monteiro"
    ],
    
    "sobrenomes": [
        "Silva", "Santos", "Oliveira", "Costa", "Ferreira", "Lima",
        "Rodrigues", "Almeida", "Souza", "Pereira", "Martins", "Rocha",
        "Gomes", "Barbosa", "Cardoso", "Dias", "Castro", "Nascimento",
        "Ribeiro", "Monteiro", "Araújo", "Carvalho", "Ramos", "Teixeira"
    ],
    
    "dominios_email": [
        "gmail.com", "hotmail.com", "yahoo.com", "outlook.com",
        "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br"
    ],
    
    "ddd_telefones": [
        "11", "12", "13", "14", "15", "16", "17", "18", "19",  # SP
        "21", "22", "24",  # RJ
        "27", "28",  # ES
        "31", "32", "33", "34", "35", "37", "38",  # MG
        "41", "42", "43", "44", "45", "46",  # PR
        "47", "48", "49",  # SC
        "51", "53", "54", "55"  # RS
    ]
}

# Mensagens de resposta
RESPONSES = {
    "success": [
        "✅ Feito com sucesso!",
        "🎉 Concluído!",
        "✨ Perfeito!",
        "🚀 Executado com êxito!"
    ],
    
    "error": [
        "❌ Ops, algo deu errado!",
        "💥 Erro encontrado!",
        "⚠️ Problema detectado!",
        "🚨 Falha na execução!"
    ],
    
    "thinking": [
        "🤔 Pensando...",
        "💭 Processando...",
        "🧠 Analisando...",
        "⚡ Executando..."
    ]
}

# Ajuda rápida
QUICK_HELP = {
    "arquivos": [
        "criar arquivo README.md",
        "listar arquivos",
        "criar arquivo main.py"
    ],
    
    "git": [
        "git status",
        "commit 'mensagem do commit'",
        "git log"
    ],
    
    "dados": [
        "gerar dados falsos",
        "dados fake",
        "nomes falsos"
    ],
    
    "sistema": [
        "data e hora",
        "info sistema",
        "help"
    ]
}
# Atualizações - Conversão para API remota (Resumo)

Este arquivo resume as alterações realizadas ao projeto para transformá-lo em uma API remota segura e com uma interface mínima.

Arquivos novos adicionados
- `core/security.py` — Middleware simples que exige `x-api-key` (comparado com `API_KEY` no `.env`) e aplica um rate limit em memória por chave (token-bucket simples).
- `core/file_manager.py` — Funções seguras para listar, ler, escrever e deletar arquivos dentro do diretório do projeto (proteção contra directory traversal).
-- LLM/chat functionality removed from this release. The project no longer exposes a `/llm` endpoint
  nor includes a local LLM wrapper by default. The server now focuses on fast, pre-defined task
  endpoints (file operations, execute, logs). If you need LLM support later, it can be reintroduced
  as an optional component (`llama-cpp-python` or other) and configured via environment variables.
- `core/remote_api.py` — Servidor FastAPI com rotas:
  - `GET /health` — health-check
  -- (removed) `POST /llm` — chat/LLM endpoint removed in favor of task endpoints
  - `GET /files/list` — listar arquivos numa pasta relativa ao projeto
  - `GET /files/read?path=` — ler arquivo
  - `POST /files/write` — gravar arquivo (JSON: path, content, overwrite)
  - `POST /files/delete?path=` — deletar arquivo (arquivo apenas)
  - `POST /execute` — endpoint mínimo para comandos controlados (ex.: `list_root`)
-- `web/ui.html` — UI estática mínima (HTML + JS) que agora expõe botões de tarefas (listar/ler/escrever/apagar)
  e usa `x-api-key`. Pode ser servida pelo mesmo servidor FastAPI (config adicional) ou por qualquer servidor estático.

Dependências adicionadas
- `fastapi`, `uvicorn`, `python-dotenv`, `reactpy` (opcional), `httpx` — adicionadas em `requirements.txt`. OpenAI was intentionally removed from requirements.

Segurança
- Autenticação por `API_KEY` no `.env` (variável obrigatória). O middleware `core/security.py` exige que o header `x-api-key` ou query param `api_key` seja igual ao valor do `.env`.
- Rate limiting em memória por API key. Valores configuráveis via `.env`:
  - `RATE_LIMIT_REQUESTS` (padrão 60)
  - `RATE_LIMIT_PERIOD` (segundos, padrão 60)

LLM
- LLM/chat support was intentionally removed in this task-focused conversion. See notes above.

UI
- Uma UI mínima `web/ui.html` foi adicionada para testes rápidos. Se quiser uma interface Python-first que gere React no cliente, podemos integrar `reactpy` (foi adicionada como dependência opcional). Se preferir, implemente o frontend em React separado e use as rotas da API.

Como rodar (exemplo rápido)
1. Crie um arquivo `.env` na raiz com pelo menos:

```
API_KEY=uma_chave_secreta
```

2. Instale dependências (recomendo usar um venv):

```
python -m pip install -r requirements.txt
```

3. Rodar a API (exemplo):

```
uvicorn core.remote_api:app --host 0.0.0.0 --port 8000 --reload
```

4. Abra a UI integrada:
  - A aplicação serve a UI em `GET /ui` e arquivos estáticos em `/static`.
  - Após subir o servidor, abra `http://localhost:8000/ui` no navegador.

Notas importantes
- Este é um scaffold inicial. Para produção recomendo:
  - Trocar o rate limiter em memória por Redis ou outro armazenamento persistente.
  - Usar TLS (HTTPS) e um proxy reverso (ex.: nginx) e restringir IPs/portas se precisar.
  - Auditar endpoints que executam comandos/sobrescrevem arquivos. Atualmente `files/write` pode escrever em qualquer arquivo dentro do diretório do projeto (controlado por API key).
  - Rotinas de backup e versionamento para evitar perda acidental.

Próximos passos que posso implementar se desejar
- Integrar um backend local de LLM (llama-cpp) e adaptá-lo para 2GB (modelos muito pequenos / quantizados).
 - Se quiser que eu configure o backend `llama_cpp` automaticamente, posso:
   - Adicionar instruções detalhadas para instalar `llama-cpp` e `llama-cpp-python` (compilação nativa necessária).
   - Adicionar um script de download e conversão para modelos quantizados compatíveis (quando você fornecer o link do modelo que deseja usar).
- Subir um UI em `reactpy` totalmente integrado ao FastAPI, com autenticação do lado cliente e armazenamento de sessão.
- Adicionar endpoints para execução de tarefas assíncronas, fila de trabalhos e histórico de comandos.

Se quiser que eu implemente imediatamente alguma das próximas etapas, diga qual delas priorizar e eu continuo com as alterações e testes.

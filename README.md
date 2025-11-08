# Jarvis Remote Assistant

Jarvis Remote Assistant é um servidor leve que expõe uma API HTTP e uma UI
simples para permitir automações remotas, manipulação de arquivos e integrações
com ferramentas externas quando necessário. Esta é a versão "API-first"
do projeto — a interface CLI foi removida em favor de um servidor remoto seguro.

Principais funcionalidades
- API REST para operações:
  - /health — verificação de integridade
  - (removed) /llm — endpoint de chat/LLM removido; esta versão foca em endpoints de tarefa rápidos
  - /files/list, /files/read, /files/write, /files/delete — operações de arquivo seguras
  - /execute — comandos controlados/permitidos
- UI leve (web) em `/ui` para execução de tarefas rápidas (listar/ler/escrever/deletar)
- Segurança: exige `x-api-key` (configurável via `.env`) e tem rate limiting por chave
-- Observação sobre LLMs: suporte a LLMs locais foi removido do runtime padrão desta
versão focada em tarefas rápidas. É possível reintroduzir suporte a modelos locais
manualmente (por exemplo via `llama-cpp-python`) — veja a seção "Reativando LLMs (opcional)" abaixo.

Instalação rápida

Recomendo usar um virtualenv. No Windows PowerShell:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
# Edite .env com sua API_KEY e outras configurações
```

Rodando o servidor

Recomendo usar o `uvicorn` (melhor para desenvolvimento/produção leve). No PowerShell:

```powershell
uvicorn core.remote_api:app --host 0.0.0.0 --port 8000 --reload
# Alternativa (wrapper): python main.py --host 0.0.0.0 --port 8000
```

Acessando a UI

 - Abra `http://localhost:8000/ui` no navegador. Insira sua `API_KEY` e use os botões para executar tarefas rápidas.

Configuração (variáveis de ambiente)

- Veja `.env.example`. Principais variáveis:
  - API_KEY — chave para autenticar requisições (usada pelo middleware)
  - HOST / PORT — bind do servidor
  - OBS: configurações de backend de LLM foram removidas nesta release focada em tarefas;
    se você precisa de LLMs, veja a seção "Reativando LLMs (opcional)" abaixo.

Chamada de exemplo via curl

```bash
curl "http://localhost:8000/files/list?path=" -H "x-api-key: <SUA_API_KEY>"
```

Arquitetura (resumida)

```
jarvis_assistente_api/
├── core/                  # Lógica do servidor: API, segurança, file manager (LLM opcional)
├── web/                   # UI estática e assets (servida em /ui e /static)
├── data/                  # armazenamento local e cache
├── templates/             # templates utilitários para geradores
├── main.py                # entrypoint para rodar o servidor (convenience wrapper)
├── requirements.txt       # dependências
└── .env.example           # exemplo de variáveis de ambiente
```

Notas de segurança e produção
- O rate limiter atual é em memória e serve para uso pessoal. Para produção migre-o para Redis ou outro armazenamento compartilhado.
- Sempre rode atrás de um proxy reverso com TLS (nginx, cloud load balancer) e restrinja acesso à API quando possível.
- Revise as permissões de `files/write` e mantenha backups de arquivos importantes.

Contribuição

Se quiser contribuir, abra issues ou PRs. Para desenvolver localmente, siga os passos de instalação acima.

Reativando LLMs (opcional)

Esta versão não ativa LLMs por padrão. Se você deseja integrar um modelo local, faça isso manualmente:

- Instale dependências adicionais (ex.: `llama-cpp-python`) em seu ambiente.
- Adicione um módulo `core/llm_wrapper.py` que exponha uma interface simples para gerar texto a partir do modelo.
- Atualize `core/remote_api.py` para adicionar uma rota opcional `/llm` **apenas se** quiser expor geração por API.

Aviso: LLMs locais podem exigir compilação nativa, bibliotecas C/C++ e memória considerável. Teste com modelos muito pequenos e em ambientes controlados.

Licença

MIT — veja `LICENSE`.

--

Este README foi atualizado para refletir a versão API-first do projeto.
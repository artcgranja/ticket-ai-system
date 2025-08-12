### Ticket AI System — Agente LangGraph (memória, persistência e streaming)

Sistema de exemplo que implementa um agente com LangGraph/LangChain para criação e gestão de tickets, incluindo:
- Memória de curto prazo (state trimming)
- Memória longa (LangGraph Store em Postgres)
- Persistência com checkpoints/threads (LangGraph Checkpointer em Postgres)
- Streaming de updates (no CLI)

### Stack
- LangGraph, LangChain
- FastAPI (API)
- SQLAlchemy + Postgres
- Pydantic v2

### Requisitos
- Python 3.12+
- Docker + Docker Compose
- Variáveis de ambiente: pelo menos `OPENAI_API_KEY` e `DATABASE_URL`

### Banco de Dados (Docker Compose)
Este repositório inclui um `docker-compose.yml` que sobe um Postgres local na porta host `5442`:
```
docker compose up -d
```

Use a `DATABASE_URL` apontando para a porta `5442` (mapeada para `5432` dentro do container):
```
postgresql://postgres:postgres@localhost:5442/ticket_ai?sslmode=disable
```

### Variáveis de ambiente
Crie um arquivo `.env` na raiz com, por exemplo:
```
OPENAI_API_KEY=seu_token_openai
OPENAI_MODEL=gpt-4o-mini
DATABASE_URL=postgresql://postgres:postgres@localhost:5442/ticket_ai?sslmode=disable
DEMO_THREAD_ID=u1:chat-001
DEMO_USER_ID=u1
```

Notas:
- `OPENAI_MODEL` é opcional; por padrão o código inicializa `openai:gpt-4o-mini` via `init_chat_model`.
- A query `?sslmode=disable` é usada como padrão no código local.

### Instalação das dependências
Opção A (pip):
```
pip install -U pip
pip install -e .
```

Opção B (uv, conforme Dockerfile):
```
pip install uv
uv pip install -e . --system
```

### Rodar o demo (CLI com streaming)
```
python main.py
```
O script:
- Inicializa `PostgresStore` (memória longa) e `PostgresSaver` (checkpointer) e garante o setup do schema
- Constrói o agente com `create_react_agent` e as tools de tickets
- Abre um loop de entrada de usuário com streaming dos updates

Para sair, digite `exit`, `quit` ou `sair`.

### Rodar a API (FastAPI)
```
uvicorn app.server:app --reload
```

Endpoint principal (experimental):
- `POST /chat`
  - Body:
    ```json
    {
      "message": "texto da mensagem",
      "thread_id": "u1:chat-001",
      "user_id": "u1"
    }
    ```
  - Resposta: `{ "message": "..." }`

Exemplo com curl:
```
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"crie um ticket","thread_id":"u1:chat-001","user_id":"u1"}'
```

Observações importantes sobre a API:
- O código atual do servidor é experimental e pode exigir ajustes para inicializar o agente com checkpointer e store (o CLI já faz isso corretamente). Caso encontre problemas, priorize o uso do CLI enquanto a API é estabilizada.

### Domínio de tickets
- `Ticket` (Pydantic):
  - Campos: `user_id`, `thread_id`, `user_name`, `subject`, `description`, `risk` ("low"|"medium"|"high"), `unique_id` (gerado no servidor)
- `TicketModel` (SQLAlchemy):
  - Enum interno `Risco` mapeado para `risk`
  - `unique_id` é um `UUIDv4` em string de 36 chars, gerado no servidor

### Tools disponíveis
- `create_ticket(ticket: Ticket)` (exposta como LangChain tool): cria e persiste um ticket e retorna o objeto serializado (incluindo `unique_id`).
- `get_ticket(unique_id: str)`: retorna um ticket pelo `unique_id`.
- `get_all_user_tickets(user_id: str)`: lista todos os tickets de um usuário.
- `edit_ticket(unique_id: str, ticket: Ticket)`: atualiza um ticket.
- `delete_ticket(unique_id: str)`: remove um ticket e retorna o objeto removido.

### Docker
Build da imagem (executa `uv` e instala o pacote em modo editável):
```
docker build -t ticket-ai-system .
```

Executar o CLI dentro do container (lembre-se de passar as variáveis de ambiente):
```
docker run --rm -it \
  -e OPENAI_API_KEY=seu_token \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5442/ticket_ai?sslmode=disable \
  ticket-ai-system
```

### Desenvolvimento
- Lint: `ruff` (configurado em `pyproject.toml`)
- Testes (opcional): dependências listadas em `[project.optional-dependencies].dev`

### Roadmap curto / Notas técnicas
- [ ] Ajustar inicialização do agente no `app.server` para usar `PostgresStore` e `PostgresSaver` como no CLI
- [ ] Padronizar a forma de passar `configurable.thread_id/user_id` para o agente na API
- [ ] Adicionar exemplos de prompts para acionar as tools de ticket


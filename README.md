### Ticket AI System — LangGraph Agent (Memória, Persistência, Streaming)

Repositório de exemplo que implementa um agente com LangGraph/LangChain incluindo:
- Memória de curto prazo (state + trim)
- Memória longa (Store Postgres)
- Persistência com checkpoints/threads (Postgres)
- Streaming de updates

#### Requisitos
- Python 3.12+
- Docker + Docker Compose
- Variáveis de ambiente: `OPENAI_API_KEY`, `DATABASE_URL`

Exemplo de `DATABASE_URL`:
```
postgresql://postgres:postgres@localhost:5432/ticket_ai
```

#### Subir Postgres
```
docker compose up -d
```

#### Instalar dependências
```
pip install -U pip
pip install -e .
```

#### Rodar demo
```
python main.py
```

O script executa:
- Inicialização de `PostgresSaver` (checkpoints) e `PostgresStore` (memória longa)
- Agente com `create_react_agent`, tools de exemplo e `pre_model_hook` para trim
- Streaming de uma conversa em uma `thread_id` fixa


#### Rodar API (FastAPI)
```
uvicorn app.server:app --reload
```

#### Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz com as chaves abaixo (veja exemplos acima):
```
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ticket_ai
DEMO_THREAD_ID=u1:chat-001
DEMO_USER_ID=u1
RECURSION_MAX_STEPS=3
```



# main.py
import os
from typing import Any, Dict
from dotenv import load_dotenv
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
from app.agent import build_agent
from app.db import init_db

def make_config(thread_id: str, user_id: str | None = None) -> Dict[str, Any]:
    # Threads e replay usam config['configurable']
    cfg: Dict[str, Any] = {"configurable": {"thread_id": thread_id}}
    if user_id:
        cfg["configurable"]["user_id"] = user_id
    return cfg

def main():
    load_dotenv()
    thread_id = os.getenv("DEMO_THREAD_ID", "u1:chat-001")
    user_id = os.getenv("DEMO_USER_ID", "u1")
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ticket_ai?sslmode=disable")

    # Cria as tabelas SQLAlchemy ao iniciar o processo
    init_db()

    # Abra as conexões e garanta que o schema do Postgres (LangGraph) exista
    with PostgresStore.from_conn_string(db_url) as store, PostgresSaver.from_conn_string(db_url) as cp:
        store.setup(); cp.setup()
        cfg = make_config(thread_id, user_id)
        agent = build_agent(cp, store)

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "sair"]:
                break
            for update in agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config=cfg,
            ):
                print(update)

if __name__ == "__main__":
    main()

from __future__ import annotations

import os

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.runtime import get_runtime

from .context import Ctx
from .tools.ticket_tool import (
    create_ticket,
    get_ticket,
    get_all_user_tickets,
    edit_ticket,
    delete_ticket,
)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value

def _prompt(state):
    rt = get_runtime(Ctx)
    sys = (
        "You are TicketAgent, helpful and concise."
        " Use tools when helpful."
    )
    return [{"role": "system", "content": sys}] + state["messages"]

def build_agent(checkpointer, store):
    _require_env("OPENAI_API_KEY")
    model = init_chat_model("openai:gpt-4o-mini", temperature=0)
    model_with_tools = model.bind_tools([create_ticket, get_ticket, get_all_user_tickets, edit_ticket, delete_ticket])

    agent = create_react_agent(
        model=model_with_tools,
        tools=[create_ticket, get_ticket, get_all_user_tickets, edit_ticket, delete_ticket],
        prompt=_prompt,
        context_schema=Ctx,
        checkpointer=checkpointer,
        store=store,
    )
    return agent



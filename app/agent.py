from __future__ import annotations

import os
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from langgraph.runtime import get_runtime

from .tools import get_weather, remember_name, get_known_name
from .context import Ctx


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def _build_pre_model_hook():
    def pre_model_hook(state: Dict[str, Any]) -> Dict[str, Any]:
        messages: List[BaseMessage] = state["messages"]
        trimmed = trim_messages(
            messages,
            strategy="last",
            max_tokens=384,
            token_counter=count_tokens_approximately,
            start_on="human",
            end_on=("human", "tool"),
        )
        return {"llm_input_messages": trimmed}

    return pre_model_hook


def _prompt(state):
    rt = get_runtime(Ctx)
    sys = (
        "You are TicketAgent, helpful and concise."
        f" The current user id is {rt.context.user_id}."
        " Use tools when helpful. If the user asks their name, first try long-term store."
    )
    return [{"role": "system", "content": sys}] + state["messages"]


def build_agent():
    db_url = _require_env("DATABASE_URL")
    _require_env("OPENAI_API_KEY")

    model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

    checkpointer = PostgresSaver.from_conn_string(db_url)
    store = PostgresStore.from_conn_string(db_url)

    agent = create_react_agent(
        model=model,
        tools=[get_weather, remember_name, get_known_name],
        pre_model_hook=_build_pre_model_hook(),
        prompt=_prompt,
        context_schema=Ctx,
        checkpointer=checkpointer,
        store=store,
    )

    # Protect against infinite loops in examples
    max_steps = int(os.getenv("RECURSION_MAX_STEPS", "3"))
    recursion_limit = 2 * max_steps + 1
    return agent.with_config(recursion_limit=recursion_limit)



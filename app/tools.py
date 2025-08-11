from __future__ import annotations

from typing import Optional

from langchain_core.tools import tool
from langgraph.config import get_store
from langchain_core.runnables import RunnableConfig


@tool
def get_weather(city: str) -> str:
    """Return a fake weather snippet for a city."""
    return f"{city}: 18–24°C, clear skies"


@tool
def remember_name(name: str, config: RunnableConfig) -> str:
    """Save user's name into the long-term store for cross-thread recall."""
    store = get_store()
    user_id: Optional[str] = config.get("context", {}).get("user_id")  # type: ignore[assignment]
    if not user_id:
        return "Missing user_id in context."
    ns = ("memories", user_id)
    store.put(ns, "name", {"data": name})
    return f"Stored name for user {user_id}."


@tool
def get_known_name(config: RunnableConfig) -> str:
    """Retrieve stored user's name from long-term store, if any."""
    store = get_store()
    user_id: Optional[str] = config.get("context", {}).get("user_id")  # type: ignore[assignment]
    if not user_id:
        return "Unknown user"
    v = store.get(("memories", user_id), "name")
    return v.value["data"] if v and v.value else "Unknown"



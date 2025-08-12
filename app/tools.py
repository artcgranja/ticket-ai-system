from __future__ import annotations

from typing import Optional

from langchain_core.tools import tool
from langgraph.config import get_store
from langchain_core.runnables import RunnableConfig


@tool
def get_weather(city: str) -> str:
    """Return a fake weather snippet for a city."""
    return f"{city}: 18–24°C, clear skies"
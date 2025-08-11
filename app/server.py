from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from .agent import build_agent

app = FastAPI(title="Ticket AI Agent")
_agent = None


class ChatInput(BaseModel):
    message: str
    thread_id: str
    user_id: str


def _get_agent():
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


@app.post("/chat")
def chat(inp: ChatInput) -> Dict[str, Any]:
    agent = _get_agent()
    out = agent.invoke({"messages": inp.message}, context={"thread_id": inp.thread_id, "user_id": inp.user_id})
    return {"message": out["messages"][-1].content}



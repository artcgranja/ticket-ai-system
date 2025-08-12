from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Ctx:
    user_id: str
    user_name: str
    thread_id: str
from pydantic import BaseModel, Field
from typing import Literal

class Ticket(BaseModel):
    user_id: str = Field(description="ID of the user creating the ticket")
    thread_id: str = Field(description="ID of the ticket thread")
    user_name: str = Field(description="Name of the user creating the ticket")
    subject: str = Field(description="Subject of the ticket")
    description: str = Field(description="Description of the ticket")
    risk: Literal["low", "medium", "high"] = Field(description="Risk of the ticket")
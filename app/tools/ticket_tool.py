from __future__ import annotations

from typing import Optional, Dict

from langchain_core.tools import tool
from app.schemas.ticket_schemas import Ticket
from app.models.ticket_model import TicketModel
from app.db import session

@tool
def create_ticket(ticket: Ticket) -> Dict:
    """
    Create a new ticket.

    Use this tool to validate and serialize a support ticket using the `Ticket` Pydantic schema.
    Persists the ticket to the database using the global scoped SQLAlchemy session.

    Args:
        ticket (Ticket): Pydantic model with ticket fields:
            - user_id (str): ID of the user creating the ticket.
            - thread_id (str): Conversation/thread ID related to the ticket.
            - user_name (str): Display name of the user.
            - subject (str): Ticket subject.
            - description (str): Detailed description of the issue or request.
            - risk (Literal["low", "medium", "high"]): Risk level.

    Returns:
        Dict: The ticket data serialized to a plain dictionary.

    Raises:
        pydantic.ValidationError: If any field is not compliant with the `Ticket` schema.

    Notes:
        - Keep the description concise for LLM consumption.
        - Call this tool only when all required fields are available.

        Example:
        ```python
        from app.schemas.ticket_schemas import Ticket

        payload = Ticket(
            user_id="u1",
            thread_id="u1:chat-001",
            user_name="Ana",
            subject="Login issue",
            description="Cannot sign in since yesterday",
            risk="medium",
        )

        result = create_ticket(payload)
        # {
        #   'user_id': 'u1',
        #   'thread_id': 'u1:chat-001',
        #   'user_name': 'Ana',
        #   'subject': 'Login issue',
        #   'description': 'Cannot sign in since yesterday',
        #   'risk': 'medium'
        # }
        ```
    """
    ticket_model = TicketModel.from_ticket(ticket)
    session.add(ticket_model)
    session.commit()
    return ticket_model.to_ticket().model_dump()
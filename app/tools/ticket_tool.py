from __future__ import annotations

from typing import Optional, Dict

from langchain_core.tools import tool
from app.schemas.ticket_schemas import Ticket

@tool
def create_ticket(ticket: Ticket) -> Dict:
    """
    Create a new ticket.

    Use this tool to validate and serialize a support ticket using the `Ticket` Pydantic schema.
    It does not persist data; database writes and integrations should be implemented in a
    service/repository layer.

    Args:
        ticket (Ticket): Pydantic model with ticket fields:
            - id_usuario (str): ID of the user creating the ticket.
            - thread_id (str): Conversation/thread ID related to the ticket.
            - nome_usuario (str): Display name of the user.
            - tema (str): Ticket subject.
            - descricao (str): Detailed description of the issue or request.
            - risco (Literal["baixo", "medio", "alto"]): Risk level.

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
            id_usuario="u1",
            thread_id="u1:chat-001",
            nome_usuario="Ana",
            tema="Login issue",
            descricao="Cannot sign in since yesterday",
            risco="medio",
        )

        result = create_ticket(payload)
        # {
        #   'id_usuario': 'u1',
        #   'thread_id': 'u1:chat-001',
        #   'nome_usuario': 'Ana',
        #   'tema': 'Login issue',
        #   'descricao': 'Cannot sign in since yesterday',
        #   'risco': 'medio'
        # }
        ```
    """
    return ticket.model_dump()
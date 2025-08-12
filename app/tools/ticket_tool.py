"""Tools for creating, retrieving, listing, updating and deleting support tickets.

All functions in this module operate on the `Ticket` Pydantic schema and the
`TicketModel` SQLAlchemy model. The `create_ticket` function is exposed as a
LangChain tool using the `@tool` decorator.
"""

from __future__ import annotations

from typing import Optional, Dict, List

from langchain_core.tools import tool
from app.schemas.ticket_schemas import Ticket
from app.models.ticket_model import TicketModel
from app.db import session

@tool
def create_ticket(ticket: Ticket) -> Dict:
    """
    Create and persist a new support ticket.

    Validates the payload using the `Ticket` Pydantic schema and persists a new
    `TicketModel` via the global SQLAlchemy session. Returns the ticket as a
    plain dict, including the server-generated `unique_id` (UUIDv4) used for tracking.

    Args:
        ticket

    Returns:
        Dict: Serialized ticket data, including `unique_id`.
    """
    ticket_model = TicketModel.from_ticket(ticket)
    session.add(ticket_model)
    session.commit()
    return ticket_model.to_ticket().model_dump()

def get_ticket(unique_id: str) -> Dict:
    """
    Retrieve a ticket by its tracking `unique_id` (UUIDv4).

    Args:
        unique_id: The server-generated UUIDv4 assigned when the ticket was created.

    Returns:
        Dict | None: The serialized ticket if found, otherwise None.
    """
    ticket_model = session.query(TicketModel).filter(TicketModel.unique_id == unique_id).first()
    return ticket_model.to_ticket().model_dump() if ticket_model else None

def get_all_user_tickets(user_id: str) -> List[Dict]:
    """
    List all tickets created by a specific user.

    Args:
        user_id: The user identifier whose tickets should be retrieved.

    Returns:
        List[Dict]: A list of serialized tickets (possibly empty).
    """
    ticket_models = session.query(TicketModel).filter(TicketModel.user_id == user_id).all()
    return [ticket_model.to_ticket().model_dump() for ticket_model in ticket_models]

def edit_ticket(unique_id: str, ticket: Ticket) -> Dict:
    """
    Update a ticket identified by its `unique_id` with new values.

    Args:
        unique_id: The tracking UUIDv4 of the ticket to edit.
        ticket: A `Ticket` payload containing the new field values.

    Returns:
        Dict: The updated ticket serialized to a dictionary.
    """
    ticket_model = session.query(TicketModel).filter(TicketModel.unique_id == unique_id).first()
    ticket_model.update(ticket)
    session.commit()
    return ticket_model.to_ticket().model_dump()

def delete_ticket(unique_id: str) -> Dict:
    """
    Delete a ticket identified by its `unique_id`.

    Args:
        unique_id: The tracking UUIDv4 of the ticket to delete.

    Returns:
        Dict | None: The deleted ticket serialized to a dictionary, or None if not found.
    """
    ticket_model = session.query(TicketModel).filter(TicketModel.unique_id == unique_id).first()
    session.delete(ticket_model)
    session.commit()
    return ticket_model.to_ticket().model_dump()
from enum import Enum as PyEnum
import uuid

from sqlalchemy import Column, Integer, String, Enum as SAEnum

from app.schemas.ticket_schemas import Ticket
from .base import Base, BaseModel

class Risco(PyEnum):
    baixo = "low"
    medio = "medium"
    alto = "high"


class TicketModel(BaseModel):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    thread_id = Column(String, index=True)
    user_name = Column(String, index=True)
    subject = Column(String, index=True)
    description = Column(String, index=True)
    risk = Column(SAEnum(Risco, name="risco_enum"), index=True)
    unique_id = Column(
        String(36),
        index=True,
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )


    def to_ticket(self) -> Ticket:
        return Ticket(
            user_id=self.user_id,
            thread_id=self.thread_id,
            user_name=self.user_name,
            subject=self.subject,
            description=self.description,
            risk=self.risk.value if isinstance(self.risk, Risco) else self.risk,
            unique_id=self.unique_id,
        )

    @staticmethod
    def from_ticket(ticket: Ticket) -> "TicketModel":
        return TicketModel(
            user_id=ticket.user_id,
            thread_id=ticket.thread_id,
            user_name=ticket.user_name,
            subject=ticket.subject,
            description=ticket.description,
            risk=Risco(ticket.risk),
        )
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Enum as SAEnum

from app.schemas.ticket_schemas import Ticket
from .base import Base

class Risco(PyEnum):
    baixo = "baixo"
    medio = "medio"
    alto = "alto"


class TicketModel(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    thread_id = Column(String, index=True)
    nome_usuario = Column(String, index=True)
    tema = Column(String, index=True)
    descricao = Column(String, index=True)
    risco = Column(SAEnum(Risco, name="risco_enum"), index=True)

    def to_ticket(self) -> Ticket:
        return Ticket(
            user_id=self.user_id,
            thread_id=self.thread_id,
            user_name=self.nome_usuario,
            subject=self.tema,
            description=self.descricao,
            risk=self.risco.value if isinstance(self.risco, Risco) else self.risco,
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
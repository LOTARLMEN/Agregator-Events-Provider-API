import uuid
import uuid as uuid_pkg
from typing import Sequence

from sqlalchemy import select, delete

from src.application.dtos.ticket import TicketRequestSchem
from .base import BaseRepo
from src.infrastructure.db.models.ticket import Ticket


class TicketRepo(BaseRepo):
    async def get_tickets(self) -> Sequence[Ticket]:
        result = await self.session.execute(select(Ticket))
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Ticket | None:
        stmt = select(Ticket).where(Ticket.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(
        self, ticket_data: TicketRequestSchem, ticket_id: uuid.UUID
    ) -> Ticket:
        new_ticket = Ticket(
            id=ticket_id,
            event_id=ticket_data.event_id,
            first_name=ticket_data.first_name,
            last_name=ticket_data.last_name,
            email=ticket_data.email,
            seat=ticket_data.seat,
        )
        self.session.add(new_ticket)
        return new_ticket

    async def delete(self, ticket_id: uuid_pkg.UUID) -> bool:
        stmt = delete(Ticket).where(Ticket.id == ticket_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def is_ticket_in(self, ticket: TicketRequestSchem) -> bool:
        query = select(Ticket).where(
            Ticket.event_id == ticket.event_id, Ticket.seat == ticket.seat
        )
        result = await self.session.execute(query)
        found_ticket = result.scalars().first()

        return found_ticket is not None

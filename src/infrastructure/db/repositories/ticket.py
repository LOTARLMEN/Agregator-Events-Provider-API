import uuid as uuid_pkg
from typing import Sequence

from sqlalchemy import select
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

    async def add(self, place: Ticket) -> None:
        self.session.add(place)

    async def delete(self, place: Ticket) -> None:
        await self.session.delete(place)

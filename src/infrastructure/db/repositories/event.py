import uuid as uuid_pkg
from typing import Sequence
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from .base import BaseRepo
from src.infrastructure.db.models.event import Event


class EventRepo(BaseRepo):

    async def get_events(self) -> Sequence[Event]:
        result = await self.session.execute(select(Event))
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Event | None:
        stmt = select(Event).options(joinedload(Event.place)).where(Event.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, event: Event) -> None:
        self.session.add(event)

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)

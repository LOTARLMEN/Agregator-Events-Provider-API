import uuid as uuid_pkg
from typing import Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from .base import BaseRepo
from src.infrastructure.db.models.event import Event


class EventRepo(BaseRepo):

    async def get_all(self) -> Sequence[Event]:
        result = await self.session.execute(select(Event))
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Event | None:
        stmt = select(Event).options(joinedload(Event.place)).where(Event.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_all(self, events_data: list[dict]):
        if not events_data:
            return

        stmt = insert(Event).values(events_data)

        stmt = stmt.on_conflict_do_update(
            index_elements=[Event.id],
            set_={
                "name": stmt.excluded.name,
                "event_time": stmt.excluded.event_time,
                "registration_deadline": stmt.excluded.registration_deadline,
                "status": stmt.excluded.status,
                "number_of_visitors": stmt.excluded.number_of_visitors,
                "place_uuid": stmt.excluded.place_uuid,
                "changed_at": stmt.excluded.changed_at,
            },
        )
        await self.session.execute(stmt)

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)

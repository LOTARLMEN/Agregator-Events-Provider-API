import uuid as uuid_pkg
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from .base import BaseRepo
from src.infrastructure.db.models.event import Event


class EventRepo(BaseRepo):

    async def get_all(self, limit: int, offset: int, date_from: datetime = None):
        stmt = select(Event).options(joinedload(Event.place))

        if date_from:
            stmt = stmt.where(Event.event_time >= date_from)

        stmt = stmt.limit(limit).offset(offset).order_by(Event.event_time)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Event | None:
        stmt = select(Event).options(joinedload(Event.place)).where(Event.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_count(self, date_from=None) -> int:
        stmt = select(count(Event.id))

        if date_from:
            stmt = stmt.where(Event.event_time >= date_from)

        result = await self.session.execute(stmt)
        return result.scalar() or 0

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
                "updated_at": stmt.excluded.updated_at,
            },
        )
        await self.session.execute(stmt)

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)

from typing import Any
from uuid import UUID
from sqlalchemy import select, update
from src.infrastructure.db.models.outbox.outbox import Outbox
from src.infrastructure.db.models.outbox.status import OutboxStatus
from src.infrastructure.db.repositories.base import BaseRepo


class OutboxRepo(BaseRepo):

    async def add(
        self,
        event_type: str,
        payload: dict[str, Any],
        status: OutboxStatus = OutboxStatus.PENDING,
    ) -> None:
        new_event = Outbox(
            event_type=event_type,
            payload=payload,
            status=status,
        )
        self.session.add(new_event)

    async def get_events(
        self,
        status: OutboxStatus = OutboxStatus.PENDING,
        limit: int = 100,
    ) -> list[Outbox]:
        stmt = (
            select(Outbox)
            .where(Outbox.status == status)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        events = await self.session.execute(stmt)
        return events.scalars().all()

    async def update_status(
        self,
        ids: list[UUID],
        status: OutboxStatus = OutboxStatus.SENT,
    ) -> None:
        stmt = update(Outbox).where(Outbox.id.in_(ids)).values(status=status)
        await self.session.execute(stmt)

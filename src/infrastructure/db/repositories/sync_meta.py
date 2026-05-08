from sqlalchemy import select

from src.infrastructure.db.models.sync.meta import SyncMeta

from .base import BaseRepo


class SyncMetaRepo(BaseRepo):
    async def get(self) -> SyncMeta | None:
        result = await self.session.execute(select(SyncMeta).limit(1))
        meta = result.scalar_one_or_none()

        if meta is None:
            meta = SyncMeta(last_changed_at=None, last_sync_time=None, sync_status=None)

            self.session.add(meta)

        return meta

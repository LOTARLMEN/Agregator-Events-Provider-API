from sqlalchemy import select
from .base import BaseRepo
from src.infrastructure.db.models.sync.meta import SyncMeta


class SyncMetaRepo(BaseRepo):

    async def get(self) -> SyncMeta | None:
        stmt = select(SyncMeta).where(SyncMeta.id == 1)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

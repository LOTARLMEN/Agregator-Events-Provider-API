from traceback import TracebackException
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.repositories.event import EventRepo
from src.infrastructure.db.repositories.place import PlaceRepo
from src.infrastructure.db.repositories.sync_meta import SyncMetaRepo
from src.infrastructure.db.repositories.ticket import TicketRepo


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.events_repo = EventRepo(self.session)
        self.places_repo = PlaceRepo(self.session)
        self.sync_meta_repo = SyncMetaRepo(self.session)
        self.ticket_repo = TicketRepo(self.session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self, exc_type: Exception, exc_val: TracebackException, exc_tb: TracebackType
    ) -> None:
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

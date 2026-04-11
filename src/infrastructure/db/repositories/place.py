import uuid as uuid_pkg
from typing import Sequence

from sqlalchemy import select
from .base import BaseRepo
from src.infrastructure.db.models.place import Place


class PlaceRepo(BaseRepo):

    async def get_places(self) -> Sequence[Place]:
        result = await self.session.execute(select(Place))
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Place | None:
        stmt = select(Place).where(Place.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, place: Place) -> None:
        self.session.add(place)

    async def delete(self, place: Place) -> None:
        await self.session.delete(place)

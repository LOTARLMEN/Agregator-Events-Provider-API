import uuid as uuid_pkg
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRepo
from src.infrastructure.db.models.place import Place


class PlaceRepo(BaseRepo):
    async def get_all(self) -> Sequence[Place]:
        result = await self.session.execute(select(Place))
        return result.scalars().all()

    async def get_by_uuid(self, uuid: uuid_pkg.UUID) -> Place | None:
        stmt = select(Place).where(Place.id == uuid)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_all(self, places_data: list[dict]):
        if not places_data:
            return

        stmt = insert(Place).values(places_data)

        stmt = stmt.on_conflict_do_update(
            index_elements=[Place.id],
            set_={
                "name": stmt.excluded.name,
                "city": stmt.excluded.city,
                "address": stmt.excluded.address,
                "seats_pattern": stmt.excluded.seats_pattern,
            },
        )
        await self.session.execute(stmt)

    async def delete(self, place: Place) -> None:
        await self.session.delete(place)

from uuid import UUID

from .base import BaseUseCase
from ..dtos.event import EventSchema


class GetEventUseCase(BaseUseCase):

    async def get_events(self) -> list[EventSchema]:
        async with self.uow:
            events = await self.uow.events_repo.get_events()
            return [EventSchema.model_validate(event) for event in events]

    async def get_by_uuid(self, uuid: UUID) -> EventSchema:
        async with self.uow:
            event = self.uow.events_repo.get_by_uuid(uuid=uuid)
            return EventSchema.model_validate(event)

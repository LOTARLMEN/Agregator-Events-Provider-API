import datetime
from uuid import UUID

from .base import BaseUseCase
from src.application.dtos.event import EventResponseSchema
from src.infrastructure.clients.events.paginator import EventsPaginator
from src.infrastructure.db.models.sync.status import SyncStatus


class GetEventsUseCase(BaseUseCase):

    async def get_events(self) -> list[EventResponseSchema]:
        async with self.uow:
            events = await self.uow.events_repo.get_all()
            return [EventResponseSchema.model_validate(event) for event in events]

    async def get_by_uuid(self, uuid: UUID) -> EventResponseSchema:
        async with self.uow:
            event = await self.uow.events_repo.get_by_uuid(uuid=uuid)
            return EventResponseSchema.model_validate(event)


class AddEventsUseCase(BaseUseCase):

    async def execute(self):
        async with self.uow:
            meta = await self.uow.sync_meta_repo.get()
            if meta is None:
                start_date = "2000-01-01"
            else:
                start_date = (
                    meta.last_changed_at.date().isoformat()
                    if meta.last_changed_at
                    else "2000-01-01"
                )

            global_max_changed_at = meta.last_changed_at

            async for batch in EventsPaginator(self.client, start_date):
                if not batch:
                    continue

                places_to_upsert = {}
                events_to_upsert = {}

                for item in batch:
                    p = item["place"]
                    places_to_upsert[p["id"]] = {
                        "id": p["id"],
                        "name": p["name"],
                        "city": p["city"],
                        "address": p["address"],
                        "seats_pattern": p["seats_pattern"],
                    }
                    events_to_upsert[item["id"]] = {
                        "id": item["id"],
                        "name": item["name"],
                        "event_time": datetime.datetime.fromisoformat(
                            item["event_time"]
                        ),
                        "registration_deadline": datetime.datetime.fromisoformat(
                            item["registration_deadline"]
                        ),
                        "status": item["status"],
                        "number_of_visitors": item["number_of_visitors"],
                        "place_uuid": p["id"],
                        "updated_at": datetime.datetime.fromisoformat(
                            item["changed_at"]
                        ),
                    }

                await self.uow.places_repo.upsert_all(list(places_to_upsert.values()))
                await self.uow.events_repo.upsert_all(list(events_to_upsert.values()))

                batch_max = max(
                    datetime.datetime.fromisoformat(item["changed_at"])
                    for item in batch
                )
                if global_max_changed_at is None or batch_max > global_max_changed_at:
                    global_max_changed_at = batch_max

            if global_max_changed_at:
                meta.last_changed_at = global_max_changed_at

            meta.sync_status = SyncStatus.updated
            meta.last_sync_time = datetime.datetime.now(datetime.timezone.utc)

            await self.uow.commit()

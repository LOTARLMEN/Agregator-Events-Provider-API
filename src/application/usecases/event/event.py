import datetime
from uuid import UUID

from sqlalchemy import text

from src.application.exceptions import EventNotFound, EventAlreadyFinished
from src.application.usecases.base import BaseUseCase
from src.application.dtos.event import EventDetailResponseSchema
from src.application.dtos.pagination import PaginationSchema
from src.infrastructure.clients.events.paginator import EventsPaginator
from src.infrastructure.db.models.sync.status import SyncStatus


class GetEventsUseCase(BaseUseCase):
    async def get_events(
        self,
        paginator: PaginationSchema,
    ) -> tuple[int, list]:
        async with self.uow:
            count = await self.uow.events_repo.get_count(date_from=paginator.data_from)

            offset = (paginator.page - 1) * paginator.page_size
            limit = paginator.page_size

            events = await self.uow.events_repo.get_all(
                limit=limit, offset=offset, date_from=paginator.data_from
            )
            await self.uow.commit()
        return count, events

    async def get_by_uuid(self, uuid: UUID) -> EventDetailResponseSchema:
        async with self.uow:
            event = await self.uow.events_repo.get_by_uuid(uuid=uuid)
            if event is None:
                raise EventNotFound("Event not found.")
            return EventDetailResponseSchema.model_validate(event)

    async def get_seats(self, event_id: UUID):
        async with self.uow:
            event = await self.uow.events_repo.get_by_uuid(event_id)

            if event is None:
                raise EventNotFound("Event not found.")

            if event.status == "finished":
                raise EventAlreadyFinished("Event already finished.")

            client_response = await self.client.seats(event_id)
            available_seats = client_response.get("seats", [])
            await self.uow.commit()

        return {"event_id": event_id, "available_seats": available_seats}


class AddEventsUseCase(BaseUseCase):
    LOCK_ID = 987654321
    CHUNK_SIZE = 50

    async def execute(self):
        await self.uow.session.execute(
            text("SELECT pg_advisory_lock(:id)"), {"id": self.LOCK_ID}
        )

        try:
            meta = await self.uow.sync_meta_repo.get()
            start_date = (
                meta.last_changed_at.date().isoformat()
                if meta and meta.last_changed_at
                else "2000-01-01"
            )
            global_max_changed_at = meta.last_changed_at if meta else None

            batch_counter = 0

            async with self.uow:
                async for batch in EventsPaginator(self.client, start_date):
                    if not batch:
                        continue

                    places_dict = {}
                    events_list = []

                    for item in batch:
                        p = item["place"]

                        if p["id"] not in places_dict:
                            places_dict[p["id"]] = {
                                "id": p["id"],
                                "name": p["name"],
                                "city": p["city"],
                                "address": p["address"],
                                "seats_pattern": p["seats_pattern"],
                            }

                        events_list.append(
                            {
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
                        )

                    await self.uow.places_repo.upsert_all(list(places_dict.values()))
                    await self.uow.events_repo.upsert_all(events_list)

                    batch_counter += 1
                    if batch_counter % self.CHUNK_SIZE == 0:
                        await self.uow.commit()

                    batch_max = max(
                        datetime.datetime.fromisoformat(item["changed_at"])
                        for item in batch
                    )
                    if not global_max_changed_at or batch_max > global_max_changed_at:
                        global_max_changed_at = batch_max

                await self.uow.commit()

            async with self.uow:
                db_meta = await self.uow.sync_meta_repo.get()
                if db_meta:
                    db_meta.last_changed_at = global_max_changed_at
                    db_meta.sync_status = SyncStatus.updated
                    db_meta.last_sync_time = datetime.datetime.now(
                        datetime.timezone.utc
                    )
                await self.uow.commit()

        finally:
            await self.uow.session.execute(
                text("SELECT pg_advisory_unlock(:id)"), {"id": self.LOCK_ID}
            )

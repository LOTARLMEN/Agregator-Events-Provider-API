import asyncio
import sentry_sdk
from httpx import HTTPStatusError

from src.infrastructure.db.session import db_helper
from src.infrastructure.db.repositories.outbox import OutboxRepo
from src.infrastructure.clients.capashino.capashino import CapashinoClient


async def run_worker():
    capashino_client = CapashinoClient()

    while True:
        events_processed = False

        try:
            async with db_helper.session_factory() as session:
                repo = OutboxRepo(session)

                events = await repo.get_events(limit=100)
                if not events:
                    await session.rollback()
                else:
                    processed_ids = []

                    for event in events:
                        try:
                            await capashino_client.notifications(
                                payload=event.payload,
                            )
                            processed_ids.append(event.id)

                        except HTTPStatusError as e:
                            if e.response.status_code == 409:
                                processed_ids.append(event.id)
                            else:
                                sentry_sdk.capture_exception(e)

                        except Exception as e:
                            sentry_sdk.capture_exception(e)

                    if processed_ids:
                        await repo.update_status(processed_ids)
                        await session.commit()
                        events_processed = True

        except Exception as e:
            sentry_sdk.capture_exception(e)
            await asyncio.sleep(2)
            continue

        if events_processed:
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(5)

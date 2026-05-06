import asyncio
import sentry_sdk
from httpx import HTTPStatusError

from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.repositories.outbox import OutboxRepo
from src.infrastructure.clients.capashino.capashino import CapashinoClient


async def run_worker():
    capashino_client = CapashinoClient()

    while True:
        has_events = False
        events_processed = False

        try:
            async for session in get_async_session():
                repo = OutboxRepo(session)

                events = await repo.get_events(limit=100)

                if not events:
                    break

                has_events = True
                processed_ids = []

                for event in events:
                    message = event.payload.get("message")
                    reference_id = event.payload.get("reference_id")
                    idempotency_key = event.payload.get("idempotency_key", event.id)

                    try:
                        await capashino_client.notifications(
                            message=message,
                            reference_id=reference_id,
                            idempotency_key=idempotency_key,
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
                else:
                    await session.rollback()

                break

        except Exception as e:
            sentry_sdk.capture_exception(e)
            await asyncio.sleep(2)
            continue

        if not has_events:
            await asyncio.sleep(5)
        elif not events_processed:
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(1)

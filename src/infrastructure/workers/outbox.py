import asyncio
import sentry_sdk

from src.infrastructure.db.session import db_helper
from src.infrastructure.db.repositories.outbox import OutboxRepo
from src.infrastructure.db.repositories.outbox import OutboxStatus
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
                    await asyncio.sleep(10)
                    print("Спим 10 секунд. Ивентов не было.")
                    continue

                else:
                    processed_ids = []
                    failed_ids = []

                    for event in events:
                        # try:
                        if event.retry > 3:
                            failed_ids.append(event.id)
                            continue

                        await capashino_client.notifications(
                            payload=event.payload,
                        )
                        processed_ids.append(event.id)
                        await repo.update_retry(event.id)
                        print(
                            f"Обработал событие: {event.id} \nПопытка номер: {event.retry}"
                        )

                    # # except HTTPStatusError as e:
                    #     if e.response.status_code == 409:
                    #         print(e.response.json())
                    #         processed_ids.append(event.id)
                    #     else:
                    #         sentry_sdk.capture_exception(e)
                    #         break

                    # except Exception as e:
                    #     print(f"Ошибка при обработке {event.id}: {e}")
                    #     sentry_sdk.capture_exception(e)
                    #     continue

                    if processed_ids:
                        await repo.update_status(processed_ids)
                        await session.commit()
                        events_processed = True
                    if failed_ids:
                        await repo.update_status(failed_ids, OutboxStatus.FAILED)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            await asyncio.sleep(3)
            continue

        if events_processed:
            await asyncio.sleep(5)

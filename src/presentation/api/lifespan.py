import asyncio
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from src.application.usecases import AddEventsUseCase
from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.uow import UnitOfWork
from src.infrastructure.di import event_client
from src.infrastructure.workers.outbox import run_worker


async def sync_job():
    async for session in get_async_session():
        uow = UnitOfWork(session)
        usecase = AddEventsUseCase(uow, event_client)
        await usecase.execute()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        sync_job,
        CronTrigger(hour=0, minute=0),
    )
    scheduler.start()
    task = asyncio.create_task(run_worker())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    scheduler.shutdown()

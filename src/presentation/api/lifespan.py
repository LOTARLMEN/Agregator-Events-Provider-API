from contextlib import asynccontextmanager
from src.infrastructure.db.session import db_helper

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from src.application.usecases import AddEventsUseCase
from src.infrastructure.db.uow import UnitOfWork
from src.infrastructure.di import event_client


async def sync_job():
    async with db_helper.get_session() as session:
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

    yield

    scheduler.shutdown()

from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.uow import UnitOfWork
from src.application.usecases import event as ev


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_uow(session: SessionDep) -> UnitOfWork:
    return UnitOfWork(session)


UoWDep = Annotated[UnitOfWork, Depends(get_uow)]


def get_add_event_usecase(uow: UoWDep) -> ev.AddEventsUseCase:
    return ev.AddEventsUseCase(uow)


def get_event_usecase(uow: UoWDep) -> ev.GetEventsUseCase:
    return ev.GetEventsUseCase(uow)


AddUseCaseDep = Annotated[ev.AddEventsUseCase, Depends(get_add_event_usecase)]
GetUseCaseDep = Annotated[ev.GetEventsUseCase, Depends(get_event_usecase)]

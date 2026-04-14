from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.uow import UnitOfWork
import src.application.usecases as usc

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_uow(session: SessionDep) -> UnitOfWork:
    return UnitOfWork(session)


UoWDep = Annotated[UnitOfWork, Depends(get_uow)]


def get_add_event_usecase(uow: UoWDep) -> usc.AddEventsUseCase:
    return usc.AddEventsUseCase(uow)


def get_event_usecase(uow: UoWDep) -> usc.GetEventsUseCase:
    return usc.GetEventsUseCase(uow)


def get_reg_ticket_usecase(uow: UoWDep) -> usc.TicketRegUseCase:
    return usc.TicketRegUseCase(uow)


AddUseCaseDep = Annotated[usc.AddEventsUseCase, Depends(get_add_event_usecase)]
GetUseCaseDep = Annotated[usc.GetEventsUseCase, Depends(get_event_usecase)]
TicketRegUseCaseDep = Annotated[usc.TicketRegUseCase, Depends(get_reg_ticket_usecase)]

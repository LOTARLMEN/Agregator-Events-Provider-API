from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.clients.events.provider import EventProviderClient
from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.uow import UnitOfWork
import src.application.usecases as usc

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


event_client = EventProviderClient()


def get_event_provider_client() -> EventProviderClient:
    return event_client


def get_uow(session: SessionDep) -> UnitOfWork:
    return UnitOfWork(session)


ClientDep = Annotated[EventProviderClient, Depends(get_event_provider_client)]
UoWDep = Annotated[UnitOfWork, Depends(get_uow)]


def get_add_event_usecase(uow: UoWDep, client: ClientDep) -> usc.AddEventsUseCase:
    return usc.AddEventsUseCase(uow, client)


def get_event_usecase(uow: UoWDep, client: ClientDep) -> usc.GetEventsUseCase:
    return usc.GetEventsUseCase(uow, client)


def get_reg_ticket_usecase(uow: UoWDep, client: ClientDep) -> usc.TicketRegUseCase:
    return usc.TicketRegUseCase(uow, client)


AddUseCaseDep = Annotated[usc.AddEventsUseCase, Depends(get_add_event_usecase)]
GetUseCaseDep = Annotated[usc.GetEventsUseCase, Depends(get_event_usecase)]
TicketRegUseCaseDep = Annotated[usc.TicketRegUseCase, Depends(get_reg_ticket_usecase)]

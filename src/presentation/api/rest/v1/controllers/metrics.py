from fastapi import APIRouter, Response
from prometheus_client import REGISTRY, generate_latest

from src.infrastructure.di import EventRepoDep, TicketRepoDep
from src.infrastructure.metrics import (
    events_total,
    tickets_cancelled_total,
    tickets_created_total,
)

router = APIRouter(tags=["Метрики"])


@router.get("/metrics")
async def metrics(
    event_repo: EventRepoDep,
    ticket_repo: TicketRepoDep,
):
    events_count = await event_repo.get_count()
    tickets_count = await ticket_repo.get_count()
    cancelled_count = 0

    events_total.set(events_count)
    tickets_created_total.set(tickets_count)
    tickets_cancelled_total.set(cancelled_count)

    return Response(
        content=generate_latest(REGISTRY),
        media_type="text/plain",
    )

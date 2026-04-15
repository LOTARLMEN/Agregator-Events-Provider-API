import uuid

from fastapi import APIRouter, Request, Depends

from src.application.dtos.event import (
    EventSeatsResponseSchem,
    EventDetailResponseSchema,
    EventsResponseSchem,
)
from src.application.dtos.pagination import PaginationSchema
from src.infrastructure import di as dep


router = APIRouter(prefix="/api/events", tags=["События"])


def get_pagination_url(
    request: Request, page: int, page_size: int, total_count: int
) -> str | None:
    if page < 1 or (page - 1) * page_size >= total_count:
        return None

    url = request.url.include_query_params(page=page, page_size=page_size)
    return str(url)


@router.get("", response_model=EventsResponseSchem)
async def get_events(
    request: Request,
    usecase: dep.GetUseCaseDep,
    paginator: PaginationSchema = Depends(),
):
    count, events = await usecase.get_events(paginator)

    next_url = get_pagination_url(
        request, paginator.page + 1, paginator.page_size, count
    )
    prev_url = get_pagination_url(
        request, paginator.page - 1, paginator.page_size, count
    )

    return {"count": count, "next": next_url, "previous": prev_url, "results": events}


@router.get("/{event_id}", response_model=EventDetailResponseSchema)
async def get_event_detail(event_id: uuid.UUID, usecase: dep.GetUseCaseDep):
    return await usecase.get_by_uuid(event_id)


@router.get("/{event_id}/seats", response_model=EventSeatsResponseSchem)
async def get_seats(event_id: uuid.UUID, usecase: dep.GetUseCaseDep) -> dict:
    return await usecase.get_seats(event_id)

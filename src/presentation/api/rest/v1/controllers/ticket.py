import uuid

from fastapi import APIRouter, status
from src.application.dtos.ticket import TicketResponseSchem, TicketRequestSchem
from src.infrastructure.di import TicketRegUseCaseDep

router = APIRouter(prefix="/api/tickets", tags=["Билеты"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=TicketResponseSchem
)
async def register_ticket(
    usecase: TicketRegUseCaseDep, ticket: TicketRequestSchem
) -> TicketResponseSchem:
    return await usecase.reg_ticket(ticket)


@router.delete("/{ticket_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_ticket(
    ticket_id: uuid.UUID, usecase: TicketRegUseCaseDep
) -> dict[str, bool]:
    return await usecase.del_ticket(ticket_id)

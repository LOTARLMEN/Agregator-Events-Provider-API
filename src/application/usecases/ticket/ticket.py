import uuid
from datetime import datetime, timezone

from httpx import ConnectTimeout, HTTPStatusError

from src.application.dtos.ticket import TicketRequestSchem, TicketResponseSchem
from src.application.usecases.base import BaseUseCase
from src.infrastructure.db.exeptions import TicketIsRegisteredException, SeatException

from fastapi import status, HTTPException


class TicketRegUseCase(BaseUseCase):

    async def reg_ticket(self, ticket: TicketRequestSchem) -> TicketResponseSchem:
        async with self.uow:
            event = await self.uow.events_repo.get_by_uuid(ticket.event_id)
            if not event or event.status != "published":
                raise HTTPException(
                    status_code=400, detail="Event not published or not found"
                )

            if (
                event.registration_deadline
                and datetime.now(timezone.utc) > event.registration_deadline
            ):
                raise HTTPException(
                    status_code=400, detail="Registration deadline has passed"
                )

            if await self.uow.ticket_repo.is_ticket_in(ticket):
                raise TicketIsRegisteredException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This seat is already booked in our system",
                )

            try:
                available_seats = await self.client.seats(ticket.event_id)
                if ticket.seat not in available_seats["seats"]:
                    raise SeatException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Seat {ticket.seat} is not available at provider",
                    )

                user_data = {
                    "first_name": ticket.first_name,
                    "last_name": ticket.last_name,
                    "email": ticket.email,
                    "seat": ticket.seat,
                }

                provider_res = await self.client.register(ticket.event_id, user_data)
                provider_ticket_id = provider_res["ticket_id"]

            except ConnectTimeout:
                raise HTTPException(status_code=504, detail="Provider server timeout")
            except HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Provider error: {e.response.text}",
                )

            new_ticket = await self.uow.ticket_repo.add(
                ticket, ticket_id=provider_ticket_id
            )

            await self.uow.commit()

            return TicketResponseSchem(id=new_ticket.id)

    async def del_ticket(self, ticket_id: uuid.UUID) -> dict[str, bool]:
        async with self.uow:
            ticket = await self.uow.ticket_repo.get_by_uuid(ticket_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")

            try:
                await self.client.unregister(
                    event_id=ticket.event_id, ticket_id=ticket.id
                )
            except HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Provider error during unregister: {e.response.text}",
                )

            await self.uow.ticket_repo.delete(ticket_id)
            await self.uow.commit()

            return {"success": True}

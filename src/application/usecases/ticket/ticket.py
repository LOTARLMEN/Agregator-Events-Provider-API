import uuid
from datetime import datetime, timezone

from src.application.dtos.ticket import TicketRequestSchem, TicketResponseSchem
from src.application.exceptions import (
    EventNotFound,
    RegistrationDeadlinePasses,
    TicketIsRegistered,
    SeatNotAvailable,
    TicketIsNotRegistered,
    EventNotPublished,
    IdempotencyKeyAlreadyExist,
)

from src.application.usecases.base import BaseUseCase
from src.infrastructure.db.models.event.status import EventStatus


class TicketRegUseCase(BaseUseCase):
    async def reg_ticket(self, ticket: TicketRequestSchem) -> TicketResponseSchem:
        async with self.uow:
            event = await self.uow.events_repo.get_by_uuid(ticket.event_id)
            if not event:
                raise EventNotFound("Event not found.")

            if ticket.idempotency_key:
                existing_event = await self.uow.outbox_repo.get_by_idempotency_key(
                    ticket.idempotency_key
                )
                if existing_event:
                    existing_ticket = await self.uow.ticket_repo.get_by_uuid(
                        existing_event.payload["reference_id"]
                    )

                    if (
                        existing_ticket.first_name == ticket.first_name
                        and existing_ticket.last_name == ticket.last_name
                        and existing_ticket.email == ticket.email
                        and existing_ticket.seat == ticket.seat
                    ):
                        return TicketResponseSchem(id=existing_ticket.id)
                    else:
                        raise IdempotencyKeyAlreadyExist(
                            "Idempotency key already exists."
                        )

            if event.status != EventStatus.PUBLISHED:
                raise EventNotPublished("Event not published.")

            if (
                event.registration_deadline
                and datetime.now(timezone.utc) > event.registration_deadline
            ):
                raise RegistrationDeadlinePasses("Registration deadline.")

            if await self.uow.ticket_repo.is_ticket_in(ticket):
                raise TicketIsRegistered("Ticket already registered.")

            available_seats = await self.client.seats(ticket.event_id)
            if ticket.seat not in available_seats["seats"]:
                raise SeatNotAvailable("Seat not available.")

            user_data = {
                "first_name": ticket.first_name,
                "last_name": ticket.last_name,
                "email": ticket.email,
                "seat": ticket.seat,
            }

            provider_res = await self.client.register(ticket.event_id, user_data)
            provider_ticket_id = provider_res["ticket_id"]

            new_ticket = await self.uow.ticket_repo.add(
                ticket, ticket_id=provider_ticket_id
            )

            payload = {
                "reference_id": new_ticket.id,
                "message": f"Ticket {new_ticket.id} has been registered.",
                "idempotency_key": ticket.idempotency_key,
            }

            await self.uow.outbox_repo.add(
                event_type="ticket_registration",
                payload=payload,
            )

            await self.uow.commit()
            return TicketResponseSchem(id=new_ticket.id)

    async def del_ticket(self, ticket_id: uuid.UUID) -> dict[str, bool]:
        async with self.uow:
            ticket = await self.uow.ticket_repo.get_by_uuid(ticket_id)

            if not ticket:
                raise TicketIsNotRegistered("Ticket not registered.")

            await self.client.unregister(event_id=ticket.event_id, ticket_id=ticket.id)

            await self.uow.ticket_repo.delete(ticket_id)
            await self.uow.commit()

            return {"success": True}

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TicketResponseSchem(BaseModel):
    ticket_id: UUID = Field(validation_alias="id")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TicketRequestSchem(BaseModel):
    event_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    seat: str
    idempotency_key: Annotated[str | None, Field(min_length=1, max_length=64)]

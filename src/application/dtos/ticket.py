from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TicketResponseSchem(BaseModel):

    id: UUID = Field(alias="ticket_id")

    model_config = ConfigDict(from_attributes=True)


class TicketRequestSchem(BaseModel):

    event_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    seat: str

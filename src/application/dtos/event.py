from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.application.dtos.place import PlaceResponseSchema


class BaseEventSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)


class EventResponseSchema(BaseEventSchema):

    id: UUID
    name: str
    place: PlaceResponseSchema
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int


class EventsSeatsResponseSchema(BaseEventSchema):

    id: UUID = Field(alias="event_id")
    available_seats: list[str]

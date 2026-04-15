from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.application.dtos.place import PlaceResponseSchema, DetailPlaceResponseSchema


class BaseEventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseEventResponseSchema(BaseEventSchema):
    id: UUID
    name: str
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int


class EventDetailResponseSchema(BaseEventResponseSchema):
    place: DetailPlaceResponseSchema


class EventResponseSchema(BaseEventResponseSchema):
    place: PlaceResponseSchema


class EventsResponseSchem(BaseEventSchema):
    count: int
    next: str | None
    previous: str | None
    results: list[EventResponseSchema]


class EventsSeatsResponseSchema(BaseEventSchema):
    id: UUID = Field(alias="event_id")
    available_seats: list[str]


class EventSeatsResponseSchem(BaseModel):
    event_id: UUID
    available_seats: list[str]

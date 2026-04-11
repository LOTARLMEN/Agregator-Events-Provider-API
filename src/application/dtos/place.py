from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PlaceResponseSchema(BaseModel):

    id: UUID
    name: str
    city: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class DetailPlaceSchema(PlaceResponseSchema):

    seats_pattern: dict[str, Any]

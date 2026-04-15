import datetime

from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):

    data_from: datetime.datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

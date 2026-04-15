from datetime import datetime
from .base import Base
from sqlalchemy import UUID, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
import uuid as uuid_pkg
from .mixins import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .place import Place


class Event(Base, TimestampMixin):
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    place: Mapped["Place"] = relationship("Place", back_populates="events")
    place_uuid: Mapped[uuid_pkg.UUID] = mapped_column(ForeignKey("places.id"))
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    registration_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(nullable=False)
    number_of_visitors: Mapped[int] = mapped_column(default=0)

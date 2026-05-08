import uuid as uuid_pkg
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.event.status import EventStatus
from src.infrastructure.db.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.infrastructure.db.models.place import Place


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
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)
    number_of_visitors: Mapped[int] = mapped_column(default=0)

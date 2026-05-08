import uuid as uuid_pkg
from typing import TYPE_CHECKING

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .event import Event


class Place(Base):
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    seats_pattern: Mapped[str] = mapped_column(nullable=False)

    events: Mapped[list["Event"]] = relationship("Event", back_populates="place")

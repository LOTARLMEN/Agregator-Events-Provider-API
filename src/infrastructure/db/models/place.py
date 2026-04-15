from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import UUID
import uuid as uuid_pkg
from .base import Base
from typing import TYPE_CHECKING

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

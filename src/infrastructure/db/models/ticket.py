from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
import uuid as uuid_pkg

from .base import Base


class Ticket(Base):
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
        unique=True,
        index=True,
    )
    event_id: Mapped[uuid_pkg.UUID] = mapped_column(ForeignKey("events.id"))
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    seat: Mapped[str] = mapped_column(nullable=False)

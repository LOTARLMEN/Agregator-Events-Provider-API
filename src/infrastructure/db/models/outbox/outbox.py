import uuid
import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import UUID, DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.outbox.status import OutboxStatus


class Outbox(Base):
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    event_type: Mapped[str] = mapped_column(nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    status: Mapped[OutboxStatus] = mapped_column(
        ENUM(OutboxStatus, name="outboxstatus", create_type=False),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    retry: Mapped[int] = mapped_column(default=0)

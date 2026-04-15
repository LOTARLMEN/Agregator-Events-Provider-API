from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from src.infrastructure.db.models.base import Base
from .status import SyncStatus


class SyncMeta(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    last_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_sync_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    sync_status: Mapped[SyncStatus] = mapped_column(nullable=False)
    error_details: Mapped[str] = mapped_column(nullable=True)

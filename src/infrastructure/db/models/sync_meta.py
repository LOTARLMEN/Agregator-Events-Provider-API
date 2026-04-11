from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.infrastructure.db.models.base import Base


class SyncMeta(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    last_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_sync_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    sync_status: Mapped[str] = mapped_column(nullable=False)
    error_details: Mapped[str] = mapped_column(nullable=True)

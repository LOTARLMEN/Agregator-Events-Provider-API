"""add_outbox_table_sync_meta

Revision ID: b3a202fdebdb
Revises: 3d70243c95a1
Create Date: 2026-05-04 13:23:51.236562

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b3a202fdebdb"
down_revision: Union[str, Sequence[str], None] = "3d70243c95a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Безопасно создаем типы ENUM через анонимный блок Postgres
    # Это предотвратит ошибку "already exists"
    op.execute(
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'outboxstatus') THEN "
        "CREATE TYPE outboxstatus AS ENUM ('SENT', 'PENDING'); "
        "END IF; "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'syncstatus') THEN "
        "CREATE TYPE syncstatus AS ENUM ('failed', 'updated'); "
        "END IF; "
        "END $$;"
    )

    # 2. Создаем таблицы
    op.create_table(
        "outboxs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        # create_type=False — это ВАЖНО!
        sa.Column(
            "status",
            sa.Enum("SENT", "PENDING", name="outboxstatus", create_type=False),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )

    op.create_table(
        "sync_metas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("last_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_sync_time", sa.DateTime(timezone=True), nullable=False),
        # Здесь тоже create_type=False
        sa.Column(
            "sync_status",
            sa.Enum("failed", "updated", name="syncstatus", create_type=False),
            nullable=False,
        ),
        sa.Column("error_details", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sync_metas")
    op.drop_table("outboxs")
    # Типы ENUM при откате обычно лучше не удалять вручную,
    # чтобы не сломать другие миграции, если нет доступа к базе.

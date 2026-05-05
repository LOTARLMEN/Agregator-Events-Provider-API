"""add_outbox_table_sync_meta

Revision ID: b3a202fdebdb
Revises: 3d70243c95a1
Create Date: 2026-05-04 13:23:51.236562

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "b3a202fdebdb"
down_revision: Union[str, Sequence[str], None] = "3d70243c95a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    DO $$ BEGIN
        CREATE TYPE outboxstatus AS ENUM ('SENT', 'PENDING');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """
    )

    op.execute(
        """
    DO $$ BEGIN
        CREATE TYPE syncstatus AS ENUM ('failed', 'updated');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """
    )

    outbox_status = ENUM("SENT", "PENDING", name="outboxstatus")
    sync_status = ENUM("failed", "updated", name="syncstatus")

    op.create_table(
        "outboxs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", outbox_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )

    op.create_table(
        "sync_metas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("last_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_sync_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sync_status", sync_status, nullable=False),
        sa.Column("error_details", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("sync_metas")
    op.drop_table("outboxs")

    op.execute("DROP TYPE IF EXISTS outboxstatus")
    op.execute("DROP TYPE IF EXISTS syncstatus")

"""add_outbox_table_sync_meta

Revision ID: b3a202fdebdb
Revises: 3d70243c95a1
Create Date: 2026-05-04 13:23:51.236562
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3a202fdebdb"
down_revision: Union[str, Sequence[str], None] = "3d70243c95a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # =========================
    # ENUM SAFE CREATE
    # =========================
    op.execute(
        """
    DO $$
    BEGIN
        CREATE TYPE outboxstatus AS ENUM ('SENT', 'PENDING');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """
    )

    op.execute(
        """
    DO $$
    BEGIN
        CREATE TYPE syncstatus AS ENUM ('failed', 'updated');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """
    )

    # =========================
    # TABLE SAFE CREATE
    # =========================
    op.execute(
        """
    DO $$
    BEGIN
        CREATE TABLE IF NOT EXISTS outboxs (
            id UUID PRIMARY KEY,
            event_type VARCHAR NOT NULL,
            payload JSONB NOT NULL,
            status VARCHAR NOT NULL,
            created_at TIMESTAMPTZ NOT NULL
        );
    EXCEPTION
        WHEN duplicate_table THEN null;
    END $$;
    """
    )

    op.execute(
        """
    DO $$
    BEGIN
        CREATE TABLE IF NOT EXISTS sync_metas (
            id SERIAL PRIMARY KEY,
            last_changed_at TIMESTAMPTZ NOT NULL,
            last_sync_time TIMESTAMPTZ NOT NULL,
            sync_status VARCHAR NOT NULL,
            error_details VARCHAR
        );
    EXCEPTION
        WHEN duplicate_table THEN null;
    END $$;
    """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS sync_metas")
    op.execute("DROP TABLE IF EXISTS outboxs")

    op.execute("DROP TYPE IF EXISTS outboxstatus")
    op.execute("DROP TYPE IF EXISTS syncstatus")

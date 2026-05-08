"""add retry column and failed status

Revision ID: e500a3f5d6f0
Revises: b6033e01c0ac
Create Date: 2026-05-08 08:55:27.677719
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e500a3f5d6f0"
down_revision: Union[str, Sequence[str], None] = "b6033e01c0ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новое значение в enum
    op.execute("ALTER TYPE outboxstatus ADD VALUE IF NOT EXISTS 'FAILED'")

    # Добавляем колонку retry
    op.add_column(
        "outboxs",
        sa.Column(
            "retry",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # Убираем server_default после заполнения существующих записей
    op.alter_column(
        "outboxs",
        "retry",
        server_default=None,
    )


def downgrade() -> None:
    # Удаляем колонку
    op.drop_column("outboxs", "retry")

    # PostgreSQL не умеет удалять enum value напрямую.
    # Для полноценного downgrade нужно пересоздавать type.
    pass

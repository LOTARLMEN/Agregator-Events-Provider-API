"""fix enum type for outbox

Revision ID: b6033e01c0ac
Revises: 6c76bdc0fb5a
Create Date: 2026-05-06 07:24:47.409416

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6033e01c0ac"
down_revision: Union[str, Sequence[str], None] = "6c76bdc0fb5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE outboxs
        ALTER COLUMN status TYPE outboxstatus
        USING status::outboxstatus;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE outboxs
        ALTER COLUMN status TYPE VARCHAR;
        """
    )

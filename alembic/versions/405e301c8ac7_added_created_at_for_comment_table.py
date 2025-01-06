"""added created_at for comment table

Revision ID: 405e301c8ac7
Revises: 01a9d73b6d76
Create Date: 2025-01-01 16:43:55.443143

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "405e301c8ac7"
down_revision: Union[str, None] = "01a9d73b6d76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "comments",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("comments", "created_at")

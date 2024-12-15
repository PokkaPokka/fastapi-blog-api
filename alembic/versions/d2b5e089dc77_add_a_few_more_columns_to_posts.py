"""add a few more columns to posts

Revision ID: d2b5e089dc77
Revises: afa299a8b6b7
Create Date: 2024-12-14 22:11:46.028337

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2b5e089dc77"
down_revision: Union[str, None] = "afa299a8b6b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )
    op.alter_column("posts", "title", nullable=False)
    op.alter_column("posts", "content", nullable=False)
    op.alter_column("posts", "owner_id", nullable=False)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    op.alter_column("posts", "title", nullable=True)
    op.alter_column("posts", "content", nullable=True)
    op.alter_column("posts", "owner_id", nullable=True)
    pass

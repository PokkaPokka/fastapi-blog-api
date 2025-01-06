"""added a comment table

Revision ID: f87b185558a2
Revises: c1e5233ef666
Create Date: 2025-01-01 15:51:35.149257

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f87b185558a2"
down_revision: Union[str, None] = "c1e5233ef666"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("content", sa.String),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    )


def downgrade() -> None:
    op.drop_table("comments")

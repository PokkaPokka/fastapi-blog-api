"""added id for comment table

Revision ID: 0c27f4f4df4f
Revises: 405e301c8ac7
Create Date: 2025-01-01 21:13:41.825499

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c27f4f4df4f"
down_revision: Union[str, None] = "405e301c8ac7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("content", sa.String),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("comments")

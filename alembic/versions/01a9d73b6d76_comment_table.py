"""comment table

Revision ID: 01a9d73b6d76
Revises: bdc97fd9dd69
Create Date: 2025-01-01 16:20:53.208581

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01a9d73b6d76"
down_revision: Union[str, None] = "bdc97fd9dd69"
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

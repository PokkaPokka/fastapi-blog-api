"""add fk to posts table

Revision ID: afa299a8b6b7
Revises: 826e73b21468
Create Date: 2024-12-14 21:28:54.483717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afa299a8b6b7"
down_revision: Union[str, None] = "826e73b21468"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer))
    op.create_foreign_key(
        "post_user_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", "posts", type_="foreignkey")
    op.drop_column("posts", "owner_id")
    pass

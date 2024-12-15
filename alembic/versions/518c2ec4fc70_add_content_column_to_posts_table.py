"""add content column to posts table

Revision ID: 518c2ec4fc70
Revises: 76b23d727509
Create Date: 2024-12-14 21:14:48.087001

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "518c2ec4fc70"
down_revision: Union[str, None] = "76b23d727509"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

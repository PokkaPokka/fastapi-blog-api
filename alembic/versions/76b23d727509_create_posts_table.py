"""create posts table

Revision ID: 76b23d727509
Revises: 
Create Date: 2024-12-14 21:04:57.822599

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76b23d727509"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

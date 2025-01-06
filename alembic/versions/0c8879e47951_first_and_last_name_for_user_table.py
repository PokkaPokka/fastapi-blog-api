"""first and last name for user table

Revision ID: 0c8879e47951
Revises: 0c27f4f4df4f
Create Date: 2025-01-02 12:25:11.364255

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c8879e47951"
down_revision: Union[str, None] = "0c27f4f4df4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("first_name", sa.String(32), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")

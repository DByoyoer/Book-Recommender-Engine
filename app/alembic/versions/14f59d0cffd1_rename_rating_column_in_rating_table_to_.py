"""Rename rating column in rating table to score

Revision ID: 14f59d0cffd1
Revises: 333b296d42e8
Create Date: 2024-04-03 02:50:37.297581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14f59d0cffd1'
down_revision: Union[str, None] = '333b296d42e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        table_name="rating",
        column_name="rating",
        new_column_name="score"
    )


def downgrade() -> None:
    op.alter_column(
        table_name="rating",
        column_name="score",
        new_column_name="rating"
    )

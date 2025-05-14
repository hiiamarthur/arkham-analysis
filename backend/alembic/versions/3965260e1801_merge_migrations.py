"""merge_migrations

Revision ID: 3965260e1801
Revises: b001beda3f4b, d6fe6cf17f6c
Create Date: 2025-04-26 01:44:22.862309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3965260e1801'
down_revision: Union[str, None] = ('b001beda3f4b', 'd6fe6cf17f6c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

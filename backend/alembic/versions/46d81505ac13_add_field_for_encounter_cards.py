"""Add field for encounter cards

Revision ID: 46d81505ac13
Revises: c8046580d78e
Create Date: 2025-08-28 21:37:52.285494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46d81505ac13'
down_revision: Union[str, None] = 'c8046580d78e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

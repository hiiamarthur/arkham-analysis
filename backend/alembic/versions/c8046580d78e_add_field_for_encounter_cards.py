"""Add field for encounter cards

Revision ID: c8046580d78e
Revises: c7a523d765fe
Create Date: 2025-08-28 21:32:34.254949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8046580d78e'
down_revision: Union[str, None] = 'c7a523d765fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

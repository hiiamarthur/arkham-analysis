"""merge_heads

Revision ID: 041875a6e777
Revises: 0a9e7a661266, ece919d978f5
Create Date: 2025-04-24 22:41:14.094278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '041875a6e777'
down_revision: Union[str, None] = ('0a9e7a661266', 'ece919d978f5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

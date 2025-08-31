"""Increase octgn_id field length

Revision ID: increase_octgn_id_length
Revises: increase_text_field_lengths
Create Date: 2025-08-30 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'increase_octgn_id_length'
down_revision: Union[str, None] = 'increase_text_field_lengths'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Increase octgn_id field length from 200 to 1000
    op.alter_column('cards', 'octgn_id',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=1000),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert octgn_id field length back to 200
    op.alter_column('cards', 'octgn_id',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)

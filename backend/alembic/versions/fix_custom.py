"""Fix customization field lengths

Revision ID: fix_custom
Revises: fix_text_lengths
Create Date: 2025-08-30 13:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_custom'
down_revision: Union[str, None] = 'fix_text_lengths'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Increase customization_text field length from 1000 to 3000
    op.alter_column('cards', 'customization_text',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=3000),
               existing_nullable=True)
    
    # Increase customization_changes field length from 1000 to 3000
    op.alter_column('cards', 'customization_changes',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=3000),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert customization_text field length back to 1000
    op.alter_column('cards', 'customization_text',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
    
    # Revert customization_changes field length back to 1000
    op.alter_column('cards', 'customization_changes',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)

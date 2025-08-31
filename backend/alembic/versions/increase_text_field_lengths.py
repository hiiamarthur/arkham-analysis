"""Increase text field lengths for flavor and back fields

Revision ID: increase_text_field_lengths
Revises: d9ae1b6e8f0d
Create Date: 2025-08-30 12:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'increase_text_field_lengths'
down_revision: Union[str, None] = 'd9ae1b6e8f0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Increase flavor field length from 500 to 2000
    op.alter_column('cards', 'flavor',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=2000),
               existing_nullable=True)
    
    # Increase back_flavor field length from 1000 to 2000
    op.alter_column('cards', 'back_flavor',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=2000),
               existing_nullable=True)
    
    # Increase back_text field length from 1000 to 2000
    op.alter_column('cards', 'back_text',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=2000),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert flavor field length back to 500
    op.alter_column('cards', 'flavor',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    
    # Revert back_flavor field length back to 1000
    op.alter_column('cards', 'back_flavor',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
    
    # Revert back_text field length back to 1000
    op.alter_column('cards', 'back_text',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)

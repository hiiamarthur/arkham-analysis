"""Fix text field lengths

Revision ID: fix_text_lengths
Revises: increase_octgn_id_length
Create Date: 2025-08-30 13:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fix_text_lengths"
down_revision: Union[str, None] = "increase_octgn_id_length"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Increase text field length from 1000 to 3000
    op.alter_column(
        "cards",
        "text",
        existing_type=sa.VARCHAR(length=1000),
        type_=sa.String(length=3000),
        existing_nullable=True,
    )

    # Increase real_text field length from 1000 to 3000
    op.alter_column(
        "cards",
        "real_text",
        existing_type=sa.VARCHAR(length=1000),
        type_=sa.String(length=3000),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert text field length back to 1000
    op.alter_column(
        "cards",
        "text",
        existing_type=sa.String(length=3000),
        type_=sa.VARCHAR(length=1000),
        existing_nullable=True,
    )

    # Revert real_text field length back to 1000
    op.alter_column(
        "cards",
        "real_text",
        existing_type=sa.String(length=3000),
        type_=sa.VARCHAR(length=1000),
        existing_nullable=True,
    )

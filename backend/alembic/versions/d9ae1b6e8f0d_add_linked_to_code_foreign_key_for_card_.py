"""Add linked_to_code foreign key for card relationships

Revision ID: d9ae1b6e8f0d
Revises: 5e9f99b78169
Create Date: 2025-08-29 23:24:17.384082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d9ae1b6e8f0d"
down_revision: Union[str, None] = "5e9f99b78169"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add linked_to_code column to cards table
    op.add_column("cards", sa.Column("linked_to_code", sa.String(50), nullable=True))

    # Add foreign key constraint
    op.create_foreign_key(
        "fk_cards_linked_to_code",
        "cards",
        "cards",
        ["linked_to_code"],
        ["code"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove foreign key constraint
    op.drop_constraint("fk_cards_linked_to_code", "cards", type_="foreignkey")

    # Remove linked_to_code column
    op.drop_column("cards", "linked_to_code")

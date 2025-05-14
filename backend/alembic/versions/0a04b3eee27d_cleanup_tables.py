"""cleanup_tables

Revision ID: 0a04b3eee27d
Revises: 3965260e1801
Create Date: 2025-04-26 01:47:30.049828

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a04b3eee27d"
down_revision: Union[str, None] = "3965260e1801"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Clean all tables
    op.execute("TRUNCATE TABLE card_traits CASCADE")
    op.execute("TRUNCATE TABLE cards CASCADE")
    op.execute("TRUNCATE TABLE traits CASCADE")

    # Reset sequences
    op.execute("ALTER SEQUENCE cards_id_seq RESTART WITH 1")
    op.execute("ALTER SEQUENCE traits_id_seq RESTART WITH 1")


def downgrade() -> None:
    pass

"""fix traits sequence

Revision ID: 0a9e7a661266
Revises: previous_revision_id
Create Date: 2024-xx-xx

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "0a9e7a661266"
down_revision = None  # Set to None if this is your first migration, otherwise use the previous revision ID
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS traits_id_seq")

    # Set sequence as default
    op.execute(
        "ALTER TABLE traits ALTER COLUMN id SET DEFAULT nextval('traits_id_seq')"
    )

    # Set sequence ownership
    op.execute("ALTER SEQUENCE traits_id_seq OWNED BY traits.id")

    # Reset sequence to current max + 1
    op.execute(
        "SELECT setval('traits_id_seq', COALESCE((SELECT MAX(id) FROM traits), 0) + 1, false)"
    )


def downgrade() -> None:
    # Remove sequence default
    op.execute("ALTER TABLE traits ALTER COLUMN id DROP DEFAULT")

    # Drop sequence
    op.execute("DROP SEQUENCE IF EXISTS traits_id_seq")

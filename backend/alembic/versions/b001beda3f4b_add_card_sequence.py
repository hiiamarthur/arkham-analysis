"""add_card_sequence

Revision ID: b001beda3f4b
Revises: d6fe6cf17f6c
Create Date: 2025-04-26 01:42:57.016390

"""

revision = "b001beda3f4b"
down_revision = None  # Set this to your previous migration ID
branch_labels = None
depends_on = None

from alembic import op


def upgrade() -> None:
    # Create sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS cards_id_seq")

    # Set sequence as default for id column
    op.execute("ALTER TABLE cards ALTER COLUMN id SET DEFAULT nextval('cards_id_seq')")

    # Set sequence ownership
    op.execute("ALTER SEQUENCE cards_id_seq OWNED BY cards.id")

    # Reset sequence to current max + 1
    op.execute(
        "SELECT setval('cards_id_seq', COALESCE((SELECT MAX(id) FROM cards), 0) + 1, false)"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE cards ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS cards_id_seq")

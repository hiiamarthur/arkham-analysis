import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
# Add project root to Python path
sys.path.insert(0, project_root)

# Now we can import from app
from app.models.base import BaseModel  # SQLAlchemy model, not Pydantic
from app.models.arkham_model import CardModel, TraitModel  # Import your models

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = BaseModel.metadata  # This line is crucial

FALLBACK_URL = "postgresql://postgres:postgres@localhost:5433/arkham_analysis_db"


def get_url() -> str:
    """Return DB URL — prefers DATABASE_URL env var, falls back to local default."""
    return os.environ.get("DATABASE_URL", FALLBACK_URL)


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

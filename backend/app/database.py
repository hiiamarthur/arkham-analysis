from asyncio.log import logger
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.core.config import settings


load_dotenv()

DB_POOL_SIZE=settings.DB_POOL_SIZE
DB_MAX_OVERFLOW=settings.DB_MAX_OVERFLOW
DB_POOL_RECYCLE=settings.DB_POOL_RECYCLE

# Use DATABASE_URL env var when available (Railway production), otherwise build from parts
_raw_url = os.environ.get("DATABASE_URL") or settings.DATABASE_URL
if _raw_url:
    # Ensure asyncpg driver prefix
    if _raw_url.startswith("postgres://"):
        DATABASE_URL = _raw_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif _raw_url.startswith("postgresql://") and "+asyncpg" not in _raw_url:
        DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        DATABASE_URL = _raw_url
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )

print(f"Connecting to: {DATABASE_URL}")  # Debug print

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Enable connection health checks
    future=True,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_recycle=DB_POOL_RECYCLE,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # Use bind instead of passing engine directly
    class_=AsyncSession,
    expire_on_commit=False,
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.orm").setLevel(logging.WARNING)


# Dependency to get DB session
# async def get_async_db():
#     async with AsyncSessionLocal() as session:
#         yield session
@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()  # Commit if no exceptions
    except Exception as e:
        logger.error(f"Session error: {e.__class__.__name__}: {str(e)}")
        await session.rollback()
        # Don't wrap the error in ResponseSchema here
        raise
    finally:
        try:
            await session.close()
        except Exception as e:
            logger.error(f"Error closing session: {e.__class__.__name__}: {str(e)}")


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions"""
    async with get_db_session() as session:
        yield session

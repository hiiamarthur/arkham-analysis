import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.core.config import settings


load_dotenv()

# Get database credentials from environment
DB_USER = settings.POSTGRES_USER
DB_PASS = settings.POSTGRES_PASSWORD
DB_HOST = settings.POSTGRES_HOST
DB_PORT = settings.POSTGRES_PORT
DB_NAME = settings.POSTGRES_DB

# Construct database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Connecting to: {DATABASE_URL}")  # Debug print

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Enable connection health checks
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
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

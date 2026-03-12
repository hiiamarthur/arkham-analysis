from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum
import os
import logging


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    TEST = "test"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Environment settings
    environment: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True

    # Application
    PROJECT_NAME: str = "Arkham Analysis API"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""

    # JWT
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 30

    # Database Pool Settings
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 60
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO_LOG: bool = False

    # Migration Settings
    MIGRATIONS_DIR: str = "migrations"
    ALEMBIC_CONFIG: str = "alembic.ini"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    GPT_API_URL: str = "https://api.openai.com/v1/chat/completions"
    ORGANIZATION_ID: Optional[str] = None
    PROJECT_ID: Optional[str] = None

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URL: Optional[str] = None

    # Cache Settings
    CACHE_TTL_DEFAULT: int = 3600  # 1 hour
    CACHE_TTL_CARDS: int = 1800  # 30 minutes
    CACHE_TTL_TRAITS: int = 7200  # 2 hours

    # Database URL
    DATABASE_URL: Optional[str] = None
    ARKHAMDB_CARDS_URL: str = "https://arkhamdb.com/api/public/cards"
    ARKHAMDB_URL: str = "https://arkhamdb.com/api"

    def get_database_url(self) -> str:
        """Get async database URL. Prefers DATABASE_URL env var (Railway), falls back to individual POSTGRES_* vars."""
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            # Ensure asyncpg driver prefix
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def get_sync_database_url(self) -> str:
        """Get synchronous database URL for migrations."""
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql+asyncpg://"):
                url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
            elif url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            return url
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

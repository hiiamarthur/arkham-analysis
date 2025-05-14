from typing import Optional
from pydantic_settings import BaseSettings
from pydantic_settings.sources import DotEnvSettingsSource
from functools import lru_cache
from enum import Enum
import os
import logging


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    TEST = "test"
    PRODUCTION = "prod"


class Settings(BaseSettings):
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
    ORGANIZATION_ID: str | None = None
    PROJECT_ID: str | None = None

    # New fields
    database_url: str = ""
    ARKHAMDB_CARDS_URL: str = "https://arkhamdb.com/api/public/cards"
    ARKHAMDB_URL: str = "https://arkhamdb.com/api/public"

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL based on environment"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get synchronous database URL for migrations"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # Add explicit logging at the start
            print("Customise sources called")  # Temporary print for debugging
            print("Customise sources method called")

            env = os.getenv("ENVIRONMENT", "dev")
            env_file = f".env.{env}"

            print(f"Checking for env file: {env_file}")
            if os.path.exists(env_file):
                print(f"Using env file: {env_file}")
                cls.env_file = env_file
            else:
                print(f"Env file {env_file} not found, using .env")
                cls.env_file = ".env"

            print(f"Final env_file setting: {cls.env_file}")

            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )


@lru_cache()
def get_settings() -> Settings:
    print("Getting settings...")
    settings = Settings()
    print("Settings initialized")
    return settings


settings = get_settings()

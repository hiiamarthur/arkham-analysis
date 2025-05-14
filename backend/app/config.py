from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    ARKHAMDB_CARDS_URL: str
    # API configurations
    API_V1_STR: str = "/api/v1"

    
    # CORS configurations
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings() 
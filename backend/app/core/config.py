"""
Core configuration settings for the FastAPI application.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost"]
    
    # API
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

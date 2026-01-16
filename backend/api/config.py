"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Constitution Recognition API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/constitution_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_DECODE_RESPONSE: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Keys (optional)
    TENCENT_COS_SECRET_ID: str = ""
    TENCENT_COS_SECRET_KEY: str = ""
    TENCENT_COS_BUCKET: str = ""
    TENCENT_COS_REGION: str = "ap-guangzhou"

    # Constitution Scoring
    SCORE_CONVERT_FACTOR: float = 2.5
    THRESHOLD_PRIMARY: int = 40
    THRESHOLD_SECONDARY: int = 30
    THRESHOLD_PEACE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()

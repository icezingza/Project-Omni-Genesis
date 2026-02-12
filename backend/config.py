"""
Project Omni-Genesis: Application Configuration
Centralized settings management using Pydantic BaseSettings.
Loads values from environment variables and .env file.
"""

import os
from typing import List, Optional

from pydantic import Field

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for environments without pydantic-settings
    from pydantic import BaseModel as BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Application ---
    APP_NAME: str = "Project Omni-Genesis"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # --- Security ---
    SECRET_KEY: str = "omni-genesis-dev-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # --- Database ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./omni_genesis.db"

    # --- Redis (optional) ---
    REDIS_URL: Optional[str] = None

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 30
    AUTH_RATE_LIMIT_PER_MINUTE: int = 10

    # --- AI / Golden Ratio ---
    PHI: float = 1.618033988749895
    GOLDEN_RATIO_BALANCE_THRESHOLD: float = 0.15

    # --- AI API Keys (optional) ---
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None

    # --- Thai NLP ---
    THAI_NLP_ENGINE: str = "newmm"

    # --- PDPA Compliance ---
    PDPA_REQUIRE_CONSENT: bool = True
    DATA_RETENTION_DAYS: int = 90

    # --- Sentry (optional) ---
    SENTRY_DSN: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


# Singleton instance
settings = Settings()

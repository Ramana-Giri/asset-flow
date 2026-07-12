"""
Application Configuration

Purpose
-------
Central configuration, read from environment variables via Pydantic Settings. Never hardcode secrets.

Responsibilities
-----------------
- Declare a Settings(BaseSettings) class with every environment-driven config value.
- Provide a single cached `settings` instance imported everywhere else.

Interacts With
--------------
- db/database.py -> reads DATABASE_URL.
- core/security.py -> reads password-hashing configuration.
- dependencies.py / core/permissions.py -> reads session/cookie configuration.
- main.py -> reads CORS_ORIGINS.
- utils/file_upload.py -> reads UPLOAD_PATH.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""
from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/assetflow"

    SESSION_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SESSION_COOKIE_NAME: str = "assetflow_session"
    BCRYPT_ROUNDS: int = 12

    UPLOAD_PATH: str = "app/uploads"

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    APP_NAME: str = "AssetFlow"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
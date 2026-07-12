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

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Environment-driven application settings.

    Expected variables (NO JWT - auth is opaque session-token based,
    backed by the `user_sessions` table):
      - DATABASE_URL
      - SESSION_TOKEN_EXPIRE_MINUTES
      - SESSION_COOKIE_NAME
      - UPLOAD_PATH
      - CORS_ORIGINS
      - BCRYPT_ROUNDS
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Fields intentionally omitted from this skeleton.


settings = Settings()

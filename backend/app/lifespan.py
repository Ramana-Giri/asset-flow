"""
Application Lifespan

Purpose
-------
Startup and shutdown hooks for the FastAPI application.

Responsibilities
-----------------
- Initialize the database engine/connection pool on startup.
- Verify database connectivity (fail fast if unreachable).
- Create upload directories if absent (app/uploads/assets, app/uploads/maintenance).
- Close database connections gracefully on shutdown.

Interacts With
--------------
- db/database.py -> the engine/session factory initialized here.
- config.py -> UPLOAD_PATH and DATABASE_URL settings.
- main.py -> registers this as the FastAPI `lifespan` context manager.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.core.logging import configure_logging, get_logger
from app.db.database import engine

logger = get_logger(__name__)

# Subdirectories that must exist under UPLOAD_PATH before the app can safely
# accept asset-document or maintenance-photo uploads (see utils/file_upload.py).
_UPLOAD_SUBFOLDERS = ("assets", "maintenance")


async def _verify_database_connectivity() -> None:
    """Run a trivial SELECT 1 to fail fast if the database is unreachable at startup."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


def _ensure_upload_directories() -> None:
    """Create app/uploads/assets and app/uploads/maintenance if they don't already exist."""
    base_path = Path(settings.UPLOAD_PATH)
    for subfolder in _UPLOAD_SUBFOLDERS:
        (base_path / subfolder).mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: verify DB connectivity, ensure upload directories exist.
    Shutdown: dispose of the DB engine's connection pool cleanly.
    """
    # --- startup ---
    configure_logging()
    logger.info("Starting %s ...", settings.APP_NAME)

    await _verify_database_connectivity()
    logger.info("Database connectivity verified.")

    _ensure_upload_directories()
    logger.info("Upload directories ready at %s", settings.UPLOAD_PATH)

    yield

    # --- shutdown ---
    logger.info("Shutting down %s ...", settings.APP_NAME)
    await engine.dispose()
    logger.info("Database engine disposed.")
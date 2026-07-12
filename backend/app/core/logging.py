"""
Logging Configuration

Purpose
-------
Configure application-wide logging and provide a helper used when writing Activity Log entries.

Responsibilities
-----------------
- configure_logging(): set up log format/level/handlers at startup (called from lifespan.py).
- get_logger(name): return a module-scoped logger.

Interacts With
--------------
- lifespan.py -> calls configure_logging() on startup.
- services/activity_log_service.py -> may use get_logger() alongside DB-persisted activity logs.
"""

import logging
import sys

from app.config import settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def configure_logging() -> None:
    """Configure root logging format/level/handlers for the application."""
    global _configured
    if _configured:
        # Idempotent: avoids duplicate handlers if lifespan startup runs
        # more than once in the same process (e.g. under test reloads).
        return

    level = logging.DEBUG if settings.DEBUG else logging.INFO

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    # Quiet down noisy third-party loggers unless we're in DEBUG mode.
    if not settings.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger instance."""
    return logging.getLogger(name)
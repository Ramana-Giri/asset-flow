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

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

import logging


def configure_logging() -> None:
    """Configure root logging format/level/handlers for the application."""
    pass


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger instance."""
    return logging.getLogger(name)

"""
Session Helpers

Purpose
-------
Thin convenience wrapper(s) around SessionLocal for use outside the request/response cycle (e.g. scheduled jobs like overdue-return detection or booking-reminder dispatch).

Responsibilities
-----------------
- get_session_context(): an async context manager yielding a session for scripts/jobs.

Interacts With
--------------
- db/database.py -> SessionLocal defined there.
- services/*.py -> scheduled-job style methods (e.g. AllocationService.notify_overdue_returns) may use this outside of a request.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from contextlib import asynccontextmanager

# from app.db.database import SessionLocal


@asynccontextmanager
async def get_session_context():
    """Yield a database session for use in scripts/scheduled jobs (outside FastAPI's request-scoped DI)."""
    yield None

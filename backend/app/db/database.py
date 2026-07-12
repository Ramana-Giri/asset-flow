"""
Database Engine & Session Factory

Purpose
-------
Create the SQLAlchemy async engine and the session factory used to produce request-scoped sessions. No models here.

Responsibilities
-----------------
- Create the async Engine from config.settings.DATABASE_URL.
- Create an async_sessionmaker (SessionLocal) bound to that engine.

Interacts With
--------------
- config.py -> DATABASE_URL.
- dependencies.py -> get_db() uses SessionLocal to yield sessions.
- lifespan.py -> disposes of the engine on shutdown.

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.config import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True, future=True,
)

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
)
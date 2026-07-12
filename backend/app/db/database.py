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
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
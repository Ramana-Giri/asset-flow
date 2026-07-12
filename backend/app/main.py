"""
Application Entry Point

Purpose
-------
Create and configure the FastAPI application instance. This file should only initialize the application. Business logic must never exist here.

Responsibilities
-----------------
- Create the FastAPI() instance, wiring in the lifespan handler.
- Register the aggregate API router (api/router.py).
- Register middleware (CORS, etc.) using settings from config.py.
- Register global exception handlers translating core/exceptions.py -> HTTP responses.

Interacts With
--------------
- lifespan.py -> startup/shutdown hooks.
- config.py -> Settings (CORS_ORIGINS, etc.).
- api/router.py -> the aggregate API router mounted here.
- core/exceptions.py -> exception handlers registered here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.lifespan import lifespan


def create_app() -> FastAPI:
    """
    Application factory. Builds and returns a fully configured FastAPI
    instance. No business logic here - only wiring.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    register_exception_handlers(app)

    return app


app = create_app()
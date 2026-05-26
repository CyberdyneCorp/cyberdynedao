"""ASGI app factory.

The only module allowed to import freely across layers — `import-linter`
ignores violations originating here so the factory can wire adapters
without the hexagonal rules getting in its way.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cyberdyne_backend import __version__
from cyberdyne_backend.adapters.inbound.api.content.router import (
    get_cyberdyne_page_uc,
    get_list_team_uc,
)
from cyberdyne_backend.adapters.inbound.api.content.router import (
    router as content_router,
)
from cyberdyne_backend.adapters.inbound.health.router import router as health_router
from cyberdyne_backend.adapters.inbound.middleware.auth import AuthMiddleware
from cyberdyne_backend.adapters.outbound.persistence.content.repository import (
    SqlAlchemyContentRepository,
)
from cyberdyne_backend.application.content.use_cases import (
    GetCyberdynePage,
    ListTeam,
)
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.database.engine import (
    dispose_engine,
    session_scope,
)
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    container = Container(settings)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        # Phase 1's public endpoints don't make outbound CyberdyneAuth-
        # authed calls, so we don't start the service-token provider
        # here. Phase 6 will: ``await container.service_token_provider.start()``.
        try:
            yield
        finally:
            await container.aclose()
            await dispose_engine()

    app = FastAPI(
        title="Cyberdyne Backend",
        version=__version__,
        description="Hexagonal FastAPI service backing the Cyberdyne SvelteKit frontend.",
        # Expose docs/openapi at default paths outside of prod.
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.environment != "production" else None,
        lifespan=lifespan,
    )

    # CORS must be installed before the auth middleware so the preflight
    # OPTIONS requests don't go through token introspection.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.add_middleware(AuthMiddleware, auth_port=container.auth_port)

    # Per-request use-case wiring. The session lifecycle is owned by
    # ``session_scope``: commits on clean exit, rolls back on raise.
    async def _list_team_dep() -> AsyncIterator[ListTeam]:
        async with session_scope() as session:
            yield ListTeam(repo=SqlAlchemyContentRepository(session))

    async def _cyberdyne_page_dep() -> AsyncIterator[GetCyberdynePage]:
        async with session_scope() as session:
            yield GetCyberdynePage(repo=SqlAlchemyContentRepository(session))

    app.dependency_overrides[get_list_team_uc] = _list_team_dep
    app.dependency_overrides[get_cyberdyne_page_uc] = _cyberdyne_page_dep

    app.include_router(health_router)
    app.include_router(content_router)
    return app


# Module-level ASGI app for uvicorn (``cyberdyne_backend.main:app``).
app = create_app()


def main() -> None:
    """Entry point used by the project script."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "cyberdyne_backend.main:app",
        host="0.0.0.0",  # binding to all interfaces inside a container is intended
        port=settings.port,
        log_level=settings.log_level.lower(),
    )

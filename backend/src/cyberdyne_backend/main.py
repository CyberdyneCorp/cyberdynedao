"""ASGI app factory.

The only module allowed to import freely across layers — `import-linter`
ignores violations originating here so the factory can wire adapters
without the hexagonal rules getting in its way.
"""

from __future__ import annotations

from fastapi import FastAPI

from cyberdyne_backend import __version__
from cyberdyne_backend.adapters.inbound.health.router import router as health_router
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Cyberdyne Backend",
        version=__version__,
        description="Hexagonal FastAPI service backing the Cyberdyne SvelteKit frontend.",
        # We expose docs/openapi at the default paths only outside of prod.
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.environment != "production" else None,
    )

    app.include_router(health_router)
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

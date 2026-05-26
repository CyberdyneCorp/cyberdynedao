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
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    admin_router as blog_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    get_create_post_uc,
    get_list_posts_uc,
    get_post_uc,
    get_publish_post_uc,
    get_rss_uc,
)
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    public_router as blog_public_router,
)
from cyberdyne_backend.adapters.inbound.api.content.router import (
    get_contact_page_uc,
    get_cyberdyne_page_uc,
    get_list_projects_uc,
    get_list_resources_uc,
    get_list_team_uc,
    get_services_page_uc,
)
from cyberdyne_backend.adapters.inbound.api.content.router import (
    router as content_router,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    admin_router as leads_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    get_admin_list_asks_uc,
    get_admin_update_ask_uc,
    get_create_ask_uc,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    public_router as leads_public_router,
)
from cyberdyne_backend.adapters.inbound.health.router import router as health_router
from cyberdyne_backend.adapters.inbound.middleware.auth import AuthMiddleware
from cyberdyne_backend.adapters.outbound.persistence.blog.repository import (
    SqlAlchemyBlogRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.content.repository import (
    SqlAlchemyContentRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.leads.repository import (
    SqlAlchemyAskRepository,
)
from cyberdyne_backend.application.blog import (
    CreateBlogPost,
    GenerateRssFeed,
    GetBlogPost,
    ListBlogPosts,
    PublishBlogPost,
)
from cyberdyne_backend.application.content.use_cases import (
    GetContactPage,
    GetCyberdynePage,
    GetServicesPage,
    ListProjects,
    ListResourceGroups,
    ListTeam,
)
from cyberdyne_backend.application.leads import (
    AdminListAsks,
    AdminUpdateAsk,
    CreateAsk,
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

    async def _list_projects_dep() -> AsyncIterator[ListProjects]:
        async with session_scope() as session:
            yield ListProjects(repo=SqlAlchemyContentRepository(session))

    async def _services_page_dep() -> AsyncIterator[GetServicesPage]:
        async with session_scope() as session:
            yield GetServicesPage(repo=SqlAlchemyContentRepository(session))

    async def _contact_page_dep() -> AsyncIterator[GetContactPage]:
        async with session_scope() as session:
            yield GetContactPage(repo=SqlAlchemyContentRepository(session))

    async def _list_resources_dep() -> AsyncIterator[ListResourceGroups]:
        async with session_scope() as session:
            yield ListResourceGroups(repo=SqlAlchemyContentRepository(session))

    async def _create_ask_dep() -> AsyncIterator[CreateAsk]:
        async with session_scope() as session:
            yield CreateAsk(
                repo=SqlAlchemyAskRepository(session),
                captcha=container.captcha_port,
                notifier=container.email_notifier,
            )

    async def _admin_list_asks_dep() -> AsyncIterator[AdminListAsks]:
        async with session_scope() as session:
            yield AdminListAsks(repo=SqlAlchemyAskRepository(session))

    async def _admin_update_ask_dep() -> AsyncIterator[AdminUpdateAsk]:
        async with session_scope() as session:
            yield AdminUpdateAsk(repo=SqlAlchemyAskRepository(session))

    async def _list_blog_posts_dep() -> AsyncIterator[ListBlogPosts]:
        async with session_scope() as session:
            yield ListBlogPosts(repo=SqlAlchemyBlogRepository(session))

    async def _get_blog_post_dep() -> AsyncIterator[GetBlogPost]:
        async with session_scope() as session:
            yield GetBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _create_blog_post_dep() -> AsyncIterator[CreateBlogPost]:
        async with session_scope() as session:
            yield CreateBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _publish_blog_post_dep() -> AsyncIterator[PublishBlogPost]:
        async with session_scope() as session:
            yield PublishBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _rss_feed_dep() -> AsyncIterator[GenerateRssFeed]:
        async with session_scope() as session:
            yield GenerateRssFeed(
                repo=SqlAlchemyBlogRepository(session),
                site_url=settings.public_site_url,
            )

    app.dependency_overrides[get_list_team_uc] = _list_team_dep
    app.dependency_overrides[get_cyberdyne_page_uc] = _cyberdyne_page_dep
    app.dependency_overrides[get_list_projects_uc] = _list_projects_dep
    app.dependency_overrides[get_services_page_uc] = _services_page_dep
    app.dependency_overrides[get_contact_page_uc] = _contact_page_dep
    app.dependency_overrides[get_list_resources_uc] = _list_resources_dep
    app.dependency_overrides[get_create_ask_uc] = _create_ask_dep
    app.dependency_overrides[get_admin_list_asks_uc] = _admin_list_asks_dep
    app.dependency_overrides[get_admin_update_ask_uc] = _admin_update_ask_dep
    app.dependency_overrides[get_list_posts_uc] = _list_blog_posts_dep
    app.dependency_overrides[get_post_uc] = _get_blog_post_dep
    app.dependency_overrides[get_create_post_uc] = _create_blog_post_dep
    app.dependency_overrides[get_publish_post_uc] = _publish_blog_post_dep
    app.dependency_overrides[get_rss_uc] = _rss_feed_dep

    app.include_router(health_router)
    app.include_router(content_router)
    app.include_router(leads_public_router)
    app.include_router(leads_admin_router)
    app.include_router(blog_public_router)
    app.include_router(blog_admin_router)
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

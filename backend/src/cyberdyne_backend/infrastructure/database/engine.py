"""Async SQLAlchemy engine + session factory.

Single engine per process, per Settings. The engine pools connections
to Postgres; the session factory hands out short-lived sessions, one
per request. Tests bind an in-memory aiosqlite engine to the same
factory via dependency overrides.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cyberdyne_backend.infrastructure.settings import Settings, get_settings


def _make_engine(settings: Settings) -> AsyncEngine:
    kwargs: dict[str, object] = {
        "echo": settings.database_echo,
        "future": True,
    }
    # SQLite (test backend) doesn't support QueuePool — leave pool args
    # off and let SQLAlchemy pick StaticPool for the in-memory variant.
    if not settings.database_url.startswith(("sqlite", "sqlite+aiosqlite")):
        kwargs["pool_size"] = settings.database_pool_size
        kwargs["max_overflow"] = settings.database_max_overflow
        kwargs["pool_pre_ping"] = True
    return create_async_engine(settings.database_url, **kwargs)


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    return _make_engine(get_settings())


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Per-request session scope. Commits on clean exit, rolls back on error."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    """Tear down the engine on shutdown so connections are returned cleanly."""
    if get_engine.cache_info().currsize:
        await get_engine().dispose()
        get_engine.cache_clear()
        get_session_factory.cache_clear()

"""Pytest fixtures shared across the test tree.

We set ``DATABASE_URL`` to an in-memory aiosqlite engine **before**
importing any application module — pydantic-settings reads env vars
once when ``get_settings()`` is first called and caches the result, so
late overrides don't apply. Keeping the override here at conftest
import time means the cached settings sees the in-memory URL from the
start, and we never accidentally hit a real Postgres during tests.
"""

from __future__ import annotations

import os

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("ENVIRONMENT", "ci")
os.environ.setdefault("LOG_LEVEL", "WARNING")

# Now safe to import application code — get_settings() picks up the
# env-var overrides on first call.
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.infrastructure.database.base import Base
from cyberdyne_backend.infrastructure.database.engine import (
    get_engine,
    get_session_factory,
)
from cyberdyne_backend.main import create_app


@pytest_asyncio.fixture
async def _prepared_schema() -> AsyncIterator[None]:
    """Create + drop all tables around each test that needs them."""
    # Import the model modules so their tables register against
    # Base.metadata before create_all runs.
    from cyberdyne_backend.adapters.outbound.persistence.content import models  # noqa: F401

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def app() -> FastAPI:
    """Fresh ASGI app per test — cheap, avoids cross-test state bleed."""
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """Per-test async session bound to the in-memory engine."""
    factory = get_session_factory()
    async with factory() as session:
        yield session

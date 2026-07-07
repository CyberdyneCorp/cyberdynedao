"""Startup prewarm hook (issue #259).

``_startup_prewarm`` must fetch the JWKS (via the container) and ping the DB
before the app serves traffic, and must NEVER crash boot if either step fails.
No live Postgres/network — the container is faked and ``ping_engine`` is
monkeypatched (except the one case that runs it against the conftest aiosqlite
engine).
"""

from __future__ import annotations

import pytest

from cyberdyne_backend import main as main_module
from cyberdyne_backend.infrastructure.database.engine import ping_engine
from cyberdyne_backend.main import _startup_prewarm

pytestmark = pytest.mark.unit


class _FakeContainer:
    def __init__(self, *, raise_auth: bool = False) -> None:
        self.prewarm_auth_called = False
        self._raise_auth = raise_auth

    async def prewarm_auth(self) -> None:
        self.prewarm_auth_called = True
        if self._raise_auth:
            raise RuntimeError("auth server down")


async def test_prewarm_invokes_auth_and_db(monkeypatch: pytest.MonkeyPatch) -> None:
    pinged = {"count": 0}

    async def fake_ping() -> None:
        pinged["count"] += 1

    monkeypatch.setattr(main_module, "ping_engine", fake_ping)
    container = _FakeContainer()

    await _startup_prewarm(container)  # type: ignore[arg-type]

    assert container.prewarm_auth_called is True
    assert pinged["count"] == 1


async def test_prewarm_swallows_auth_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    pinged = {"count": 0}

    async def fake_ping() -> None:
        pinged["count"] += 1

    monkeypatch.setattr(main_module, "ping_engine", fake_ping)
    container = _FakeContainer(raise_auth=True)

    # A failing auth prewarm must not crash boot, and the DB ping still runs.
    await _startup_prewarm(container)  # type: ignore[arg-type]

    assert container.prewarm_auth_called is True
    assert pinged["count"] == 1


async def test_prewarm_swallows_db_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def boom() -> None:
        raise RuntimeError("db not ready")

    monkeypatch.setattr(main_module, "ping_engine", boom)
    container = _FakeContainer()

    await _startup_prewarm(container)  # type: ignore[arg-type] — must not raise

    assert container.prewarm_auth_called is True


async def test_ping_engine_runs_select_one() -> None:
    # Against the conftest in-memory aiosqlite engine — no Postgres, no schema.
    await ping_engine()

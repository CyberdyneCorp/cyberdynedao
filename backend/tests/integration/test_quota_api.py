"""Integration tests for server-side quota / Pro fair-use (issue #230).

Free users are blocked with 402 after the free cap; Pro users pass the free
cap and are only soft-capped (429); certificate issuance is Pro-only. Uses the
real EnforceQuota + SqlAlchemy counter repo so enforcement is end-to-end.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.ai_chat import router as chat_router
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import get_run_turn_uc
from cyberdyne_backend.adapters.inbound.api.code.router import get_run_code_uc
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import get_enforce_quota_uc
from cyberdyne_backend.adapters.inbound.api.rate_limit import SlidingWindowRateLimiter
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    optional_principal,
    require_principal,
)
from cyberdyne_backend.adapters.outbound.persistence.quota.repository import (
    SqlAlchemyUsageCounterRepository,
)
from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.application.quota import EnforceQuota
from cyberdyne_backend.domain.ai_chat import MatlabRunResult
from cyberdyne_backend.domain.ai_chat.entities import ChatMessage, ChatRole
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration


def _user(uid: str, *, pro: bool) -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.UUID(uid),
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
        entitlements=frozenset({"pro:annual"}) if pro else frozenset(),
    )


_FREE = _user("11111111-1111-1111-1111-111111111111", pro=False)
_PRO = _user("22222222-2222-2222-2222-222222222222", pro=True)


async def _real_enforcer() -> AsyncIterator[EnforceQuota]:
    async with session_scope() as session:
        yield EnforceQuota(repo=SqlAlchemyUsageCounterRepository(session))


class _FakeRunTurn:
    async def execute(self, *, session_id, user_content, **_kwargs) -> ChatMessage:
        return ChatMessage(
            id=uuid.uuid4(),
            session_id=session_id,
            role=ChatRole.ASSISTANT,
            content="ok",
            created_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
        )


class _FakeMatlab:
    async def run_repl(self, *, source, session_id, bearer):
        return MatlabRunResult(ok=True, stdout="ok", stderr="", session_id=session_id)

    async def run_plot(self, *, source, session_id, bearer, fmt="png"):
        return MatlabRunResult(ok=True, stdout="", stderr="", session_id=session_id)


def _chat_client(app: FastAPI, principal: UserPrincipal, monkeypatch) -> TestClient:
    # Neutralize the per-IP chat limiter (module-global, stateful across tests)
    # so it doesn't mask the per-user quota under test.
    monkeypatch.setattr(
        chat_router,
        "_chat_rate_limiter",
        SlidingWindowRateLimiter(limit=10_000, window_s=60.0, detail="rl"),
    )
    app.dependency_overrides[optional_principal] = lambda: principal
    app.dependency_overrides[get_enforce_quota_uc] = _real_enforcer
    app.dependency_overrides[get_run_turn_uc] = lambda: _FakeRunTurn()
    return TestClient(app)


@pytest.mark.usefixtures("_prepared_schema")
def test_free_user_blocked_after_tutor_cap(app: FastAPI, monkeypatch) -> None:
    client = _chat_client(app, _FREE, monkeypatch)
    session = uuid.uuid4()
    for _ in range(10):  # 10 free tutor messages / month
        ok = client.post(f"/api/v1/chat/sessions/{session}/messages", json={"content": "hi"})
        assert ok.status_code == 200, ok.text
    blocked = client.post(f"/api/v1/chat/sessions/{session}/messages", json={"content": "more"})
    assert blocked.status_code == 402, blocked.text
    assert blocked.json()["detail"]["code"] == "quota_exceeded"
    assert blocked.headers["X-Quota-Limit"] == "10"
    assert blocked.headers["X-Quota-Remaining"] == "0"


@pytest.mark.usefixtures("_prepared_schema")
def test_pro_user_passes_free_cap(app: FastAPI, monkeypatch) -> None:
    client = _chat_client(app, _PRO, monkeypatch)
    session = uuid.uuid4()
    # Well past the free cap of 10 — Pro is only soft-capped at 500.
    for _ in range(15):
        resp = client.post(f"/api/v1/chat/sessions/{session}/messages", json={"content": "hi"})
        assert resp.status_code == 200, resp.text
    # Quota meter headers are surfaced for the client.
    last = client.post(f"/api/v1/chat/sessions/{session}/messages", json={"content": "hi"})
    assert last.headers["X-Quota-Limit"] == "500"


@pytest.mark.usefixtures("_prepared_schema")
def test_free_user_blocked_after_daily_code_runs(app: FastAPI) -> None:
    app.dependency_overrides[optional_principal] = lambda: _FREE
    app.dependency_overrides[require_principal] = lambda: _FREE
    app.dependency_overrides[get_enforce_quota_uc] = _real_enforcer
    app.dependency_overrides[get_run_code_uc] = lambda: RunLessonCode(matlab=_FakeMatlab())  # type: ignore[arg-type]
    client = TestClient(app)
    lesson = uuid.uuid4()
    for _ in range(20):  # 20 code runs / day
        ok = client.post(f"/api/v1/lessons/{lesson}/code/run", json={"source": "2+2"})
        assert ok.status_code == 200, ok.text
    blocked = client.post(f"/api/v1/lessons/{lesson}/code/run", json={"source": "2+2"})
    assert blocked.status_code == 402
    assert blocked.json()["detail"]["code"] == "quota_exceeded"


@pytest.mark.usefixtures("_prepared_schema")
def test_certificate_is_pro_only(app: FastAPI) -> None:
    # Free learner is refused with a paywall signal before the use case runs.
    app.dependency_overrides[require_principal] = lambda: _FREE
    free = TestClient(app)
    refused = free.post("/api/v1/courses/ghost/certificate")
    assert refused.status_code == 402
    assert refused.json()["detail"]["code"] == "pro_required"

    # Pro learner passes the gate (then 404 because the course doesn't exist).
    app.dependency_overrides[require_principal] = lambda: _PRO
    pro = TestClient(app)
    passed = pro.post("/api/v1/courses/ghost/certificate")
    assert passed.status_code == 404

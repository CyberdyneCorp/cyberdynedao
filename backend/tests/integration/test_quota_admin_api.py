"""Integration tests for the admin quota-reset endpoint (real repo + DB)."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.quota.router import (
    get_reset_quota_uc,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor, require_principal
from cyberdyne_backend.adapters.outbound.persistence.quota.repository import (
    SqlAlchemyUsageCounterRepository,
)
from cyberdyne_backend.application.quota import ResetQuota
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quota import QuotaMeter, QuotaPeriod, period_key, policy_for
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration

_USER = uuid.UUID("33333333-3333-3333-3333-333333333333")
_NOW = datetime(2026, 7, 11, 12, 0, tzinfo=UTC)


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="ed",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="l",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


async def _reset_uc() -> AsyncIterator[ResetQuota]:
    async with session_scope() as session:
        yield ResetQuota(repo=SqlAlchemyUsageCounterRepository(session), now=lambda: _NOW)


async def _seed_usage(meter: QuotaMeter, count: int) -> None:
    bucket = period_key(policy_for(meter).period, _NOW)
    async with session_scope() as session:
        repo = SqlAlchemyUsageCounterRepository(session)
        for _ in range(count):
            await repo.increment(user_id=_USER, meter=meter, period_key=bucket)


async def _current(meter: QuotaMeter) -> int:
    bucket = period_key(policy_for(meter).period, _NOW)
    async with session_scope() as session:
        return await SqlAlchemyUsageCounterRepository(session).current(
            user_id=_USER, meter=meter, period_key=bucket
        )


@pytest.fixture
def admin_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[get_reset_quota_uc] = _reset_uc
    return TestClient(app)


@pytest.mark.usefixtures("_prepared_schema")
def test_requires_authentication(app: FastAPI) -> None:
    # The endpoint is guarded by require_editor; an anonymous caller (no
    # resolved principal) is refused. Editor-vs-learner (403) semantics are
    # covered by test_require_editor.py.
    app.dependency_overrides[get_reset_quota_uc] = _reset_uc
    r = TestClient(app).post("/api/v1/admin/quota/reset", json={"userId": str(_USER)})
    assert r.status_code == 401


async def test_reset_one_meter_clears_the_counter(admin_client: TestClient) -> None:
    await _seed_usage(QuotaMeter.TUTOR_MESSAGES, 10)
    assert await _current(QuotaMeter.TUTOR_MESSAGES) == 10

    r = admin_client.post(
        "/api/v1/admin/quota/reset",
        json={"userId": str(_USER), "meter": "tutor_messages"},
    )
    assert r.status_code == 200
    assert r.json() == {"userId": str(_USER), "reset": ["tutor_messages"]}
    assert await _current(QuotaMeter.TUTOR_MESSAGES) == 0


async def test_reset_all_meters(admin_client: TestClient) -> None:
    await _seed_usage(QuotaMeter.TUTOR_MESSAGES, 3)
    await _seed_usage(QuotaMeter.SCANS, 2)

    r = admin_client.post("/api/v1/admin/quota/reset", json={"userId": str(_USER)})
    assert r.status_code == 200
    assert set(r.json()["reset"]) == {"tutor_messages", "scans"}
    assert await _current(QuotaMeter.TUTOR_MESSAGES) == 0
    assert await _current(QuotaMeter.SCANS) == 0


def test_unknown_meter_is_422(admin_client: TestClient) -> None:
    r = admin_client.post(
        "/api/v1/admin/quota/reset", json={"userId": str(_USER), "meter": "bogus"}
    )
    assert r.status_code == 422


def test_reset_with_no_usage_returns_empty(admin_client: TestClient) -> None:
    r = admin_client.post("/api/v1/admin/quota/reset", json={"userId": str(uuid.uuid4())})
    assert r.status_code == 200
    assert r.json()["reset"] == []


def _period_sanity() -> None:
    # Guard: tutor_messages is monthly (so the reset bucket matches enforcement).
    assert policy_for(QuotaMeter.TUTOR_MESSAGES).period is QuotaPeriod.MONTHLY

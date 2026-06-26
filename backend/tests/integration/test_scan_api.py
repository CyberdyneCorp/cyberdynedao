"""Integration tests for Scan-to-Learn (issue #231).

Drives router -> ScanToLearn -> CatalogSearchIndex over the real SQLAlchemy
course repo (in-memory sqlite), with a fake vision reader (no network) and the
deterministic static embedder. Exercises the real EnforceQuota so the SCANS
quota is metered end-to-end. An in-catalog photo returns ranked matches; an
out-of-catalog photo returns noMatch with the extracted query; a non-image is
415; an unauthenticated request is 401/403.
"""

from __future__ import annotations

import io
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.course_finder.router import get_scan_to_learn_uc
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import get_enforce_quota_uc
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    optional_principal,
    require_editor,
    require_principal,
)
from cyberdyne_backend.adapters.outbound.course_finder.catalog_source import (
    CourseCatalogTextSource,
)
from cyberdyne_backend.adapters.outbound.llm.embedding_client import StaticEmbeddingClient
from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quota.repository import (
    SqlAlchemyUsageCounterRepository,
)
from cyberdyne_backend.application.course_finder import CatalogSearchIndex, ScanToLearn
from cyberdyne_backend.application.quota import EnforceQuota
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.course_finder import ScanQuery
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("44444444-4444-4444-4444-444444444444"),
    username="learner",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="editor",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


class _FakeReader:
    """Stand-in for the vision step — returns a fixed extracted query so the
    test never reaches OpenAI."""

    def __init__(self, query: ScanQuery) -> None:
        self._query = query

    async def read_question(self, *, image_bytes: bytes, content_type: str) -> ScanQuery:
        return self._query


async def _real_enforcer() -> AsyncIterator[EnforceQuota]:
    async with session_scope() as session:
        yield EnforceQuota(repo=SqlAlchemyUsageCounterRepository(session))


class _SessionScopedSource:
    async def entries(self):  # type: ignore[no-untyped-def]
        async with session_scope() as session:
            return await CourseCatalogTextSource(
                courses=SqlAlchemyCourseRepository(session)
            ).entries()


def _scan_dep(query: ScanQuery):  # type: ignore[no-untyped-def]
    index = CatalogSearchIndex(source=_SessionScopedSource(), embedder=StaticEmbeddingClient())

    async def _dep() -> ScanToLearn:
        return ScanToLearn(reader=_FakeReader(query), index=index)

    return _dep


def _seed_published_course(client: TestClient) -> None:
    assert (
        client.post(
            "/api/v1/admin/courses",
            json={
                "title": "Linear Algebra",
                "description": "Vectors, matrices, eigenvalues and eigenvectors.",
                "level": "Beginner",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/admin/courses/linear-algebra/lessons",
            json={
                "title": "Eigenvalues and eigenvectors",
                "lessonType": "text",
                "textBody": "body",
            },
        ).status_code
        == 201
    )
    assert client.post("/api/v1/admin/courses/linear-algebra/publish").status_code == 200


def _png_bytes() -> bytes:
    # Minimal valid-enough PNG header; the fake reader never decodes it.
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 64


def _seed_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def _learner_client(app: FastAPI, query: ScanQuery) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    app.dependency_overrides[optional_principal] = lambda: _LEARNER
    app.dependency_overrides[get_enforce_quota_uc] = _real_enforcer
    app.dependency_overrides[get_scan_to_learn_uc] = _scan_dep(query)
    return TestClient(app)


def _post_scan(client: TestClient, *, data: bytes, content_type: str):  # type: ignore[no-untyped-def]
    return client.post(
        "/api/v1/learning/scan",
        files={"file": ("question.png", io.BytesIO(data), content_type)},
    )


@pytest.mark.usefixtures("_prepared_schema")
def test_scan_returns_ranked_matches_for_in_catalog_photo(app: FastAPI) -> None:
    _seed_published_course(_seed_client(app))
    client = _learner_client(
        app,
        ScanQuery(question="Find the eigenvalues of matrix A", subject="Math", keywords=()),
    )
    resp = _post_scan(client, data=_png_bytes(), content_type="image/png")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["noMatch"] is False
    assert body["matches"]
    assert body["matches"][0]["courseSlug"] == "linear-algebra"
    assert body["query"]["question"] == "Find the eigenvalues of matrix A"
    # The lesson-level entry is deep-linkable.
    assert any(m["lessonId"] for m in body["matches"])
    assert resp.headers["X-Quota-Meter"] == "scans"


@pytest.mark.usefixtures("_prepared_schema")
def test_scan_no_match_returns_extracted_query(app: FastAPI) -> None:
    _seed_published_course(_seed_client(app))
    client = _learner_client(
        app,
        ScanQuery(
            question="Explain Roman siege warfare tactics",
            subject="History",
            keywords=("legion",),
        ),
    )
    resp = _post_scan(client, data=_png_bytes(), content_type="image/png")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["noMatch"] is True
    assert body["matches"] == []
    assert body["query"]["subject"] == "History"
    assert body["query"]["keywords"] == ["legion"]


@pytest.mark.usefixtures("_prepared_schema")
def test_scan_rejects_non_image(app: FastAPI) -> None:
    client = _learner_client(app, ScanQuery(question="x"))
    resp = _post_scan(client, data=b"%PDF-1.4", content_type="application/pdf")
    assert resp.status_code == 415, resp.text


@pytest.mark.usefixtures("_prepared_schema")
def test_scan_requires_authentication(app: FastAPI) -> None:
    # No require_principal override → the auth middleware leaves the request
    # anonymous and the guard rejects it.
    resp = _post_scan(TestClient(app), data=_png_bytes(), content_type="image/png")
    assert resp.status_code in (401, 403)


@pytest.mark.usefixtures("_prepared_schema")
def test_scan_counts_toward_scans_quota(app: FastAPI) -> None:
    _seed_published_course(_seed_client(app))
    client = _learner_client(app, ScanQuery(question="eigenvalues of a matrix", subject="Math"))
    # Free SCANS cap is 5 / month.
    for _ in range(5):
        ok = _post_scan(client, data=_png_bytes(), content_type="image/png")
        assert ok.status_code == 200, ok.text
    blocked = _post_scan(client, data=_png_bytes(), content_type="image/png")
    assert blocked.status_code == 402, blocked.text
    assert blocked.json()["detail"]["code"] == "quota_exceeded"

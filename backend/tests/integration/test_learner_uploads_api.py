"""Learner attachment uploads: POST /api/v1/uploads (issue #220).

A signed-in learner attaches a file (image / CSV / …) for the AI tutor.
Reuses the same save-upload use case as the admin endpoint, but guarded by
``require_principal`` (any user token), and adds a ``status`` field to the
response contract.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.uploads.router import get_save_upload_uc
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.adapters.outbound.persistence.uploads.repository import (
    SqlAlchemyUploadRepository,
)
from cyberdyne_backend.adapters.outbound.storage.local import LocalFileStorage
from cyberdyne_backend.application.uploads import SaveUpload
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def learner_client(app: FastAPI, tmp_path: Path) -> Iterator[TestClient]:
    storage = LocalFileStorage(tmp_path)

    async def _save() -> AsyncIterator[SaveUpload]:
        async with get_session_factory()() as session:
            yield SaveUpload(
                repo=SqlAlchemyUploadRepository(session),
                storage=storage,
                media_url_prefix="/media",
            )
            await session.commit()

    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[get_save_upload_uc] = _save
    yield TestClient(app)


@pytest.mark.usefixtures("_prepared_schema")
def test_learner_uploads_image(learner_client: TestClient) -> None:
    resp = learner_client.post(
        "/api/v1/uploads",
        files={"file": ("diagram.png", b"\x89PNG\r\n\x1a\n" + b"x" * 32, "image/png")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["id"]  # the uploadId the learner sends back as an attachment
    assert body["originalFilename"] == "diagram.png"
    assert body["contentType"] == "image/png"
    assert body["status"] == "stored"
    assert body["category"] == "image"


@pytest.mark.usefixtures("_prepared_schema")
def test_learner_uploads_csv(learner_client: TestClient) -> None:
    resp = learner_client.post(
        "/api/v1/uploads",
        files={"file": ("rows.csv", b"a,b\n1,2\n", "text/csv")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["contentType"] == "text/csv"
    assert body["category"] == "document"


@pytest.mark.usefixtures("_prepared_schema")
def test_unsupported_type_rejected(learner_client: TestClient) -> None:
    resp = learner_client.post(
        "/api/v1/uploads",
        files={"file": ("evil.exe", b"MZ", "application/x-msdownload")},
    )
    assert resp.status_code == 415, resp.text


@pytest.mark.usefixtures("_prepared_schema")
def test_unauthenticated_rejected(app: FastAPI, tmp_path: Path) -> None:
    # No require_principal override + no token → middleware leaves principal
    # None → 401.
    storage = LocalFileStorage(tmp_path)

    async def _save() -> AsyncIterator[SaveUpload]:
        async with get_session_factory()() as session:
            yield SaveUpload(
                repo=SqlAlchemyUploadRepository(session),
                storage=storage,
                media_url_prefix="/media",
            )

    app.dependency_overrides[get_save_upload_uc] = _save
    client = TestClient(app)
    resp = client.post(
        "/api/v1/uploads",
        files={"file": ("rows.csv", b"a,b\n1,2\n", "text/csv")},
    )
    assert resp.status_code in (401, 403), resp.text

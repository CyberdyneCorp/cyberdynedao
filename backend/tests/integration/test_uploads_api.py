"""End-to-end tests for uploads — local storage + the HTTP API.

Storage writes go to a per-test ``tmp_path`` (the upload use-case deps
are overridden to point a ``LocalFileStorage`` there) so nothing touches
the repo's real media dir.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.uploads.router import (
    get_save_upload_uc,
    get_save_uploads_uc,
    get_upload_uc,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.adapters.outbound.persistence.uploads.repository import (
    SqlAlchemyUploadRepository,
)
from cyberdyne_backend.adapters.outbound.storage.local import LocalFileStorage
from cyberdyne_backend.application.uploads import GetUpload, SaveUpload, SaveUploads
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.uploads import UploadCategory
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="editor",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def upload_client(app: FastAPI, tmp_path: Path) -> Iterator[TestClient]:
    storage = LocalFileStorage(tmp_path)

    async def _save() -> AsyncIterator[SaveUpload]:
        async with session_scope() as session:
            yield SaveUpload(
                repo=SqlAlchemyUploadRepository(session),
                storage=storage,
                media_url_prefix="/media",
            )

    async def _save_many() -> AsyncIterator[SaveUploads]:
        async with session_scope() as session:
            yield SaveUploads(
                inner=SaveUpload(
                    repo=SqlAlchemyUploadRepository(session),
                    storage=storage,
                    media_url_prefix="/media",
                )
            )

    async def _get() -> AsyncIterator[GetUpload]:
        async with session_scope() as session:
            yield GetUpload(repo=SqlAlchemyUploadRepository(session))

    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[get_save_upload_uc] = _save
    app.dependency_overrides[get_save_uploads_uc] = _save_many
    app.dependency_overrides[get_upload_uc] = _get
    client = TestClient(app)
    client.tmp_path = tmp_path  # type: ignore[attr-defined]
    yield client


@pytest.mark.usefixtures("_prepared_schema")
def test_upload_and_fetch(upload_client: TestClient) -> None:
    resp = upload_client.post(
        "/api/v1/admin/uploads",
        files={"file": ("hero.png", b"\x89PNG\r\n" + b"x" * 50, "image/png")},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["category"] == "image"
    assert body["originalFilename"] == "hero.png"
    assert body["url"].startswith("/media/image/")
    assert body["storedFilename"].endswith(".png")

    # Bytes actually landed on disk under the image category.
    stored_path = upload_client.tmp_path / "image" / body["storedFilename"]  # type: ignore[attr-defined]
    assert stored_path.exists()

    # Metadata is fetchable.
    meta = upload_client.get(f"/api/v1/uploads/{body['id']}")
    assert meta.status_code == 200
    assert meta.json()["storedFilename"] == body["storedFilename"]


@pytest.mark.usefixtures("_prepared_schema")
def test_traversal_filename_is_neutralised(upload_client: TestClient) -> None:
    resp = upload_client.post(
        "/api/v1/admin/uploads",
        files={"file": ("../../../../etc/passwd.png", b"data", "image/png")},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["originalFilename"] == "passwd.png"
    # Stored name is a UUID — no path components escaped.
    assert "/" not in body["storedFilename"] and ".." not in body["storedFilename"]


@pytest.mark.usefixtures("_prepared_schema")
def test_unsupported_type_is_415(upload_client: TestClient) -> None:
    resp = upload_client.post(
        "/api/v1/admin/uploads",
        files={"file": ("evil.exe", b"MZ", "application/x-msdownload")},
    )
    assert resp.status_code == 415


@pytest.mark.usefixtures("_prepared_schema")
def test_oversize_image_is_413(upload_client: TestClient) -> None:
    big = b"x" * (11 * 1024 * 1024)  # image cap is 10MB
    resp = upload_client.post(
        "/api/v1/admin/uploads",
        files={"file": ("big.png", big, "image/png")},
    )
    assert resp.status_code == 413


@pytest.mark.usefixtures("_prepared_schema")
def test_batch_upload(upload_client: TestClient) -> None:
    resp = upload_client.post(
        "/api/v1/admin/uploads/batch",
        files=[
            ("files", ("a.png", b"a", "image/png")),
            ("files", ("doc.pdf", b"%PDF-1.4", "application/pdf")),
        ],
    )
    assert resp.status_code == 201, resp.text
    cats = {item["category"] for item in resp.json()["items"]}
    assert cats == {"image", "document"}


def test_upload_requires_editor(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/admin/uploads",
        files={"file": ("a.png", b"a", "image/png")},
    )
    assert resp.status_code in (401, 403)


# ── LocalFileStorage adapter directly ────────────────────────────────


async def test_local_storage_writes_and_guards(tmp_path: Path) -> None:
    storage = LocalFileStorage(tmp_path)
    rel = await storage.save(
        category=UploadCategory.IMAGE, stored_filename="abc.png", data=b"hello"
    )
    assert rel == "image/abc.png"
    assert (tmp_path / "image" / "abc.png").read_bytes() == b"hello"

    # A traversal-laden stored filename can't escape the root.
    with pytest.raises(ValueError, match="escapes storage root"):
        await storage.save(
            category=UploadCategory.IMAGE,
            stored_filename="../../escape.png",
            data=b"x",
        )

    await storage.delete(rel)
    assert not (tmp_path / "image" / "abc.png").exists()

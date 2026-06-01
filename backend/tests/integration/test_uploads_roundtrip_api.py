"""Full upload round-trip: POST a file, then fetch it back over /media.

The existing upload test asserts the bytes land on disk + metadata round-
trips; this closes the remaining link by GET-ing the returned ``url``
through the StaticFiles mount and checking the served bytes match what
was uploaded. To do that the storage root and the media mount must point
at the same directory, so we build a fresh app with ``MEDIA_ROOT`` set to
a temp dir (both the LocalFileStorage and the StaticFiles mount read
``settings.media_root``).
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.settings import reset_settings_cache

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
def media_client(tmp_path: Path) -> Iterator[TestClient]:
    # Point MEDIA_ROOT at a temp dir BEFORE building the app so the
    # storage adapter and the /media StaticFiles mount share it.
    prev = os.environ.get("MEDIA_ROOT")
    os.environ["MEDIA_ROOT"] = str(tmp_path)
    reset_settings_cache()
    # Import after the env is set so create_app() sees the temp root.
    from cyberdyne_backend.main import create_app

    app = create_app()
    app.dependency_overrides[require_editor] = _editor
    client = TestClient(app)
    try:
        yield client
    finally:
        if prev is None:
            os.environ.pop("MEDIA_ROOT", None)
        else:
            os.environ["MEDIA_ROOT"] = prev
        reset_settings_cache()


@pytest.mark.usefixtures("_prepared_schema")
def test_upload_then_fetch_over_media(media_client: TestClient) -> None:
    payload = b"\x89PNG\r\n\x1a\n" + b"cyberdyne-academy-roundtrip" * 8

    up = media_client.post(
        "/api/v1/admin/uploads",
        files={"file": ("badge.png", payload, "image/png")},
    )
    assert up.status_code == 201, up.text
    body = up.json()
    url = body["url"]
    assert url.startswith("/media/image/")

    # Fetch the stored file back through the StaticFiles mount.
    got = media_client.get(url)
    assert got.status_code == 200, f"serve failed: {got.status_code}"
    assert got.content == payload  # bytes survive the round-trip
    assert got.headers["content-type"].startswith("image/")

"""End-to-end tests for the lesson-notes endpoints (issue #188)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_USER = uuid.UUID("d4d4d4d4-d4d4-d4d4-d4d4-d4d4d4d4d4d4")
_OTHER = uuid.UUID("e5e5e5e5-e5e5-e5e5-e5e5-e5e5e5e5e5e5")


def _principal(uid: uuid.UUID) -> UserPrincipal:
    return UserPrincipal(
        user_id=uid,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    return TestClient(app)


def _payload(body: str = "my note", quote: str | None = "highlighted") -> dict:
    return {"courseSlug": "rotational-motion", "body": body, "quote": quote}


def test_create_list_by_lesson_and_course(client: TestClient) -> None:
    created = client.post("/api/v1/lessons/l1/notes", json=_payload())
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["lessonId"] == "l1"
    assert body["courseSlug"] == "rotational-motion"
    assert body["quote"] == "highlighted"

    by_lesson = client.get("/api/v1/lessons/l1/notes").json()
    assert [n["body"] for n in by_lesson] == ["my note"]

    across = client.get("/api/v1/notes?courseSlug=rotational-motion").json()
    assert [n["id"] for n in across["items"]] == [body["id"]]


def test_client_supplied_id_is_idempotent(client: TestClient) -> None:
    cid = str(uuid.uuid4())
    first = client.post("/api/v1/lessons/l1/notes", json={**_payload("v1"), "id": cid})
    assert first.status_code == 201
    # Re-sync same id → 200 (updated in place), no duplicate.
    second = client.post("/api/v1/lessons/l1/notes", json={**_payload("v2"), "id": cid})
    assert second.status_code == 200
    assert second.json()["id"] == cid

    all_notes = client.get("/api/v1/lessons/l1/notes").json()
    assert len(all_notes) == 1
    assert all_notes[0]["body"] == "v2"


def test_update_and_delete(client: TestClient) -> None:
    nid = client.post("/api/v1/lessons/l1/notes", json=_payload()).json()["id"]

    patched = client.patch(f"/api/v1/notes/{nid}", json={"body": "edited"})
    assert patched.status_code == 200
    assert patched.json()["body"] == "edited"
    assert patched.json()["quote"] == "highlighted"  # untouched

    # Explicit null clears the quote.
    cleared = client.patch(f"/api/v1/notes/{nid}", json={"quote": None})
    assert cleared.json()["quote"] is None

    deleted = client.delete(f"/api/v1/notes/{nid}")
    assert deleted.status_code == 204
    assert client.get("/api/v1/lessons/l1/notes").json() == []


def test_empty_body_rejected(client: TestClient) -> None:
    resp = client.post("/api/v1/lessons/l1/notes", json={"courseSlug": "c", "body": "   "})
    # Whitespace-only passes min_length=1 at the schema but fails domain validation → 422.
    assert resp.status_code == 422


def test_update_missing_note_404(client: TestClient) -> None:
    assert client.patch(f"/api/v1/notes/{uuid.uuid4()}", json={"body": "x"}).status_code == 404


def test_notes_are_user_scoped(app: FastAPI, _prepared_schema: None) -> None:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    me = TestClient(app)
    nid = me.post("/api/v1/lessons/l1/notes", json=_payload()).json()["id"]

    app.dependency_overrides[require_principal] = lambda: _principal(_OTHER)
    other = TestClient(app)
    assert other.get("/api/v1/lessons/l1/notes").json() == []
    assert other.patch(f"/api/v1/notes/{nid}", json={"body": "x"}).status_code == 404
    assert other.delete(f"/api/v1/notes/{nid}").status_code == 404

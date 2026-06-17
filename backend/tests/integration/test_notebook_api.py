"""End-to-end tests for the notebook notes endpoints (issue #161)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_USER = uuid.UUID("a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1")
_OTHER = uuid.UUID("b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2")


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


def _note(title: str = "Ohm's Law", type_: str = "code") -> dict:
    return {
        "title": title,
        "type": type_,
        "body": "V = I·R",
        "code": "print(2+2)",
        "language": "python",
        "runResult": {"ok": True, "stdout": "4"},
        "plotRefs": ["fig1.png"],
        "tags": ["electronics"],
    }


def test_create_get_update_delete(client: TestClient) -> None:
    created = client.post("/api/v1/notebook/notes", json=_note())
    assert created.status_code == 201, created.text
    body = created.json()
    nid = body["id"]
    assert body["title"] == "Ohm's Law"
    assert body["runResult"] == {"ok": True, "stdout": "4"}
    assert body["plotRefs"] == ["fig1.png"]
    assert "createdAt" in body  # camelCase

    got = client.get(f"/api/v1/notebook/notes/{nid}")
    assert got.status_code == 200
    assert got.json()["code"] == "print(2+2)"

    patched = client.patch(
        f"/api/v1/notebook/notes/{nid}", json=_note(title="Updated", type_="theory")
    )
    assert patched.status_code == 200
    assert patched.json()["title"] == "Updated"
    assert patched.json()["type"] == "theory"

    deleted = client.delete(f"/api/v1/notebook/notes/{nid}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/notebook/notes/{nid}").status_code == 404


def test_invalid_type_rejected(client: TestClient) -> None:
    resp = client.post("/api/v1/notebook/notes", json=_note(type_="bogus"))
    assert resp.status_code == 422


def test_get_missing_404(client: TestClient) -> None:
    assert client.get(f"/api/v1/notebook/notes/{uuid.uuid4()}").status_code == 404


def test_list_filter_by_type_and_search(client: TestClient) -> None:
    client.post("/api/v1/notebook/notes", json=_note(title="Fourier", type_="theory"))
    client.post("/api/v1/notebook/notes", json=_note(title="Loop demo", type_="code"))

    by_type = client.get("/api/v1/notebook/notes?type=theory").json()
    assert [n["title"] for n in by_type["items"]] == ["Fourier"]

    found = client.get("/api/v1/notebook/notes?q=loop").json()
    assert [n["title"] for n in found["items"]] == ["Loop demo"]


def test_list_pagination_cursor(client: TestClient) -> None:
    # Distinct created_at ordering — create in sequence; newest first.
    for i in range(3):
        client.post("/api/v1/notebook/notes", json=_note(title=f"n{i}"))

    first = client.get("/api/v1/notebook/notes?limit=2").json()
    assert len(first["items"]) == 2
    assert first["nextCursor"] is not None

    second = client.get(f"/api/v1/notebook/notes?limit=2&cursor={first['nextCursor']}").json()
    assert len(second["items"]) == 1
    assert second["nextCursor"] is None

    # Pages together cover all 3 distinct notes.
    titles = {n["title"] for n in first["items"]} | {n["title"] for n in second["items"]}
    assert titles == {"n0", "n1", "n2"}


def test_notes_are_user_scoped(app: FastAPI, _prepared_schema: None) -> None:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    me = TestClient(app)
    created = me.post("/api/v1/notebook/notes", json=_note())
    nid = created.json()["id"]

    app.dependency_overrides[require_principal] = lambda: _principal(_OTHER)
    other = TestClient(app)
    # Other user can't read or list it.
    assert other.get(f"/api/v1/notebook/notes/{nid}").status_code == 404
    assert other.get("/api/v1/notebook/notes").json()["items"] == []


def test_flashcard_crud(client: TestClient) -> None:
    note_id = client.post("/api/v1/notebook/notes", json=_note()).json()["id"]

    created = client.post(
        f"/api/v1/notebook/notes/{note_id}/flashcards",
        json={"question": "What is V=IR?", "answer": "Ohm's Law"},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["question"] == "What is V=IR?"
    assert body["noteId"] == note_id
    fid = body["id"]

    listed = client.get(f"/api/v1/notebook/notes/{note_id}/flashcards")
    assert [c["answer"] for c in listed.json()] == ["Ohm's Law"]

    deleted = client.delete(f"/api/v1/notebook/notes/{note_id}/flashcards/{fid}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/notebook/notes/{note_id}/flashcards").json() == []


def test_flashcard_on_missing_note_404(client: TestClient) -> None:
    resp = client.post(
        f"/api/v1/notebook/notes/{uuid.uuid4()}/flashcards",
        json={"question": "q", "answer": "a"},
    )
    assert resp.status_code == 404


def test_empty_flashcard_rejected(client: TestClient) -> None:
    note_id = client.post("/api/v1/notebook/notes", json=_note()).json()["id"]
    resp = client.post(
        f"/api/v1/notebook/notes/{note_id}/flashcards",
        json={"question": "", "answer": "a"},
    )
    assert resp.status_code == 422


def test_flashcards_are_user_scoped(app: FastAPI, _prepared_schema: None) -> None:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    me = TestClient(app)
    note_id = me.post("/api/v1/notebook/notes", json=_note()).json()["id"]
    me.post(
        f"/api/v1/notebook/notes/{note_id}/flashcards",
        json={"question": "q", "answer": "a"},
    )

    app.dependency_overrides[require_principal] = lambda: _principal(_OTHER)
    other = TestClient(app)
    # Other user can't reach flashcards on my note (note lookup 404s).
    assert other.get(f"/api/v1/notebook/notes/{note_id}/flashcards").status_code == 404

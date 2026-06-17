"""End-to-end tests for the concepts library endpoints (issue #168)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_EDITOR = UserPrincipal(
    user_id=uuid.uuid4(),
    username="editor",
    scopes=frozenset({"editor"}),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


@pytest.fixture
def editor_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_editor] = lambda: _EDITOR
    return TestClient(app)


def _payload(slug: str, *, domain: str = "Electronics", title: str | None = None) -> dict:
    return {
        "slug": slug,
        "title": title or slug.replace("-", " ").title(),
        "domain": domain,
        "summary": f"Summary for {slug}.",
        "formula": "V = I·R",
    }


def test_create_get_and_public_browse(editor_client: TestClient) -> None:
    created = editor_client.post("/api/v1/admin/concepts", json=_payload("ohms-law"))
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["slug"] == "ohms-law"
    assert body["formula"] == "V = I·R"
    assert "createdAt" in body  # camelCase

    # Public GET by slug (no auth needed).
    got = editor_client.get("/api/v1/concepts/ohms-law")
    assert got.status_code == 200
    assert got.json()["title"] == "Ohms Law"

    # Public browse.
    listed = editor_client.get("/api/v1/concepts")
    assert [c["slug"] for c in listed.json()["items"]] == ["ohms-law"]


def test_duplicate_slug_conflicts(editor_client: TestClient) -> None:
    editor_client.post("/api/v1/admin/concepts", json=_payload("kvl"))
    dup = editor_client.post("/api/v1/admin/concepts", json=_payload("kvl"))
    assert dup.status_code == 409


def test_invalid_slug_rejected(editor_client: TestClient) -> None:
    bad = editor_client.post("/api/v1/admin/concepts", json=_payload("Not A Slug"))
    assert bad.status_code == 422


def test_update_and_delete(editor_client: TestClient) -> None:
    editor_client.post("/api/v1/admin/concepts", json=_payload("kcl"))
    updated = editor_client.put(
        "/api/v1/admin/concepts/kcl",
        json=_payload("kcl", title="Kirchhoff Current Law"),
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Kirchhoff Current Law"

    deleted = editor_client.delete("/api/v1/admin/concepts/kcl")
    assert deleted.status_code == 204
    assert editor_client.get("/api/v1/concepts/kcl").status_code == 404


def test_update_missing_concept_404(editor_client: TestClient) -> None:
    resp = editor_client.put("/api/v1/admin/concepts/ghost", json=_payload("ghost"))
    assert resp.status_code == 404


def test_search_and_domain_filter(editor_client: TestClient) -> None:
    editor_client.post("/api/v1/admin/concepts", json=_payload("fourier", domain="Math"))
    editor_client.post("/api/v1/admin/concepts", json=_payload("ohms-law", domain="Electronics"))

    # domain filter
    math = editor_client.get("/api/v1/concepts?domain=Math").json()
    assert [c["slug"] for c in math["items"]] == ["fourier"]

    # full-text-ish search on title/summary
    found = editor_client.get("/api/v1/concepts?q=fourier").json()
    assert [c["slug"] for c in found["items"]] == ["fourier"]


def test_browse_pagination_cursor(editor_client: TestClient) -> None:
    for slug in ["a-one", "b-two", "c-three"]:
        editor_client.post("/api/v1/admin/concepts", json=_payload(slug))

    first = editor_client.get("/api/v1/concepts?limit=2").json()
    assert [c["slug"] for c in first["items"]] == ["a-one", "b-two"]
    assert first["nextCursor"] is not None

    second = editor_client.get(f"/api/v1/concepts?limit=2&cursor={first['nextCursor']}").json()
    assert [c["slug"] for c in second["items"]] == ["c-three"]
    assert second["nextCursor"] is None


def test_admin_requires_editor(client: TestClient) -> None:
    # No editor override → auth gate rejects.
    resp = client.post("/api/v1/admin/concepts", json=_payload("x-ray"))
    assert resp.status_code in (401, 403)

"""End-to-end tests for the learning catalogue admin-CRUD endpoints.

The in-memory schema starts empty (no migration seed), so each test creates
the modules/paths it needs and asserts the public read endpoints reflect the
writes — proving curriculum is authorable via the API with no redeploy.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_NOW = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
_USER = uuid.UUID("55555555-5555-5555-5555-555555555555")


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER, username="l", scopes=frozenset(), audience=None, expires_at=_NOW
    )


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="e",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_NOW,
    )


@pytest.fixture
def admin_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


_MODULE = {
    "title": "Programming Fundamentals",
    "category": "Foundations",
    "description": "Variables, control flow, functions and recursion.",
    "level": "Beginner",
    "duration": "1 hr",
    "icon": "💻",
    "topics": ["Variables & Types", "Control Flow"],
}


def _make_module(client: TestClient, *, slug: str, title: str, level: str = "Beginner") -> None:
    resp = client.post(
        "/api/v1/admin/learning/modules",
        json={**_MODULE, "slug": slug, "title": title, "level": level},
    )
    assert resp.status_code == 201, resp.text


def test_create_module_appears_in_public_catalogue(admin_client: TestClient) -> None:
    resp = admin_client.post("/api/v1/admin/learning/modules", json=_MODULE)
    assert resp.status_code == 201, resp.text
    assert resp.json()["slug"] == "programming-fundamentals"

    public = admin_client.get("/api/v1/learning/modules").json()
    assert any(m["slug"] == "programming-fundamentals" for m in public)


def test_duplicate_module_conflicts(admin_client: TestClient) -> None:
    assert admin_client.post("/api/v1/admin/learning/modules", json=_MODULE).status_code == 201
    dup = admin_client.post("/api/v1/admin/learning/modules", json=_MODULE)
    assert dup.status_code == 409, dup.text


def test_invalid_level_rejected(admin_client: TestClient) -> None:
    resp = admin_client.post("/api/v1/admin/learning/modules", json={**_MODULE, "level": "Expert"})
    assert resp.status_code == 422, resp.text


def test_update_and_delete_module(admin_client: TestClient) -> None:
    _make_module(admin_client, slug="m1", title="M1")
    patched = admin_client.patch("/api/v1/admin/learning/modules/m1", json={"title": "M1 v2"})
    assert patched.status_code == 200
    assert patched.json()["title"] == "M1 v2"
    assert patched.json()["level"] == "Beginner"  # unchanged

    assert admin_client.delete("/api/v1/admin/learning/modules/m1").status_code == 204
    assert (
        admin_client.patch("/api/v1/admin/learning/modules/m1", json={"title": "x"}).status_code
        == 404
    )


def test_create_path_with_modules_is_public_and_enrollable(admin_client: TestClient) -> None:
    _make_module(admin_client, slug="programming-fundamentals", title="Programming Fundamentals")
    _make_module(admin_client, slug="digital-logic", title="Digital Logic", level="Beginner")

    resp = admin_client.post(
        "/api/v1/admin/learning/paths",
        json={
            "title": "Computer Engineering",
            "description": "The full hardware-software stack.",
            "moduleSlugs": ["programming-fundamentals", "digital-logic"],
            "estimatedTime": "16-24 weeks",
            "icon": "🖥️",
        },
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["slug"] == "computer-engineering"
    assert resp.json()["moduleSlugs"] == ["programming-fundamentals", "digital-logic"]

    public = admin_client.get("/api/v1/learning/paths").json()
    assert any(p["slug"] == "computer-engineering" for p in public)

    enroll = admin_client.post("/api/v1/learning/paths/computer-engineering/enroll")
    assert enroll.status_code in (200, 201), enroll.text


def test_path_with_unknown_module_rejected_and_not_persisted(admin_client: TestClient) -> None:
    _make_module(admin_client, slug="m1", title="M1")
    resp = admin_client.post(
        "/api/v1/admin/learning/paths",
        json={
            "title": "Broken",
            "description": "d",
            "moduleSlugs": ["m1", "ghost"],
            "estimatedTime": "1 wk",
            "icon": "❓",
        },
    )
    assert resp.status_code == 422, resp.text
    assert admin_client.get("/api/v1/learning/paths").json() == []


def test_reorder_changes_gating_order(admin_client: TestClient) -> None:
    _make_module(admin_client, slug="m1", title="M1")
    _make_module(admin_client, slug="m2", title="M2")
    admin_client.post(
        "/api/v1/admin/learning/paths",
        json={
            "title": "P",
            "description": "d",
            "moduleSlugs": ["m1", "m2"],
            "estimatedTime": "1 wk",
            "icon": "📦",
        },
    )
    gates = {g["moduleSlug"]: g for g in admin_client.get("/api/v1/learning/paths/p/gating").json()}
    assert gates["m1"]["unlocked"] is True
    assert gates["m2"]["unlocked"] is False
    assert gates["m2"]["blockedBy"] == "m1"

    reorder = admin_client.post(
        "/api/v1/admin/learning/paths/p/modules/reorder",
        json={"moduleSlugs": ["m2", "m1"]},
    )
    assert reorder.status_code == 200, reorder.text

    gates = {g["moduleSlug"]: g for g in admin_client.get("/api/v1/learning/paths/p/gating").json()}
    assert gates["m2"]["unlocked"] is True
    assert gates["m1"]["unlocked"] is False
    assert gates["m1"]["blockedBy"] == "m2"


def test_unknown_path_update_and_delete_404(admin_client: TestClient) -> None:
    assert (
        admin_client.patch("/api/v1/admin/learning/paths/ghost", json={"title": "x"}).status_code
        == 404
    )
    assert admin_client.delete("/api/v1/admin/learning/paths/ghost").status_code == 404


def test_admin_routes_require_editor(client: TestClient) -> None:
    # No auth overrides on this client → the editor guard rejects.
    resp = client.post("/api/v1/admin/learning/modules", json=_MODULE)
    assert resp.status_code in (401, 403), resp.text


def test_module_can_link_real_courses(admin_client: TestClient) -> None:
    # Create + publish a real course, then bundle it into a stage.
    created = admin_client.post(
        "/api/v1/admin/courses",
        json={"title": "Linkable Course", "description": "d", "level": "Beginner"},
    )
    assert created.status_code in (200, 201), created.text
    course_slug = created.json()["slug"]
    assert admin_client.post(f"/api/v1/admin/courses/{course_slug}/publish").status_code == 200

    resp = admin_client.post(
        "/api/v1/admin/learning/modules",
        json={**_MODULE, "slug": "stage-1", "courseSlugs": [course_slug]},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["courseSlugs"] == [course_slug]

    # Public catalogue exposes the linkage AND the resolved course cards
    # (slug/title/level) so the app can render the courses in a stage.
    public = {m["slug"]: m for m in admin_client.get("/api/v1/learning/modules").json()}
    assert public["stage-1"]["courseSlugs"] == [course_slug]
    assert public["stage-1"]["courses"] == [
        {"slug": course_slug, "title": "Linkable Course", "level": "Beginner"}
    ]


def test_module_linking_unknown_course_rejected(admin_client: TestClient) -> None:
    resp = admin_client.post(
        "/api/v1/admin/learning/modules",
        json={**_MODULE, "slug": "stage-x", "courseSlugs": ["no-such-course"]},
    )
    assert resp.status_code == 422, resp.text
    assert admin_client.get("/api/v1/learning/modules").json() == []

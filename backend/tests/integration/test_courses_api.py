"""End-to-end API tests for the courses endpoints.

Drives the real router → use case → SQLAlchemy repository → in-memory
sqlite stack. Admin endpoints are exercised by overriding the
``require_editor`` dependency with a fake editor principal.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.domain.auth_identity import UserPrincipal

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
def editor_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


@pytest.mark.usefixtures("_prepared_schema")
def test_course_lifecycle(editor_client: TestClient) -> None:
    # Create → starts as a draft, invisible to anonymous list.
    create = editor_client.post(
        "/api/v1/admin/courses",
        json={"title": "Solidity 101", "description": "learn solidity", "level": "Beginner"},
    )
    assert create.status_code == 201, create.text
    body = create.json()
    assert body["slug"] == "solidity-101"
    assert body["status"] == "draft"
    assert body["lessonCount"] == 0

    # Anonymous catalogue excludes the draft.
    anon = TestClient(editor_client.app)
    assert anon.get("/api/v1/courses").json() == []

    # Add a lesson, then publish.
    lesson = editor_client.post(
        "/api/v1/admin/courses/solidity-101/lessons",
        json={"title": "Intro", "lessonType": "text", "textBody": "# Hello"},
    )
    assert lesson.status_code == 201, lesson.text
    assert lesson.json()["lessonType"] == "text"

    pub = editor_client.post("/api/v1/admin/courses/solidity-101/publish")
    assert pub.status_code == 200
    assert pub.json()["status"] == "published"

    # Now anonymous can see it, with the lesson embedded in detail.
    listed = anon.get("/api/v1/courses").json()
    assert [c["slug"] for c in listed] == ["solidity-101"]
    detail = anon.get("/api/v1/courses/solidity-101").json()
    assert detail["lessonCount"] == 1
    assert detail["lessons"][0]["title"] == "Intro"


@pytest.mark.usefixtures("_prepared_schema")
def test_course_deadline_set_status_and_clear(editor_client: TestClient) -> None:
    editor_client.post(
        "/api/v1/admin/courses",
        json={"title": "Deadline Course", "description": "d", "level": "Beginner"},
    )
    detail = editor_client.put(
        "/api/v1/admin/courses/deadline-course/deadline",
        json={"dueAt": "2999-01-01T00:00:00Z"},
    )
    assert detail.status_code == 200, detail.text
    body = detail.json()
    assert body["dueAt"] is not None
    assert body["deadlineStatus"] == "upcoming"
    assert body["daysRemaining"] > 0

    # A past due date reads as overdue with negative days remaining.
    overdue = editor_client.put(
        "/api/v1/admin/courses/deadline-course/deadline",
        json={"dueAt": "2000-01-01T00:00:00Z"},
    ).json()
    assert overdue["deadlineStatus"] == "overdue"
    assert overdue["daysRemaining"] < 0

    # Clearing resets to none.
    cleared = editor_client.put(
        "/api/v1/admin/courses/deadline-course/deadline",
        json={"dueAt": None},
    ).json()
    assert cleared["dueAt"] is None
    assert cleared["deadlineStatus"] == "none"
    assert cleared["daysRemaining"] is None


@pytest.mark.usefixtures("_prepared_schema")
def test_course_deadline_unknown_course_404(editor_client: TestClient) -> None:
    resp = editor_client.put("/api/v1/admin/courses/ghost/deadline", json={"dueAt": None})
    assert resp.status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_invalid_lesson_content_is_422(editor_client: TestClient) -> None:
    editor_client.post(
        "/api/v1/admin/courses",
        json={"title": "C", "description": "d", "level": "Beginner"},
    )
    # A video lesson with no contentUrl violates the domain invariant.
    resp = editor_client.post(
        "/api/v1/admin/courses/c/lessons",
        json={"title": "v", "lessonType": "video"},
    )
    assert resp.status_code == 422


@pytest.mark.usefixtures("_prepared_schema")
def test_duplicate_slug_is_409(editor_client: TestClient) -> None:
    payload = {"title": "Dup", "description": "d", "level": "Beginner"}
    assert editor_client.post("/api/v1/admin/courses", json=payload).status_code == 201
    assert editor_client.post("/api/v1/admin/courses", json=payload).status_code == 409


@pytest.mark.usefixtures("_prepared_schema")
def test_unknown_course_is_404(editor_client: TestClient) -> None:
    assert editor_client.get("/api/v1/courses/nope").status_code == 404


def test_admin_requires_editor(client: TestClient) -> None:
    # No auth → middleware leaves no principal → require_editor 401s.
    resp = client.post(
        "/api/v1/admin/courses",
        json={"title": "x", "description": "d", "level": "Beginner"},
    )
    assert resp.status_code in (401, 403)

"""End-to-end API tests for course completion certificates.

An editor authors + publishes a course; a learner completes every
lesson, claims the certificate, fetches it, and verifies it publicly.
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


@pytest.fixture
def authed_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def _make_published_course(client: TestClient, slug_title: str = "Cert Course") -> list[str]:
    assert (
        client.post(
            "/api/v1/admin/courses",
            json={"title": slug_title, "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    slug = slug_title.lower().replace(" ", "-")
    ids = []
    for i in range(2):
        lesson = client.post(
            f"/api/v1/admin/courses/{slug}/lessons",
            json={"title": f"Lesson {i}", "lessonType": "text", "textBody": "body"},
        )
        ids.append(lesson.json()["id"])
    assert client.post(f"/api/v1/admin/courses/{slug}/publish").status_code == 200
    return ids


@pytest.mark.usefixtures("_prepared_schema")
def test_certificate_issued_on_completion_and_verifies(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)

    # Not complete yet -> claiming the certificate is a 409.
    early = authed_client.post("/api/v1/courses/cert-course/certificate")
    assert early.status_code == 409

    # Complete every lesson.
    for lid in lesson_ids:
        authed_client.put(
            f"/api/v1/courses/cert-course/lessons/{lid}/progress", json={"percent": 100}
        )

    # Claim the certificate.
    issued = authed_client.post("/api/v1/courses/cert-course/certificate")
    assert issued.status_code == 201, issued.text
    cert = issued.json()
    assert cert["courseSlug"] == "cert-course"
    cert_id = cert["id"]

    # Idempotent: claiming again returns the same certificate.
    again = authed_client.post("/api/v1/courses/cert-course/certificate")
    assert again.status_code == 201
    assert again.json()["id"] == cert_id

    # The learner can fetch their certificate.
    mine = authed_client.get("/api/v1/courses/cert-course/certificate")
    assert mine.status_code == 200
    assert mine.json()["id"] == cert_id

    # Public verification confirms the signature.
    verify = authed_client.get(f"/api/v1/courses/certificates/{cert_id}/verify")
    assert verify.status_code == 200
    body = verify.json()
    assert body["valid"] is True
    assert body["certificate"]["id"] == cert_id

    # The certificate renders as a downloadable PDF.
    pdf = authed_client.get(f"/api/v1/courses/certificates/{cert_id}/pdf")
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content.startswith(b"%PDF")


@pytest.mark.usefixtures("_prepared_schema")
def test_certificate_auto_issued_on_progress_completion(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)
    # Complete every lesson via the progress endpoint — no explicit claim.
    for lid in lesson_ids:
        authed_client.put(
            f"/api/v1/courses/cert-course/lessons/{lid}/progress", json={"percent": 100}
        )
    # The certificate now exists without the learner POSTing to claim it.
    mine = authed_client.get("/api/v1/courses/cert-course/certificate")
    assert mine.status_code == 200
    assert mine.json()["courseSlug"] == "cert-course"


@pytest.mark.usefixtures("_prepared_schema")
def test_certificate_auto_issued_when_quiz_completes_course(authed_client: TestClient) -> None:
    # Single quiz lesson — passing it completes the only lesson, so the
    # course completes and the certificate is auto-issued.
    assert (
        authed_client.post(
            "/api/v1/admin/courses",
            json={"title": "Quiz Only", "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    lesson = authed_client.post(
        "/api/v1/admin/courses/quiz-only/lessons",
        json={"title": "Assessment", "lessonType": "quiz"},
    )
    lesson_id = lesson.json()["id"]
    authed_client.post("/api/v1/admin/courses/quiz-only/publish")
    authed_client.put(
        f"/api/v1/admin/lessons/{lesson_id}/quiz",
        json={
            "passingScore": 70,
            "questions": [
                {
                    "prompt": "2 + 2 = ?",
                    "explanation": "Addition.",
                    "options": [
                        {"text": "3", "isCorrect": False},
                        {"text": "4", "isCorrect": True},
                    ],
                }
            ],
        },
    )
    editor_view = authed_client.get(f"/api/v1/admin/lessons/{lesson_id}/quiz").json()
    answers = {
        q["id"]: next(o["id"] for o in q["options"] if o["isCorrect"])
        for q in editor_view["questions"]
    }
    assert (
        authed_client.post(
            f"/api/v1/lessons/{lesson_id}/quiz/attempts", json={"answers": answers}
        ).json()["passed"]
        is True
    )
    # Course auto-completed by the quiz pass -> certificate exists.
    assert authed_client.get("/api/v1/courses/quiz-only/certificate").status_code == 200


@pytest.mark.usefixtures("_prepared_schema")
def test_get_certificate_404_before_issue(authed_client: TestClient) -> None:
    _make_published_course(authed_client)
    assert authed_client.get("/api/v1/courses/cert-course/certificate").status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_issue_unknown_course_404(authed_client: TestClient) -> None:
    assert authed_client.post("/api/v1/courses/ghost/certificate").status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_verify_unknown_certificate_is_invalid(authed_client: TestClient) -> None:
    resp = authed_client.get(f"/api/v1/courses/certificates/{uuid.uuid4()}/verify")
    assert resp.status_code == 200
    assert resp.json()["valid"] is False


@pytest.mark.usefixtures("_prepared_schema")
def test_pdf_unknown_certificate_is_404(authed_client: TestClient) -> None:
    assert authed_client.get(f"/api/v1/courses/certificates/{uuid.uuid4()}/pdf").status_code == 404


def test_certificate_requires_auth(client: TestClient) -> None:
    assert client.post("/api/v1/courses/x/certificate").status_code in (401, 403)

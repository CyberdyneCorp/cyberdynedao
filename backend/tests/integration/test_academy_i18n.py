"""Locale-aware Academy reads: repository overlay + API Accept-Language.

Covers course/lesson and quiz content served per-language with per-field
English fallback when a translation row (or field) is absent.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.adapters.outbound.persistence.academy.translation_repository import (
    SqlAlchemyTranslationRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.application.academy.translation import content_hash
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.courses import CourseStatus, new_course, new_lesson
from cyberdyne_backend.domain.quizzes import build_question, new_quiz

pytestmark = pytest.mark.integration


# ── Repository overlay + per-field fallback (direct, no HTTP) ─────────


@pytest.mark.usefixtures("_prepared_schema")
async def test_course_repo_overlay_and_per_field_fallback(db_session: AsyncSession) -> None:
    course = new_course(title="Algebra", description="Learn algebra", level="Beginner", slug="alg")
    course.status = CourseStatus.PUBLISHED
    l1 = new_lesson(
        course_id=course.id, title="Intro", lesson_type="text", text_body="Hello", sort_order=0
    )
    l2 = new_lesson(
        course_id=course.id, title="Vectors", lesson_type="text", text_body="World", sort_order=1
    )
    course.lessons.extend([l1, l2])
    repo = SqlAlchemyCourseRepository(db_session)
    await repo.save(course)

    tr = SqlAlchemyTranslationRepository(db_session)
    # Course: title translated, description left empty → English fallback.
    await tr.upsert_course_translation(
        course_id=course.id, language="pt-BR", title="Álgebra", description="", source_hash="h"
    )
    # Only the first lesson is translated; the second falls back to English.
    await tr.upsert_lesson_translation(
        lesson_id=l1.id, language="pt-BR", title="Introdução", text_body="Olá", source_hash="h"
    )

    pt = await repo.get_by_slug("alg", include_drafts=True, locale="pt-BR")
    assert pt.title == "Álgebra"
    assert pt.description == "Learn algebra"  # per-field English fallback
    assert pt.lessons[0].title == "Introdução"
    assert pt.lessons[0].text_body == "Olá"
    assert pt.lessons[1].title == "Vectors"  # untranslated lesson → English
    assert pt.lessons[1].text_body == "World"

    en = await repo.get_by_slug("alg", include_drafts=True, locale="en")
    assert en.title == "Algebra"
    assert en.lessons[0].title == "Intro"


@pytest.mark.usefixtures("_prepared_schema")
async def test_quiz_repo_overlay_and_fallback(db_session: AsyncSession) -> None:
    lesson_id = uuid.uuid4()
    quiz = new_quiz(
        lesson_id=lesson_id,
        questions=[
            build_question(
                prompt="What is 2+2?",
                explanation="basic arithmetic",
                options=[("3", False), ("4", True)],
            )
        ],
        passing_score=70,
    )
    repo = SqlAlchemyQuizRepository(db_session)
    await repo.upsert(quiz)
    question = quiz.questions[0]
    opt_correct = next(o for o in question.options if o.is_correct)

    tr = SqlAlchemyTranslationRepository(db_session)
    # Prompt translated, explanation left empty → English fallback.
    await tr.upsert_question_translation(
        question_id=question.id,
        language="pt-BR",
        prompt="Quanto é 2+2?",
        explanation="",
        source_hash="h",
    )
    await tr.upsert_option_translation(
        option_id=opt_correct.id, language="pt-BR", text="quatro", source_hash="h"
    )

    pt = await repo.get_by_lesson(lesson_id, locale="pt-BR")
    q = pt.questions[0]
    assert q.prompt == "Quanto é 2+2?"
    assert q.explanation == "basic arithmetic"  # fallback
    texts = {o.text for o in q.options}
    assert "quatro" in texts  # translated option
    assert "3" in texts  # untranslated option → English

    en = await repo.get_by_lesson(lesson_id, locale="en")
    assert en.questions[0].prompt == "What is 2+2?"


# ── API: Accept-Language threads through to localized content ─────────


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="editor",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.mark.usefixtures("_prepared_schema")
async def test_course_api_serves_accept_language(app: FastAPI, db_session: AsyncSession) -> None:
    app.dependency_overrides[require_editor] = _editor
    client = TestClient(app)

    created = client.post(
        "/api/v1/admin/courses",
        json={"title": "Calculus", "description": "Learn calculus", "level": "Beginner"},
    )
    assert created.status_code == 201, created.text
    course_id = uuid.UUID(created.json()["id"])
    lesson = client.post(
        "/api/v1/admin/courses/calculus/lessons",
        json={"title": "Limits", "lessonType": "text", "textBody": "# Limits"},
    )
    lesson_id = uuid.UUID(lesson.json()["id"])
    assert client.post("/api/v1/admin/courses/calculus/publish").status_code == 200

    # Seed pt-BR translations directly, then commit so the app session sees them.
    tr = SqlAlchemyTranslationRepository(db_session)
    await tr.upsert_course_translation(
        course_id=course_id,
        language="pt-BR",
        title="Cálculo",
        description="Aprenda cálculo",
        source_hash=content_hash("Calculus", "Learn calculus"),
    )
    await tr.upsert_lesson_translation(
        lesson_id=lesson_id,
        language="pt-BR",
        title="Limites",
        text_body="# Limites",
        source_hash="h",
    )
    await db_session.commit()

    anon = TestClient(app)
    # Header-driven locale.
    pt = anon.get("/api/v1/courses/calculus", headers={"Accept-Language": "pt-BR"}).json()
    assert pt["title"] == "Cálculo"
    assert pt["description"] == "Aprenda cálculo"
    assert pt["lessons"][0]["title"] == "Limites"

    # Query-param override.
    pt_q = anon.get("/api/v1/courses/calculus?lang=pt-BR").json()
    assert pt_q["title"] == "Cálculo"

    # Default English.
    en = anon.get("/api/v1/courses/calculus").json()
    assert en["title"] == "Calculus"
    assert en["lessons"][0]["title"] == "Limits"

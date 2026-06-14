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
async def test_lesson_translation_title_accepts_long_values(db_session: AsyncSession) -> None:
    # Regression: translated titles are TEXT, not VARCHAR(256) — a longer
    # translation (or an over-eager model) must not crash the job.
    course = new_course(title="C", description="d", level="Beginner", slug="long")
    lesson = new_lesson(course_id=course.id, title="Intro", lesson_type="text", text_body="x")
    course.lessons.append(lesson)
    await SqlAlchemyCourseRepository(db_session).save(course)

    long_title = "Título " * 80  # ~560 chars, well past the old 256 cap
    tr = SqlAlchemyTranslationRepository(db_session)
    await tr.upsert_lesson_translation(
        lesson_id=lesson.id, language="pt-BR", title=long_title, text_body="y", source_hash="h"
    )
    await tr.upsert_course_translation(
        course_id=course.id, language="pt-BR", title=long_title, description="d", source_hash="h"
    )
    pt = await SqlAlchemyCourseRepository(db_session).get_by_slug(
        "long", include_drafts=True, locale="pt-BR"
    )
    assert pt.title == long_title
    assert pt.lessons[0].title == long_title


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


# ── Admin: course languages + translate endpoints ────────────────────


@pytest.mark.usefixtures("_prepared_schema")
async def test_repo_course_languages_lists_distinct(db_session: AsyncSession) -> None:
    course = new_course(title="X", description="d", level="Beginner", slug="x")
    course.status = CourseStatus.PUBLISHED
    await SqlAlchemyCourseRepository(db_session).save(course)
    tr = SqlAlchemyTranslationRepository(db_session)
    assert await tr.course_languages(course.id) == []
    await tr.upsert_course_translation(
        course_id=course.id, language="pt-BR", title="X", description="d", source_hash="h"
    )
    await tr.upsert_course_translation(
        course_id=course.id, language="es", title="X", description="d", source_hash="h"
    )
    langs = await tr.course_languages(course.id)
    assert sorted(langs) == ["es", "pt-BR"]


@pytest.mark.usefixtures("_prepared_schema")
def test_get_course_languages_endpoint(app: FastAPI) -> None:
    from cyberdyne_backend.adapters.inbound.api.courses.router import translation_available

    app.dependency_overrides[require_editor] = _editor
    # Pin translation availability so the test doesn't depend on ambient env.
    app.dependency_overrides[translation_available] = lambda: True
    client = TestClient(app)
    client.post(
        "/api/v1/admin/courses",
        json={"title": "Logic", "description": "d", "level": "Beginner"},
    )
    body = client.get("/api/v1/admin/courses/logic/translations").json()
    assert body["available"] == ["en"]
    assert set(body["supported"]) == {"en", "pt-BR", "es", "fr"}
    assert body["canTranslate"] is True


@pytest.mark.usefixtures("_prepared_schema")
def test_translate_endpoint_enqueues_durable_job(app: FastAPI) -> None:
    from cyberdyne_backend.adapters.inbound.api.courses.router import (
        get_translation_job_store,
        translation_available,
    )

    calls: list[tuple[str, str]] = []

    class _SpyJobStore:
        async def enqueue(self, course_slug: str, language: str) -> None:
            calls.append((course_slug, language))

    async def _spy_store_dep():
        yield _SpyJobStore()

    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[translation_available] = lambda: True
    app.dependency_overrides[get_translation_job_store] = _spy_store_dep
    client = TestClient(app)
    client.post(
        "/api/v1/admin/courses",
        json={"title": "Topology", "description": "d", "level": "Beginner"},
    )

    resp = client.post("/api/v1/admin/courses/topology/translations/pt-BR")
    assert resp.status_code == 202, resp.text
    assert resp.json() == {"slug": "topology", "language": "pt-BR", "status": "started"}
    # The endpoint enqueues a durable job instead of running it in-process.
    assert calls == [("topology", "pt-BR")]

    # Unsupported language → 422; English is rejected (it's the base).
    assert client.post("/api/v1/admin/courses/topology/translations/de").status_code == 422
    assert client.post("/api/v1/admin/courses/topology/translations/en").status_code == 422
    # Unknown course → 404.
    assert client.post("/api/v1/admin/courses/nope/translations/es").status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_translate_endpoint_503_when_unavailable(app: FastAPI) -> None:
    from cyberdyne_backend.adapters.inbound.api.courses.router import translation_available

    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[translation_available] = lambda: False
    client = TestClient(app)
    client.post(
        "/api/v1/admin/courses",
        json={"title": "Graphs", "description": "d", "level": "Beginner"},
    )
    resp = client.post("/api/v1/admin/courses/graphs/translations/pt-BR")
    assert resp.status_code == 503


# ── Lesson-aware "available" flag (durable-translation fix) ──────────


@pytest.mark.usefixtures("_prepared_schema")
async def test_translated_lesson_counts_per_language(db_session: AsyncSession) -> None:
    course = new_course(title="X", description="d", level="Beginner", slug="x")
    course.status = CourseStatus.PUBLISHED
    l1 = new_lesson(course_id=course.id, title="A", lesson_type="text", text_body="a", sort_order=0)
    l2 = new_lesson(course_id=course.id, title="B", lesson_type="text", text_body="b", sort_order=1)
    course.lessons.extend([l1, l2])
    await SqlAlchemyCourseRepository(db_session).save(course)
    tr = SqlAlchemyTranslationRepository(db_session)
    assert await tr.translated_lesson_counts(course.id) == {}
    await tr.upsert_lesson_translation(
        lesson_id=l1.id, language="pt-BR", title="A", text_body="a", source_hash="h"
    )
    assert await tr.translated_lesson_counts(course.id) == {"pt-BR": 1}
    await tr.upsert_lesson_translation(
        lesson_id=l2.id, language="pt-BR", title="B", text_body="b", source_hash="h"
    )
    assert await tr.translated_lesson_counts(course.id) == {"pt-BR": 2}


@pytest.mark.usefixtures("_prepared_schema")
def test_languages_endpoint_requires_all_lessons_translated(app: FastAPI) -> None:
    """Regression: a course-level translation row alone must NOT report the
    language available — every lesson must be translated too."""
    from cyberdyne_backend.adapters.inbound.api.courses.router import translation_available

    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[translation_available] = lambda: True
    client = TestClient(app)
    client.post(
        "/api/v1/admin/courses",
        json={"title": "Sets", "description": "d", "level": "Beginner"},
    )
    client.post(
        "/api/v1/admin/courses/sets/lessons",
        json={"title": "Intro", "lessonType": "text", "textBody": "hi"},
    )
    # No translations yet → English only.
    assert client.get("/api/v1/admin/courses/sets/translations").json()["available"] == ["en"]


# ── Durable translation job store (SQLAlchemy adapter) ───────────────


@pytest.mark.usefixtures("_prepared_schema")
async def test_job_store_enqueue_claim_done(db_session: AsyncSession) -> None:
    from cyberdyne_backend.adapters.outbound.persistence.academy.job_store import (
        SqlAlchemyTranslationJobStore,
    )

    store = SqlAlchemyTranslationJobStore(db_session)
    await store.enqueue("alg", "pt-BR")
    await store.enqueue("alg", "pt-BR")  # idempotent upsert

    job = await store.claim_next()
    assert job is not None
    assert (job.course_slug, job.language) == ("alg", "pt-BR")
    # Now running → nothing else to claim.
    assert await store.claim_next() is None

    await store.mark_done(job.id)
    # Requeue only resets running jobs; a done job stays done.
    assert await store.requeue_running() == 0


@pytest.mark.usefixtures("_prepared_schema")
async def test_job_store_requeue_running_and_failure_retry(db_session: AsyncSession) -> None:
    from cyberdyne_backend.adapters.outbound.persistence.academy.job_store import (
        SqlAlchemyTranslationJobStore,
    )

    store = SqlAlchemyTranslationJobStore(db_session)
    await store.enqueue("alg", "es")
    job = await store.claim_next()
    assert job is not None
    # Simulate a restart stranding the job in 'running'.
    assert await store.requeue_running() == 1
    again = await store.claim_next()
    assert again is not None and again.id == job.id

    await store.mark_failed(again.id, "boom")
    # Under the retry cap → back to pending and reclaimable.
    retried = await store.claim_next()
    assert retried is not None and retried.id == job.id


@pytest.mark.usefixtures("_prepared_schema")
async def test_reseed_preserves_lesson_translations(db_session: AsyncSession) -> None:
    """Regression: re-saving a course (as ``seed_academy`` does on every boot)
    must NOT wipe lesson translations. ``save()`` previously delete+reinserted
    the lesson rows, and ``lesson_translations`` cascades on ``lessons.id`` —
    so every reseed silently destroyed all lesson (and quiz) translations while
    leaving the course-level translation intact."""
    course = new_course(title="Robotics", description="Robots", level="Beginner", slug="rob")
    course.status = CourseStatus.PUBLISHED
    lesson = new_lesson(
        course_id=course.id, title="Joints", lesson_type="text", text_body="Body", sort_order=0
    )
    course.lessons.append(lesson)
    repo = SqlAlchemyCourseRepository(db_session)
    await repo.save(course)

    tr = SqlAlchemyTranslationRepository(db_session)
    await tr.upsert_lesson_translation(
        lesson_id=lesson.id, language="pt-BR", title="Juntas", text_body="Corpo", source_hash="h"
    )
    await db_session.flush()

    # Re-save the same course aggregate — exactly what a boot-time reseed does.
    reloaded = await repo.get_by_slug("rob", include_drafts=True)
    await repo.save(reloaded)
    await db_session.flush()

    # The lesson translation must survive the reseed (was wiped before the fix).
    localized = await repo.get_by_slug("rob", include_drafts=True, locale="pt-BR")
    assert localized.lessons[0].title == "Juntas"
    assert localized.lessons[0].text_body == "Corpo"

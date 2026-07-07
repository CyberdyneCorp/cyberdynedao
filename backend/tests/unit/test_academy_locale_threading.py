"""The read use cases must forward ``locale`` to the repository."""

from __future__ import annotations

import uuid

import pytest

from cyberdyne_backend.application.courses.use_cases import GetCourse, ListCourses
from cyberdyne_backend.application.quizzes.use_cases import GetQuiz
from cyberdyne_backend.domain.courses import new_course
from cyberdyne_backend.domain.quizzes import build_question, new_quiz

pytestmark = pytest.mark.unit


class RecordingCourseRepo:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def get_by_slug(self, slug, *, include_drafts=False, locale="en"):
        self.calls.append(locale)
        return new_course(title="C", description="d", level="Beginner", slug=slug)

    async def list_courses(
        self,
        *,
        level=None,
        include_drafts=False,
        locale="en",
        limit=None,
        offset=0,
        include_lessons=True,
    ):
        self.calls.append(locale)
        return []


class RecordingQuizRepo:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def get_by_lesson(self, lesson_id, *, locale="en"):
        self.calls.append(locale)
        return new_quiz(
            lesson_id=lesson_id,
            questions=[
                build_question(prompt="q", explanation="e", options=[("a", True), ("b", False)])
            ],
            passing_score=70,
        )


async def test_get_course_forwards_locale() -> None:
    repo = RecordingCourseRepo()
    await GetCourse(repo=repo).execute("slug", locale="pt-BR")
    assert repo.calls == ["pt-BR"]


async def test_list_courses_forwards_locale() -> None:
    repo = RecordingCourseRepo()
    await ListCourses(repo=repo).execute(locale="es")
    assert repo.calls == ["es"]


async def test_get_quiz_forwards_locale() -> None:
    repo = RecordingQuizRepo()
    await GetQuiz(repo=repo).execute(uuid.uuid4(), locale="fr")
    assert repo.calls == ["fr"]

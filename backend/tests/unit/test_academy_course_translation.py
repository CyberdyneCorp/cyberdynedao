"""Unit tests for the per-course translation use cases."""

from __future__ import annotations

import pytest

from cyberdyne_backend.application.academy import (
    GetCourseLanguages,
    MarkdownAwareTranslator,
    TranslateCourse,
)
from cyberdyne_backend.domain.ai_chat import LLMResponse
from cyberdyne_backend.domain.courses import CourseNotFoundError, new_course, new_lesson
from cyberdyne_backend.domain.quizzes import QuizNotFoundError

pytestmark = pytest.mark.unit


class EchoLLM:
    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        return LLMResponse(content=f"[T] {messages[-1].content}")


class FakeCourseRepo:
    def __init__(self, course=None) -> None:
        self._course = course

    async def get_by_slug(self, slug, *, include_drafts=False, locale="en"):
        if self._course is None or self._course.slug != slug:
            raise CourseNotFoundError(slug)
        return self._course


class FakeQuizRepo:
    async def get_by_lesson(self, lesson_id, *, locale="en"):
        raise QuizNotFoundError(str(lesson_id))


class FakeTranslationRepo:
    def __init__(self, languages=None) -> None:
        self._languages = languages or []
        self.courses: list = []
        self.lessons: list = []

    async def course_languages(self, course_id):
        return list(self._languages)

    async def course_hashes(self, language):
        return {}

    async def lesson_hashes(self, language):
        return {}

    async def question_hashes(self, language):
        return {}

    async def option_hashes(self, language):
        return {}

    async def upsert_course_translation(self, **kw):
        self.courses.append(kw)

    async def upsert_lesson_translation(self, **kw):
        self.lessons.append(kw)

    async def upsert_question_translation(self, **kw):
        pass

    async def upsert_option_translation(self, **kw):
        pass


def _course():
    c = new_course(title="Algebra", description="d", level="Beginner", slug="alg")
    c.lessons.append(new_lesson(course_id=c.id, title="Intro", lesson_type="text", text_body="hi"))
    return c


async def test_get_course_languages_prepends_en_and_sorts() -> None:
    course = _course()
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        translation_repo=FakeTranslationRepo(languages=["pt-BR", "es"]),
    )
    assert await uc.execute("alg") == ["en", "es", "pt-BR"]


async def test_get_course_languages_en_only_when_no_translations() -> None:
    course = _course()
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course), translation_repo=FakeTranslationRepo()
    )
    assert await uc.execute("alg") == ["en"]


async def test_get_course_languages_unknown_slug_raises() -> None:
    uc = GetCourseLanguages(course_repo=FakeCourseRepo(), translation_repo=FakeTranslationRepo())
    with pytest.raises(CourseNotFoundError):
        await uc.execute("nope")


async def test_translate_course_translates_and_persists() -> None:
    course = _course()
    repo = FakeTranslationRepo()
    uc = TranslateCourse(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=repo,
        translator=MarkdownAwareTranslator(llm=EchoLLM()),
    )
    stats = await uc.execute("alg", "pt-BR")
    assert len(repo.courses) == 1  # course title/description
    assert len(repo.lessons) == 1  # the text lesson
    assert stats.translated == 2
    assert stats.failed == 0

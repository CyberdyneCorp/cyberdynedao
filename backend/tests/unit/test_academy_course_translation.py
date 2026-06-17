"""Unit tests for the per-course translation use cases."""

from __future__ import annotations

from types import SimpleNamespace

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
    """Returns a stub quiz with N questions for lessons in ``questions_by_lesson``
    (keyed by lesson id), else raises QuizNotFoundError. Only ``len(questions)``
    is read by the language/translate use cases."""

    def __init__(self, questions_by_lesson=None) -> None:
        self._q = questions_by_lesson or {}

    async def get_by_lesson(self, lesson_id, *, locale="en"):
        n = self._q.get(lesson_id)
        if n is None:
            raise QuizNotFoundError(str(lesson_id))
        return SimpleNamespace(questions=[object()] * n)


class FakeTranslationRepo:
    def __init__(self, languages=None, lesson_counts=None, question_counts=None) -> None:
        self._languages = languages or []
        self._lesson_counts = lesson_counts or {}
        self._question_counts = question_counts or {}
        self.courses: list = []
        self.lessons: list = []

    async def course_languages(self, course_id):
        return list(self._languages)

    async def translated_lesson_counts(self, course_id):
        return dict(self._lesson_counts)

    async def translated_question_counts(self, course_id):
        return dict(self._question_counts)

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
    # Both languages have all lessons (1) translated → both available.
    course = _course()
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(
            languages=["pt-BR", "es"], lesson_counts={"pt-BR": 1, "es": 1}
        ),
    )
    assert await uc.execute("alg") == ["en", "es", "pt-BR"]


async def test_get_course_languages_en_only_when_no_translations() -> None:
    course = _course()
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(),
    )
    assert await uc.execute("alg") == ["en"]


async def test_get_course_languages_course_only_translation_not_available() -> None:
    # Regression: a course-level translation row WITHOUT lesson rows must NOT
    # report the language available (the old bug). 1 lesson, 0 translated.
    course = _course()
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(languages=["pt-BR"], lesson_counts={}),
    )
    assert await uc.execute("alg") == ["en"]


async def test_get_course_languages_all_lessons_translated_available() -> None:
    # Course row + every lesson translated → available.
    course = _course()  # one lesson
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(languages=["pt-BR"], lesson_counts={"pt-BR": 1}),
    )
    assert await uc.execute("alg") == ["en", "pt-BR"]


async def test_get_course_languages_partial_lessons_not_available() -> None:
    # Two-lesson course with only one lesson translated → NOT available.
    course = _course()
    course.lessons.append(
        new_lesson(course_id=course.id, title="More", lesson_type="text", text_body="x")
    )
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(languages=["pt-BR"], lesson_counts={"pt-BR": 1}),
    )
    assert await uc.execute("alg") == ["en"]


async def test_get_course_languages_quiz_untranslated_not_available() -> None:
    # Regression (the prod bug): a course with all LESSONS translated but its
    # QUIZ questions still in English must NOT report the language available --
    # otherwise the UI shows a green "translated" badge while quizzes stay
    # English. Course translated before quiz support hits exactly this.
    course = _course()  # one lesson
    lesson_id = course.lessons[0].id
    quiz_repo = FakeQuizRepo(questions_by_lesson={lesson_id: 2})  # 2 quiz questions
    not_done = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=quiz_repo,
        translation_repo=FakeTranslationRepo(
            languages=["pt-BR"], lesson_counts={"pt-BR": 1}, question_counts={}
        ),
    )
    assert await not_done.execute("alg") == ["en"]  # quizzes missing → not available

    done = GetCourseLanguages(
        course_repo=FakeCourseRepo(course),
        quiz_repo=quiz_repo,
        translation_repo=FakeTranslationRepo(
            languages=["pt-BR"], lesson_counts={"pt-BR": 1}, question_counts={"pt-BR": 2}
        ),
    )
    assert await done.execute("alg") == ["en", "pt-BR"]  # lessons + quizzes → available


async def test_get_course_languages_unknown_slug_raises() -> None:
    uc = GetCourseLanguages(
        course_repo=FakeCourseRepo(),
        quiz_repo=FakeQuizRepo(),
        translation_repo=FakeTranslationRepo(),
    )
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

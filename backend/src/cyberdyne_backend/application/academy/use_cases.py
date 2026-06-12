"""Per-course translation use cases (admin-facing).

Lets an editor see which languages a course is available in and translate a
single course on demand — including hand-authored (non-seed) courses. Reuses
the same :class:`TranslateAcademy` pipeline as the bulk seed job.
"""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.application.academy.translation import (
    MarkdownAwareTranslator,
    TranslateAcademy,
    TranslationRepository,
    TranslationStats,
)
from cyberdyne_backend.domain.courses import CourseRepository
from cyberdyne_backend.domain.quizzes import QuizNotFoundError, QuizRepository


@dataclass(slots=True)
class GetCourseLanguages:
    """Languages a course is available in — always ``en`` (the base) plus any
    non-English language that has a course translation row."""

    course_repo: CourseRepository
    translation_repo: TranslationRepository

    async def execute(self, slug: str) -> list[str]:
        # Raises CourseNotFoundError if the slug is unknown (router → 404).
        course = await self.course_repo.get_by_slug(slug, include_drafts=True)
        extra = await self.translation_repo.course_languages(course.id)
        return ["en", *sorted(lang for lang in extra if lang != "en")]


@dataclass(slots=True)
class TranslateCourse:
    """Translate one course (title/description, lessons, and its quizzes) into
    a target language. Idempotent: unchanged content is skipped by source
    hash, so a re-run only fills gaps."""

    course_repo: CourseRepository
    quiz_repo: QuizRepository
    translation_repo: TranslationRepository
    translator: MarkdownAwareTranslator

    async def execute(self, slug: str, language: str) -> TranslationStats:
        course = await self.course_repo.get_by_slug(slug, include_drafts=True)
        quizzes = []
        for lesson in course.lessons:
            try:
                quizzes.append(await self.quiz_repo.get_by_lesson(lesson.id))
            except QuizNotFoundError:
                continue
        orchestrator = TranslateAcademy(translator=self.translator, repo=self.translation_repo)
        return await orchestrator.run(courses=[course], quizzes=quizzes, languages=[language])


__all__ = ["GetCourseLanguages", "TranslateCourse"]

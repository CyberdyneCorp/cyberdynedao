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
    """Languages a course is *fully* available in — always ``en`` (the base)
    plus any non-English language whose course translation row exists AND
    which has a translation row for every lesson AND every quiz question in
    the course.

    Reporting a language as available off the course-level row (or lessons
    alone) is misleading: a course translated before quiz support, or by a
    job interrupted mid-run, leaves the lessons translated but the quiz
    questions still in English. A language counts only when the whole course
    (title/description + every lesson + every quiz question) is translated."""

    course_repo: CourseRepository
    quiz_repo: QuizRepository
    translation_repo: TranslationRepository

    async def execute(self, slug: str) -> list[str]:
        # Raises CourseNotFoundError if the slug is unknown (router → 404).
        course = await self.course_repo.get_by_slug(slug, include_drafts=True)
        course_langs = {
            lang for lang in await self.translation_repo.course_languages(course.id) if lang != "en"
        }
        total_lessons = len(course.lessons)
        total_questions = 0
        for lesson in course.lessons:
            try:
                quiz = await self.quiz_repo.get_by_lesson(lesson.id)
            except QuizNotFoundError:
                continue
            total_questions += len(quiz.questions)
        lesson_counts = await self.translation_repo.translated_lesson_counts(course.id)
        question_counts = await self.translation_repo.translated_question_counts(course.id)
        available = [
            lang
            for lang in course_langs
            if lesson_counts.get(lang, 0) >= total_lessons
            and question_counts.get(lang, 0) >= total_questions
        ]
        return ["en", *sorted(available)]


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

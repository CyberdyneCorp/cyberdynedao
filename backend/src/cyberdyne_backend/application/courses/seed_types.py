"""Shared data types for the Academy course seed (kept here so the content
modules — ``seed`` and ``seed_languages`` — can import them without a cycle)."""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_PASSING_SCORE = 70


@dataclass(frozen=True, slots=True)
class SeedQuizOption:
    text: str
    is_correct: bool = False


@dataclass(frozen=True, slots=True)
class SeedQuizQuestion:
    prompt: str
    options: tuple[SeedQuizOption, ...]
    explanation: str = ""


@dataclass(frozen=True, slots=True)
class SeedLesson:
    title: str
    lesson_type: str  # 'text' | 'code' | 'quiz' | …
    text_body: str | None = None
    duration: str | None = None
    # For a ``quiz`` lesson: the curated questions to author against it. The
    # seed creates the lesson, then upserts this quiz once lesson ids are
    # stable (see ``seed.seed_courses``). Empty → the quiz lesson is created
    # but left for hand-authoring (legacy behaviour).
    quiz: tuple[SeedQuizQuestion, ...] = ()
    passing_score: int = DEFAULT_PASSING_SCORE


@dataclass(frozen=True, slots=True)
class SeedCourse:
    slug: str
    title: str
    description: str
    level: str
    lessons: tuple[SeedLesson, ...] = field(default_factory=tuple)


def quiz_lesson(
    title: str,
    questions: tuple[SeedQuizQuestion, ...],
    *,
    passing_score: int = DEFAULT_PASSING_SCORE,
    duration: str = "2 min",
) -> SeedLesson:
    """A ``quiz`` lesson carrying its curated questions."""
    return SeedLesson(
        title=title,
        lesson_type="quiz",
        duration=duration,
        quiz=questions,
        passing_score=passing_score,
    )


def q(prompt: str, options: tuple[SeedQuizOption, ...], explanation: str = "") -> SeedQuizQuestion:
    """Terse constructor for a quiz question."""
    return SeedQuizQuestion(prompt=prompt, options=options, explanation=explanation)


def opt(text: str, *, correct: bool = False) -> SeedQuizOption:
    return SeedQuizOption(text=text, is_correct=correct)


def with_checkpoint_quizzes(
    lessons: tuple[SeedLesson, ...],
    quizzes: dict[str, tuple[SeedQuizQuestion, ...]],
    *,
    prefix: str = "Quiz:",
) -> tuple[SeedLesson, ...]:
    """Interleave a checkpoint ``quiz`` lesson after each content lesson whose
    title is a key in ``quizzes``. Existing ``quiz`` lessons (e.g. a final
    'Check your knowledge') are passed through untouched. Quiz lesson titles
    are ``"{prefix} {lesson title}"`` so they're stable keys for the
    title-matched seed reconciliation."""
    out: list[SeedLesson] = []
    for lesson in lessons:
        out.append(lesson)
        questions = quizzes.get(lesson.title)
        if lesson.lesson_type in ("text", "code") and questions:
            out.append(quiz_lesson(f"{prefix} {lesson.title}", questions))
    return tuple(out)


__all__ = [
    "DEFAULT_PASSING_SCORE",
    "SeedCourse",
    "SeedLesson",
    "SeedQuizOption",
    "SeedQuizQuestion",
    "opt",
    "q",
    "quiz_lesson",
    "with_checkpoint_quizzes",
]

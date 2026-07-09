"""Shared data types for the Academy course seed (kept here so the content
modules — ``seed`` and ``seed_languages`` — can import them without a cycle)."""

from __future__ import annotations

from dataclasses import dataclass, field, replace

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
    lesson_type: str  # 'text' | 'code' | 'quiz' | 'video' | …
    text_body: str | None = None
    # For URL-backed lessons ('video' | 'pdf' | 'presentation'): the external
    # asset (e.g. a YouTube link). The domain invariant requires it for those
    # types and forbids a text_body.
    content_url: str | None = None
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


def video_lesson(
    title: str, url: str, *, duration: str | None = None, body: str | None = None
) -> SeedLesson:
    """A ``video`` lesson backed by an external URL (e.g. YouTube), with an
    optional markdown companion body rendered below the player."""
    return SeedLesson(
        title=title, lesson_type="video", content_url=url, text_body=body, duration=duration
    )


def q(prompt: str, options: tuple[SeedQuizOption, ...], explanation: str = "") -> SeedQuizQuestion:
    """Terse constructor for a quiz question."""
    return SeedQuizQuestion(prompt=prompt, options=options, explanation=explanation)


def opt(text: str, *, correct: bool = False) -> SeedQuizOption:
    return SeedQuizOption(text=text, is_correct=correct)


@dataclass(frozen=True, slots=True)
class CourseQuiz:
    """The full quiz spec for one course: a checkpoint quiz after each named
    content lesson (``per_lesson`` keyed by exact lesson title) plus a final
    comprehensive quiz (``final``)."""

    per_lesson: dict[str, tuple[SeedQuizQuestion, ...]] = field(default_factory=dict)
    final: tuple[SeedQuizQuestion, ...] = ()


def apply_quiz_spec(course: SeedCourse, spec: CourseQuiz) -> SeedCourse:
    """Return a copy of ``course`` with a checkpoint quiz interleaved after each
    content lesson named in ``spec.per_lesson``, and the final 'Check your
    knowledge' quiz authored from ``spec.final`` (appended if the course has no
    final quiz lesson yet). Used to attach the registry's quizzes at assembly
    time without editing each track's course module."""
    out: list[SeedLesson] = []
    final_placed = False
    for lesson in course.lessons:
        is_final = (
            lesson.lesson_type == "quiz" and lesson.title.casefold() == "check your knowledge"
        )
        if is_final and spec.final:
            out.append(quiz_lesson(lesson.title, spec.final, duration=lesson.duration or "3 min"))
            final_placed = True
            continue
        out.append(lesson)
        if lesson.lesson_type in ("text", "code"):
            questions = spec.per_lesson.get(lesson.title)
            if questions:
                out.append(quiz_lesson(f"Quiz: {lesson.title}", questions))
    if spec.final and not final_placed:
        out.append(quiz_lesson("Check your knowledge", spec.final))
    return replace(course, lessons=tuple(out))


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
    "CourseQuiz",
    "SeedCourse",
    "SeedLesson",
    "SeedQuizOption",
    "SeedQuizQuestion",
    "apply_quiz_spec",
    "opt",
    "q",
    "quiz_lesson",
    "video_lesson",
    "with_checkpoint_quizzes",
]

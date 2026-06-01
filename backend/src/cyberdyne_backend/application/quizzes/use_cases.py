"""Use cases for the quizzes context.

Admin authoring (upsert / delete the lesson's quiz) plus the learner
player loop: fetch the quiz, submit an attempt (graded server-side,
attempt number assigned), and list past attempts. Grading lives in the
domain; these use cases orchestrate persistence around it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from cyberdyne_backend.domain.quizzes import (
    DEFAULT_PASSING_SCORE,
    GradedAttempt,
    Question,
    Quiz,
    QuizAttempt,
    QuizRepository,
    build_question,
    grade,
    new_attempt,
    new_quiz,
)

# ── Reads ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class GetQuiz:
    """Load a lesson's quiz. The router decides whether to strip answers
    (player) or include them (editor) — both call this."""

    repo: QuizRepository

    async def execute(self, lesson_id: UUID) -> Quiz:
        return await self.repo.get_by_lesson(lesson_id)


@dataclass(slots=True)
class ListMyAttempts:
    repo: QuizRepository

    async def execute(self, *, user_id: UUID, lesson_id: UUID) -> list[QuizAttempt]:
        quiz = await self.repo.get_by_lesson(lesson_id)
        return await self.repo.list_attempts(user_id=user_id, quiz_id=quiz.id)


# ── Admin authoring ───────────────────────────────────────────────────


@dataclass(slots=True)
class OptionInput:
    text: str
    is_correct: bool


@dataclass(slots=True)
class QuestionInput:
    prompt: str
    explanation: str
    options: list[OptionInput]


@dataclass(slots=True)
class UpsertQuizCommand:
    questions: list[QuestionInput]
    passing_score: int = DEFAULT_PASSING_SCORE


@dataclass(slots=True)
class UpsertQuiz:
    """Create or fully replace the quiz attached to a lesson."""

    repo: QuizRepository

    async def execute(self, lesson_id: UUID, cmd: UpsertQuizCommand) -> Quiz:
        questions: list[Question] = [
            build_question(
                prompt=q.prompt,
                explanation=q.explanation,
                options=[(o.text, o.is_correct) for o in q.options],
                sort_order=i,
            )
            for i, q in enumerate(cmd.questions)
        ]
        quiz = new_quiz(
            lesson_id=lesson_id,
            questions=questions,
            passing_score=cmd.passing_score,
        )
        await self.repo.upsert(quiz)
        return quiz


@dataclass(slots=True)
class DeleteQuiz:
    repo: QuizRepository

    async def execute(self, lesson_id: UUID) -> None:
        # Surface QuizNotFoundError if absent so the router can 404.
        await self.repo.get_by_lesson(lesson_id)
        await self.repo.delete_by_lesson(lesson_id)


# ── Player ────────────────────────────────────────────────────────────


@dataclass(slots=True)
class SubmittedAttempt:
    attempt: QuizAttempt
    graded: GradedAttempt


@dataclass(slots=True)
class SubmitQuizAttempt:
    """Grade a learner's answers, persist the attempt with the next
    monotonic attempt number, and return both the stored attempt and the
    per-question feedback. Retries are unrestricted — each submission is
    a fresh attempt."""

    repo: QuizRepository
    # Reserved for a future per-quiz attempt cap; unlimited today.
    max_attempts: int | None = field(default=None)

    async def execute(
        self,
        *,
        user_id: UUID,
        lesson_id: UUID,
        answers: dict[UUID, UUID],
    ) -> SubmittedAttempt:
        quiz = await self.repo.get_by_lesson(lesson_id)
        graded = grade(quiz, answers)
        prior = await self.repo.count_attempts(user_id=user_id, quiz_id=quiz.id)
        attempt = new_attempt(
            user_id=user_id,
            quiz=quiz,
            graded=graded,
            answers=answers,
            attempt_number=prior + 1,
        )
        stored = await self.repo.add_attempt(attempt)
        return SubmittedAttempt(attempt=stored, graded=graded)


__all__ = [
    "DeleteQuiz",
    "GetQuiz",
    "ListMyAttempts",
    "OptionInput",
    "QuestionInput",
    "SubmitQuizAttempt",
    "SubmittedAttempt",
    "UpsertQuiz",
    "UpsertQuizCommand",
]

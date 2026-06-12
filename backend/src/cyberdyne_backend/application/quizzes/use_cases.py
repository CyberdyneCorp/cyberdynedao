"""Use cases for the quizzes context.

Admin authoring (upsert / delete the lesson's quiz) plus the learner
player loop: fetch the quiz, submit an attempt (graded server-side,
attempt number assigned), and list past attempts. Grading lives in the
domain; these use cases orchestrate persistence around it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import ChatLLMPort, ChatMessage, ChatRole
from cyberdyne_backend.domain.quizzes import (
    DEFAULT_PASSING_SCORE,
    GradedAttempt,
    LessonCompleter,
    Question,
    QuestionResult,
    Quiz,
    QuizAttempt,
    QuizRepository,
    build_question,
    grade,
    new_attempt,
    new_quiz,
)

# Tutor persona for AI contextual feedback. Deliberately constrained:
# explain, don't quiz; encouraging; no AI self-reference.
_TUTOR_SYSTEM_PROMPT = (
    "You are a patient tutor for Cyberdyne Academy. A learner answered a quiz question "
    "incorrectly. In 2-3 sentences, kindly explain why their choice is wrong and why the "
    "correct answer is right, building on the provided note. Do not ask questions and do not "
    "mention that you are an AI."
)

# Human-readable language names so the tutor can reply in the learner's
# language. Unknown / English locales add no instruction (English default).
_LANGUAGE_NAMES = {
    "pt-BR": "Brazilian Portuguese",
    "es": "Spanish",
    "fr": "French",
}


def _tutor_prompt_for(locale: str) -> str:
    name = _LANGUAGE_NAMES.get(locale)
    if name is None:
        return _TUTOR_SYSTEM_PROMPT
    return f"{_TUTOR_SYSTEM_PROMPT} Respond in {name}."

# ── Reads ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class GetQuiz:
    """Load a lesson's quiz. The router decides whether to strip answers
    (player) or include them (editor) — both call this."""

    repo: QuizRepository

    async def execute(self, lesson_id: UUID, *, locale: str = "en") -> Quiz:
        return await self.repo.get_by_lesson(lesson_id, locale=locale)


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
    # Optional seam: when set, a passing attempt auto-completes the
    # quiz's lesson in the course-progress context. None keeps quizzes
    # self-contained (e.g. quizzes not attached to a course).
    lesson_completer: LessonCompleter | None = field(default=None)

    async def execute(
        self,
        *,
        user_id: UUID,
        lesson_id: UUID,
        answers: dict[UUID, UUID],
        locale: str = "en",
    ) -> SubmittedAttempt:
        quiz = await self.repo.get_by_lesson(lesson_id, locale=locale)
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
        if graded.passed and self.lesson_completer is not None:
            await self.lesson_completer.complete_lesson(user_id=user_id, lesson_id=lesson_id)
        return SubmittedAttempt(attempt=stored, graded=graded)


@dataclass(slots=True)
class AnswerFeedback:
    question_id: UUID
    prompt: str
    is_correct: bool
    selected_option_id: UUID | None
    correct_option_id: UUID
    static_explanation: str
    ai_explanation: str | None  # populated only for incorrect answers


@dataclass(slots=True)
class ExplainQuizAnswers:
    """AI contextual feedback. Grades the learner's answers (post-
    submission, so the answer key is fair game) and, for each WRONG
    question, asks the LLM for a personalized 'why it's wrong' on top of
    the question's static explanation. Correct answers get no LLM call."""

    repo: QuizRepository
    llm: ChatLLMPort

    async def execute(
        self, *, lesson_id: UUID, answers: dict[UUID, UUID], locale: str = "en"
    ) -> list[AnswerFeedback]:
        quiz = await self.repo.get_by_lesson(lesson_id, locale=locale)
        graded = grade(quiz, answers, strict=False)
        questions = {q.id: q for q in quiz.questions}
        feedback: list[AnswerFeedback] = []
        for result in graded.results:
            question = questions[result.question_id]
            ai_explanation: str | None = None
            if not result.is_correct:
                ai_explanation = await self._explain(question, result, locale=locale)
            feedback.append(
                AnswerFeedback(
                    question_id=question.id,
                    prompt=question.prompt,
                    is_correct=result.is_correct,
                    selected_option_id=result.selected_option_id,
                    correct_option_id=result.correct_option_id,
                    static_explanation=question.explanation,
                    ai_explanation=ai_explanation,
                )
            )
        return feedback

    async def _explain(
        self, question: Question, result: QuestionResult, *, locale: str = "en"
    ) -> str:
        option_text = {o.id: o.text for o in question.options}
        chosen = (
            option_text.get(result.selected_option_id, "(no answer)")
            if result.selected_option_id
            else "(no answer)"
        )
        correct = option_text.get(result.correct_option_id, "")
        prompt = (
            f"Question: {question.prompt}\n"
            f"Learner chose: {chosen}\n"
            f"Correct answer: {correct}\n"
            f"Note: {question.explanation or '(none)'}\n"
            "Explain why the learner's choice is wrong and the correct answer is right."
        )
        message = ChatMessage(
            id=uuid.uuid4(),
            session_id=uuid.uuid4(),
            role=ChatRole.USER,
            content=prompt,
        )
        response = await self.llm.complete(
            messages=[message], tools=[], system_prompt=_tutor_prompt_for(locale)
        )
        return response.content


__all__ = [
    "AnswerFeedback",
    "DeleteQuiz",
    "ExplainQuizAnswers",
    "GetQuiz",
    "ListMyAttempts",
    "OptionInput",
    "QuestionInput",
    "SubmitQuizAttempt",
    "SubmittedAttempt",
    "UpsertQuiz",
    "UpsertQuizCommand",
]

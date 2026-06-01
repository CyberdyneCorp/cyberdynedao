"""Use-case tests for the quizzes context, with a fake repo."""

from __future__ import annotations

import uuid
from uuid import UUID

import pytest

from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    GetQuiz,
    ListMyAttempts,
    OptionInput,
    QuestionInput,
    SubmitQuizAttempt,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.domain.quizzes import (
    InvalidQuizError,
    Quiz,
    QuizAttempt,
    QuizNotFoundError,
    QuizRepository,
)


class FakeQuizRepo:
    def __init__(self) -> None:
        self._by_lesson: dict[UUID, Quiz] = {}
        self._attempts: list[QuizAttempt] = []

    async def get_by_lesson(self, lesson_id: UUID) -> Quiz:
        quiz = self._by_lesson.get(lesson_id)
        if quiz is None:
            raise QuizNotFoundError(str(lesson_id))
        return quiz

    async def upsert(self, quiz: Quiz) -> None:
        self._by_lesson[quiz.lesson_id] = quiz

    async def delete_by_lesson(self, lesson_id: UUID) -> None:
        self._by_lesson.pop(lesson_id, None)
        self._attempts = [a for a in self._attempts if a.lesson_id != lesson_id]

    async def add_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        self._attempts.append(attempt)
        return attempt

    async def list_attempts(self, *, user_id: UUID, quiz_id: UUID) -> list[QuizAttempt]:
        return [a for a in self._attempts if a.user_id == user_id and a.quiz_id == quiz_id]

    async def count_attempts(self, *, user_id: UUID, quiz_id: UUID) -> int:
        return len(await self.list_attempts(user_id=user_id, quiz_id=quiz_id))


def test_fake_repo_matches_port() -> None:
    assert isinstance(FakeQuizRepo(), QuizRepository)


def _cmd() -> UpsertQuizCommand:
    return UpsertQuizCommand(
        passing_score=70,
        questions=[
            QuestionInput(
                prompt="2+2?",
                explanation="basic arithmetic",
                options=[
                    OptionInput(text="3", is_correct=False),
                    OptionInput(text="4", is_correct=True),
                ],
            ),
            QuestionInput(
                prompt="Sky colour?",
                explanation="rayleigh scattering",
                options=[
                    OptionInput(text="blue", is_correct=True),
                    OptionInput(text="green", is_correct=False),
                ],
            ),
        ],
    )


class TestUpsertQuiz:
    async def test_creates_quiz(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        quiz = await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        assert quiz.lesson_id == lesson_id
        assert len(quiz.questions) == 2

    async def test_invalid_quiz_propagates(self) -> None:
        repo = FakeQuizRepo()
        bad = UpsertQuizCommand(
            questions=[
                QuestionInput(
                    prompt="q",
                    explanation="",
                    options=[
                        OptionInput(text="a", is_correct=True),
                        OptionInput(text="b", is_correct=True),
                    ],
                )
            ]
        )
        with pytest.raises(InvalidQuizError):
            await UpsertQuiz(repo=repo).execute(uuid.uuid4(), bad)


class TestSubmitAndAttempts:
    async def test_attempt_numbers_increment(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        user_id = uuid.uuid4()
        submit = SubmitQuizAttempt(repo=repo)

        first = await submit.execute(user_id=user_id, lesson_id=lesson_id, answers={})
        second = await submit.execute(user_id=user_id, lesson_id=lesson_id, answers={})
        assert first.attempt.attempt_number == 1
        assert second.attempt.attempt_number == 2

    async def test_correct_answers_pass(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        quiz = await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        answers = {q.id: q.correct_option_id for q in quiz.questions}
        result = await SubmitQuizAttempt(repo=repo).execute(
            user_id=uuid.uuid4(), lesson_id=lesson_id, answers=answers
        )
        assert result.graded.score == 100
        assert result.graded.passed is True

    async def test_submit_unknown_quiz_raises(self) -> None:
        with pytest.raises(QuizNotFoundError):
            await SubmitQuizAttempt(repo=FakeQuizRepo()).execute(
                user_id=uuid.uuid4(), lesson_id=uuid.uuid4(), answers={}
            )

    async def test_list_my_attempts(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        user_id = uuid.uuid4()
        await SubmitQuizAttempt(repo=repo).execute(user_id=user_id, lesson_id=lesson_id, answers={})
        attempts = await ListMyAttempts(repo=repo).execute(user_id=user_id, lesson_id=lesson_id)
        assert len(attempts) == 1


class TestGetAndDelete:
    async def test_get_quiz(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        quiz = await GetQuiz(repo=repo).execute(lesson_id)
        assert quiz.lesson_id == lesson_id

    async def test_delete_quiz(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        await DeleteQuiz(repo=repo).execute(lesson_id)
        with pytest.raises(QuizNotFoundError):
            await GetQuiz(repo=repo).execute(lesson_id)

    async def test_delete_missing_raises(self) -> None:
        with pytest.raises(QuizNotFoundError):
            await DeleteQuiz(repo=FakeQuizRepo()).execute(uuid.uuid4())

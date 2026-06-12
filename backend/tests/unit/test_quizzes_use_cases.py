"""Use-case tests for the quizzes context, with a fake repo."""

from __future__ import annotations

import uuid
from uuid import UUID

import pytest

from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    ExplainQuizAnswers,
    GetQuiz,
    ListMyAttempts,
    OptionInput,
    QuestionInput,
    SubmitQuizAttempt,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.domain.ai_chat import ChatMessage, LLMResponse, ToolSchema
from cyberdyne_backend.domain.quizzes import (
    InvalidQuizError,
    Quiz,
    QuizAttempt,
    QuizNotFoundError,
    QuizRepository,
)


class ScriptedLLM:
    """Records each prompt it sees and returns a canned tutor reply."""

    def __init__(self) -> None:
        self.prompts: list[str] = []
        self.system_prompts: list[str] = []

    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse:
        self.prompts.append(messages[-1].content)
        self.system_prompts.append(system_prompt)
        return LLMResponse(
            content="You confused the two options; the right one is correct because X."
        )


class FakeQuizRepo:
    def __init__(self) -> None:
        self._by_lesson: dict[UUID, Quiz] = {}
        self._attempts: list[QuizAttempt] = []

    async def get_by_lesson(self, lesson_id: UUID, *, locale: str = "en") -> Quiz:
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


class _RecordingCompleter:
    """Records (user_id, lesson_id) for each completion call."""

    def __init__(self) -> None:
        self.completed: list[tuple[UUID, UUID]] = []

    async def complete_lesson(self, *, user_id: UUID, lesson_id: UUID) -> None:
        self.completed.append((user_id, lesson_id))


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

    async def test_passing_attempt_completes_lesson(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        quiz = await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        completer = _RecordingCompleter()
        user_id = uuid.uuid4()
        answers = {q.id: q.correct_option_id for q in quiz.questions}
        await SubmitQuizAttempt(repo=repo, lesson_completer=completer).execute(
            user_id=user_id, lesson_id=lesson_id, answers=answers
        )
        assert completer.completed == [(user_id, lesson_id)]

    async def test_failing_attempt_does_not_complete_lesson(self) -> None:
        repo = FakeQuizRepo()
        lesson_id = uuid.uuid4()
        await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        completer = _RecordingCompleter()
        # Empty answers -> score 0 -> fail -> no completion.
        await SubmitQuizAttempt(repo=repo, lesson_completer=completer).execute(
            user_id=uuid.uuid4(), lesson_id=lesson_id, answers={}
        )
        assert completer.completed == []


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


class TestExplainQuizAnswers:
    async def _seed(self, repo: FakeQuizRepo) -> tuple[UUID, Quiz]:
        lesson_id = uuid.uuid4()
        quiz = await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())
        return lesson_id, quiz

    def _wrong_option(self, quiz: Quiz, question_index: int) -> UUID:
        question = quiz.questions[question_index]
        return next(o.id for o in question.options if o.id != question.correct_option_id)

    async def test_ai_explanation_only_for_wrong_answers(self) -> None:
        repo = FakeQuizRepo()
        lesson_id, quiz = await self._seed(repo)
        llm = ScriptedLLM()
        # Q0 wrong, Q1 correct.
        answers = {
            quiz.questions[0].id: self._wrong_option(quiz, 0),
            quiz.questions[1].id: quiz.questions[1].correct_option_id,
        }
        feedback = await ExplainQuizAnswers(repo=repo, llm=llm).execute(
            lesson_id=lesson_id, answers=answers
        )
        assert len(feedback) == 2
        wrong, right = feedback[0], feedback[1]
        assert wrong.is_correct is False
        assert wrong.ai_explanation is not None
        assert wrong.static_explanation == "basic arithmetic"
        assert right.is_correct is True
        assert right.ai_explanation is None
        # The LLM was consulted exactly once — only for the wrong answer.
        assert len(llm.prompts) == 1
        assert llm.system_prompts[0].startswith("You are a patient tutor")

    async def test_prompt_carries_chosen_and_correct_text(self) -> None:
        repo = FakeQuizRepo()
        lesson_id, quiz = await self._seed(repo)
        llm = ScriptedLLM()
        answers = {quiz.questions[0].id: self._wrong_option(quiz, 0)}
        await ExplainQuizAnswers(repo=repo, llm=llm).execute(lesson_id=lesson_id, answers=answers)
        prompt = llm.prompts[0]
        assert "2+2?" in prompt
        assert "Learner chose: 3" in prompt
        assert "Correct answer: 4" in prompt

    async def test_unanswered_question_reports_no_answer(self) -> None:
        repo = FakeQuizRepo()
        lesson_id, quiz = await self._seed(repo)
        llm = ScriptedLLM()
        # Empty answers → every question wrong, none selected.
        feedback = await ExplainQuizAnswers(repo=repo, llm=llm).execute(
            lesson_id=lesson_id, answers={}
        )
        assert all(f.is_correct is False for f in feedback)
        assert all(f.selected_option_id is None for f in feedback)
        assert "Learner chose: (no answer)" in llm.prompts[0]
        assert len(llm.prompts) == len(quiz.questions)

    async def test_unknown_quiz_raises(self) -> None:
        with pytest.raises(QuizNotFoundError):
            await ExplainQuizAnswers(repo=FakeQuizRepo(), llm=ScriptedLLM()).execute(
                lesson_id=uuid.uuid4(), answers={}
            )

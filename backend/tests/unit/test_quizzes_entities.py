"""Domain tests for the quizzes context — invariants + grading."""

from __future__ import annotations

import uuid

import pytest

from cyberdyne_backend.domain.quizzes import (
    DEFAULT_PASSING_SCORE,
    InvalidAttemptError,
    InvalidQuizError,
    build_question,
    grade,
    new_attempt,
    new_quiz,
)


def _q(prompt: str, options: list[tuple[str, bool]], explanation: str = "because") -> object:
    return build_question(prompt=prompt, explanation=explanation, options=options)


def _simple_quiz(passing_score: int = DEFAULT_PASSING_SCORE):  # type: ignore[no-untyped-def]
    return new_quiz(
        lesson_id=uuid.uuid4(),
        passing_score=passing_score,
        questions=[
            _q("2+2?", [("3", False), ("4", True), ("5", False)]),
            _q("Sky?", [("Blue", True), ("Green", False)]),
        ],
    )


class TestQuizInvariants:
    def test_default_passing_score(self) -> None:
        quiz = _simple_quiz()
        assert quiz.passing_score == 70

    def test_too_many_questions_raises(self) -> None:
        qs = [_q(f"q{i}", [("a", True), ("b", False)]) for i in range(16)]
        with pytest.raises(InvalidQuizError, match="questions"):
            new_quiz(lesson_id=uuid.uuid4(), questions=qs)

    def test_zero_questions_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="questions"):
            new_quiz(lesson_id=uuid.uuid4(), questions=[])

    def test_too_few_options_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="options"):
            new_quiz(lesson_id=uuid.uuid4(), questions=[_q("q", [("only", True)])])

    def test_too_many_options_raises(self) -> None:
        opts = [(f"o{i}", i == 0) for i in range(7)]
        with pytest.raises(InvalidQuizError, match="options"):
            new_quiz(lesson_id=uuid.uuid4(), questions=[_q("q", opts)])

    def test_no_correct_option_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="exactly one correct"):
            new_quiz(
                lesson_id=uuid.uuid4(),
                questions=[_q("q", [("a", False), ("b", False)])],
            )

    def test_multiple_correct_options_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="exactly one correct"):
            new_quiz(
                lesson_id=uuid.uuid4(),
                questions=[_q("q", [("a", True), ("b", True)])],
            )

    def test_passing_score_out_of_range_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="passing_score"):
            _simple_quiz(passing_score=0)

    def test_empty_prompt_raises(self) -> None:
        with pytest.raises(InvalidQuizError, match="prompt"):
            build_question(prompt="  ", explanation="", options=[("a", True), ("b", False)])


class TestGrading:
    def test_all_correct_passes(self) -> None:
        quiz = _simple_quiz()
        answers = {q.id: q.correct_option_id for q in quiz.questions}
        result = grade(quiz, answers)
        assert result.score == 100
        assert result.passed is True
        assert all(r.is_correct for r in result.results)

    def test_half_correct_below_threshold_fails(self) -> None:
        quiz = _simple_quiz()
        # Answer only the first correctly → 50% < 70%.
        answers = {quiz.questions[0].id: quiz.questions[0].correct_option_id}
        result = grade(quiz, answers)
        assert result.score == 50
        assert result.passed is False

    def test_feedback_carries_explanation_and_correct_id(self) -> None:
        quiz = _simple_quiz()
        result = grade(quiz, {})
        first = result.results[0]
        assert first.explanation == "because"
        assert first.correct_option_id == quiz.questions[0].correct_option_id
        assert first.selected_option_id is None
        assert first.is_correct is False

    def test_unknown_question_strict_raises(self) -> None:
        quiz = _simple_quiz()
        with pytest.raises(InvalidAttemptError, match="unknown question"):
            grade(quiz, {uuid.uuid4(): uuid.uuid4()})

    def test_option_not_belonging_strict_raises(self) -> None:
        quiz = _simple_quiz()
        with pytest.raises(InvalidAttemptError, match="does not belong"):
            grade(quiz, {quiz.questions[0].id: uuid.uuid4()})

    def test_non_strict_ignores_unknowns(self) -> None:
        quiz = _simple_quiz()
        result = grade(quiz, {uuid.uuid4(): uuid.uuid4()}, strict=False)
        assert result.score == 0


class TestNewAttempt:
    def test_serialises_answers_to_strings(self) -> None:
        quiz = _simple_quiz()
        answers = {q.id: q.correct_option_id for q in quiz.questions}
        graded = grade(quiz, answers)
        attempt = new_attempt(
            user_id=uuid.uuid4(),
            quiz=quiz,
            graded=graded,
            answers=answers,
            attempt_number=3,
        )
        assert attempt.attempt_number == 3
        assert attempt.passed is True
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in attempt.answers.items())

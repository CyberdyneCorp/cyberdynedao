"""Domain errors for the quizzes context."""

from __future__ import annotations


class QuizNotFoundError(LookupError):
    """No quiz exists for the requested lesson."""


class InvalidQuizError(ValueError):
    """The quiz violates a structural invariant — question count out of
    range, option count out of range, or a question without exactly one
    correct option."""


class InvalidAttemptError(ValueError):
    """A submitted attempt references unknown questions/options or omits
    answers the quiz requires."""

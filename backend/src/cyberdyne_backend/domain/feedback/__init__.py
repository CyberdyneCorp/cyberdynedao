"""Learner-feedback bounded context.

A general feedback channel — problem reports and feature requests — open to
all signed-in learners (issue #233).
"""

from cyberdyne_backend.domain.feedback.entities import (
    Feedback,
    FeedbackKind,
    FeedbackStatus,
    new_feedback,
    parse_feedback_kind,
    parse_feedback_status,
)
from cyberdyne_backend.domain.feedback.errors import (
    InvalidFeedbackKindError,
    InvalidFeedbackStatusError,
)
from cyberdyne_backend.domain.feedback.ports import FeedbackRepository

__all__ = [
    "Feedback",
    "FeedbackKind",
    "FeedbackRepository",
    "FeedbackStatus",
    "InvalidFeedbackKindError",
    "InvalidFeedbackStatusError",
    "new_feedback",
    "parse_feedback_kind",
    "parse_feedback_status",
]

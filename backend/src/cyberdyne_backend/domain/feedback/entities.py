"""Entities for the learner-feedback context.

A general feedback channel for signed-in learners to report problems or
request features (issue #233). Distinct from per-quiz feedback and from the
course/topic demand registry (issue #232), which captures wanted courses.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.feedback.errors import (
    InvalidFeedbackKindError,
    InvalidFeedbackStatusError,
)


class FeedbackKind(StrEnum):
    """What a learner is sending in."""

    PROBLEM = "problem"
    FEATURE = "feature"


class FeedbackStatus(StrEnum):
    """Triage lifecycle of a feedback item."""

    NEW = "new"
    TRIAGED = "triaged"
    CLOSED = "closed"


def parse_feedback_kind(raw: str) -> FeedbackKind:
    try:
        return FeedbackKind(raw)
    except ValueError as exc:
        allowed = ", ".join(k.value for k in FeedbackKind)
        raise InvalidFeedbackKindError(
            f"unknown feedback kind {raw!r}; expected one of: {allowed}"
        ) from exc


def parse_feedback_status(raw: str) -> FeedbackStatus:
    try:
        return FeedbackStatus(raw)
    except ValueError as exc:
        allowed = ", ".join(s.value for s in FeedbackStatus)
        raise InvalidFeedbackStatusError(
            f"unknown feedback status {raw!r}; expected one of: {allowed}"
        ) from exc


@dataclass(slots=True)
class Feedback:
    """A single learner-submitted problem report or feature request.

    ``course_id``/``lesson_id`` are optional free-form references to the
    in-context item the learner was looking at; ``app_version``/``platform``
    help the team reproduce. New items start ``NEW`` and move through triage.
    """

    id: UUID
    user_id: UUID
    kind: FeedbackKind
    status: FeedbackStatus
    message: str
    course_id: str | None
    lesson_id: str | None
    app_version: str | None
    platform: str | None
    created_at: datetime
    updated_at: datetime


def new_feedback(
    *,
    user_id: UUID,
    kind: FeedbackKind,
    message: str,
    course_id: str | None = None,
    lesson_id: str | None = None,
    app_version: str | None = None,
    platform: str | None = None,
    now: datetime | None = None,
) -> Feedback:
    moment = now or datetime.now(tz=UTC)
    return Feedback(
        id=uuid.uuid4(),
        user_id=user_id,
        kind=kind,
        status=FeedbackStatus.NEW,
        message=message,
        course_id=course_id,
        lesson_id=lesson_id,
        app_version=app_version,
        platform=platform,
        created_at=moment,
        updated_at=moment,
    )

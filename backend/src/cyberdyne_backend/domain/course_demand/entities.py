"""Entities for the course/topic demand registry (issue #232).

Captures learner requests for courses/topics we don't yet offer, from two
entry points — a typed "Request a course/topic" and a Scan-to-Learn photo that
found no matching course — into one registry. Requests are clustered by a
normalized topic key so the authoring backlog shows *ranked demand* ("42
learners want eigenvalues") rather than raw rows.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.course_demand.errors import InvalidRequestSourceError


class RequestSource(StrEnum):
    """Where a course request came from."""

    TYPED = "typed"  # learner typed "Request a course/topic"
    SCAN = "scan"  # Scan-to-Learn photo found no matching course
    AGENT = "agent"  # Global Agent Chat answered an out-of-catalog topic (issue #234)


def parse_request_source(raw: str) -> RequestSource:
    try:
        return RequestSource(raw)
    except ValueError as exc:
        allowed = ", ".join(s.value for s in RequestSource)
        raise InvalidRequestSourceError(
            f"unknown request source {raw!r}; expected one of: {allowed}"
        ) from exc


_PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)
_WHITESPACE = re.compile(r"\s+")


def normalize_topic(topic: str) -> str:
    """Collapse a free-text topic to a stable clustering key: lower-cased,
    punctuation removed, whitespace collapsed. So "Linear Algebra: eigenvalues"
    and "linear algebra eigenvalues!" cluster together, and a typed request and
    a scan no-match for the same topic land in the same cluster."""
    lowered = topic.strip().lower()
    no_punct = _PUNCTUATION.sub(" ", lowered)
    return _WHITESPACE.sub(" ", no_punct).strip()


@dataclass(slots=True)
class CourseRequest:
    """A single learner request for a course/topic we don't yet offer."""

    id: UUID
    user_id: UUID
    topic: str
    topic_key: str
    subject: str | None
    source: RequestSource
    source_question_text: str | None
    course_id: str | None
    lesson_id: str | None
    created_at: datetime


@dataclass(slots=True)
class DemandCluster:
    """Aggregated demand for one normalized topic — the unit the authoring
    backlog ranks by. ``topic``/``subject`` are a representative (most recent)
    label for display; ``count`` is how many requests clustered here."""

    topic_key: str
    topic: str
    subject: str | None
    count: int
    last_requested_at: datetime


def new_course_request(
    *,
    user_id: UUID,
    topic: str,
    source: RequestSource,
    subject: str | None = None,
    source_question_text: str | None = None,
    course_id: str | None = None,
    lesson_id: str | None = None,
    now: datetime | None = None,
) -> CourseRequest:
    return CourseRequest(
        id=uuid.uuid4(),
        user_id=user_id,
        topic=topic,
        topic_key=normalize_topic(topic),
        subject=subject,
        source=source,
        source_question_text=source_question_text,
        course_id=course_id,
        lesson_id=lesson_id,
        created_at=now or datetime.now(tz=UTC),
    )

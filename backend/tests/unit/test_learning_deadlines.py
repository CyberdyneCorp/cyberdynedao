"""Tests for enrollment deadlines (domain + use cases)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from cyberdyne_backend.application.learning import GetMyDeadlines, SetEnrollmentDeadline
from cyberdyne_backend.domain.learning import (
    DeadlineStatus,
    Enrollment,
    EnrollmentNotFoundError,
    EnrollmentStatus,
    days_remaining,
    deadline_status,
)

_NOW = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


class TestDeadlineStatus:
    def test_none_when_unset(self) -> None:
        assert deadline_status(None, now=_NOW) is DeadlineStatus.NONE

    def test_overdue_in_the_past(self) -> None:
        assert deadline_status(_NOW - timedelta(hours=1), now=_NOW) is DeadlineStatus.OVERDUE

    def test_due_exactly_now_is_overdue(self) -> None:
        assert deadline_status(_NOW, now=_NOW) is DeadlineStatus.OVERDUE

    def test_urgent_within_three_days(self) -> None:
        assert deadline_status(_NOW + timedelta(days=2), now=_NOW) is DeadlineStatus.URGENT
        # Boundary: exactly 3 days is still urgent.
        assert deadline_status(_NOW + timedelta(days=3), now=_NOW) is DeadlineStatus.URGENT

    def test_upcoming_beyond_threshold(self) -> None:
        assert deadline_status(_NOW + timedelta(days=10), now=_NOW) is DeadlineStatus.UPCOMING

    def test_custom_urgent_window(self) -> None:
        assert (
            deadline_status(_NOW + timedelta(days=5), now=_NOW, urgent_within_days=7)
            is DeadlineStatus.URGENT
        )


class TestDaysRemaining:
    def test_none(self) -> None:
        assert days_remaining(None, now=_NOW) is None

    def test_rounds_up_future(self) -> None:
        assert days_remaining(_NOW + timedelta(hours=1), now=_NOW) == 1
        assert days_remaining(_NOW + timedelta(hours=25), now=_NOW) == 2

    def test_negative_when_overdue(self) -> None:
        assert days_remaining(_NOW - timedelta(hours=1), now=_NOW) == -1
        assert days_remaining(_NOW - timedelta(days=2, hours=1), now=_NOW) == -3


# ── Use cases ────────────────────────────────────────────────────────


class _FakeRepo:
    def __init__(self, enrollments: list[Enrollment] | None = None) -> None:
        self.enrollments = enrollments or []

    async def list_enrollments_for_user(self, user_id: uuid.UUID) -> list[Enrollment]:
        return [e for e in self.enrollments if e.user_id == user_id]

    async def set_enrollment_deadline(
        self, *, user_id: uuid.UUID, path_slug: str, due_at: datetime | None
    ) -> Enrollment:
        for e in self.enrollments:
            if e.user_id == user_id and e.path_slug == path_slug:
                e.due_at = due_at
                return e
        raise EnrollmentNotFoundError(path_slug)


def _enrollment(user_id: uuid.UUID, slug: str, due_at: datetime | None = None) -> Enrollment:
    return Enrollment(
        id=uuid.uuid4(),
        user_id=user_id,
        path_slug=slug,
        started_at=_NOW,
        status=EnrollmentStatus.ACTIVE,
        due_at=due_at,
    )


class TestSetEnrollmentDeadline:
    async def test_sets_due_at(self) -> None:
        user = uuid.uuid4()
        repo = _FakeRepo([_enrollment(user, "p1")])
        due = _NOW + timedelta(days=5)
        result = await SetEnrollmentDeadline(repo=repo).execute(
            user_id=user, path_slug="p1", due_at=due
        )
        assert result.due_at == due

    async def test_clears_due_at_with_none(self) -> None:
        user = uuid.uuid4()
        repo = _FakeRepo([_enrollment(user, "p1", due_at=_NOW)])
        result = await SetEnrollmentDeadline(repo=repo).execute(
            user_id=user, path_slug="p1", due_at=None
        )
        assert result.due_at is None

    async def test_missing_enrollment_raises(self) -> None:
        with pytest.raises(EnrollmentNotFoundError):
            await SetEnrollmentDeadline(repo=_FakeRepo()).execute(
                user_id=uuid.uuid4(), path_slug="ghost", due_at=None
            )


class TestGetMyDeadlines:
    async def test_computes_status_per_enrollment(self) -> None:
        user = uuid.uuid4()
        repo = _FakeRepo(
            [
                _enrollment(user, "overdue", due_at=_NOW - timedelta(days=1)),
                _enrollment(user, "urgent", due_at=_NOW + timedelta(days=1)),
                _enrollment(user, "later", due_at=_NOW + timedelta(days=30)),
                _enrollment(user, "none", due_at=None),
            ]
        )
        result = await GetMyDeadlines(repo=repo).execute(user, now=_NOW)
        by_slug = {d.path_slug: d.status for d in result}
        assert by_slug["overdue"] is DeadlineStatus.OVERDUE
        assert by_slug["urgent"] is DeadlineStatus.URGENT
        assert by_slug["later"] is DeadlineStatus.UPCOMING
        assert by_slug["none"] is DeadlineStatus.NONE

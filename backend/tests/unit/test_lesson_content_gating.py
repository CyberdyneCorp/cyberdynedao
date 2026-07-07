"""Regression: guests may read only the FIRST lesson of a course.

``GET /api/v1/courses/{slug}`` is public, so an anonymous viewer gets the
full lesson LIST — but the actual content (``text_body`` / ``content_url``)
of every lesson past the first must be withheld until they sign in. Hiding
it in the UI is not enough; the bodies must never leave the API.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Request

from cyberdyne_backend.adapters.inbound.api.courses.router import (
    _detail,
    _summary,
    _viewer_is_authenticated,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.courses.entities import (
    Course,
    CourseLevel,
    CourseStatus,
    Lesson,
    LessonType,
)

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
# Far-future deadline so the derived status is a stable "upcoming" with a
# large positive days_remaining regardless of the wall clock at test time.
_DUE_AT = datetime(2999, 1, 1, tzinfo=UTC)


def _course() -> Course:
    cid = uuid4()
    return Course(
        id=cid,
        slug="solidity-101",
        title="Solidity 101",
        description="d",
        level=CourseLevel.BEGINNER,
        status=CourseStatus.PUBLISHED,
        # Non-default org policy so the anonymous-neutralisation is observable.
        mandatory=True,
        sort_order=0,
        due_at=_DUE_AT,
        created_at=_NOW,
        published_at=_NOW,
        lessons=[
            Lesson(
                id=uuid4(),
                course_id=cid,
                title="Intro",
                lesson_type=LessonType.TEXT,
                sort_order=0,
                text_body="# first body",
            ),
            Lesson(
                id=uuid4(),
                course_id=cid,
                title="Deep dive",
                lesson_type=LessonType.TEXT,
                sort_order=1,
                text_body="# second body",
            ),
            Lesson(
                id=uuid4(),
                course_id=cid,
                title="Watch",
                lesson_type=LessonType.VIDEO,
                sort_order=2,
                content_url="https://v/abc",
            ),
        ],
    )


def test_guest_detail_keeps_only_first_lesson_body() -> None:
    detail = _detail(_course(), full_content=False)
    # Every lesson's metadata stays so the syllabus still renders.
    assert [lesson.title for lesson in detail.lessons] == ["Intro", "Deep dive", "Watch"]
    # First lesson keeps its body; the rest are stripped.
    assert detail.lessons[0].text_body == "# first body"
    assert detail.lessons[1].text_body is None
    assert detail.lessons[2].content_url is None


def test_authenticated_detail_keeps_all_bodies() -> None:
    detail = _detail(_course(), full_content=True)
    assert detail.lessons[1].text_body == "# second body"
    assert detail.lessons[2].content_url == "https://v/abc"


def test_anonymous_summary_neutralises_member_policy_fields() -> None:
    # Issue #260: the public catalogue must not leak org policy (which courses
    # are mandatory, their deadlines) to anonymous callers. Neutral values
    # equal the schema defaults, so the JSON shape is unchanged.
    summary = _summary(_course(), member_policy=False)
    assert summary.mandatory is False
    assert summary.due_at is None
    assert summary.deadline_status == "none"
    assert summary.days_remaining is None
    # Non-policy fields are untouched.
    assert summary.slug == "solidity-101"
    assert summary.lesson_count == 3


def test_authenticated_summary_exposes_member_policy_fields() -> None:
    summary = _summary(_course())  # member_policy defaults True
    assert summary.mandatory is True
    assert summary.due_at == _DUE_AT
    assert summary.deadline_status == "upcoming"
    assert summary.days_remaining is not None
    assert summary.days_remaining > 0


def test_anonymous_detail_neutralises_policy_but_keeps_all_lessons() -> None:
    detail = _detail(_course(), full_content=False, member_policy=False)
    # Policy neutralised for the guest.
    assert detail.mandatory is False
    assert detail.due_at is None
    assert detail.deadline_status == "none"
    assert detail.days_remaining is None
    # The syllabus (lesson list) is unaffected by the policy gating.
    assert [lesson.title for lesson in detail.lessons] == ["Intro", "Deep dive", "Watch"]


def test_authenticated_detail_keeps_member_policy_fields() -> None:
    detail = _detail(_course(), full_content=True, member_policy=True)
    assert detail.mandatory is True
    assert detail.due_at == _DUE_AT
    assert detail.deadline_status == "upcoming"


def _request_with(principal: object) -> Request:
    req = Request({"type": "http", "headers": []})
    req.state.principal = principal
    return req


def test_viewer_is_authenticated_distinguishes_user_from_guest() -> None:
    user = UserPrincipal(
        user_id=uuid4(),
        username="u",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )
    assert _viewer_is_authenticated(_request_with(user)) is True
    assert _viewer_is_authenticated(_request_with(None)) is False

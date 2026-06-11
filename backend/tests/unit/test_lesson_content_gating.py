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


def _course() -> Course:
    cid = uuid4()
    return Course(
        id=cid,
        slug="solidity-101",
        title="Solidity 101",
        description="d",
        level=CourseLevel.BEGINNER,
        status=CourseStatus.PUBLISHED,
        mandatory=False,
        sort_order=0,
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

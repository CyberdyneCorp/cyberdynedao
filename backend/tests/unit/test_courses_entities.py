"""Domain tests for the courses context."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.domain.courses import (
    CourseLevel,
    CourseStatus,
    InvalidCourseLevelError,
    InvalidLessonContentError,
    LessonType,
    new_course,
    new_lesson,
    normalize_slug,
    parse_level,
)


class TestNewCourse:
    def test_creates_draft_with_derived_slug(self) -> None:
        course = new_course(title="Intro to Web3", description="d", level="Beginner")
        assert course.status is CourseStatus.DRAFT
        assert course.slug == "intro-to-web3"
        assert course.level is CourseLevel.BEGINNER
        assert course.published_at is None
        assert course.mandatory is False

    def test_explicit_slug_is_normalised(self) -> None:
        course = new_course(title="x", description="d", level="Advanced", slug="My Slug!")
        assert course.slug == "my-slug"

    def test_accepts_level_enum(self) -> None:
        course = new_course(title="x", description="d", level=CourseLevel.INTERMEDIATE)
        assert course.level is CourseLevel.INTERMEDIATE

    def test_empty_title_raises(self) -> None:
        with pytest.raises(ValueError, match="title cannot be empty"):
            new_course(title="   ", description="d", level="Beginner")

    def test_slug_normalising_to_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="slug normalises to empty"):
            new_course(title="!!!", description="d", level="Beginner")

    def test_invalid_level_raises(self) -> None:
        with pytest.raises(InvalidCourseLevelError):
            new_course(title="x", description="d", level="Wizard")


class TestPublishUnpublish:
    def test_publish_sets_timestamp_and_status(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        moment = datetime(2030, 1, 1, tzinfo=UTC)
        course.publish(now=moment)
        assert course.status is CourseStatus.PUBLISHED
        assert course.published_at == moment
        assert course.is_visible_to_anonymous() is True

    def test_republish_preserves_original_published_at(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        first = datetime(2030, 1, 1, tzinfo=UTC)
        course.publish(now=first)
        course.unpublish()
        assert course.is_visible_to_anonymous() is False
        course.publish(now=datetime(2031, 1, 1, tzinfo=UTC))
        assert course.published_at == first

    def test_unpublished_draft_not_visible(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        assert course.is_visible_to_anonymous() is False


class TestNewLesson:
    def _course_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def test_text_lesson_requires_body(self) -> None:
        with pytest.raises(InvalidLessonContentError, match="text lesson"):
            new_lesson(course_id=self._course_id(), title="t", lesson_type="text")

    def test_text_lesson_with_body(self) -> None:
        lesson = new_lesson(
            course_id=self._course_id(),
            title="t",
            lesson_type="text",
            text_body="# Hello",
        )
        assert lesson.lesson_type is LessonType.TEXT
        assert lesson.text_body == "# Hello"
        assert lesson.content_url is None

    @pytest.mark.parametrize("kind", ["video", "pdf", "presentation"])
    def test_url_backed_lesson_requires_content_url(self, kind: str) -> None:
        with pytest.raises(InvalidLessonContentError, match="content_url"):
            new_lesson(course_id=self._course_id(), title="t", lesson_type=kind)

    def test_video_lesson_with_url(self) -> None:
        lesson = new_lesson(
            course_id=self._course_id(),
            title="t",
            lesson_type="video",
            content_url="https://youtu.be/abc",
            duration="10 min",
        )
        assert lesson.content_url == "https://youtu.be/abc"
        assert lesson.duration == "10 min"

    def test_quiz_lesson_needs_no_content(self) -> None:
        lesson = new_lesson(course_id=self._course_id(), title="Final quiz", lesson_type="quiz")
        assert lesson.lesson_type is LessonType.QUIZ
        assert lesson.content_url is None
        assert lesson.text_body is None

    def test_code_lesson_needs_no_content(self) -> None:
        lesson = new_lesson(course_id=self._course_id(), title="Try it", lesson_type="code")
        assert lesson.lesson_type is LessonType.CODE
        assert lesson.content_url is None

    def test_code_lesson_allows_instructions_in_text_body(self) -> None:
        lesson = new_lesson(
            course_id=self._course_id(),
            title="Plot a sine wave",
            lesson_type="code",
            text_body="% starter\nx = linspace(0, 2*pi);",
        )
        assert lesson.lesson_type is LessonType.CODE
        assert lesson.text_body is not None

    def test_empty_title_raises(self) -> None:
        with pytest.raises(ValueError, match="title cannot be empty"):
            new_lesson(course_id=self._course_id(), title=" ", lesson_type="quiz")

    def test_set_content_revalidates_invariant(self) -> None:
        lesson = new_lesson(
            course_id=self._course_id(),
            title="t",
            lesson_type="video",
            content_url="https://x",
        )
        # Blanking the URL on a video lesson must fail the invariant.
        with pytest.raises(InvalidLessonContentError):
            lesson.set_content(content_url="")

    def test_set_content_updates_fields(self) -> None:
        lesson = new_lesson(
            course_id=self._course_id(),
            title="t",
            lesson_type="text",
            text_body="old",
        )
        lesson.set_content(title="new title", text_body="new body", sort_order=5)
        assert lesson.title == "new title"
        assert lesson.text_body == "new body"
        assert lesson.sort_order == 5


def test_normalize_slug() -> None:
    assert normalize_slug("  Hello World!! ") == "hello-world"
    assert normalize_slug("a/b/c") == "a-b-c"


def test_parse_level_roundtrip() -> None:
    assert parse_level("Beginner") is CourseLevel.BEGINNER
    with pytest.raises(InvalidCourseLevelError):
        parse_level("nope")

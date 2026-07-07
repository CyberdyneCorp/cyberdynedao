"""Courses domain entities + invariants.

A *course* is an ordered collection of *lessons*. Courses live in one of
three levels (Beginner / Intermediate / Advanced) and carry a publish
state (draft / published), a mandatory flag, and a ``sort_order`` used
for drag-to-reorder within a level. Lessons are typed — video, pdf,
presentation, text, or quiz — with content invariants enforced by the
``new_lesson`` factory below.

This context is distinct from ``learning`` (which owns the path/module
catalogue + per-user progress). Courses are the admin-authored teaching
material; a later phase wires per-lesson progress and the quiz engine
against these rows.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.courses.errors import (
    InvalidCourseLevelError,
    InvalidLessonContentError,
)

# Public catalogue paging cap. The catalogue is unpaged by default (the
# full list, for backward compatibility with existing clients); when a
# caller passes an optional ``limit`` it is clamped to this ceiling so a
# single request can never fetch (and eager-load lessons for) an
# unbounded number of courses.
MAX_COURSE_LIST_LIMIT = 200


class CourseLevel(StrEnum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class CourseStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"


class LessonType(StrEnum):
    VIDEO = "video"
    PDF = "pdf"
    PRESENTATION = "presentation"
    TEXT = "text"
    QUIZ = "quiz"
    # Interactive code lesson: runs against the MATLAB-LLVM engine. Like
    # quiz, it's content-free at the lesson level (text_body may hold
    # instructions / starter code, but neither field is required).
    CODE = "code"


# Lesson types whose content is an external/uploaded asset referenced by
# URL (YouTube link, uploaded MP4/WebM/OGG, PDF, PPT/PPTX).
_URL_BACKED_TYPES = frozenset({LessonType.VIDEO, LessonType.PDF, LessonType.PRESENTATION})


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_slug(text: str) -> str:
    """Lowercase, replace non-alphanumerics with hyphens, trim hyphens."""
    return _SLUG_RE.sub("-", text.strip().lower()).strip("-")


def parse_level(value: str) -> CourseLevel:
    """Coerce a wire string to a ``CourseLevel`` or raise."""
    try:
        return CourseLevel(value)
    except ValueError as exc:
        raise InvalidCourseLevelError(
            f"level must be one of {[lvl.value for lvl in CourseLevel]}, got {value!r}"
        ) from exc


@dataclass(slots=True)
class Lesson:
    """A single lesson within a course.

    Content invariants (enforced by ``new_lesson`` / ``set_content``):
      * ``video`` | ``pdf`` | ``presentation`` → ``content_url`` set,
        ``text_body`` empty.
      * ``text`` → ``text_body`` set, ``content_url`` empty.
      * ``quiz`` → neither required; the questions live in the quiz
        context and reference this lesson by id.
    """

    id: UUID
    course_id: UUID
    title: str
    lesson_type: LessonType
    sort_order: int
    content_url: str | None = None
    text_body: str | None = None
    duration: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None

    def set_content(
        self,
        *,
        title: str | None = None,
        content_url: str | None = None,
        text_body: str | None = None,
        duration: str | None = None,
        sort_order: int | None = None,
        now: datetime | None = None,
    ) -> None:
        if title is not None:
            if not title.strip():
                raise ValueError("title cannot be empty")
            self.title = title.strip()
        if content_url is not None:
            self.content_url = content_url.strip() or None
        if text_body is not None:
            self.text_body = text_body.strip() or None
        if duration is not None:
            self.duration = duration.strip() or None
        if sort_order is not None:
            self.sort_order = sort_order
        _validate_lesson_content(self.lesson_type, self.content_url, self.text_body)
        self.updated_at = now or datetime.now(tz=UTC)


@dataclass(slots=True)
class Category:
    """A browsable course category (topic). Stored data — not derived from the
    course slug. A course references at most one; deleting a category leaves its
    courses uncategorized (the slug-derived topic stays as a public fallback).

    Categories form a one-level hierarchy via ``parent_id``: a top-level
    category (``parent_id is None``) is a *group* (e.g. "Programming"); a child
    is a *sub-category* (e.g. "Languages"). Deleting a parent re-parents its
    children to top level (FK ON DELETE SET NULL)."""

    id: UUID
    slug: str
    name: str
    icon: str = ""
    sort_order: int = 0
    parent_id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None


@dataclass(slots=True)
class Course:
    id: UUID
    slug: str
    title: str
    description: str
    level: CourseLevel
    status: CourseStatus
    mandatory: bool
    sort_order: int
    created_at: datetime
    published_at: datetime | None = None
    updated_at: datetime | None = None
    # Optional course-level deadline; the overdue/urgent/upcoming status
    # is derived from this relative to now at the read boundary.
    due_at: datetime | None = None
    lessons: list[Lesson] = field(default_factory=list)
    # Assigned category (None = uncategorized). Set on read by the repo's join;
    # on write, ``save`` persists ``category.id`` (or NULL).
    category: Category | None = None
    # Read-time lesson count, populated by count-only list reads that
    # deliberately skip hydrating lesson bodies (public catalogue). It is
    # NOT a persisted column — derived at the read boundary like
    # ``deadline_status``. ``None`` means "not provided", so a caller falls
    # back to ``len(lessons)`` and behaviour stays byte-identical to before.
    lesson_count: int | None = None

    def is_visible_to_anonymous(self) -> bool:
        return self.status is CourseStatus.PUBLISHED and self.published_at is not None

    def set_deadline(self, due_at: datetime | None, now: datetime | None = None) -> None:
        """Set or clear (``due_at=None``) the course's completion deadline."""
        self.due_at = due_at
        self.updated_at = now or datetime.now(tz=UTC)

    def publish(self, now: datetime | None = None) -> None:
        moment = now or datetime.now(tz=UTC)
        self.status = CourseStatus.PUBLISHED
        if self.published_at is None:
            self.published_at = moment
        self.updated_at = moment

    def unpublish(self, now: datetime | None = None) -> None:
        self.status = CourseStatus.DRAFT
        # Keep ``published_at`` so re-publishing preserves the original
        # first-publish timestamp; visibility is gated on status.
        self.updated_at = now or datetime.now(tz=UTC)


# ── Factories + invariants ───────────────────────────────────────────


def _validate_lesson_content(
    lesson_type: LessonType,
    content_url: str | None,
    text_body: str | None,
) -> None:
    if lesson_type in _URL_BACKED_TYPES and not content_url:
        raise InvalidLessonContentError(f"{lesson_type.value} lesson requires a content_url")
    if lesson_type is LessonType.TEXT and not text_body:
        raise InvalidLessonContentError("text lesson requires a text_body")


def new_course(
    *,
    title: str,
    description: str,
    level: CourseLevel | str,
    slug: str | None = None,
    mandatory: bool = False,
    sort_order: int = 0,
    due_at: datetime | None = None,
    now: datetime | None = None,
) -> Course:
    if not title.strip():
        raise ValueError("title cannot be empty")
    effective_slug = normalize_slug(slug) if slug else normalize_slug(title)
    if not effective_slug:
        raise ValueError("slug normalises to empty")
    parsed_level = level if isinstance(level, CourseLevel) else parse_level(level)
    created_at = now or datetime.now(tz=UTC)
    return Course(
        id=uuid.uuid4(),
        slug=effective_slug,
        title=title.strip(),
        description=description.strip(),
        level=parsed_level,
        status=CourseStatus.DRAFT,
        mandatory=mandatory,
        sort_order=sort_order,
        created_at=created_at,
        due_at=due_at,
    )


def new_category(
    *,
    name: str,
    slug: str | None = None,
    icon: str = "",
    sort_order: int = 0,
    parent_id: UUID | None = None,
    now: datetime | None = None,
) -> Category:
    if not name.strip():
        raise ValueError("name cannot be empty")
    effective_slug = normalize_slug(slug) if slug else normalize_slug(name)
    if not effective_slug:
        raise ValueError("slug normalises to empty")
    return Category(
        id=uuid.uuid4(),
        slug=effective_slug,
        name=name.strip(),
        icon=icon.strip(),
        sort_order=sort_order,
        parent_id=parent_id,
        created_at=now or datetime.now(tz=UTC),
    )


def new_lesson(
    *,
    course_id: UUID,
    title: str,
    lesson_type: LessonType | str,
    content_url: str | None = None,
    text_body: str | None = None,
    duration: str | None = None,
    sort_order: int = 0,
    now: datetime | None = None,
) -> Lesson:
    if not title.strip():
        raise ValueError("title cannot be empty")
    parsed_type = lesson_type if isinstance(lesson_type, LessonType) else LessonType(lesson_type)
    url = (content_url or "").strip() or None
    body = (text_body or "").strip() or None
    _validate_lesson_content(parsed_type, url, body)
    moment = now or datetime.now(tz=UTC)
    return Lesson(
        id=uuid.uuid4(),
        course_id=course_id,
        title=title.strip(),
        lesson_type=parsed_type,
        sort_order=sort_order,
        content_url=url,
        text_body=body,
        duration=(duration or "").strip() or None,
        created_at=moment,
        updated_at=moment,
    )

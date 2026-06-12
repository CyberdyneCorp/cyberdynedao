"""Ports the courses context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.courses.certificates import CourseCertificate
from cyberdyne_backend.domain.courses.entities import Course, CourseLevel
from cyberdyne_backend.domain.courses.progress import LessonProgress


@runtime_checkable
class CourseRepository(Protocol):
    async def save(self, course: Course) -> None:
        """Insert or update a course **and its lessons**.

        Raises ``DuplicateCourseSlugError`` if another course already
        owns the slug.
        """
        ...

    async def get_by_slug(
        self, slug: str, *, include_drafts: bool = False, locale: str = "en"
    ) -> Course:
        """Load a course (with its ordered lessons) by slug. Raises
        ``CourseNotFoundError``. Drafts resolve only when
        ``include_drafts`` is true (editor scope). When ``locale`` is a
        non-English language, localized title/description/lesson bodies are
        overlaid with per-field English fallback."""
        ...

    async def get_by_id(self, course_id: UUID) -> Course | None:
        """Load a course (with its lessons) by id, or ``None`` if absent.
        Used by cross-cutting flows that hold a course id (e.g. awarding a
        certificate when progress marks the course complete)."""
        ...

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
        locale: str = "en",
    ) -> list[Course]:
        """All courses ordered by (level, sort_order). Drafts are
        filtered out unless ``include_drafts`` is true. Lessons are
        included so a catalogue render needs a single round-trip. A
        non-English ``locale`` overlays localized fields (English fallback)."""
        ...

    async def delete(self, course_id: UUID) -> None:
        """Delete a course and its lessons. No-op if absent."""
        ...


@runtime_checkable
class CourseProgressRepository(Protocol):
    """Persists per-lesson learner progress for the courses context."""

    async def get_lesson_progress(self, *, user_id: UUID, lesson_id: UUID) -> LessonProgress | None:
        """The learner's row for a single lesson, or ``None`` if they
        have not started it."""
        ...

    async def upsert_lesson_progress(self, progress: LessonProgress) -> None:
        """Insert or update a learner's progress for one lesson."""
        ...

    async def list_course_progress(self, *, user_id: UUID, course_id: UUID) -> list[LessonProgress]:
        """Every lesson-progress row the learner has within a course."""
        ...

    async def list_all_progress_for_user(self, *, user_id: UUID) -> list[LessonProgress]:
        """Every lesson-progress row the learner has across ALL courses, in
        one query — for building a per-course progress overview."""
        ...

    async def get_lesson_course_id(self, lesson_id: UUID) -> UUID | None:
        """The course a lesson belongs to, or ``None`` if no such lesson
        exists. Lets a cross-context caller (e.g. quiz completion) resolve
        the owning course without holding a courses repository."""
        ...


@runtime_checkable
class CourseCertificateRepository(Protocol):
    """Persists course completion certificates (one per user+course)."""

    async def save(self, certificate: CourseCertificate) -> None:
        """Insert the certificate. Issuance is idempotent at the use-case
        layer, so this is only reached for a genuinely new certificate."""
        ...

    async def get_for_user_and_course(
        self, *, user_id: UUID, course_slug: str
    ) -> CourseCertificate | None:
        """The learner's certificate for a course, or ``None``."""
        ...

    async def get_by_id(self, certificate_id: UUID) -> CourseCertificate | None:
        """A certificate by id (for public verification), or ``None``."""
        ...

    async def list_for_user(self, user_id: UUID) -> list[CourseCertificate]:
        """Every course certificate the learner has earned."""
        ...


@runtime_checkable
class CourseCertificateSigner(Protocol):
    """Signs/verifies a certificate's verification hash. Structurally
    satisfied by the shared HMAC signer."""

    def sign(self, message: str) -> str: ...

    def verify(self, message: str, signature: str) -> bool: ...


@runtime_checkable
class CourseCertificatePdfRenderer(Protocol):
    """Renders a course certificate to a downloadable PDF. Structurally
    satisfied by the shared reportlab renderer."""

    def render(
        self, *, certificate: CourseCertificate, subject_title: str, verify_url: str
    ) -> bytes: ...


@runtime_checkable
class CourseCertificateAwarder(Protocol):
    """Awards a course certificate when a learner's progress completes
    the course. Idempotent and a no-op when not yet eligible, so the
    progress write-path can fire it unconditionally."""

    async def award_if_complete(self, *, user_id: UUID, course_id: UUID) -> None: ...

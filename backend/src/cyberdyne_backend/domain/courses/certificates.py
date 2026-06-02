"""Course completion certificates (courses context).

A learner earns a certificate for a course once they've completed every
lesson in it. This mirrors the learning context's path certificates but
is course-scoped and self-contained: the signature is computed by an
injected signer (so the domain stays crypto-free), and verification
re-derives the hash over the public claims.

Distinct from the learning ``Certificate`` (path-keyed); the two don't
share storage or claims.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.courses.entities import Course
from cyberdyne_backend.domain.courses.errors import CourseCertificateNotEligibleError
from cyberdyne_backend.domain.courses.progress import LessonProgress, build_course_progress


@dataclass(slots=True)
class CourseCertificate:
    id: UUID
    user_id: UUID
    course_slug: str
    issued_at: datetime
    verification_hash: str
    # Signature over the verification hash; carried, not computed, here.
    signed_payload: str


# Local structural shim so the factory stays pure-domain (no port import).
@runtime_checkable
class _SignsCertificates(Protocol):  # pragma: no cover - structural shim only
    def sign(self, message: str) -> str: ...


def course_certificate_eligible(
    course: Course,
    progress_by_lesson: dict[UUID, LessonProgress],
) -> bool:
    """Eligible iff the course has lessons and every one is completed."""
    progress = build_course_progress(
        course_id=course.id,
        slug=course.slug,
        lessons=[(lesson.id, lesson.title) for lesson in course.lessons],
        progress_by_lesson=progress_by_lesson,
    )
    return progress.completed


def new_course_certificate(
    *,
    user_id: UUID,
    course: Course,
    progress_by_lesson: dict[UUID, LessonProgress],
    signer: _SignsCertificates,
    now: datetime | None = None,
) -> CourseCertificate:
    """Mint a course certificate IF every lesson is completed.

    Raises ``CourseCertificateNotEligibleError`` otherwise.
    """
    if not course_certificate_eligible(course, progress_by_lesson):
        raise CourseCertificateNotEligibleError(
            f"user {user_id} hasn't completed every lesson in course {course.slug}"
        )
    moment = now or datetime.now(tz=UTC)
    lesson_ids = ",".join(sorted(str(lesson.id) for lesson in course.lessons))
    claims = (
        f"sub={user_id};course={course.slug};issued_at={moment.isoformat()};lessons={lesson_ids}"
    )
    verification_hash = hashlib.sha256(claims.encode("utf-8")).hexdigest()
    signed_payload = signer.sign(verification_hash)
    return CourseCertificate(
        id=uuid.uuid4(),
        user_id=user_id,
        course_slug=course.slug,
        issued_at=moment,
        verification_hash=verification_hash,
        signed_payload=signed_payload,
    )


__all__ = [
    "CourseCertificate",
    "course_certificate_eligible",
    "new_course_certificate",
]

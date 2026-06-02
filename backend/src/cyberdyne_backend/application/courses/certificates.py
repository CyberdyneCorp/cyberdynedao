"""Course certificate use cases.

A learner claims their certificate for a course once every lesson is
complete (eligibility enforced server-side); issuance is idempotent.
Verification is public and re-checks the signature over the stored
claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.courses import (
    CourseCertificate,
    CourseCertificateNotFoundError,
    CourseCertificatePdfRenderer,
    CourseCertificateRepository,
    CourseCertificateSigner,
    CourseNotFoundError,
    CourseProgressRepository,
    CourseRepository,
    new_course_certificate,
)


@dataclass(slots=True)
class IssueCourseCertificate:
    """Mint (or return the existing) certificate for a learner's
    completed course. Raises ``CourseNotFoundError`` if the course is
    absent and ``CourseCertificateNotEligibleError`` if not every lesson
    is complete."""

    courses: CourseRepository
    progress: CourseProgressRepository
    certificates: CourseCertificateRepository
    signer: CourseCertificateSigner

    async def execute(self, *, user_id: UUID, slug: str) -> CourseCertificate:
        course = await self.courses.get_by_slug(slug)  # CourseNotFoundError if absent
        existing = await self.certificates.get_for_user_and_course(
            user_id=user_id, course_slug=course.slug
        )
        if existing is not None:
            return existing
        rows = await self.progress.list_course_progress(user_id=user_id, course_id=course.id)
        certificate = new_course_certificate(
            user_id=user_id,
            course=course,
            progress_by_lesson={row.lesson_id: row for row in rows},
            signer=self.signer,
        )
        await self.certificates.save(certificate)
        return certificate


@dataclass(slots=True)
class CourseCertificateVerification:
    valid: bool
    certificate: CourseCertificate | None


@dataclass(slots=True)
class VerifyCourseCertificate:
    certificates: CourseCertificateRepository
    signer: CourseCertificateSigner

    async def execute(self, certificate_id: UUID) -> CourseCertificateVerification:
        cert = await self.certificates.get_by_id(certificate_id)
        if cert is None:
            return CourseCertificateVerification(valid=False, certificate=None)
        valid = self.signer.verify(cert.verification_hash, cert.signed_payload)
        return CourseCertificateVerification(valid=valid, certificate=cert)


@dataclass(slots=True)
class GetMyCourseCertificate:
    certificates: CourseCertificateRepository

    async def execute(self, *, user_id: UUID, course_slug: str) -> CourseCertificate | None:
        return await self.certificates.get_for_user_and_course(
            user_id=user_id, course_slug=course_slug
        )


@dataclass(slots=True)
class RenderCourseCertificatePdf:
    """Render a course certificate as a downloadable PDF. The PDF carries
    the course title and a public verify URL."""

    certificates: CourseCertificateRepository
    courses: CourseRepository
    renderer: CourseCertificatePdfRenderer
    verify_url_base: str

    async def execute(self, certificate_id: UUID) -> bytes:
        cert = await self.certificates.get_by_id(certificate_id)
        if cert is None:
            raise CourseCertificateNotFoundError(str(certificate_id))
        try:
            course = await self.courses.get_by_slug(cert.course_slug, include_drafts=True)
            title = course.title
        except CourseNotFoundError:
            # Course retired since issuance — fall back to the slug.
            title = cert.course_slug
        verify_url = (
            f"{self.verify_url_base.rstrip('/')}/api/v1/courses/certificates/{cert.id}/verify"
        )
        return self.renderer.render(certificate=cert, subject_title=title, verify_url=verify_url)


__all__ = [
    "CourseCertificateVerification",
    "GetMyCourseCertificate",
    "IssueCourseCertificate",
    "RenderCourseCertificatePdf",
    "VerifyCourseCertificate",
]

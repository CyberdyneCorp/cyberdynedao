"""Domain + use-case tests for course completion certificates."""

from __future__ import annotations

import uuid
from uuid import UUID

import pytest

from cyberdyne_backend.application.courses import (
    GetMyCourseCertificate,
    IssueCourseCertificate,
    RenderCourseCertificatePdf,
    VerifyCourseCertificate,
)
from cyberdyne_backend.domain.courses import (
    Course,
    CourseCertificate,
    CourseCertificateNotEligibleError,
    CourseCertificateNotFoundError,
    CourseCertificateRepository,
    CourseNotFoundError,
    course_certificate_eligible,
    new_course,
    new_course_certificate,
    new_lesson,
    new_lesson_progress,
)
from cyberdyne_backend.domain.courses.progress import LessonProgress


class FakeSigner:
    """Deterministic stand-in for the HMAC signer."""

    def sign(self, message: str) -> str:
        return f"sig::{message}"

    def verify(self, message: str, signature: str) -> bool:
        return signature == f"sig::{message}"


def _course(n_lessons: int) -> Course:
    course = new_course(title="Solidity", description="d", level="Beginner")
    course.lessons = [
        new_lesson(
            course_id=course.id, title=f"L{i}", lesson_type="text", text_body="b", sort_order=i
        )
        for i in range(n_lessons)
    ]
    return course


def _all_completed(course: Course, user_id: UUID) -> dict[UUID, LessonProgress]:
    return {
        lesson.id: new_lesson_progress(
            user_id=user_id, course_id=course.id, lesson_id=lesson.id, percent=100
        )
        for lesson in course.lessons
    }


# ── Domain ────────────────────────────────────────────────────────────


class TestEligibility:
    def test_all_complete_is_eligible(self) -> None:
        course = _course(2)
        assert course_certificate_eligible(course, _all_completed(course, uuid.uuid4())) is True

    def test_partial_is_not_eligible(self) -> None:
        course = _course(2)
        user = uuid.uuid4()
        progress = {
            course.lessons[0].id: new_lesson_progress(
                user_id=user, course_id=course.id, lesson_id=course.lessons[0].id, percent=100
            )
        }
        assert course_certificate_eligible(course, progress) is False

    def test_course_without_lessons_is_not_eligible(self) -> None:
        course = _course(0)
        assert course_certificate_eligible(course, {}) is False

    def test_new_certificate_signs_claims(self) -> None:
        course = _course(1)
        user = uuid.uuid4()
        cert = new_course_certificate(
            user_id=user,
            course=course,
            progress_by_lesson=_all_completed(course, user),
            signer=FakeSigner(),
        )
        assert cert.course_slug == course.slug
        assert cert.signed_payload == f"sig::{cert.verification_hash}"

    def test_new_certificate_rejects_incomplete(self) -> None:
        course = _course(2)
        with pytest.raises(CourseCertificateNotEligibleError):
            new_course_certificate(
                user_id=uuid.uuid4(),
                course=course,
                progress_by_lesson={},
                signer=FakeSigner(),
            )


# ── Use cases (fakes) ─────────────────────────────────────────────────


class FakeCourseRepo:
    def __init__(self, course: Course | None) -> None:
        self._course = course

    async def save(self, course: Course) -> None:  # pragma: no cover - unused
        raise NotImplementedError

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        if self._course is None or self._course.slug != slug:
            raise CourseNotFoundError(slug)
        return self._course

    async def list_courses(self, *, level: object = None, include_drafts: bool = False):  # type: ignore[no-untyped-def]
        raise NotImplementedError  # pragma: no cover - unused

    async def delete(self, course_id: UUID) -> None:  # pragma: no cover - unused
        raise NotImplementedError


class FakeProgressRepo:
    def __init__(self, rows: list[LessonProgress]) -> None:
        self._rows = rows

    async def get_lesson_progress(self, *, user_id: UUID, lesson_id: UUID):  # type: ignore[no-untyped-def]
        raise NotImplementedError  # pragma: no cover - unused

    async def upsert_lesson_progress(self, progress: LessonProgress) -> None:  # pragma: no cover
        raise NotImplementedError

    async def list_course_progress(self, *, user_id: UUID, course_id: UUID) -> list[LessonProgress]:
        return list(self._rows)

    async def get_lesson_course_id(self, lesson_id: UUID):  # type: ignore[no-untyped-def]
        raise NotImplementedError  # pragma: no cover - unused


class FakeCertRepo:
    def __init__(self) -> None:
        self.saved: list[CourseCertificate] = []

    async def save(self, certificate: CourseCertificate) -> None:
        self.saved.append(certificate)

    async def get_for_user_and_course(
        self, *, user_id: UUID, course_slug: str
    ) -> CourseCertificate | None:
        for c in self.saved:
            if c.user_id == user_id and c.course_slug == course_slug:
                return c
        return None

    async def get_by_id(self, certificate_id: UUID) -> CourseCertificate | None:
        return next((c for c in self.saved if c.id == certificate_id), None)

    async def list_for_user(self, user_id: UUID) -> list[CourseCertificate]:
        return [c for c in self.saved if c.user_id == user_id]


def test_fake_cert_repo_matches_port() -> None:
    assert isinstance(FakeCertRepo(), CourseCertificateRepository)


class TestIssueCourseCertificate:
    async def test_issues_when_complete(self) -> None:
        course = _course(2)
        user = uuid.uuid4()
        rows = list(_all_completed(course, user).values())
        uc = IssueCourseCertificate(
            courses=FakeCourseRepo(course),
            progress=FakeProgressRepo(rows),
            certificates=FakeCertRepo(),
            signer=FakeSigner(),
        )
        cert = await uc.execute(user_id=user, slug=course.slug)
        assert cert.course_slug == course.slug

    async def test_idempotent(self) -> None:
        course = _course(1)
        user = uuid.uuid4()
        rows = list(_all_completed(course, user).values())
        certs = FakeCertRepo()
        uc = IssueCourseCertificate(
            courses=FakeCourseRepo(course),
            progress=FakeProgressRepo(rows),
            certificates=certs,
            signer=FakeSigner(),
        )
        first = await uc.execute(user_id=user, slug=course.slug)
        second = await uc.execute(user_id=user, slug=course.slug)
        assert first.id == second.id
        assert len(certs.saved) == 1

    async def test_not_eligible_raises(self) -> None:
        course = _course(2)
        uc = IssueCourseCertificate(
            courses=FakeCourseRepo(course),
            progress=FakeProgressRepo([]),  # no progress
            certificates=FakeCertRepo(),
            signer=FakeSigner(),
        )
        with pytest.raises(CourseCertificateNotEligibleError):
            await uc.execute(user_id=uuid.uuid4(), slug=course.slug)

    async def test_unknown_course_raises(self) -> None:
        uc = IssueCourseCertificate(
            courses=FakeCourseRepo(None),
            progress=FakeProgressRepo([]),
            certificates=FakeCertRepo(),
            signer=FakeSigner(),
        )
        with pytest.raises(CourseNotFoundError):
            await uc.execute(user_id=uuid.uuid4(), slug="ghost")


class TestVerifyAndGet:
    async def _issue(self, certs: FakeCertRepo) -> tuple[UUID, CourseCertificate]:
        course = _course(1)
        user = uuid.uuid4()
        rows = list(_all_completed(course, user).values())
        cert = await IssueCourseCertificate(
            courses=FakeCourseRepo(course),
            progress=FakeProgressRepo(rows),
            certificates=certs,
            signer=FakeSigner(),
        ).execute(user_id=user, slug=course.slug)
        return user, cert

    async def test_verify_valid(self) -> None:
        certs = FakeCertRepo()
        _, cert = await self._issue(certs)
        result = await VerifyCourseCertificate(certificates=certs, signer=FakeSigner()).execute(
            cert.id
        )
        assert result.valid is True
        assert result.certificate is not None

    async def test_verify_unknown_is_invalid(self) -> None:
        result = await VerifyCourseCertificate(
            certificates=FakeCertRepo(), signer=FakeSigner()
        ).execute(uuid.uuid4())
        assert result.valid is False
        assert result.certificate is None

    async def test_get_my_certificate(self) -> None:
        certs = FakeCertRepo()
        user, cert = await self._issue(certs)
        got = await GetMyCourseCertificate(certificates=certs).execute(
            user_id=user, course_slug=cert.course_slug
        )
        assert got is not None
        assert got.id == cert.id


class _FakeRenderer:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def render(
        self, *, certificate: CourseCertificate, subject_title: str, verify_url: str
    ) -> bytes:
        self.calls.append((subject_title, verify_url))
        return b"%PDF-FAKE"


class TestRenderCourseCertificatePdf:
    async def _cert(self, certs: FakeCertRepo, course: Course) -> CourseCertificate:
        user = uuid.uuid4()
        cert = await IssueCourseCertificate(
            courses=FakeCourseRepo(course),
            progress=FakeProgressRepo(list(_all_completed(course, user).values())),
            certificates=certs,
            signer=FakeSigner(),
        ).execute(user_id=user, slug=course.slug)
        return cert

    async def test_renders_with_course_title(self) -> None:
        course = _course(1)
        certs = FakeCertRepo()
        cert = await self._cert(certs, course)
        renderer = _FakeRenderer()
        uc = RenderCourseCertificatePdf(
            certificates=certs,
            courses=FakeCourseRepo(course),
            renderer=renderer,
            verify_url_base="https://x.test/",
        )
        out = await uc.execute(cert.id)
        assert out == b"%PDF-FAKE"
        title, verify_url = renderer.calls[0]
        assert title == course.title
        assert verify_url == f"https://x.test/api/v1/courses/certificates/{cert.id}/verify"

    async def test_falls_back_to_slug_when_course_gone(self) -> None:
        course = _course(1)
        certs = FakeCertRepo()
        cert = await self._cert(certs, course)
        renderer = _FakeRenderer()
        uc = RenderCourseCertificatePdf(
            certificates=certs,
            courses=FakeCourseRepo(None),  # course retired
            renderer=renderer,
            verify_url_base="https://x.test",
        )
        await uc.execute(cert.id)
        assert renderer.calls[0][0] == cert.course_slug

    async def test_missing_certificate_raises(self) -> None:
        uc = RenderCourseCertificatePdf(
            certificates=FakeCertRepo(),
            courses=FakeCourseRepo(None),
            renderer=_FakeRenderer(),
            verify_url_base="https://x.test",
        )
        with pytest.raises(CourseCertificateNotFoundError):
            await uc.execute(uuid.uuid4())

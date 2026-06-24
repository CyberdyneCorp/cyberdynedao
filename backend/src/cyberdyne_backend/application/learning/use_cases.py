"""Use cases for the learning context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.application.academy import SUPPORTED_LANGUAGES
from cyberdyne_backend.domain.learning import (
    VALID_LEVELS,
    Certificate,
    CertificateNotFoundError,
    CertificatePdfRenderer,
    CertificateSigner,
    CourseLinkReader,
    Enrollment,
    EnrollmentDeadline,
    LearningContentNotFoundError,
    LearningContentValidationError,
    LearningModule,
    LearningPath,
    LearningRepository,
    LearningTranslation,
    ModuleGate,
    ModuleProgress,
    compute_path_gates,
    days_remaining,
    deadline_status,
    derived_module_percent,
    new_certificate,
    new_enrollment,
    new_module,
    new_path,
    new_progress,
    next_unlocked_module,
    with_courses,
)


async def _ensure_modules_exist(repo: LearningRepository, module_slugs: tuple[str, ...]) -> None:
    """Raise ``LearningContentValidationError`` if any slug in
    ``module_slugs`` is not a known module."""
    known = {m.slug for m in await repo.list_modules()}
    missing = [s for s in module_slugs if s not in known]
    if missing:
        raise LearningContentValidationError(
            f"path references unknown module slug(s): {', '.join(missing)}"
        )


async def _ensure_courses_exist(
    reader: CourseLinkReader | None, course_slugs: tuple[str, ...]
) -> None:
    """Raise ``LearningContentValidationError`` if any slug in ``course_slugs``
    is not a known course. A ``None`` reader (e.g. in unit tests with no
    course context wired) skips the check."""
    if reader is None or not course_slugs:
        return
    known = await reader.existing_course_slugs()
    missing = [s for s in course_slugs if s not in known]
    if missing:
        raise LearningContentValidationError(
            f"module references unknown course slug(s): {', '.join(missing)}"
        )


async def _derived_progress_map(
    repo: LearningRepository,
    reader: CourseLinkReader | None,
    user_id: UUID,
) -> dict[str, ModuleProgress]:
    """The user's module-progress map, with course-backed stages overridden
    by completion DERIVED from their linked courses. Course-less modules keep
    their self-reported progress. With no course reader, returns the raw map
    (legacy behaviour)."""
    raw = await repo.get_progress_map_for_user(user_id)
    if reader is None:
        return raw
    modules = await repo.list_modules()
    course_backed = [m for m in modules if m.course_slugs]
    if not course_backed:
        return raw
    percents = await reader.percent_by_course(user_id)
    merged = dict(raw)
    for module in course_backed:
        percent = derived_module_percent(module.course_slugs, percents)
        merged[module.slug] = new_progress(
            user_id=user_id, module_slug=module.slug, percent=percent
        )
    return merged


@dataclass(slots=True)
class ListModules:
    repo: LearningRepository
    # Optional courses reader: when present, each stage's ``course_slugs`` are
    # resolved to ``LinkedCourse`` display cards (locale-aware) so the catalogue
    # can render the courses in a module without N extra calls.
    course_reader: CourseLinkReader | None = None

    async def execute(self, *, locale: str = "en") -> list[LearningModule]:
        modules = await self.repo.list_modules(locale=locale)
        if self.course_reader is None:
            return modules
        cards = await self.course_reader.course_cards(locale=locale)
        return [
            with_courses(m, tuple(cards[s] for s in m.course_slugs if s in cards))
            if m.course_slugs
            else m
            for m in modules
        ]


@dataclass(slots=True)
class ListPaths:
    repo: LearningRepository

    async def execute(self, *, locale: str = "en") -> list[LearningPath]:
        return await self.repo.list_paths(locale=locale)


# ── Admin catalogue CRUD ─────────────────────────────────────────────


@dataclass(slots=True)
class CreateModuleCommand:
    title: str
    category: str
    description: str
    level: str
    duration: str
    icon: str
    topics: tuple[str, ...] = ()
    course_slugs: tuple[str, ...] = ()
    slug: str | None = None


@dataclass(slots=True)
class CreateModule:
    repo: LearningRepository
    # Optional read into the courses context, to validate linked courses.
    course_reader: CourseLinkReader | None = None

    async def execute(self, cmd: CreateModuleCommand) -> LearningModule:
        await _ensure_courses_exist(self.course_reader, cmd.course_slugs)
        module = new_module(
            title=cmd.title,
            category=cmd.category,
            description=cmd.description,
            level=cmd.level,
            duration=cmd.duration,
            icon=cmd.icon,
            topics=cmd.topics,
            course_slugs=cmd.course_slugs,
            slug=cmd.slug,
        )
        return await self.repo.create_module(module)


@dataclass(slots=True)
class UpdateModuleCommand:
    slug: str
    title: str | None = None
    category: str | None = None
    description: str | None = None
    level: str | None = None
    duration: str | None = None
    icon: str | None = None
    topics: tuple[str, ...] | None = None
    course_slugs: tuple[str, ...] | None = None


@dataclass(slots=True)
class UpdateModule:
    repo: LearningRepository
    course_reader: CourseLinkReader | None = None

    async def execute(self, cmd: UpdateModuleCommand) -> LearningModule:
        if cmd.level is not None and cmd.level not in VALID_LEVELS:
            raise LearningContentValidationError(
                f"level must be one of {VALID_LEVELS}, got {cmd.level!r}"
            )
        if cmd.course_slugs is not None:
            await _ensure_courses_exist(self.course_reader, cmd.course_slugs)
        return await self.repo.update_module(
            cmd.slug,
            title=cmd.title,
            category=cmd.category,
            description=cmd.description,
            level=cmd.level,
            duration=cmd.duration,
            icon=cmd.icon,
            topics=cmd.topics,
            course_slugs=cmd.course_slugs,
        )


@dataclass(slots=True)
class DeleteModule:
    repo: LearningRepository

    async def execute(self, slug: str) -> None:
        await self.repo.delete_module(slug)


@dataclass(slots=True)
class CreatePathCommand:
    title: str
    description: str
    module_slugs: tuple[str, ...]
    estimated_time: str
    icon: str
    slug: str | None = None


@dataclass(slots=True)
class CreatePath:
    repo: LearningRepository

    async def execute(self, cmd: CreatePathCommand) -> LearningPath:
        await _ensure_modules_exist(self.repo, cmd.module_slugs)
        path = new_path(
            title=cmd.title,
            description=cmd.description,
            module_slugs=cmd.module_slugs,
            estimated_time=cmd.estimated_time,
            icon=cmd.icon,
            slug=cmd.slug,
        )
        return await self.repo.create_path(path)


@dataclass(slots=True)
class UpdatePathCommand:
    slug: str
    title: str | None = None
    description: str | None = None
    module_slugs: tuple[str, ...] | None = None
    estimated_time: str | None = None
    icon: str | None = None


@dataclass(slots=True)
class UpdatePath:
    repo: LearningRepository

    async def execute(self, cmd: UpdatePathCommand) -> LearningPath:
        if cmd.module_slugs is not None:
            await _ensure_modules_exist(self.repo, cmd.module_slugs)
        return await self.repo.update_path(
            cmd.slug,
            title=cmd.title,
            description=cmd.description,
            module_slugs=cmd.module_slugs,
            estimated_time=cmd.estimated_time,
            icon=cmd.icon,
        )


@dataclass(slots=True)
class DeletePath:
    repo: LearningRepository

    async def execute(self, slug: str) -> None:
        await self.repo.delete_path(slug)


@dataclass(slots=True)
class ReorderPathModules:
    repo: LearningRepository

    async def execute(self, *, slug: str, module_slugs: tuple[str, ...]) -> LearningPath:
        await _ensure_modules_exist(self.repo, module_slugs)
        return await self.repo.update_path(slug, module_slugs=module_slugs)


# ── Translations (admin) ─────────────────────────────────────────────


def _validate_language(language: str) -> None:
    """A translation language must be a supported, non-English tag."""
    if language == "en" or language not in SUPPORTED_LANGUAGES:
        allowed = ", ".join(lang for lang in SUPPORTED_LANGUAGES if lang != "en")
        raise LearningContentValidationError(
            f"language must be one of {allowed} (got {language!r})"
        )


@dataclass(slots=True)
class ListModuleTranslations:
    repo: LearningRepository

    async def execute(self, slug: str) -> list[LearningTranslation]:
        return await self.repo.list_module_translations(slug)


@dataclass(slots=True)
class UpsertModuleTranslation:
    repo: LearningRepository

    async def execute(
        self, *, slug: str, language: str, title: str, description: str
    ) -> LearningTranslation:
        _validate_language(language)
        return await self.repo.upsert_module_translation(
            slug, language=language, title=title, description=description
        )


@dataclass(slots=True)
class DeleteModuleTranslation:
    repo: LearningRepository

    async def execute(self, *, slug: str, language: str) -> None:
        _validate_language(language)
        await self.repo.delete_module_translation(slug, language=language)


@dataclass(slots=True)
class ListPathTranslations:
    repo: LearningRepository

    async def execute(self, slug: str) -> list[LearningTranslation]:
        return await self.repo.list_path_translations(slug)


@dataclass(slots=True)
class UpsertPathTranslation:
    repo: LearningRepository

    async def execute(
        self, *, slug: str, language: str, title: str, description: str
    ) -> LearningTranslation:
        _validate_language(language)
        return await self.repo.upsert_path_translation(
            slug, language=language, title=title, description=description
        )


@dataclass(slots=True)
class DeletePathTranslation:
    repo: LearningRepository

    async def execute(self, *, slug: str, language: str) -> None:
        _validate_language(language)
        await self.repo.delete_path_translation(slug, language=language)


@dataclass(slots=True)
class EnrollInPath:
    """Idempotent on (user_id, path_slug). Returns the existing
    enrollment if one already exists, otherwise creates a new one."""

    repo: LearningRepository

    async def execute(self, *, user_id: UUID, path_slug: str) -> Enrollment:
        # Verify the path exists; raise LearningContentNotFoundError otherwise.
        await self.repo.get_path(path_slug)
        candidate = new_enrollment(user_id=user_id, path_slug=path_slug)
        return await self.repo.upsert_enrollment(candidate)


@dataclass(slots=True)
class UpdateModuleProgress:
    """Idempotent on (user_id, module_slug). Upserts and returns the
    new state. Caller passes the absolute percent (not a delta)."""

    repo: LearningRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        module_slug: str,
        percent: int,
    ) -> ModuleProgress:
        # If a row already exists, update it (preserves started_at).
        # Otherwise create with started_at = now.
        existing = (await self.repo.get_progress_map_for_user(user_id)).get(module_slug)
        if existing is None:
            progress = new_progress(user_id=user_id, module_slug=module_slug, percent=percent)
        else:
            existing.update(percent)
            progress = existing
        return await self.repo.upsert_progress(progress)


@dataclass(slots=True)
class MyLearningState:
    enrollments: list[Enrollment]
    progress_by_module: dict[str, ModuleProgress]
    certificates: list[Certificate]


@dataclass(slots=True)
class GetMyLearningState:
    """Bundle endpoint backing the LearnView's authenticated panels."""

    repo: LearningRepository
    course_reader: CourseLinkReader | None = None

    async def execute(self, user_id: UUID) -> MyLearningState:
        enrollments = await self.repo.list_enrollments_for_user(user_id)
        progress = await _derived_progress_map(self.repo, self.course_reader, user_id)
        certificates = []
        for enr in enrollments:
            cert = await self.repo.get_certificate_for_user_and_path(user_id, enr.path_slug)
            if cert is not None:
                certificates.append(cert)
        return MyLearningState(
            enrollments=enrollments,
            progress_by_module=progress,
            certificates=certificates,
        )


@dataclass(slots=True)
class IssueCertificate:
    """Admin-only. Mints a signed-JSON certificate for a user iff every
    module in the path is at 100%."""

    repo: LearningRepository
    signer: CertificateSigner
    course_reader: CourseLinkReader | None = None

    async def execute(self, *, user_id: UUID, path_slug: str) -> Certificate:
        path = await self.repo.get_path(path_slug)
        progress = await _derived_progress_map(self.repo, self.course_reader, user_id)
        cert = new_certificate(
            user_id=user_id,
            path=path,
            progress_by_module=progress,
            signer=self.signer,
        )
        await self.repo.save_certificate(cert)
        return cert


@dataclass(slots=True)
class CertificateVerification:
    valid: bool
    certificate: Certificate | None


@dataclass(slots=True)
class VerifyCertificate:
    """Public verification of a certificate by id. ``valid`` is true iff
    the certificate exists and its stored signature matches its
    verification hash (i.e. the claims weren't tampered with)."""

    repo: LearningRepository
    signer: CertificateSigner

    async def execute(self, certificate_id: UUID) -> CertificateVerification:
        cert = await self.repo.get_certificate_by_id(certificate_id)
        if cert is None:
            return CertificateVerification(valid=False, certificate=None)
        valid = self.signer.verify(cert.verification_hash, cert.signed_payload)
        return CertificateVerification(valid=valid, certificate=cert)


@dataclass(slots=True)
class RenderCertificatePdf:
    """Render a downloadable PDF for a certificate. The PDF carries the
    path title and a verify URL so a holder can prove authenticity."""

    repo: LearningRepository
    renderer: CertificatePdfRenderer
    verify_url_base: str

    async def execute(self, certificate_id: UUID) -> bytes:
        cert = await self.repo.get_certificate_by_id(certificate_id)
        if cert is None:
            raise CertificateNotFoundError(str(certificate_id))
        try:
            path = await self.repo.get_path(cert.path_slug)
            path_title = path.title
        except LearningContentNotFoundError:
            # Path was retired since issuance — fall back to the slug.
            path_title = cert.path_slug
        verify_url = (
            f"{self.verify_url_base.rstrip('/')}/api/v1/learning/certificates/{cert.id}/verify"
        )
        return self.renderer.render(
            certificate=cert, subject_title=path_title, verify_url=verify_url
        )


@dataclass(slots=True)
class SetEnrollmentDeadline:
    """Admin-only. Sets (or clears, with ``due_at=None``) the deadline on
    a user's path enrollment."""

    repo: LearningRepository

    async def execute(
        self, *, user_id: UUID, path_slug: str, due_at: datetime | None
    ) -> Enrollment:
        return await self.repo.set_enrollment_deadline(
            user_id=user_id, path_slug=path_slug, due_at=due_at
        )


@dataclass(slots=True)
class GetMyDeadlines:
    """A learner's enrollments with their computed deadline status
    (overdue / urgent / upcoming / none)."""

    repo: LearningRepository

    async def execute(
        self, user_id: UUID, *, now: datetime | None = None
    ) -> list[EnrollmentDeadline]:
        moment = now or datetime.now(tz=UTC)
        enrollments = await self.repo.list_enrollments_for_user(user_id)
        return [
            EnrollmentDeadline(
                path_slug=e.path_slug,
                due_at=e.due_at,
                status=deadline_status(e.due_at, now=moment),
                days_remaining=days_remaining(e.due_at, now=moment),
            )
            for e in enrollments
        ]


@dataclass(slots=True)
class GetPathGating:
    """Per-module lock state for a user against a path — backs the
    player's prerequisite gating (level + sequential) and the lock
    tooltips. Read-only; computed from the catalogue + the user's
    progress."""

    repo: LearningRepository
    course_reader: CourseLinkReader | None = None

    async def execute(self, *, user_id: UUID, path_slug: str) -> list[ModuleGate]:
        # Raises LearningContentNotFoundError if the path is unknown.
        path = await self.repo.get_path(path_slug)
        modules = await self.repo.list_modules()
        modules_by_slug = {m.slug: m for m in modules}
        progress = await _derived_progress_map(self.repo, self.course_reader, user_id)
        return compute_path_gates(path, modules_by_slug, progress)


@dataclass(slots=True)
class EligibilityResult:
    eligible: bool
    already_enrolled: bool
    next_module: str | None
    reason: str | None


@dataclass(slots=True)
class CheckEnrollmentEligibility:
    """Eligibility pre-check for enrolling in a path. A path is
    enrollable when it resolves to at least one module; surfaces whether
    the user is already enrolled and the first module they'd start on."""

    repo: LearningRepository
    course_reader: CourseLinkReader | None = None

    async def execute(self, *, user_id: UUID, path_slug: str) -> EligibilityResult:
        path = await self.repo.get_path(path_slug)
        modules = await self.repo.list_modules()
        modules_by_slug = {m.slug: m for m in modules}
        progress = await _derived_progress_map(self.repo, self.course_reader, user_id)
        gates = compute_path_gates(path, modules_by_slug, progress)

        enrollments = await self.repo.list_enrollments_for_user(user_id)
        already_enrolled = any(e.path_slug == path_slug for e in enrollments)

        if not gates:
            return EligibilityResult(
                eligible=False,
                already_enrolled=already_enrolled,
                next_module=None,
                reason="path has no resolvable modules",
            )
        return EligibilityResult(
            eligible=True,
            already_enrolled=already_enrolled,
            next_module=next_unlocked_module(gates),
            reason=None,
        )

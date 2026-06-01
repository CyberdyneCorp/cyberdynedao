"""Use cases for the learning context."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.learning import (
    Certificate,
    CertificateSigner,
    Enrollment,
    LearningModule,
    LearningPath,
    LearningRepository,
    ModuleProgress,
    new_certificate,
    new_enrollment,
    new_progress,
)


@dataclass(slots=True)
class ListModules:
    repo: LearningRepository

    async def execute(self) -> list[LearningModule]:
        return await self.repo.list_modules()


@dataclass(slots=True)
class ListPaths:
    repo: LearningRepository

    async def execute(self) -> list[LearningPath]:
        return await self.repo.list_paths()


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

    async def execute(self, user_id: UUID) -> MyLearningState:
        enrollments = await self.repo.list_enrollments_for_user(user_id)
        progress = await self.repo.get_progress_map_for_user(user_id)
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

    async def execute(self, *, user_id: UUID, path_slug: str) -> Certificate:
        path = await self.repo.get_path(path_slug)
        progress = await self.repo.get_progress_map_for_user(user_id)
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

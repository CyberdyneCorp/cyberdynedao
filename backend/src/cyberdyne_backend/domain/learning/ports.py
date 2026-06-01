"""Ports for the learning context."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.learning.entities import (
    Certificate,
    Enrollment,
    LearningModule,
    LearningPath,
    ModuleProgress,
)


@runtime_checkable
class LearningRepository(Protocol):
    # Catalogue (read-only, seeded)
    async def list_modules(self) -> list[LearningModule]: ...
    async def list_paths(self) -> list[LearningPath]: ...
    async def get_path(self, slug: str) -> LearningPath: ...

    # Per-user state
    async def upsert_enrollment(self, enrollment: Enrollment) -> Enrollment:
        """Insert if (user_id, path_slug) is new; return the existing
        row otherwise. Caller passes a fresh ``new_enrollment(...)``
        each time; the repo enforces uniqueness."""
        ...

    async def list_enrollments_for_user(self, user_id: UUID) -> list[Enrollment]: ...

    async def set_enrollment_deadline(
        self, *, user_id: UUID, path_slug: str, due_at: datetime | None
    ) -> Enrollment:
        """Set (or clear, with ``None``) the deadline on an existing
        enrollment. Raises ``EnrollmentNotFoundError`` if the user isn't
        enrolled in the path."""
        ...

    async def upsert_progress(self, progress: ModuleProgress) -> ModuleProgress:
        """Insert or update by ``(user_id, module_slug)``. Returns the
        stored row."""
        ...

    async def get_progress_map_for_user(self, user_id: UUID) -> dict[str, ModuleProgress]:
        """``{module_slug: ModuleProgress}`` for every module the user
        has touched. Missing slugs mean "never started"."""
        ...

    async def save_certificate(self, certificate: Certificate) -> None: ...

    async def get_certificate_for_user_and_path(
        self, user_id: UUID, path_slug: str
    ) -> Certificate | None: ...

    async def get_certificate_by_id(self, certificate_id: UUID) -> Certificate | None:
        """Load a certificate by its id, for public verification. None if
        no such certificate."""
        ...


@runtime_checkable
class CertificateSigner(Protocol):
    """Signs (and verifies) the certificate's verification hash. Real
    impl uses HMAC-SHA256 over the env-loaded shared secret."""

    def sign(self, message: str) -> str: ...

    def verify(self, message: str, signature: str) -> bool:
        """True iff ``signature`` is this signer's signature of
        ``message`` — i.e. the certificate hasn't been tampered with."""
        ...


@runtime_checkable
class CertificatePdfRenderer(Protocol):
    """Renders a certificate to a downloadable PDF document."""

    def render(self, *, certificate: Certificate, path_title: str, verify_url: str) -> bytes: ...

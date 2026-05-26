"""Learning domain entities + invariants."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.learning.errors import (
    CertificateNotEligibleError,
    ProgressOutOfRangeError,
)

# ── Content catalogue (read-only, seeded) ────────────────────────────


@dataclass(frozen=True, slots=True)
class LearningModule:
    slug: str
    title: str
    category: str
    description: str
    level: str  # 'Beginner' | 'Intermediate' | 'Advanced'
    duration: str  # human-readable like '1h 30min'
    icon: str
    topics: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LearningPath:
    slug: str
    title: str
    description: str
    module_slugs: tuple[str, ...]
    estimated_time: str
    icon: str


# ── Per-user state ───────────────────────────────────────────────────


class EnrollmentStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


@dataclass(slots=True)
class Enrollment:
    id: UUID
    user_id: UUID
    path_slug: str
    started_at: datetime
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE


@dataclass(slots=True)
class ModuleProgress:
    """A user's progress through a single module.

    Invariant: ``completed_at`` is non-null iff ``percent == 100``.
    Enforced by the factory + ``update`` method below; the persistence
    adapter never reaches in and writes ``percent`` and ``completed_at``
    independently.
    """

    id: UUID
    user_id: UUID
    module_slug: str
    percent: int
    started_at: datetime
    completed_at: datetime | None = None
    updated_at: datetime | None = None

    def update(self, new_percent: int, now: datetime | None = None) -> None:
        if not 0 <= new_percent <= 100:
            raise ProgressOutOfRangeError(f"percent must be 0..100, got {new_percent}")
        moment = now or datetime.now(tz=UTC)
        self.percent = new_percent
        self.updated_at = moment
        if new_percent == 100 and self.completed_at is None:
            self.completed_at = moment
        elif new_percent < 100:
            # Allow re-opening a previously-completed module by dropping
            # the percent back below 100 — clears the completion marker.
            self.completed_at = None

    @property
    def is_completed(self) -> bool:
        return self.percent == 100 and self.completed_at is not None


@dataclass(slots=True)
class Certificate:
    id: UUID
    user_id: UUID
    path_slug: str
    issued_at: datetime
    verification_hash: str
    # JWS-style compact signature over (sub, path, issued_at, hash).
    # The signer adapter actually computes this; the domain object just
    # carries it.
    signed_payload: str


# ── Factories + invariants ───────────────────────────────────────────


def new_enrollment(
    *,
    user_id: UUID,
    path_slug: str,
    now: datetime | None = None,
) -> Enrollment:
    return Enrollment(
        id=uuid.uuid4(),
        user_id=user_id,
        path_slug=path_slug,
        started_at=now or datetime.now(tz=UTC),
    )


def new_progress(
    *,
    user_id: UUID,
    module_slug: str,
    percent: int = 0,
    now: datetime | None = None,
) -> ModuleProgress:
    if not 0 <= percent <= 100:
        raise ProgressOutOfRangeError(f"percent must be 0..100, got {percent}")
    moment = now or datetime.now(tz=UTC)
    completed_at = moment if percent == 100 else None
    return ModuleProgress(
        id=uuid.uuid4(),
        user_id=user_id,
        module_slug=module_slug,
        percent=percent,
        started_at=moment,
        completed_at=completed_at,
        updated_at=moment,
    )


def certificate_eligible(
    path: LearningPath,
    progress_by_module: dict[str, ModuleProgress],
) -> bool:
    """A user is eligible iff every module in the path is at 100%."""
    return all(
        progress_by_module.get(slug) is not None and progress_by_module[slug].is_completed
        for slug in path.module_slugs
    )


def new_certificate(
    *,
    user_id: UUID,
    path: LearningPath,
    progress_by_module: dict[str, ModuleProgress],
    signer: _SignsCertificates,
    now: datetime | None = None,
) -> Certificate:
    """Mint a certificate IF the user has completed every module.

    Raises ``CertificateNotEligibleError`` otherwise. The signer is
    injected so the domain stays free of crypto-library imports — the
    real Ed25519 signer lives in
    ``adapters/outbound/certificates/signer.py``.
    """
    if not certificate_eligible(path, progress_by_module):
        raise CertificateNotEligibleError(
            f"user {user_id} hasn't completed every module in path {path.slug}"
        )
    moment = now or datetime.now(tz=UTC)
    # Verification hash is deterministic over the public certificate
    # claims. A verifier re-computes it and checks the signature.
    claims = (
        f"sub={user_id};"
        f"path={path.slug};"
        f"issued_at={moment.isoformat()};"
        f"modules={','.join(path.module_slugs)}"
    )
    verification_hash = hashlib.sha256(claims.encode("utf-8")).hexdigest()
    signed_payload = signer.sign(verification_hash)
    return Certificate(
        id=uuid.uuid4(),
        user_id=user_id,
        path_slug=path.slug,
        issued_at=moment,
        verification_hash=verification_hash,
        signed_payload=signed_payload,
    )


# Local Protocol declaration to avoid the circular import with ports.py.
# Same shape as ``CertificateSigner`` in ports — repeating the contract
# here keeps the entity factory pure-domain (no port import).
@runtime_checkable
class _SignsCertificates(Protocol):  # pragma: no cover - structural shim only
    def sign(self, message: str) -> str: ...


# Suppress unused-warning on field; we may extend Certificate to carry
# more claim metadata later (issuer DID, etc.).
_: object = field

"""Learning domain entities + invariants."""

from __future__ import annotations

import hashlib
import re
import uuid
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.learning.errors import (
    CertificateNotEligibleError,
    LearningContentValidationError,
    ProgressOutOfRangeError,
)

# Catalogue levels, in increasing order (mirrors the gating module).
VALID_LEVELS: tuple[str, ...] = ("Beginner", "Intermediate", "Advanced")

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_slug(text: str) -> str:
    """Lowercase, replace non-alphanumerics with hyphens, trim hyphens."""
    return _SLUG_RE.sub("-", text.strip().lower()).strip("-")


def with_translation[T](
    entity: T, *, title: str | None = None, description: str | None = None
) -> T:
    """Return a copy of a module/path with translated ``title``/``description``
    substituted, **per field, only when the translated value is non-empty**
    (English base value is kept otherwise). Both ``LearningModule`` and
    ``LearningPath`` are frozen dataclasses carrying those two fields."""
    updates: dict[str, str] = {}
    if title:
        updates["title"] = title
    if description:
        updates["description"] = description
    return replace(entity, **updates) if updates else entity  # type: ignore[type-var]


# ── Content catalogue (admin-managed; originally seeded) ──────────────


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
    # Courses this stage bundles. When non-empty, the module's per-user
    # completion is DERIVED from these courses (complete iff all are);
    # empty keeps the legacy self-reported progress behaviour.
    course_slugs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LearningPath:
    slug: str
    title: str
    description: str
    module_slugs: tuple[str, ...]
    estimated_time: str
    icon: str


@dataclass(frozen=True, slots=True)
class LearningTranslation:
    """A localized title/description for a module or path in one language."""

    language: str
    title: str
    description: str


def new_module(
    *,
    title: str,
    category: str,
    description: str,
    level: str,
    duration: str,
    icon: str,
    topics: tuple[str, ...] = (),
    course_slugs: tuple[str, ...] = (),
    slug: str | None = None,
) -> LearningModule:
    """Build a validated module. ``slug`` is derived from ``title`` when
    omitted; ``level`` must be one of ``VALID_LEVELS``. Referential
    validation of ``course_slugs`` against the catalogue is the use-case's
    job (it needs the course reader)."""
    if level not in VALID_LEVELS:
        raise LearningContentValidationError(f"level must be one of {VALID_LEVELS}, got {level!r}")
    effective_slug = normalize_slug(slug) if slug else normalize_slug(title)
    if not effective_slug:
        raise LearningContentValidationError("module slug/title must be non-empty")
    return LearningModule(
        slug=effective_slug,
        title=title,
        category=category,
        description=description,
        level=level,
        duration=duration,
        icon=icon,
        topics=tuple(topics),
        course_slugs=tuple(course_slugs),
    )


def new_path(
    *,
    title: str,
    description: str,
    module_slugs: tuple[str, ...],
    estimated_time: str,
    icon: str,
    slug: str | None = None,
) -> LearningPath:
    """Build a validated path. ``slug`` is derived from ``title`` when
    omitted. Referential validation of ``module_slugs`` against the
    catalogue is the use-case's job (needs the repository)."""
    effective_slug = normalize_slug(slug) if slug else normalize_slug(title)
    if not effective_slug:
        raise LearningContentValidationError("path slug/title must be non-empty")
    return LearningPath(
        slug=effective_slug,
        title=title,
        description=description,
        module_slugs=tuple(module_slugs),
        estimated_time=estimated_time,
        icon=icon,
    )


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
    # Optional enrollment-level deadline. None = no deadline set.
    due_at: datetime | None = None


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


def derived_module_percent(course_slugs: tuple[str, ...], percent_by_course: dict[str, int]) -> int:
    """A course-backed stage's percent = the mean of its courses' percents
    (a missing course counts as 0). Returns 100 only when EVERY linked
    course is at 100, so 'stage complete iff all its courses complete'
    holds. Empty ``course_slugs`` returns 0 (caller falls back to the
    self-reported percent)."""
    if not course_slugs:
        return 0
    total = sum(max(0, min(100, percent_by_course.get(slug, 0))) for slug in course_slugs)
    return total // len(course_slugs)


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

"""SQLAlchemy adapter for ``LearningRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    CertificateRow,
    EnrollmentRow,
    LearningModuleRow,
    LearningPathRow,
    ModuleProgressRow,
)
from cyberdyne_backend.domain.learning import (
    Certificate,
    Enrollment,
    EnrollmentNotFoundError,
    EnrollmentStatus,
    LearningContentConflictError,
    LearningContentNotFoundError,
    LearningModule,
    LearningPath,
    ModuleProgress,
)


def _row_to_module(row: LearningModuleRow) -> LearningModule:
    return LearningModule(
        slug=row.slug,
        title=row.title,
        category=row.category,
        description=row.description,
        level=row.level,
        duration=row.duration,
        icon=row.icon,
        topics=tuple(row.topics),
        course_slugs=tuple(row.course_slugs or ()),
    )


def _row_to_path(row: LearningPathRow) -> LearningPath:
    return LearningPath(
        slug=row.slug,
        title=row.title,
        description=row.description,
        module_slugs=tuple(row.module_slugs),
        estimated_time=row.estimated_time,
        icon=row.icon,
    )


def _as_utc(value: datetime | None) -> datetime | None:
    """SQLite drops tzinfo on read; re-attach UTC so domain comparisons
    against an aware ``now`` don't blow up. Postgres rows are already
    aware, so this is a no-op there."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_enrollment(row: EnrollmentRow) -> Enrollment:
    return Enrollment(
        id=row.id,
        user_id=row.user_id,
        path_slug=row.path_slug,
        started_at=row.started_at,
        status=EnrollmentStatus(row.status),
        due_at=_as_utc(row.due_at),
    )


def _row_to_progress(row: ModuleProgressRow) -> ModuleProgress:
    return ModuleProgress(
        id=row.id,
        user_id=row.user_id,
        module_slug=row.module_slug,
        percent=row.percent,
        started_at=row.started_at,
        completed_at=row.completed_at,
        updated_at=row.updated_at,
    )


def _row_to_cert(row: CertificateRow) -> Certificate:
    return Certificate(
        id=row.id,
        user_id=row.user_id,
        path_slug=row.path_slug,
        issued_at=row.issued_at,
        verification_hash=row.verification_hash,
        signed_payload=row.signed_payload,
    )


class SqlAlchemyLearningRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Catalogue ────────────────────────────────────────────────────
    async def list_modules(self) -> list[LearningModule]:
        rows = (
            (
                await self._session.execute(
                    select(LearningModuleRow).order_by(
                        LearningModuleRow.sort_order, LearningModuleRow.slug
                    )
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_module(r) for r in rows]

    async def list_paths(self) -> list[LearningPath]:
        rows = (
            (
                await self._session.execute(
                    select(LearningPathRow).order_by(
                        LearningPathRow.sort_order, LearningPathRow.slug
                    )
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_path(r) for r in rows]

    async def get_path(self, slug: str) -> LearningPath:
        row = await self._session.get(LearningPathRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning path with slug={slug!r}")
        return _row_to_path(row)

    async def get_module(self, slug: str) -> LearningModule:
        row = await self._session.get(LearningModuleRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning module with slug={slug!r}")
        return _row_to_module(row)

    # ── Catalogue writes (admin) ─────────────────────────────────────
    async def _next_sort_order(self, column: InstrumentedAttribute[int]) -> int:
        current = (await self._session.execute(select(func.max(column)))).scalar()
        return (current or 0) + 1

    async def create_module(self, module: LearningModule) -> LearningModule:
        if await self._session.get(LearningModuleRow, module.slug) is not None:
            raise LearningContentConflictError(f"learning module {module.slug!r} already exists")
        row = LearningModuleRow(
            slug=module.slug,
            title=module.title,
            category=module.category,
            description=module.description,
            level=module.level,
            duration=module.duration,
            icon=module.icon,
            topics=list(module.topics),
            course_slugs=list(module.course_slugs),
            sort_order=await self._next_sort_order(LearningModuleRow.sort_order),
        )
        self._session.add(row)
        await self._session.flush()
        return _row_to_module(row)

    async def update_module(
        self,
        slug: str,
        *,
        title: str | None = None,
        category: str | None = None,
        description: str | None = None,
        level: str | None = None,
        duration: str | None = None,
        icon: str | None = None,
        topics: tuple[str, ...] | None = None,
        course_slugs: tuple[str, ...] | None = None,
    ) -> LearningModule:
        row = await self._session.get(LearningModuleRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning module with slug={slug!r}")
        if title is not None:
            row.title = title
        if category is not None:
            row.category = category
        if description is not None:
            row.description = description
        if level is not None:
            row.level = level
        if duration is not None:
            row.duration = duration
        if icon is not None:
            row.icon = icon
        if topics is not None:
            row.topics = list(topics)
        if course_slugs is not None:
            row.course_slugs = list(course_slugs)
        await self._session.flush()
        return _row_to_module(row)

    async def delete_module(self, slug: str) -> None:
        row = await self._session.get(LearningModuleRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning module with slug={slug!r}")
        await self._session.delete(row)
        await self._session.flush()

    async def create_path(self, path: LearningPath) -> LearningPath:
        if await self._session.get(LearningPathRow, path.slug) is not None:
            raise LearningContentConflictError(f"learning path {path.slug!r} already exists")
        row = LearningPathRow(
            slug=path.slug,
            title=path.title,
            description=path.description,
            module_slugs=list(path.module_slugs),
            estimated_time=path.estimated_time,
            icon=path.icon,
            sort_order=await self._next_sort_order(LearningPathRow.sort_order),
        )
        self._session.add(row)
        await self._session.flush()
        return _row_to_path(row)

    async def update_path(
        self,
        slug: str,
        *,
        title: str | None = None,
        description: str | None = None,
        module_slugs: tuple[str, ...] | None = None,
        estimated_time: str | None = None,
        icon: str | None = None,
    ) -> LearningPath:
        row = await self._session.get(LearningPathRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning path with slug={slug!r}")
        if title is not None:
            row.title = title
        if description is not None:
            row.description = description
        if module_slugs is not None:
            row.module_slugs = list(module_slugs)
        if estimated_time is not None:
            row.estimated_time = estimated_time
        if icon is not None:
            row.icon = icon
        await self._session.flush()
        return _row_to_path(row)

    async def delete_path(self, slug: str) -> None:
        row = await self._session.get(LearningPathRow, slug)
        if row is None:
            raise LearningContentNotFoundError(f"no learning path with slug={slug!r}")
        await self._session.delete(row)
        await self._session.flush()

    # ── Enrollments ──────────────────────────────────────────────────
    async def upsert_enrollment(self, enrollment: Enrollment) -> Enrollment:
        existing = (
            await self._session.execute(
                select(EnrollmentRow).where(
                    EnrollmentRow.user_id == enrollment.user_id,
                    EnrollmentRow.path_slug == enrollment.path_slug,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            return _row_to_enrollment(existing)
        self._session.add(
            EnrollmentRow(
                id=enrollment.id,
                user_id=enrollment.user_id,
                path_slug=enrollment.path_slug,
                started_at=enrollment.started_at,
                status=enrollment.status.value,
                due_at=enrollment.due_at,
            )
        )
        await self._session.flush()
        return enrollment

    async def set_enrollment_deadline(
        self, *, user_id: UUID, path_slug: str, due_at: datetime | None
    ) -> Enrollment:
        existing = (
            await self._session.execute(
                select(EnrollmentRow).where(
                    EnrollmentRow.user_id == user_id,
                    EnrollmentRow.path_slug == path_slug,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            raise EnrollmentNotFoundError(f"user {user_id} is not enrolled in {path_slug!r}")
        existing.due_at = due_at
        await self._session.flush()
        return _row_to_enrollment(existing)

    async def list_enrollments_for_user(self, user_id: UUID) -> list[Enrollment]:
        rows = (
            (
                await self._session.execute(
                    select(EnrollmentRow)
                    .where(EnrollmentRow.user_id == user_id)
                    .order_by(EnrollmentRow.started_at.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_enrollment(r) for r in rows]

    # ── Progress ─────────────────────────────────────────────────────
    async def upsert_progress(self, progress: ModuleProgress) -> ModuleProgress:
        existing = (
            await self._session.execute(
                select(ModuleProgressRow).where(
                    ModuleProgressRow.user_id == progress.user_id,
                    ModuleProgressRow.module_slug == progress.module_slug,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            self._session.add(
                ModuleProgressRow(
                    id=progress.id,
                    user_id=progress.user_id,
                    module_slug=progress.module_slug,
                    percent=progress.percent,
                    started_at=progress.started_at,
                    completed_at=progress.completed_at,
                    updated_at=progress.updated_at,
                )
            )
        else:
            existing.percent = progress.percent
            existing.completed_at = progress.completed_at
            existing.updated_at = progress.updated_at
        await self._session.flush()
        return progress

    async def get_progress_map_for_user(self, user_id: UUID) -> dict[str, ModuleProgress]:
        rows = (
            (
                await self._session.execute(
                    select(ModuleProgressRow).where(ModuleProgressRow.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        return {r.module_slug: _row_to_progress(r) for r in rows}

    # ── Certificates ─────────────────────────────────────────────────
    async def save_certificate(self, certificate: Certificate) -> None:
        existing = (
            await self._session.execute(
                select(CertificateRow).where(
                    CertificateRow.user_id == certificate.user_id,
                    CertificateRow.path_slug == certificate.path_slug,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            # Re-issue idempotently — overwrite the signature blob with
            # the fresher one.
            existing.issued_at = certificate.issued_at
            existing.verification_hash = certificate.verification_hash
            existing.signed_payload = certificate.signed_payload
        else:
            self._session.add(
                CertificateRow(
                    id=certificate.id,
                    user_id=certificate.user_id,
                    path_slug=certificate.path_slug,
                    issued_at=certificate.issued_at,
                    verification_hash=certificate.verification_hash,
                    signed_payload=certificate.signed_payload,
                )
            )
        await self._session.flush()

    async def get_certificate_for_user_and_path(
        self, user_id: UUID, path_slug: str
    ) -> Certificate | None:
        row = (
            await self._session.execute(
                select(CertificateRow).where(
                    CertificateRow.user_id == user_id,
                    CertificateRow.path_slug == path_slug,
                )
            )
        ).scalar_one_or_none()
        return _row_to_cert(row) if row else None

    async def get_certificate_by_id(self, certificate_id: UUID) -> Certificate | None:
        row = await self._session.get(CertificateRow, certificate_id)
        return _row_to_cert(row) if row else None

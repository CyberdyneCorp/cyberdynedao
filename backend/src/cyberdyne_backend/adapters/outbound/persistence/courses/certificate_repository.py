"""SQLAlchemy adapter for ``CourseCertificateRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CourseCertificateRow,
)
from cyberdyne_backend.domain.courses import CourseCertificate


def _as_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo on read; re-attach UTC. No-op on Postgres."""
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value


def _row_to_cert(row: CourseCertificateRow) -> CourseCertificate:
    return CourseCertificate(
        id=row.id,
        user_id=row.user_id,
        course_slug=row.course_slug,
        issued_at=_as_utc(row.issued_at),
        verification_hash=row.verification_hash,
        signed_payload=row.signed_payload,
    )


class SqlAlchemyCourseCertificateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, certificate: CourseCertificate) -> None:
        self._session.add(
            CourseCertificateRow(
                id=certificate.id,
                user_id=certificate.user_id,
                course_slug=certificate.course_slug,
                issued_at=certificate.issued_at,
                verification_hash=certificate.verification_hash,
                signed_payload=certificate.signed_payload,
            )
        )
        await self._session.flush()

    async def get_for_user_and_course(
        self, *, user_id: UUID, course_slug: str
    ) -> CourseCertificate | None:
        row = (
            await self._session.execute(
                select(CourseCertificateRow).where(
                    CourseCertificateRow.user_id == user_id,
                    CourseCertificateRow.course_slug == course_slug,
                )
            )
        ).scalar_one_or_none()
        return _row_to_cert(row) if row is not None else None

    async def get_by_id(self, certificate_id: UUID) -> CourseCertificate | None:
        row = await self._session.get(CourseCertificateRow, certificate_id)
        return _row_to_cert(row) if row is not None else None

    async def list_for_user(self, user_id: UUID) -> list[CourseCertificate]:
        rows = (
            (
                await self._session.execute(
                    select(CourseCertificateRow).where(CourseCertificateRow.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_cert(row) for row in rows]

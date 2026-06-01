"""SQLAlchemy adapter for ``UploadRepository``."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.uploads.models import UploadRow
from cyberdyne_backend.domain.uploads import (
    StoredFile,
    UploadCategory,
    UploadNotFoundError,
)


def _row_to_stored(row: UploadRow) -> StoredFile:
    return StoredFile(
        id=row.id,
        original_filename=row.original_filename,
        stored_filename=row.stored_filename,
        category=UploadCategory(row.category),
        content_type=row.content_type,
        size_bytes=row.size_bytes,
        relative_path=row.relative_path,
        url=row.url,
        uploaded_by=row.uploaded_by,
        created_at=row.created_at,
    )


class SqlAlchemyUploadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, stored: StoredFile) -> None:
        self._session.add(
            UploadRow(
                id=stored.id,
                original_filename=stored.original_filename,
                stored_filename=stored.stored_filename,
                category=stored.category.value,
                content_type=stored.content_type,
                size_bytes=stored.size_bytes,
                relative_path=stored.relative_path,
                url=stored.url,
                uploaded_by=stored.uploaded_by,
                created_at=stored.created_at,
            )
        )
        await self._session.flush()

    async def get(self, upload_id: UUID) -> StoredFile:
        row = await self._session.get(UploadRow, upload_id)
        if row is None:
            raise UploadNotFoundError(str(upload_id))
        return _row_to_stored(row)

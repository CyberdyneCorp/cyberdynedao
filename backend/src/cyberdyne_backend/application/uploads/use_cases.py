"""Use cases for the uploads context.

The inbound adapter reads the raw bytes (enforcing the hard global cap
while streaming) and hands ``(filename, content_type, data)`` here.
``SaveUpload`` then classifies the MIME, enforces the precise per-category
cap, mints a traversal-proof stored name, writes via the storage port,
records metadata, and returns the ``StoredFile``.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.uploads import (
    FileStorage,
    StoredFile,
    UploadRepository,
    build_stored_filename,
    classify,
    new_stored_file,
    validate_size,
)


@dataclass(slots=True)
class UploadInput:
    filename: str
    content_type: str
    data: bytes


@dataclass(slots=True)
class SaveUpload:
    repo: UploadRepository
    storage: FileStorage
    media_url_prefix: str

    async def execute(self, item: UploadInput, *, uploaded_by: UUID | None = None) -> StoredFile:
        classification = classify(item.content_type)
        validate_size(classification, len(item.data))
        stored_filename = build_stored_filename(classification)
        relative_path = await self.storage.save(
            category=classification.category,
            stored_filename=stored_filename,
            data=item.data,
        )
        url = f"{self.media_url_prefix.rstrip('/')}/{relative_path}"
        stored = new_stored_file(
            original_filename=item.filename,
            content_type=item.content_type,
            size_bytes=len(item.data),
            classification=classification,
            stored_filename=stored_filename,
            relative_path=relative_path,
            url=url,
            uploaded_by=uploaded_by,
        )
        await self.repo.save(stored)
        return stored


@dataclass(slots=True)
class SaveUploads:
    """Batch wrapper around ``SaveUpload`` — all-or-nothing within the
    request's transaction (a raise rolls the session back)."""

    inner: SaveUpload

    async def execute(
        self, items: list[UploadInput], *, uploaded_by: UUID | None = None
    ) -> list[StoredFile]:
        return [await self.inner.execute(item, uploaded_by=uploaded_by) for item in items]


@dataclass(slots=True)
class GetUpload:
    repo: UploadRepository

    async def execute(self, upload_id: UUID) -> StoredFile:
        return await self.repo.get(upload_id)


__all__ = [
    "GetUpload",
    "SaveUpload",
    "SaveUploads",
    "UploadInput",
]

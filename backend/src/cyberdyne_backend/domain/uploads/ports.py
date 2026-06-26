"""Ports the uploads context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.uploads.entities import StoredFile, UploadCategory


@runtime_checkable
class FileStorage(Protocol):
    async def save(self, *, category: UploadCategory, stored_filename: str, data: bytes) -> str:
        """Persist ``data`` under ``<category>/<stored_filename>`` and
        return the storage-relative path. Implementations must refuse any
        path that would resolve outside the storage root."""
        ...

    async def delete(self, relative_path: str) -> None:
        """Remove a stored object. No-op if it doesn't exist."""
        ...

    async def read(self, relative_path: str) -> bytes:
        """Return the bytes of a stored object addressed by its
        ``<category>/<stored_filename>`` relative path. Raises
        ``UploadNotFoundError`` if the object is missing."""
        ...


@runtime_checkable
class UploadRepository(Protocol):
    async def save(self, stored: StoredFile) -> None: ...

    async def get(self, upload_id: UUID) -> StoredFile:
        """Raises ``UploadNotFoundError`` if absent."""
        ...

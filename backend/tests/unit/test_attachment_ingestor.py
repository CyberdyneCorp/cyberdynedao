"""UploadAttachmentIngestor: image → vision, doc → extract, unknown → skip."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

import pytest

from cyberdyne_backend.adapters.outbound.attachments import UploadAttachmentIngestor
from cyberdyne_backend.domain.uploads import (
    StoredFile,
    UploadCategory,
    UploadNotFoundError,
)

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


def _stored(category: UploadCategory, *, content_type: str, name: str) -> StoredFile:
    return StoredFile(
        id=uuid.uuid4(),
        original_filename=name,
        stored_filename=f"{uuid.uuid4().hex}",
        category=category,
        content_type=content_type,
        size_bytes=4,
        relative_path=f"{category.value}/stored",
        url="/media/x",
        uploaded_by=None,
        created_at=datetime(2026, 6, 26, tzinfo=UTC),
    )


class _FakeUploadRepo:
    def __init__(self, files: dict[UUID, StoredFile]) -> None:
        self._files = files

    async def save(self, stored: StoredFile) -> None:  # pragma: no cover
        self._files[stored.id] = stored

    async def get(self, upload_id: UUID) -> StoredFile:
        if upload_id not in self._files:
            raise UploadNotFoundError(str(upload_id))
        return self._files[upload_id]


class _FakeStorage:
    async def save(self, *, category, stored_filename, data):  # pragma: no cover
        return f"{category.value}/{stored_filename}"

    async def delete(self, relative_path: str) -> None:  # pragma: no cover
        return None

    async def read(self, relative_path: str) -> bytes:
        return b"raw-bytes"


class _FakeVision:
    async def describe_image(self, *, image_bytes, content_type, prompt) -> str:
        return "a vision description"


class _FakeExtractor:
    async def extract(self, *, data: bytes, content_type: str) -> str:
        return f"extracted:{content_type}"


def _ingestor(files: dict[UUID, StoredFile]) -> UploadAttachmentIngestor:
    return UploadAttachmentIngestor(
        repo=_FakeUploadRepo(files),
        storage=_FakeStorage(),
        extractor=_FakeExtractor(),
        vision=_FakeVision(),
    )


async def test_image_goes_to_vision() -> None:
    img = _stored(UploadCategory.IMAGE, content_type="image/png", name="pic.png")
    result = await _ingestor({img.id: img}).ingest((img.id,))
    assert len(result) == 1
    assert result[0].text == "a vision description"
    assert result[0].ref.filename == "pic.png"
    assert result[0].ref.content_type == "image/png"


async def test_document_goes_to_extractor() -> None:
    doc = _stored(UploadCategory.DOCUMENT, content_type="text/csv", name="data.csv")
    result = await _ingestor({doc.id: doc}).ingest((doc.id,))
    assert len(result) == 1
    assert result[0].text == "extracted:text/csv"
    assert result[0].ref.id == doc.id


async def test_unknown_id_is_skipped() -> None:
    doc = _stored(UploadCategory.DOCUMENT, content_type="text/csv", name="data.csv")
    missing = uuid.uuid4()
    result = await _ingestor({doc.id: doc}).ingest((missing, doc.id))
    assert len(result) == 1
    assert result[0].ref.id == doc.id

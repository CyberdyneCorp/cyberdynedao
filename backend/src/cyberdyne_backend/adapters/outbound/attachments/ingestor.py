"""Resolve stored upload ids into grounded attachment content.

For each id: load the stored file's metadata + bytes, then route by
category — images go to the vision port (description / OCR), everything
else to the text extractor. Ids that don't resolve (deleted / unknown)
are skipped, so a stale reference never fails the whole turn.
"""

from __future__ import annotations

from uuid import UUID

from cyberdyne_backend.domain.ai_chat import (
    AttachmentRef,
    IngestedAttachment,
    TextExtractorPort,
    VisionPort,
)
from cyberdyne_backend.domain.uploads import (
    FileStorage,
    UploadCategory,
    UploadNotFoundError,
    UploadRepository,
)

_VISION_PROMPT = (
    "Describe this image and transcribe any text in it (OCR) so it can be "
    "used to answer a question about it. Be concise and factual."
)


class UploadAttachmentIngestor:
    def __init__(
        self,
        *,
        repo: UploadRepository,
        storage: FileStorage,
        extractor: TextExtractorPort,
        vision: VisionPort,
    ) -> None:
        self._repo = repo
        self._storage = storage
        self._extractor = extractor
        self._vision = vision

    async def ingest(self, upload_ids: tuple[UUID, ...]) -> tuple[IngestedAttachment, ...]:
        ingested: list[IngestedAttachment] = []
        for upload_id in upload_ids:
            item = await self._ingest_one(upload_id)
            if item is not None:
                ingested.append(item)
        return tuple(ingested)

    async def _ingest_one(self, upload_id: UUID) -> IngestedAttachment | None:
        try:
            stored = await self._repo.get(upload_id)
        except UploadNotFoundError:
            return None
        try:
            data = await self._storage.read(stored.relative_path)
        except UploadNotFoundError:
            return None
        if stored.category == UploadCategory.IMAGE:
            text = await self._vision.describe_image(
                image_bytes=data,
                content_type=stored.content_type,
                prompt=_VISION_PROMPT,
            )
        else:
            text = await self._extractor.extract(data=data, content_type=stored.content_type)
        ref = AttachmentRef(
            id=stored.id,
            filename=stored.original_filename,
            content_type=stored.content_type,
        )
        return IngestedAttachment(ref=ref, text=text)

"""Attachment ingestion adapters for the AI tutor (issue #220).

``MultiFormatTextExtractor`` turns document bytes (PDF/DOCX/CSV/XLSX/text)
into plain text; ``UploadAttachmentIngestor`` resolves stored upload ids to
their content — extracting documents or vision-describing images — so the
tutor can answer grounded in attached files.
"""

from cyberdyne_backend.adapters.outbound.attachments.extractor import (
    MultiFormatTextExtractor,
)
from cyberdyne_backend.adapters.outbound.attachments.ingestor import (
    UploadAttachmentIngestor,
)

__all__ = [
    "MultiFormatTextExtractor",
    "UploadAttachmentIngestor",
]

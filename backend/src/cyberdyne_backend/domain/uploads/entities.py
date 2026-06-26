"""Uploads domain — media policy, filename safety, and the StoredFile.

The policy here is the single source of truth for what may be uploaded:
the MIME allow-list, the category each type routes to, and the per-
category size cap. Filename sanitisation strips any path component so a
malicious ``../../etc/passwd`` or an absolute path can never escape the
storage root — the stored name is always a fresh UUID plus the validated
extension, and the original name is kept only as display metadata.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.uploads.errors import (
    FileTooLargeError,
    UnsafeFilenameError,
    UnsupportedMediaTypeError,
)

_MB = 1024 * 1024


class UploadCategory(StrEnum):
    IMAGE = "image"
    DOCUMENT = "document"
    PRESENTATION = "presentation"
    VIDEO = "video"


# MIME → (category, extension). The extension is authoritative — we never
# trust the client-supplied filename extension for the stored file.
_MIME_TABLE: dict[str, tuple[UploadCategory, str]] = {
    "image/png": (UploadCategory.IMAGE, ".png"),
    "image/jpeg": (UploadCategory.IMAGE, ".jpg"),
    "image/webp": (UploadCategory.IMAGE, ".webp"),
    "image/gif": (UploadCategory.IMAGE, ".gif"),
    "application/pdf": (UploadCategory.DOCUMENT, ".pdf"),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
        UploadCategory.DOCUMENT,
        ".docx",
    ),
    "text/csv": (UploadCategory.DOCUMENT, ".csv"),
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        UploadCategory.DOCUMENT,
        ".xlsx",
    ),
    "application/vnd.ms-powerpoint": (UploadCategory.PRESENTATION, ".ppt"),
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": (
        UploadCategory.PRESENTATION,
        ".pptx",
    ),
    "video/mp4": (UploadCategory.VIDEO, ".mp4"),
    "video/webm": (UploadCategory.VIDEO, ".webm"),
    "video/ogg": (UploadCategory.VIDEO, ".ogv"),
}

# Per-category size caps (bytes).
_SIZE_CAPS: dict[UploadCategory, int] = {
    UploadCategory.IMAGE: 10 * _MB,
    UploadCategory.DOCUMENT: 25 * _MB,
    UploadCategory.PRESENTATION: 50 * _MB,
    UploadCategory.VIDEO: 200 * _MB,
}

# Largest cap across categories — the inbound adapter uses this as the
# hard read ceiling before the category is even known.
MAX_UPLOAD_BYTES = max(_SIZE_CAPS.values())

_SAFE_BASENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True, slots=True)
class MediaClassification:
    category: UploadCategory
    extension: str
    max_bytes: int


def classify(content_type: str) -> MediaClassification:
    """Map a MIME type to its category + canonical extension + cap.

    Raises ``UnsupportedMediaTypeError`` for anything off the allow-list.
    """
    # Normalise ``image/png; charset=...`` style values.
    mime = content_type.split(";", 1)[0].strip().lower()
    entry = _MIME_TABLE.get(mime)
    if entry is None:
        raise UnsupportedMediaTypeError(content_type)
    category, extension = entry
    return MediaClassification(
        category=category, extension=extension, max_bytes=_SIZE_CAPS[category]
    )


def validate_size(classification: MediaClassification, size_bytes: int) -> None:
    if size_bytes > classification.max_bytes:
        raise FileTooLargeError(
            f"{classification.category.value} upload is {size_bytes} bytes; "
            f"cap is {classification.max_bytes}"
        )


def safe_display_name(original_filename: str) -> str:
    """Reduce a client filename to a safe display basename.

    Drops any directory component (both ``/`` and ``\\``), strips leading
    dots, and replaces unsafe characters. Raises ``UnsafeFilenameError``
    if nothing usable remains.
    """
    # Take the last path segment for either separator.
    base = original_filename.replace("\\", "/").split("/")[-1].strip()
    base = base.lstrip(".")  # no leading-dot hidden/relative names
    base = _SAFE_BASENAME_RE.sub("_", base)
    base = base.strip("._")
    if not base:
        raise UnsafeFilenameError(original_filename)
    return base[:200]


def build_stored_filename(classification: MediaClassification) -> str:
    """A collision-free, traversal-proof stored name: ``<uuid><ext>``."""
    return f"{uuid.uuid4().hex}{classification.extension}"


@dataclass(slots=True)
class StoredFile:
    id: UUID
    original_filename: str
    stored_filename: str
    category: UploadCategory
    content_type: str
    size_bytes: int
    relative_path: str
    url: str
    uploaded_by: UUID | None
    created_at: datetime


def new_stored_file(
    *,
    original_filename: str,
    content_type: str,
    size_bytes: int,
    classification: MediaClassification,
    stored_filename: str,
    relative_path: str,
    url: str,
    uploaded_by: UUID | None = None,
    now: datetime | None = None,
) -> StoredFile:
    return StoredFile(
        id=uuid.uuid4(),
        original_filename=safe_display_name(original_filename),
        stored_filename=stored_filename,
        category=classification.category,
        content_type=content_type.split(";", 1)[0].strip().lower(),
        size_bytes=size_bytes,
        relative_path=relative_path,
        url=url,
        uploaded_by=uploaded_by,
        created_at=now or datetime.now(tz=UTC),
    )

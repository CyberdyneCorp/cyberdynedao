"""Uploads bounded context.

Admin-only media uploads for course/lesson content: images, PDFs,
presentations, and video. The domain owns the MIME allow-list, the
category routing, the per-category size caps, and filename safety;
adapters provide the storage backend (local disk) and metadata
persistence. Stored files are served read-only under a media URL prefix.
"""

from cyberdyne_backend.domain.uploads.entities import (
    MAX_UPLOAD_BYTES,
    MediaClassification,
    StoredFile,
    UploadCategory,
    build_stored_filename,
    classify,
    new_stored_file,
    safe_display_name,
    validate_size,
)
from cyberdyne_backend.domain.uploads.errors import (
    FileTooLargeError,
    UnsafeFilenameError,
    UnsupportedMediaTypeError,
    UploadNotFoundError,
)
from cyberdyne_backend.domain.uploads.ports import (
    FileStorage,
    UploadRepository,
)

__all__ = [
    "MAX_UPLOAD_BYTES",
    "FileStorage",
    "FileTooLargeError",
    "MediaClassification",
    "StoredFile",
    "UnsafeFilenameError",
    "UnsupportedMediaTypeError",
    "UploadCategory",
    "UploadNotFoundError",
    "UploadRepository",
    "build_stored_filename",
    "classify",
    "new_stored_file",
    "safe_display_name",
    "validate_size",
]

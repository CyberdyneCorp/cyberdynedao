"""Domain errors for the uploads context."""

from __future__ import annotations


class UnsupportedMediaTypeError(ValueError):
    """The uploaded content type isn't on the allow-list."""


class FileTooLargeError(ValueError):
    """The upload exceeds the size cap for its category."""


class UnsafeFilenameError(ValueError):
    """The original filename can't be reduced to a safe basename
    (path-traversal attempt, empty after sanitisation, etc.)."""


class UploadNotFoundError(LookupError):
    """No stored upload with the requested id."""

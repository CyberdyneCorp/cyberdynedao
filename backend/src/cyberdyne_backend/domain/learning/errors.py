"""Domain errors for the learning context."""

from __future__ import annotations


class LearningContentNotFoundError(LookupError):
    """Module / path with that slug doesn't exist."""


class LearningContentConflictError(Exception):
    """A module / path with that slug already exists."""


class LearningContentValidationError(ValueError):
    """Invalid catalogue content — an unknown level, or a path referencing
    a module slug that doesn't exist."""


class EnrollmentNotFoundError(LookupError):
    """User isn't enrolled in this path."""


class ProgressOutOfRangeError(ValueError):
    """Progress percent must be in [0, 100]."""


class CertificateNotEligibleError(ValueError):
    """The user hasn't completed every module in the path."""


class CertificateNotFoundError(LookupError):
    """No certificate exists with that id."""

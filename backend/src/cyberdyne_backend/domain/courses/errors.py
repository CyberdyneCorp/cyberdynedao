"""Domain errors for the courses context."""

from __future__ import annotations


class CourseNotFoundError(LookupError):
    """No course with the requested slug exists (or it's a draft and the
    caller has no editor scope)."""


class LessonNotFoundError(LookupError):
    """No lesson with the requested id exists within the course."""


class DuplicateCourseSlugError(ValueError):
    """A course with this slug already exists."""


class InvalidLessonContentError(ValueError):
    """A lesson's content doesn't satisfy the invariants for its type
    (e.g. a ``video`` lesson with no ``content_url``, or a ``text``
    lesson with no ``text_body``)."""


class InvalidCourseLevelError(ValueError):
    """The requested level is not one of Beginner/Intermediate/Advanced."""


class ProgressOutOfRangeError(ValueError):
    """A lesson-progress percent fell outside the 0..100 range."""


class CourseCertificateNotEligibleError(ValueError):
    """The learner hasn't completed every lesson, so no certificate can
    be issued for the course yet."""


class CourseCertificateNotFoundError(LookupError):
    """No course certificate with the requested id exists."""

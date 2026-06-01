"""Courses bounded context.

Admin-authored teaching material: a catalogue of courses (levels,
publish state, mandatory flag, drag-to-reorder) each holding an ordered
list of typed lessons (video / pdf / presentation / text / quiz).
Public read is unauthenticated and shows published courses only; all
writes require the ``editor`` scope.
"""

from cyberdyne_backend.domain.courses.entities import (
    Course,
    CourseLevel,
    CourseStatus,
    Lesson,
    LessonType,
    new_course,
    new_lesson,
    normalize_slug,
    parse_level,
)
from cyberdyne_backend.domain.courses.errors import (
    CourseNotFoundError,
    DuplicateCourseSlugError,
    InvalidCourseLevelError,
    InvalidLessonContentError,
    LessonNotFoundError,
)
from cyberdyne_backend.domain.courses.ports import (
    CourseRepository,
)

__all__ = [
    "Course",
    "CourseLevel",
    "CourseNotFoundError",
    "CourseRepository",
    "CourseStatus",
    "DuplicateCourseSlugError",
    "InvalidCourseLevelError",
    "InvalidLessonContentError",
    "Lesson",
    "LessonNotFoundError",
    "LessonType",
    "new_course",
    "new_lesson",
    "normalize_slug",
    "parse_level",
]

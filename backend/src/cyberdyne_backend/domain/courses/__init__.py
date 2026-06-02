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
    ProgressOutOfRangeError,
)
from cyberdyne_backend.domain.courses.ports import (
    CourseProgressRepository,
    CourseRepository,
)
from cyberdyne_backend.domain.courses.progress import (
    CourseProgress,
    LessonProgress,
    LessonProgressView,
    build_course_progress,
    new_lesson_progress,
)

__all__ = [
    "Course",
    "CourseLevel",
    "CourseNotFoundError",
    "CourseProgress",
    "CourseProgressRepository",
    "CourseRepository",
    "CourseStatus",
    "DuplicateCourseSlugError",
    "InvalidCourseLevelError",
    "InvalidLessonContentError",
    "Lesson",
    "LessonNotFoundError",
    "LessonProgress",
    "LessonProgressView",
    "LessonType",
    "ProgressOutOfRangeError",
    "build_course_progress",
    "new_course",
    "new_lesson",
    "new_lesson_progress",
    "normalize_slug",
    "parse_level",
]

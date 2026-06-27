"""Courses bounded context.

Admin-authored teaching material: a catalogue of courses (levels,
publish state, mandatory flag, drag-to-reorder) each holding an ordered
list of typed lessons (video / pdf / presentation / text / quiz).
Public read is unauthenticated and shows published courses only; all
writes require the ``editor`` scope.
"""

from cyberdyne_backend.domain.courses.certificates import (
    CourseCertificate,
    course_certificate_eligible,
    new_course_certificate,
)
from cyberdyne_backend.domain.courses.entities import (
    MAX_COURSE_LIST_LIMIT,
    Category,
    Course,
    CourseLevel,
    CourseStatus,
    Lesson,
    LessonType,
    new_category,
    new_course,
    new_lesson,
    normalize_slug,
    parse_level,
)
from cyberdyne_backend.domain.courses.errors import (
    CategoryNotFoundError,
    CourseCertificateNotEligibleError,
    CourseCertificateNotFoundError,
    CourseNotFoundError,
    DuplicateCategorySlugError,
    DuplicateCourseSlugError,
    InvalidCourseLevelError,
    InvalidLessonContentError,
    LessonNotFoundError,
    ProgressOutOfRangeError,
)
from cyberdyne_backend.domain.courses.ports import (
    CategoryRepository,
    CourseCertificateAwarder,
    CourseCertificatePdfRenderer,
    CourseCertificateRepository,
    CourseCertificateSigner,
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
    "MAX_COURSE_LIST_LIMIT",
    "Category",
    "CategoryNotFoundError",
    "CategoryRepository",
    "Course",
    "CourseCertificate",
    "CourseCertificateAwarder",
    "CourseCertificateNotEligibleError",
    "CourseCertificateNotFoundError",
    "CourseCertificatePdfRenderer",
    "CourseCertificateRepository",
    "CourseCertificateSigner",
    "CourseLevel",
    "CourseNotFoundError",
    "CourseProgress",
    "CourseProgressRepository",
    "CourseRepository",
    "CourseStatus",
    "DuplicateCategorySlugError",
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
    "course_certificate_eligible",
    "new_category",
    "new_course",
    "new_course_certificate",
    "new_lesson",
    "new_lesson_progress",
    "normalize_slug",
    "parse_level",
]

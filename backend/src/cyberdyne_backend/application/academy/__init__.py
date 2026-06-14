"""Academy cross-context application services (course + quiz i18n)."""

from cyberdyne_backend.application.academy.jobs import (
    MAX_ATTEMPTS,
    TranslateCourseFactory,
    TranslateCourseScope,
    TranslationJob,
    TranslationJobStore,
    TranslationWorker,
)
from cyberdyne_backend.application.academy.translation import (
    SUPPORTED_LANGUAGES,
    MarkdownAwareTranslator,
    TranslateAcademy,
    TranslationRepository,
    TranslationStats,
    content_hash,
)
from cyberdyne_backend.application.academy.use_cases import (
    GetCourseLanguages,
    TranslateCourse,
)

__all__ = [
    "MAX_ATTEMPTS",
    "SUPPORTED_LANGUAGES",
    "GetCourseLanguages",
    "MarkdownAwareTranslator",
    "TranslateAcademy",
    "TranslateCourse",
    "TranslateCourseFactory",
    "TranslateCourseScope",
    "TranslationJob",
    "TranslationJobStore",
    "TranslationRepository",
    "TranslationStats",
    "TranslationWorker",
    "content_hash",
]

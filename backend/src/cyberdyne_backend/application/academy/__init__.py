"""Academy cross-context application services (course + quiz i18n)."""

from cyberdyne_backend.application.academy.jobs import (
    MAX_ATTEMPTS,
    TranslateCourseFactory,
    TranslateCourseScope,
    TranslationJob,
    TranslationJobStore,
    TranslationJobView,
    TranslationWorker,
    summarize_failures,
)
from cyberdyne_backend.application.academy.translation import (
    SUPPORTED_LANGUAGES,
    MarkdownAwareTranslator,
    TranslateAcademy,
    TranslationFailure,
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
    "TranslationFailure",
    "TranslationJob",
    "TranslationJobStore",
    "TranslationJobView",
    "TranslationRepository",
    "TranslationStats",
    "TranslationWorker",
    "content_hash",
    "summarize_failures",
]

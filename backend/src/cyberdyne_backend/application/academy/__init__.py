"""Academy cross-context application services (course + quiz i18n)."""

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
    "SUPPORTED_LANGUAGES",
    "GetCourseLanguages",
    "MarkdownAwareTranslator",
    "TranslateAcademy",
    "TranslateCourse",
    "TranslationRepository",
    "TranslationStats",
    "content_hash",
]

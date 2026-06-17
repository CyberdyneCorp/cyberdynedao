"""Lesson-notes bounded context.

Per-user, lesson-scoped annotations (optional highlighted quote + note
body) that the client syncs from on-device storage. Distinct from the
richer `notebook` context — this is the precise slice the Learn client
already uses. See issue #188.
"""

from cyberdyne_backend.domain.lesson_notes.entities import (
    LessonNote,
    LessonNotePage,
    new_lesson_note,
)
from cyberdyne_backend.domain.lesson_notes.errors import (
    InvalidLessonNoteError,
    LessonNoteNotFoundError,
)
from cyberdyne_backend.domain.lesson_notes.ports import LessonNoteRepository

__all__ = [
    "InvalidLessonNoteError",
    "LessonNote",
    "LessonNoteNotFoundError",
    "LessonNotePage",
    "LessonNoteRepository",
    "new_lesson_note",
]

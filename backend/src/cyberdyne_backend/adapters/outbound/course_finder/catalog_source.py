"""Catalog text source for Scan-to-Learn (issue #231).

Adapts the courses ``CourseRepository`` into the ``CatalogTextSource`` port: one
indexable text per PUBLISHED course (``"{title}. {description}"``) plus one per
lesson (``"{course title} — {lesson title}"``). Drafts are skipped. The yielded
entries carry no vectors — the index embeds them.
"""

from __future__ import annotations

from cyberdyne_backend.domain.course_finder import CatalogEntry
from cyberdyne_backend.domain.courses import CourseRepository


class CourseCatalogTextSource:
    def __init__(self, *, courses: CourseRepository) -> None:
        self._courses = courses

    async def entries(self) -> list[CatalogEntry]:
        # ``list_courses`` already filters drafts (include_drafts defaults to
        # False) and includes lessons in one round-trip.
        courses = await self._courses.list_courses()
        entries: list[CatalogEntry] = []
        for course in courses:
            course_text = f"{course.title}. {course.description}".strip()
            entries.append(CatalogEntry(course_slug=course.slug, lesson_id=None, text=course_text))
            for lesson in course.lessons:
                entries.append(
                    CatalogEntry(
                        course_slug=course.slug,
                        lesson_id=lesson.id,
                        text=f"{course.title} — {lesson.title}",
                    )
                )
        return entries

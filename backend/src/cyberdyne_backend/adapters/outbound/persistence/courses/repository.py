"""SQLAlchemy adapter for ``CourseRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CategoryRow,
    CourseRow,
    CourseTranslationRow,
    LessonRow,
    LessonTranslationRow,
)
from cyberdyne_backend.domain.courses import (
    Category,
    Course,
    CourseLevel,
    CourseNotFoundError,
    CourseStatus,
    DuplicateCategorySlugError,
    DuplicateCourseSlugError,
    Lesson,
    LessonType,
)


def _is_base_locale(locale: str) -> bool:
    """English is stored in the base rows, so it needs no translation join."""
    return locale == "en" or not locale


def _as_utc(value: datetime | None) -> datetime | None:
    """SQLite drops tzinfo on read; re-attach UTC so deadline comparisons
    against an aware ``now`` don't blow up. No-op on Postgres."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_lesson(row: LessonRow, tr: LessonTranslationRow | None = None) -> Lesson:
    # Per-field English fallback: use a translation value only when present
    # and non-empty, otherwise keep the English base.
    title = tr.title if tr and tr.title else row.title
    text_body = tr.text_body if tr and tr.text_body else row.text_body
    return Lesson(
        id=row.id,
        course_id=row.course_id,
        title=title,
        lesson_type=LessonType(row.lesson_type),
        sort_order=row.sort_order,
        content_url=row.content_url,
        text_body=text_body,
        duration=row.duration,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _row_to_category(row: CategoryRow) -> Category:
    return Category(
        id=row.id,
        slug=row.slug,
        name=row.name,
        icon=row.icon,
        sort_order=row.sort_order,
        parent_id=row.parent_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _row_to_course(
    row: CourseRow,
    lessons: list[LessonRow],
    course_tr: CourseTranslationRow | None = None,
    lesson_tr: dict[UUID, LessonTranslationRow] | None = None,
    category: Category | None = None,
) -> Course:
    title = course_tr.title if course_tr and course_tr.title else row.title
    description = course_tr.description if course_tr and course_tr.description else row.description
    tr_by_lesson = lesson_tr or {}
    return Course(
        id=row.id,
        slug=row.slug,
        title=title,
        description=description,
        level=CourseLevel(row.level),
        status=CourseStatus(row.status),
        mandatory=row.mandatory,
        sort_order=row.sort_order,
        created_at=row.created_at,
        published_at=row.published_at,
        updated_at=row.updated_at,
        due_at=_as_utc(row.due_at),
        lessons=[
            _row_to_lesson(les, tr_by_lesson.get(les.id))
            for les in sorted(lessons, key=lambda x: x.sort_order)
        ],
        category=category,
    )


class SqlAlchemyCourseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, course: Course) -> None:
        existing = await self._session.get(CourseRow, course.id)
        if existing is None:
            collision = await self._session.execute(
                select(CourseRow.id).where(CourseRow.slug == course.slug)
            )
            if collision.scalar_one_or_none() is not None:
                raise DuplicateCourseSlugError(course.slug)
            self._session.add(_course_to_row(course))
        else:
            existing.slug = course.slug
            existing.title = course.title
            existing.description = course.description
            existing.level = course.level.value
            existing.status = course.status.value
            existing.mandatory = course.mandatory
            existing.sort_order = course.sort_order
            existing.category_id = course.category.id if course.category else None
            existing.published_at = course.published_at
            existing.updated_at = course.updated_at
            existing.due_at = course.due_at
        # Upsert the lesson set IN PLACE — never wholesale-delete.
        # ``lesson_translations`` (and quiz translations) cascade on
        # ``lessons.id``, so the previous delete-then-reinsert silently wiped
        # every translation on each reseed (``seed_academy`` runs on every
        # boot). Instead: update matched rows in place — preserving the row and
        # its cascaded translations — insert genuinely new lessons, and delete
        # only lessons the aggregate dropped. Lesson counts per course are small.
        existing_rows = {row.id: row for row in await self._lessons_for(course.id)}
        incoming_ids = {lesson.id for lesson in course.lessons}
        for lesson_id, stale in existing_rows.items():
            if lesson_id not in incoming_ids:
                await self._session.delete(stale)
        for lesson in course.lessons:
            match = existing_rows.get(lesson.id)
            if match is None:
                self._session.add(_lesson_to_row(lesson))
                continue
            match.course_id = lesson.course_id
            match.title = lesson.title
            match.lesson_type = lesson.lesson_type.value
            match.content_url = lesson.content_url
            match.text_body = lesson.text_body
            match.duration = lesson.duration
            match.sort_order = lesson.sort_order
            match.updated_at = lesson.updated_at
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise DuplicateCourseSlugError(course.slug) from exc

    async def get_by_slug(
        self, slug: str, *, include_drafts: bool = False, locale: str = "en"
    ) -> Course:
        stmt = select(CourseRow).where(CourseRow.slug == slug)
        if not include_drafts:
            stmt = stmt.where(CourseRow.status == CourseStatus.PUBLISHED.value)
        row = (await self._session.execute(stmt)).scalar_one_or_none()
        if row is None:
            raise CourseNotFoundError(slug)
        lessons = await self._lessons_for(row.id)
        cats = await self._categories_by_id()
        category = cats.get(row.category_id) if row.category_id else None
        if _is_base_locale(locale):
            return _row_to_course(row, lessons, category=category)
        course_tr = (await self._course_translations([row.id], locale)).get(row.id)
        lesson_tr = await self._lesson_translations([le.id for le in lessons], locale)
        return _row_to_course(row, lessons, course_tr, lesson_tr, category=category)

    async def get_by_id(self, course_id: UUID) -> Course | None:
        row = await self._session.get(CourseRow, course_id)
        if row is None:
            return None
        lessons = await self._lessons_for(row.id)
        cats = await self._categories_by_id()
        return _row_to_course(
            row, lessons, category=cats.get(row.category_id) if row.category_id else None
        )

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
        locale: str = "en",
    ) -> list[Course]:
        stmt = select(CourseRow)
        if not include_drafts:
            stmt = stmt.where(CourseRow.status == CourseStatus.PUBLISHED.value)
        if level is not None:
            stmt = stmt.where(CourseRow.level == level.value)
        stmt = stmt.order_by(CourseRow.level, CourseRow.sort_order, CourseRow.title)
        rows = (await self._session.execute(stmt)).scalars().all()
        if not rows:
            return []
        lessons_by_course = await self._lessons_for_many([r.id for r in rows])
        cats = await self._categories_by_id()

        def _cat(r: CourseRow) -> Category | None:
            return cats.get(r.category_id) if r.category_id else None

        if _is_base_locale(locale):
            return [
                _row_to_course(r, lessons_by_course.get(r.id, []), category=_cat(r)) for r in rows
            ]
        course_tr = await self._course_translations([r.id for r in rows], locale)
        all_lesson_ids = [le.id for les in lessons_by_course.values() for le in les]
        lesson_tr = await self._lesson_translations(all_lesson_ids, locale)
        return [
            _row_to_course(
                r,
                lessons_by_course.get(r.id, []),
                course_tr.get(r.id),
                lesson_tr,
                category=_cat(r),
            )
            for r in rows
        ]

    async def delete(self, course_id: UUID) -> None:
        await self._session.execute(delete(LessonRow).where(LessonRow.course_id == course_id))
        await self._session.execute(delete(CourseRow).where(CourseRow.id == course_id))
        await self._session.flush()

    async def set_category(self, course_id: UUID, category_id: UUID | None) -> None:
        await self._session.execute(
            update(CourseRow).where(CourseRow.id == course_id).values(category_id=category_id)
        )
        await self._session.flush()

    async def _categories_by_id(self) -> dict[UUID, Category]:
        # The category set is tiny (one row per topic), so load it whole and
        # resolve in memory rather than join per course.
        rows = (await self._session.execute(select(CategoryRow))).scalars().all()
        return {row.id: _row_to_category(row) for row in rows}

    async def _lessons_for(self, course_id: UUID) -> list[LessonRow]:
        result = await self._session.execute(
            select(LessonRow).where(LessonRow.course_id == course_id)
        )
        return list(result.scalars().all())

    async def _lessons_for_many(self, course_ids: list[UUID]) -> dict[UUID, list[LessonRow]]:
        result = await self._session.execute(
            select(LessonRow).where(LessonRow.course_id.in_(course_ids))
        )
        out: dict[UUID, list[LessonRow]] = {}
        for row in result.scalars().all():
            out.setdefault(row.course_id, []).append(row)
        return out

    async def _course_translations(
        self, course_ids: list[UUID], locale: str
    ) -> dict[UUID, CourseTranslationRow]:
        if not course_ids:
            return {}
        result = await self._session.execute(
            select(CourseTranslationRow).where(
                CourseTranslationRow.course_id.in_(course_ids),
                CourseTranslationRow.language == locale,
            )
        )
        return {row.course_id: row for row in result.scalars().all()}

    async def _lesson_translations(
        self, lesson_ids: list[UUID], locale: str
    ) -> dict[UUID, LessonTranslationRow]:
        if not lesson_ids:
            return {}
        result = await self._session.execute(
            select(LessonTranslationRow).where(
                LessonTranslationRow.lesson_id.in_(lesson_ids),
                LessonTranslationRow.language == locale,
            )
        )
        return {row.lesson_id: row for row in result.scalars().all()}


def _course_to_row(course: Course) -> CourseRow:
    return CourseRow(
        id=course.id,
        slug=course.slug,
        title=course.title,
        description=course.description,
        level=course.level.value,
        status=course.status.value,
        mandatory=course.mandatory,
        sort_order=course.sort_order,
        category_id=course.category.id if course.category else None,
        created_at=course.created_at,
        published_at=course.published_at,
        updated_at=course.updated_at,
        due_at=course.due_at,
    )


class SqlAlchemyCategoryRepository:
    """SQLAlchemy adapter for ``CategoryRepository``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_categories(self) -> list[Category]:
        rows = (
            (
                await self._session.execute(
                    select(CategoryRow).order_by(CategoryRow.sort_order, CategoryRow.name)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_category(r) for r in rows]

    async def get_by_id(self, category_id: UUID) -> Category | None:
        row = await self._session.get(CategoryRow, category_id)
        return _row_to_category(row) if row is not None else None

    async def get_by_slug(self, slug: str) -> Category | None:
        row = (
            await self._session.execute(select(CategoryRow).where(CategoryRow.slug == slug))
        ).scalar_one_or_none()
        return _row_to_category(row) if row is not None else None

    async def save(self, category: Category) -> None:
        existing = await self._session.get(CategoryRow, category.id)
        if existing is None:
            collision = await self._session.execute(
                select(CategoryRow.id).where(CategoryRow.slug == category.slug)
            )
            if collision.scalar_one_or_none() is not None:
                raise DuplicateCategorySlugError(category.slug)
            self._session.add(
                CategoryRow(
                    id=category.id,
                    slug=category.slug,
                    name=category.name,
                    icon=category.icon,
                    sort_order=category.sort_order,
                    parent_id=category.parent_id,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
            )
        else:
            existing.slug = category.slug
            existing.name = category.name
            existing.icon = category.icon
            existing.sort_order = category.sort_order
            existing.parent_id = category.parent_id
            existing.updated_at = category.updated_at
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise DuplicateCategorySlugError(category.slug) from exc

    async def delete(self, category_id: UUID) -> None:
        row = await self._session.get(CategoryRow, category_id)
        if row is not None:
            await self._session.delete(row)
            await self._session.flush()


def _lesson_to_row(lesson: Lesson) -> LessonRow:
    return LessonRow(
        id=lesson.id,
        course_id=lesson.course_id,
        title=lesson.title,
        lesson_type=lesson.lesson_type.value,
        content_url=lesson.content_url,
        text_body=lesson.text_body,
        duration=lesson.duration,
        sort_order=lesson.sort_order,
        created_at=lesson.created_at,
        updated_at=lesson.updated_at,
    )

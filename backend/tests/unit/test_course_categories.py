"""Unit tests for course categories: use cases + the slug-derived assignment."""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from cyberdyne_backend.application.courses import (
    CreateCategory,
    CreateCategoryCommand,
    DeleteCategory,
    ListCategories,
    SetCourseCategory,
)
from cyberdyne_backend.application.courses.categories import (
    assign_course_categories,
    category_slug_for,
    seed_categories,
)
from cyberdyne_backend.domain.courses import (
    Category,
    CategoryNotFoundError,
    CategoryRepository,
    CourseNotFoundError,
    DuplicateCategorySlugError,
    new_category,
    new_course,
)

pytestmark = pytest.mark.unit


class FakeCategoryRepo:
    def __init__(self) -> None:
        self._by_id: dict[UUID, Category] = {}

    async def list_categories(self) -> list[Category]:
        return sorted(self._by_id.values(), key=lambda c: (c.sort_order, c.name))

    async def get_by_id(self, category_id: UUID) -> Category | None:
        return self._by_id.get(category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        return next((c for c in self._by_id.values() if c.slug == slug), None)

    async def save(self, category: Category) -> None:
        clash = next(
            (c for c in self._by_id.values() if c.slug == category.slug and c.id != category.id),
            None,
        )
        if clash is not None:
            raise DuplicateCategorySlugError(category.slug)
        self._by_id[category.id] = category

    async def delete(self, category_id: UUID) -> None:
        self._by_id.pop(category_id, None)


class FakeCourseRepo:
    def __init__(self, courses=()) -> None:
        self._by_id = {c.id: c for c in courses}
        self.assigned: dict[UUID, UUID | None] = {}  # course_id -> category_id

    async def get_by_slug(self, slug, *, include_drafts=False, locale="en"):
        course = next((c for c in self._by_id.values() if c.slug == slug), None)
        if course is None:
            raise CourseNotFoundError(slug)
        return course

    async def list_courses(self, *, level=None, include_drafts=False, locale="en"):
        return list(self._by_id.values())

    async def set_category(self, course_id, category_id):
        self.assigned[course_id] = category_id


def test_fake_category_repo_matches_port() -> None:
    assert isinstance(FakeCategoryRepo(), CategoryRepository)


def test_category_slug_for_mirrors_frontend_mapping() -> None:
    assert category_slug_for("comparch-basics") == "computer-architecture"
    assert category_slug_for("sysverilog-advanced") == "computer-architecture"
    assert category_slug_for("python-course") == "foundations"
    assert category_slug_for("c-basics") == "languages"
    assert category_slug_for("fpga-intermediate") == "electronic-engineering"
    assert category_slug_for("ml-transformers") == "ai-machine-learning"
    # Unmapped slugs fall to the "Other" bucket (None) — parity with the frontend.
    assert category_slug_for("csharp-basics") is None
    assert category_slug_for("linux-basics") is None


async def test_create_list_delete_category() -> None:
    repo = FakeCategoryRepo()
    create = CreateCategory(repo=repo)
    cat = await create.execute(CreateCategoryCommand(name="Quantum", icon="⚛️"))
    assert cat.slug == "quantum"
    assert [c.name for c in await ListCategories(repo=repo).execute()] == ["Quantum"]
    await DeleteCategory(repo=repo).execute(cat.id)
    assert await ListCategories(repo=repo).execute() == []


async def test_create_category_rejects_duplicate_slug() -> None:
    repo = FakeCategoryRepo()
    create = CreateCategory(repo=repo)
    await create.execute(CreateCategoryCommand(name="Robotics"))
    with pytest.raises(DuplicateCategorySlugError):
        await create.execute(CreateCategoryCommand(name="Robotics"))


async def test_set_course_category_validates_existence() -> None:
    course = new_course(title="Comp Arch", description="d", level="Beginner", slug="comparch-basics")
    course_repo = FakeCourseRepo([course])
    cat_repo = FakeCategoryRepo()
    cat = new_category(name="Computer Architecture", slug="computer-architecture")
    await cat_repo.save(cat)
    uc = SetCourseCategory(course_repo=course_repo, category_repo=cat_repo)

    # Assigning an unknown category id → CategoryNotFoundError.
    with pytest.raises(CategoryNotFoundError):
        await uc.execute("comparch-basics", uuid4())

    # A real category id is accepted (and the repo records the assignment).
    await uc.execute("comparch-basics", cat.id)
    assert course_repo.assigned[course.id] == cat.id

    # None clears the category (uncategorized).
    await uc.execute("comparch-basics", None)
    assert course_repo.assigned[course.id] is None


async def test_seed_categories_idempotent_and_assignment_fills_only_uncategorized() -> None:
    cat_repo = FakeCategoryRepo()
    cats = await seed_categories(cat_repo)
    assert "computer-architecture" in cats
    # Re-seed reuses existing categories (no duplicates).
    again = await seed_categories(cat_repo)
    assert {c.id for c in cats.values()} == {c.id for c in again.values()}

    comparch = new_course(title="CA", description="d", level="Beginner", slug="comparch-basics")
    already = new_course(title="Phys", description="d", level="Beginner", slug="physics-basics")
    already.category = cats["foundations"]  # pretend a manual assignment
    course_repo = FakeCourseRepo([comparch, already])
    assigned = await assign_course_categories(course_repo, cats)
    assert assigned == 1  # only the uncategorized comparch course
    assert course_repo.assigned[comparch.id] == cats["computer-architecture"].id
    assert already.id not in course_repo.assigned  # manual assignment untouched

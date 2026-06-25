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
    UpdateCategory,
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
    assert category_slug_for("software-quality-basics") == "software-engineering"
    assert category_slug_for("computational-thinking-advanced") == "foundations"
    assert category_slug_for("technical-english-basics") == "foundations"
    assert category_slug_for("english-br-basics") == "foundations"
    assert category_slug_for("django-basics") == "web-development"
    assert category_slug_for("rails-advanced") == "web-development"
    assert category_slug_for("software-architecture-basics") == "software-engineering"
    assert category_slug_for("algorithms-logic-computing") == "foundations"
    assert category_slug_for("prob-stats-python-basics") == "mathematics"
    assert category_slug_for("circuit-analysis-basics") == "electronic-engineering"
    assert category_slug_for("filter-design-advanced") == "electronic-engineering"
    assert category_slug_for("data-converters-intermediate") == "electronic-engineering"
    assert category_slug_for("rfic-basics") == "electronic-engineering"
    assert category_slug_for("stochastic-processes-basics") == "mathematics"
    assert category_slug_for("coding-theory-advanced") == "electronic-engineering"
    assert category_slug_for("wireless-comms-basics") == "electronic-engineering"
    assert category_slug_for("radar-intermediate") == "electronic-engineering"
    assert category_slug_for("audio-processing-basics") == "electronic-engineering"
    assert category_slug_for("adaptive-dsp-advanced") == "electronic-engineering"
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
    course = new_course(
        title="Comp Arch", description="d", level="Beginner", slug="comparch-basics"
    )
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


async def test_create_category_under_parent_and_validation() -> None:
    repo = FakeCategoryRepo()
    create = CreateCategory(repo=repo)
    group = await create.execute(CreateCategoryCommand(name="Programming"))
    child = await create.execute(CreateCategoryCommand(name="Languages", parent_id=group.id))
    assert child.parent_id == group.id

    # Parent must exist.
    with pytest.raises(CategoryNotFoundError):
        await create.execute(CreateCategoryCommand(name="X", parent_id=uuid4()))
    # Parent must be top-level (no nesting under a sub-category) → max 2 levels.
    with pytest.raises(ValueError, match="top-level"):
        await create.execute(CreateCategoryCommand(name="Y", parent_id=child.id))


async def test_update_category_reparents_renames_and_guards_cycles() -> None:
    repo = FakeCategoryRepo()
    create = CreateCategory(repo=repo)
    update = UpdateCategory(repo=repo)
    g1 = await create.execute(CreateCategoryCommand(name="Programming"))
    g2 = await create.execute(CreateCategoryCommand(name="Engineering"))
    leaf = await create.execute(CreateCategoryCommand(name="Languages", parent_id=g1.id))

    # Rename + reparent to another top-level group.
    moved = await update.execute(leaf.id, name="Langs", set_parent=True, parent_id=g2.id)
    assert moved.name == "Langs"
    assert moved.parent_id == g2.id

    # Clear the parent → top-level.
    cleared = await update.execute(leaf.id, set_parent=True, parent_id=None)
    assert cleared.parent_id is None

    # A category cannot be its own parent.
    with pytest.raises(ValueError, match="own parent"):
        await update.execute(g1.id, set_parent=True, parent_id=g1.id)

    # Unknown category → not found.
    with pytest.raises(CategoryNotFoundError):
        await update.execute(uuid4(), name="z")


async def test_seed_categories_builds_two_level_hierarchy() -> None:
    repo = FakeCategoryRepo()
    cats = await seed_categories(repo)
    # Parent groups exist as top-level categories.
    assert cats["programming"].parent_id is None
    # Built-in leaves are parented to their group.
    assert cats["languages"].parent_id == cats["programming"].id
    assert cats["computer-architecture"].parent_id == cats["engineering-robotics"].id
    # Mathematics stays top-level (no parent group), as today.
    assert cats["mathematics"].parent_id is None


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

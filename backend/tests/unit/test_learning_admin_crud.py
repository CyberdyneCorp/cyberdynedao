"""Unit tests for the learning catalogue admin-CRUD use cases.

Uses an in-memory fake repository implementing the new write methods, so the
use-case validation (slug derivation, level enum, moduleSlugs referential
integrity, conflict/not-found) is exercised without a database.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from cyberdyne_backend.application.learning import (
    CreateModule,
    CreateModuleCommand,
    CreatePath,
    CreatePathCommand,
    DeleteModule,
    DeletePath,
    ReorderPathModules,
    UpdateModule,
    UpdateModuleCommand,
    UpdatePath,
    UpdatePathCommand,
)
from cyberdyne_backend.domain.learning import (
    LearningContentConflictError,
    LearningContentNotFoundError,
    LearningContentValidationError,
    LearningModule,
    LearningPath,
)


class _FakeRepo:
    """Implements only the catalogue-write surface the use cases touch."""

    def __init__(self) -> None:
        self.modules: dict[str, LearningModule] = {}
        self.paths: dict[str, LearningPath] = {}

    async def list_modules(self) -> list[LearningModule]:
        return list(self.modules.values())

    async def get_module(self, slug: str) -> LearningModule:
        if slug not in self.modules:
            raise LearningContentNotFoundError(slug)
        return self.modules[slug]

    async def create_module(self, module: LearningModule) -> LearningModule:
        if module.slug in self.modules:
            raise LearningContentConflictError(module.slug)
        self.modules[module.slug] = module
        return module

    async def update_module(self, slug: str, **fields: object) -> LearningModule:
        if slug not in self.modules:
            raise LearningContentNotFoundError(slug)
        current = self.modules[slug]
        updates = {k: v for k, v in fields.items() if v is not None}
        merged = LearningModule(
            slug=slug,
            title=updates.get("title", current.title),
            category=updates.get("category", current.category),
            description=updates.get("description", current.description),
            level=updates.get("level", current.level),
            duration=updates.get("duration", current.duration),
            icon=updates.get("icon", current.icon),
            topics=tuple(updates.get("topics", current.topics)),
        )
        self.modules[slug] = merged
        return merged

    async def delete_module(self, slug: str) -> None:
        if slug not in self.modules:
            raise LearningContentNotFoundError(slug)
        del self.modules[slug]

    async def create_path(self, path: LearningPath) -> LearningPath:
        if path.slug in self.paths:
            raise LearningContentConflictError(path.slug)
        self.paths[path.slug] = path
        return path

    async def update_path(self, slug: str, **fields: object) -> LearningPath:
        if slug not in self.paths:
            raise LearningContentNotFoundError(slug)
        current = self.paths[slug]
        updates = {k: v for k, v in fields.items() if v is not None}
        merged = LearningPath(
            slug=slug,
            title=updates.get("title", current.title),
            description=updates.get("description", current.description),
            module_slugs=tuple(updates.get("module_slugs", current.module_slugs)),
            estimated_time=updates.get("estimated_time", current.estimated_time),
            icon=updates.get("icon", current.icon),
        )
        self.paths[slug] = merged
        return merged

    async def delete_path(self, slug: str) -> None:
        if slug not in self.paths:
            raise LearningContentNotFoundError(slug)
        del self.paths[slug]


def _module_cmd(**kw: object) -> CreateModuleCommand:
    base = {
        "title": "Programming Fundamentals",
        "category": "Foundations",
        "description": "Variables, control flow, functions.",
        "level": "Beginner",
        "duration": "1 hr",
        "icon": "💻",
        "topics": ("Variables", "Control Flow"),
    }
    base.update(kw)
    return CreateModuleCommand(**base)  # type: ignore[arg-type]


# ── Modules ──────────────────────────────────────────────────────────


async def test_create_module_derives_slug_and_persists() -> None:
    repo = _FakeRepo()
    module = await CreateModule(repo=repo).execute(_module_cmd())
    assert module.slug == "programming-fundamentals"  # derived from title
    assert repo.modules["programming-fundamentals"].title == "Programming Fundamentals"


async def test_create_module_explicit_slug_is_normalized() -> None:
    repo = _FakeRepo()
    module = await CreateModule(repo=repo).execute(_module_cmd(slug="Data Structures!"))
    assert module.slug == "data-structures"


async def test_create_module_duplicate_conflicts() -> None:
    repo = _FakeRepo()
    await CreateModule(repo=repo).execute(_module_cmd())
    with pytest.raises(LearningContentConflictError):
        await CreateModule(repo=repo).execute(_module_cmd())


async def test_create_module_invalid_level_rejected() -> None:
    repo = _FakeRepo()
    with pytest.raises(LearningContentValidationError):
        await CreateModule(repo=repo).execute(_module_cmd(level="Expert"))


async def test_update_module_unknown_not_found() -> None:
    repo = _FakeRepo()
    with pytest.raises(LearningContentNotFoundError):
        await UpdateModule(repo=repo).execute(UpdateModuleCommand(slug="ghost", title="x"))


async def test_update_module_partial_and_invalid_level() -> None:
    repo = _FakeRepo()
    await CreateModule(repo=repo).execute(_module_cmd())
    updated = await UpdateModule(repo=repo).execute(
        UpdateModuleCommand(slug="programming-fundamentals", title="PF v2")
    )
    assert updated.title == "PF v2"
    assert updated.level == "Beginner"  # unchanged
    with pytest.raises(LearningContentValidationError):
        await UpdateModule(repo=repo).execute(
            UpdateModuleCommand(slug="programming-fundamentals", level="Wizard")
        )


async def test_delete_module() -> None:
    repo = _FakeRepo()
    await CreateModule(repo=repo).execute(_module_cmd())
    await DeleteModule(repo=repo).execute("programming-fundamentals")
    assert "programming-fundamentals" not in repo.modules
    with pytest.raises(LearningContentNotFoundError):
        await DeleteModule(repo=repo).execute("programming-fundamentals")


# ── Paths ────────────────────────────────────────────────────────────


async def _seed_two_modules(repo: _FakeRepo) -> None:
    await CreateModule(repo=repo).execute(_module_cmd(title="M1", slug="m1"))
    await CreateModule(repo=repo).execute(_module_cmd(title="M2", slug="m2"))


async def test_create_path_with_valid_modules() -> None:
    repo = _FakeRepo()
    await _seed_two_modules(repo)
    path = await CreatePath(repo=repo).execute(
        CreatePathCommand(
            title="Computer Engineering",
            description="The full stack.",
            module_slugs=("m1", "m2"),
            estimated_time="16-24 weeks",
            icon="🖥️",
        )
    )
    assert path.slug == "computer-engineering"
    assert path.module_slugs == ("m1", "m2")


async def test_create_path_unknown_module_rejected_and_not_persisted() -> None:
    repo = _FakeRepo()
    await _seed_two_modules(repo)
    with pytest.raises(LearningContentValidationError):
        await CreatePath(repo=repo).execute(
            CreatePathCommand(
                title="Broken",
                description="d",
                module_slugs=("m1", "ghost"),
                estimated_time="1 wk",
                icon="❓",
            )
        )
    assert repo.paths == {}  # nothing persisted


async def test_update_path_validates_modules_and_reorders() -> None:
    repo = _FakeRepo()
    await _seed_two_modules(repo)
    await CreateModule(repo=repo).execute(_module_cmd(title="M3", slug="m3"))
    await CreatePath(repo=repo).execute(
        CreatePathCommand(
            title="P",
            description="d",
            module_slugs=("m1", "m2", "m3"),
            estimated_time="1 wk",
            icon="📦",
        )
    )
    reordered = await ReorderPathModules(repo=repo).execute(
        slug="p", module_slugs=("m3", "m1", "m2")
    )
    assert reordered.module_slugs == ("m3", "m1", "m2")
    with pytest.raises(LearningContentValidationError):
        await UpdatePath(repo=repo).execute(
            UpdatePathCommand(slug="p", module_slugs=("m1", "ghost"))
        )


async def test_delete_path() -> None:
    repo = _FakeRepo()
    await _seed_two_modules(repo)
    await CreatePath(repo=repo).execute(
        CreatePathCommand(
            title="P",
            description="d",
            module_slugs=("m1",),
            estimated_time="1 wk",
            icon="📦",
        )
    )
    await DeletePath(repo=repo).execute("p")
    assert repo.paths == {}
    with pytest.raises(LearningContentNotFoundError):
        await DeletePath(repo=repo).execute("p")


# ── Regression: the seeded catalogue is preserved by this change ─────


def _load_seed_migration() -> object:
    path = (
        Path(__file__).resolve().parents[2]
        / "alembic"
        / "versions"
        / "202605270003_phase4_learning.py"
    )
    spec = importlib.util.spec_from_file_location("_phase4_learning", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_seed_migration_still_has_5_paths_and_12_modules() -> None:
    migration = _load_seed_migration()
    assert len(migration._MODULES) == 12
    assert len(migration._PATHS) == 5


def test_computer_engineering_payloads_are_valid() -> None:
    from cyberdyne_backend.cli.create_computer_engineering_path import build_payloads
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    modules, path = build_payloads()
    assert len(modules) == 10
    module_slugs = {m["slug"] for m in modules}
    # Every level is valid and the path references only modules built here.
    assert all(m["level"] in VALID_LEVELS for m in modules)
    assert set(path["moduleSlugs"]) <= module_slugs
    assert path["slug"] == "computer-engineering"


def test_life_sciences_payloads_are_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.create_life_sciences_paths import build_payloads
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    modules, paths = build_payloads()
    # 50 tracks -> 50 modules across the three degree-stage paths.
    assert len(modules) == 50
    assert [p["slug"] for p in paths] == [
        "life-sciences-foundations",
        "bioinformatics-omics",
        "drug-design-ai",
    ]
    module_slugs = [m["slug"] for m in modules]
    assert len(module_slugs) == len(set(module_slugs)), "duplicate module slugs"
    assert all(m["level"] in VALID_LEVELS for m in modules)
    # Each path references only modules built here, and together they cover all.
    referenced: set[str] = set()
    for p in paths:
        assert set(p["moduleSlugs"]) <= set(module_slugs)
        referenced.update(p["moduleSlugs"])
    assert referenced == set(module_slugs)
    # Every bundled course slug is a real seeded course (3 per track = 150).
    catalogue = {c.slug for c in ACADEMY_COURSES}
    bundled = [s for m in modules for s in m["courseSlugs"]]
    assert len(bundled) == 150
    missing = sorted(set(bundled) - catalogue)
    assert not missing, f"modules reference unseeded courses: {missing}"


def test_startups_ai_module_payload_is_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.add_startups_ai_to_computer_engineering import (
        appended_module_slugs,
        build_module_payload,
    )
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    module = build_module_payload()
    assert module["slug"] == "startups-in-the-age-of-ai"
    assert module["level"] in VALID_LEVELS
    # The module bundles only real seeded courses.
    catalogue = {c.slug for c in ACADEMY_COURSES}
    missing = sorted(set(module["courseSlugs"]) - catalogue)
    assert not missing, f"module references unseeded courses: {missing}"
    # Appending is idempotent: present -> no-op, absent -> appended at the end.
    assert appended_module_slugs(["a", module["slug"]], module["slug"]) is None
    assert appended_module_slugs(["a", "b"], module["slug"]) == ["a", "b", module["slug"]]


def test_selling_software_module_payload_is_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.add_selling_software_to_computer_engineering import (
        appended_module_slugs,
        build_module_payload,
    )
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    module = build_module_payload()
    assert module["slug"] == "selling-software-in-the-age-of-ai"
    assert module["level"] in VALID_LEVELS
    # The module bundles only real seeded courses.
    catalogue = {c.slug for c in ACADEMY_COURSES}
    missing = sorted(set(module["courseSlugs"]) - catalogue)
    assert not missing, f"module references unseeded courses: {missing}"
    # Appending is idempotent: present -> no-op, absent -> appended at the end.
    assert appended_module_slugs(["a", module["slug"]], module["slug"]) is None
    assert appended_module_slugs(["a", "b"], module["slug"]) == ["a", "b", module["slug"]]


def test_react_basics_module_payload_is_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.add_react_basics_to_computer_engineering import (
        appended_module_slugs,
        build_module_payload,
    )
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    module = build_module_payload()
    assert module["slug"] == "react-basics"
    assert module["level"] in VALID_LEVELS
    # The module bundles only real seeded courses.
    catalogue = {c.slug for c in ACADEMY_COURSES}
    missing = sorted(set(module["courseSlugs"]) - catalogue)
    assert not missing, f"module references unseeded courses: {missing}"
    # Appending is idempotent: present -> no-op, absent -> appended at the end.
    assert appended_module_slugs(["a", module["slug"]], module["slug"]) is None
    assert appended_module_slugs(["a", "b"], module["slug"]) == ["a", "b", module["slug"]]


def test_svelte_basics_module_payload_is_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.add_svelte_basics_to_computer_engineering import (
        appended_module_slugs,
        build_module_payload,
    )
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    module = build_module_payload()
    assert module["slug"] == "svelte-basics"
    assert module["level"] in VALID_LEVELS
    # The module bundles only real seeded courses.
    catalogue = {c.slug for c in ACADEMY_COURSES}
    missing = sorted(set(module["courseSlugs"]) - catalogue)
    assert not missing, f"module references unseeded courses: {missing}"
    # Appending is idempotent: present -> no-op, absent -> appended at the end.
    assert appended_module_slugs(["a", module["slug"]], module["slug"]) is None
    assert appended_module_slugs(["a", "b"], module["slug"]) == ["a", "b", module["slug"]]


def test_mechanical_engineering_payloads_are_valid() -> None:
    from cyberdyne_backend.application.courses.seed import ACADEMY_COURSES
    from cyberdyne_backend.cli.create_mechanical_engineering_paths import build_payloads
    from cyberdyne_backend.domain.learning import VALID_LEVELS

    modules, paths = build_payloads()
    # 27 tracks -> 27 modules across the three degree-stage paths.
    assert len(modules) == 27
    assert [p["slug"] for p in paths] == [
        "mechanical-foundations",
        "mechatronics-robotics",
        "generative-design-ai",
    ]
    module_slugs = [m["slug"] for m in modules]
    assert len(module_slugs) == len(set(module_slugs)), "duplicate module slugs"
    assert all(m["level"] in VALID_LEVELS for m in modules)
    referenced: set[str] = set()
    for p in paths:
        assert set(p["moduleSlugs"]) <= set(module_slugs)
        referenced.update(p["moduleSlugs"])
    assert referenced == set(module_slugs)
    # Every bundled course slug is a real seeded course (3 per track = 81).
    catalogue = {c.slug for c in ACADEMY_COURSES}
    bundled = [s for m in modules for s in m["courseSlugs"]]
    assert len(bundled) == 81
    missing = sorted(set(bundled) - catalogue)
    assert not missing, f"modules reference unseeded courses: {missing}"

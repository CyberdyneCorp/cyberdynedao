"""Unit tests for course-backed learning stages: a module that bundles
courses derives its completion from those courses, and admin assignment
validates the course slugs.
"""

from __future__ import annotations

import uuid

import pytest

from cyberdyne_backend.application.learning import (
    CheckEnrollmentEligibility,
    CreateModule,
    CreateModuleCommand,
    GetMyLearningState,
    GetPathGating,
)
from cyberdyne_backend.domain.learning import (
    LearningContentNotFoundError,
    LearningContentValidationError,
    LearningModule,
    LearningPath,
    ModuleProgress,
    derived_module_percent,
    new_module,
)

_USER = uuid.UUID("66666666-6666-6666-6666-666666666666")


# ── domain: derived percent ──────────────────────────────────────────


def test_derived_percent_empty_is_zero() -> None:
    assert derived_module_percent((), {}) == 0


def test_derived_percent_100_only_when_all_complete() -> None:
    assert derived_module_percent(("c1", "c2"), {"c1": 100, "c2": 100}) == 100
    # One course short of done → strictly below 100 (the completion gate).
    assert derived_module_percent(("c1", "c2"), {"c1": 100, "c2": 99}) < 100
    # Missing course counts as 0.
    assert derived_module_percent(("c1", "c2"), {"c1": 100}) == 50


# ── fakes ────────────────────────────────────────────────────────────


class _FakeReader:
    def __init__(self, slugs: set[str], percents: dict[str, int]) -> None:
        self._slugs = slugs
        self._percents = percents

    async def existing_course_slugs(self) -> set[str]:
        return self._slugs

    async def percent_by_course(self, user_id: uuid.UUID) -> dict[str, int]:
        return dict(self._percents)


class _FakeRepo:
    def __init__(self, modules: list[LearningModule], paths: dict[str, LearningPath]) -> None:
        self._modules = modules
        self._paths = paths
        self.created: list[LearningModule] = []

    async def list_modules(self) -> list[LearningModule]:
        return list(self._modules)

    async def get_path(self, slug: str) -> LearningPath:
        if slug not in self._paths:
            raise LearningContentNotFoundError(slug)
        return self._paths[slug]

    async def get_progress_map_for_user(self, user_id: uuid.UUID) -> dict[str, ModuleProgress]:
        return {}  # nothing self-reported

    async def list_enrollments_for_user(self, user_id: uuid.UUID) -> list:
        return []

    async def create_module(self, module: LearningModule) -> LearningModule:
        self.created.append(module)
        return module


def _course_module(slug: str, course_slugs: tuple[str, ...]) -> LearningModule:
    return new_module(
        title=slug,
        category="Foundations",
        description="d",
        level="Beginner",
        duration="1 hr",
        icon="📦",
        course_slugs=course_slugs,
        slug=slug,
    )


# ── admin: assigning courses validates the slugs ─────────────────────


async def test_create_module_with_known_courses_ok() -> None:
    repo = _FakeRepo([], {})
    reader = _FakeReader({"python-course"}, {})
    module = await CreateModule(repo=repo, course_reader=reader).execute(
        CreateModuleCommand(
            title="Foundations",
            category="Foundations",
            description="d",
            level="Beginner",
            duration="1 hr",
            icon="📦",
            course_slugs=("python-course",),
        )
    )
    assert module.course_slugs == ("python-course",)


async def test_create_module_with_unknown_course_rejected() -> None:
    repo = _FakeRepo([], {})
    reader = _FakeReader({"python-course"}, {})
    with pytest.raises(LearningContentValidationError):
        await CreateModule(repo=repo, course_reader=reader).execute(
            CreateModuleCommand(
                title="Foundations",
                category="Foundations",
                description="d",
                level="Beginner",
                duration="1 hr",
                icon="📦",
                course_slugs=("python-course", "ghost-course"),
            )
        )
    assert repo.created == []  # nothing persisted


# ── derived completion drives gating ─────────────────────────────────


async def test_gating_marks_stage_complete_when_all_courses_done() -> None:
    module = _course_module("foundations", ("c1", "c2"))
    path = LearningPath(
        slug="eng",
        title="Engineering",
        description="d",
        module_slugs=("foundations",),
        estimated_time="1 wk",
        icon="🖥️",
    )
    repo = _FakeRepo([module], {"eng": path})

    done = GetPathGating(repo=repo, course_reader=_FakeReader(set(), {"c1": 100, "c2": 100}))
    gates = await done.execute(user_id=_USER, path_slug="eng")
    assert gates[0].completed is True

    partial = GetPathGating(repo=repo, course_reader=_FakeReader(set(), {"c1": 100, "c2": 40}))
    gates = await partial.execute(user_id=_USER, path_slug="eng")
    assert gates[0].completed is False


async def test_my_state_reports_derived_module_progress() -> None:
    module = _course_module("foundations", ("c1",))
    repo = _FakeRepo([module], {})
    state = await GetMyLearningState(
        repo=repo, course_reader=_FakeReader(set(), {"c1": 100})
    ).execute(_USER)
    assert state.progress_by_module["foundations"].is_completed is True


async def test_eligibility_uses_derived_completion() -> None:
    module = _course_module("foundations", ("c1",))
    path = LearningPath(
        slug="eng",
        title="Engineering",
        description="d",
        module_slugs=("foundations",),
        estimated_time="1 wk",
        icon="🖥️",
    )
    repo = _FakeRepo([module], {"eng": path})
    result = await CheckEnrollmentEligibility(
        repo=repo, course_reader=_FakeReader(set(), {"c1": 100})
    ).execute(user_id=_USER, path_slug="eng")
    # All stages complete → no next module to start.
    assert result.next_module is None

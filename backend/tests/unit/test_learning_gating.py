"""Tests for learning prerequisite gating (domain + use cases)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.learning import (
    CheckEnrollmentEligibility,
    GetPathGating,
)
from cyberdyne_backend.domain.learning import (
    Enrollment,
    LearningContentNotFoundError,
    LearningModule,
    LearningPath,
    ModuleProgress,
    compute_path_gates,
    new_enrollment,
    new_progress,
    next_unlocked_module,
)


def _module(slug: str, level: str) -> LearningModule:
    return LearningModule(
        slug=slug,
        title=slug,
        category="c",
        description="d",
        level=level,
        duration="1h",
        icon="x",
        topics=(),
    )


def _completed_progress(user_id: uuid.UUID, slug: str) -> ModuleProgress:
    return new_progress(
        user_id=user_id,
        module_slug=slug,
        percent=100,
        now=datetime(2026, 1, 1, tzinfo=UTC),
    )


# Path: two Beginner modules then one Intermediate, declared in order.
def _path() -> LearningPath:
    return LearningPath(
        slug="p1",
        title="Path",
        description="d",
        module_slugs=("b1", "b2", "i1"),
        estimated_time="4w",
        icon="x",
    )


def _modules() -> dict[str, LearningModule]:
    return {
        "b1": _module("b1", "Beginner"),
        "b2": _module("b2", "Beginner"),
        "i1": _module("i1", "Intermediate"),
    }


class TestComputePathGates:
    def test_fresh_user_only_first_unlocked(self) -> None:
        gates = compute_path_gates(_path(), _modules(), {})
        by_slug = {g.module_slug: g for g in gates}
        assert by_slug["b1"].unlocked is True
        assert by_slug["b2"].unlocked is False
        assert by_slug["i1"].unlocked is False
        # Output preserves declared order.
        assert [g.module_slug for g in gates] == ["b1", "b2", "i1"]

    def test_sequential_gating_within_level(self) -> None:
        # Fresh user: b2 is blocked by b1, both Beginner → "sequential".
        gates = {g.module_slug: g for g in compute_path_gates(_path(), _modules(), {})}
        assert gates["b2"].unlocked is False
        assert gates["b2"].blocked_by == "b1"
        assert gates["b2"].reason == "sequential"

    def test_completing_first_unlocks_next_in_level(self) -> None:
        user = uuid.uuid4()
        progress = {"b1": _completed_progress(user, "b1")}
        gates = {g.module_slug: g for g in compute_path_gates(_path(), _modules(), progress)}
        # b1 done → b2 unlocks (same level, next in sequence).
        assert gates["b2"].unlocked is True
        # i1 still locked behind b2; b2 is a lower level → "level" gating.
        assert gates["i1"].unlocked is False
        assert gates["i1"].blocked_by == "b2"
        assert gates["i1"].reason == "level"

    def test_all_beginner_done_unlocks_intermediate(self) -> None:
        user = uuid.uuid4()
        progress = {
            "b1": _completed_progress(user, "b1"),
            "b2": _completed_progress(user, "b2"),
        }
        gates = {g.module_slug: g for g in compute_path_gates(_path(), _modules(), progress)}
        assert gates["i1"].unlocked is True
        assert gates["i1"].blocked_by is None
        assert gates["i1"].reason is None

    def test_level_reason_when_blocker_is_lower_level(self) -> None:
        # Path where an Intermediate is declared before a second Beginner;
        # gating order sorts Beginner first, so the Intermediate is gated
        # by a lower-level (Beginner) module → reason "level".
        path = LearningPath(
            slug="p",
            title="t",
            description="d",
            module_slugs=("i1", "b1"),
            estimated_time="x",
            icon="x",
        )
        modules = {"i1": _module("i1", "Intermediate"), "b1": _module("b1", "Beginner")}
        gates = {g.module_slug: g for g in compute_path_gates(path, modules, {})}
        # b1 (Beginner) sorts first and is unlocked; i1 is blocked by b1.
        assert gates["b1"].unlocked is True
        assert gates["i1"].unlocked is False
        assert gates["i1"].blocked_by == "b1"
        assert gates["i1"].reason == "level"

    def test_unknown_module_slugs_are_skipped(self) -> None:
        path = LearningPath(
            slug="p",
            title="t",
            description="d",
            module_slugs=("b1", "ghost", "b2"),
            estimated_time="x",
            icon="x",
        )
        gates = compute_path_gates(path, _modules(), {})
        assert [g.module_slug for g in gates] == ["b1", "b2"]


class TestNextUnlocked:
    def test_picks_first_unlocked_incomplete(self) -> None:
        user = uuid.uuid4()
        progress = {"b1": _completed_progress(user, "b1")}
        gates = compute_path_gates(_path(), _modules(), progress)
        assert next_unlocked_module(gates) == "b2"

    def test_none_when_all_done(self) -> None:
        user = uuid.uuid4()
        progress = {k: _completed_progress(user, k) for k in ("b1", "b2", "i1")}
        gates = compute_path_gates(_path(), _modules(), progress)
        assert next_unlocked_module(gates) is None


# ── Use cases via a fake repo ────────────────────────────────────────


class _FakeRepo:
    def __init__(self) -> None:
        self.modules = list(_modules().values())
        self.paths = {"p1": _path()}
        self.enrollments: list[Enrollment] = []
        self.progress: dict[tuple[uuid.UUID, str], ModuleProgress] = {}

    async def list_modules(self) -> list[LearningModule]:
        return list(self.modules)

    async def get_path(self, slug: str) -> LearningPath:
        if slug not in self.paths:
            raise LearningContentNotFoundError(slug)
        return self.paths[slug]

    async def list_enrollments_for_user(self, user_id: uuid.UUID) -> list[Enrollment]:
        return [e for e in self.enrollments if e.user_id == user_id]

    async def get_progress_map_for_user(self, user_id: uuid.UUID) -> dict[str, ModuleProgress]:
        return {slug: p for (uid, slug), p in self.progress.items() if uid == user_id}


class TestGetPathGating:
    async def test_returns_gates(self) -> None:
        repo = _FakeRepo()
        gates = await GetPathGating(repo=repo).execute(user_id=uuid.uuid4(), path_slug="p1")
        assert [g.module_slug for g in gates] == ["b1", "b2", "i1"]

    async def test_missing_path_raises(self) -> None:
        with pytest.raises(LearningContentNotFoundError):
            await GetPathGating(repo=_FakeRepo()).execute(user_id=uuid.uuid4(), path_slug="nope")


class TestCheckEnrollmentEligibility:
    async def test_eligible_with_next_module(self) -> None:
        repo = _FakeRepo()
        result = await CheckEnrollmentEligibility(repo=repo).execute(
            user_id=uuid.uuid4(), path_slug="p1"
        )
        assert result.eligible is True
        assert result.already_enrolled is False
        assert result.next_module == "b1"

    async def test_reports_already_enrolled(self) -> None:
        repo = _FakeRepo()
        user = uuid.uuid4()
        repo.enrollments.append(new_enrollment(user_id=user, path_slug="p1"))
        result = await CheckEnrollmentEligibility(repo=repo).execute(user_id=user, path_slug="p1")
        assert result.already_enrolled is True

    async def test_empty_path_not_eligible(self) -> None:
        repo = _FakeRepo()
        repo.paths["empty"] = LearningPath(
            slug="empty",
            title="t",
            description="d",
            module_slugs=(),
            estimated_time="x",
            icon="x",
        )
        result = await CheckEnrollmentEligibility(repo=repo).execute(
            user_id=uuid.uuid4(), path_slug="empty"
        )
        assert result.eligible is False
        assert result.next_module is None

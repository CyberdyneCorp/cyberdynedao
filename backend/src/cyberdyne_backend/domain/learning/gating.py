"""Prerequisite gating for a learning path.

Two rules, both spec'd:

  * **Level gating** — a learner can't start an Intermediate module until
    every Beginner module in the path is complete, and likewise
    Intermediate → Advanced.
  * **Sequential gating within a level** — within one level, modules
    unlock in the path's declared order.

Both reduce to a single computation: sort the path's modules by
``(level_rank, position_in_path)`` and a module is unlocked iff every
module before it in that order is complete. The first module is always
unlocked. ``blocked_by`` names the nearest incomplete predecessor and
``reason`` says whether it blocks by level or by sequence — handy for the
player UI's lock tooltip.

Pure domain: this reads only entities + a progress map and returns a
plain value object. No I/O, no ports.
"""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.learning.entities import (
    LearningModule,
    LearningPath,
    ModuleProgress,
)

# Beginner → Intermediate → Advanced. Unknown levels sort last so a
# mis-tagged module never silently gates everything behind it.
LEVEL_ORDER: dict[str, int] = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
_UNKNOWN_LEVEL_RANK = 99


def level_rank(level: str) -> int:
    return LEVEL_ORDER.get(level, _UNKNOWN_LEVEL_RANK)


@dataclass(frozen=True, slots=True)
class ModuleGate:
    module_slug: str
    level: str
    position: int  # index in the path's declared module order
    unlocked: bool
    completed: bool
    blocked_by: str | None  # slug of the nearest incomplete predecessor
    reason: str | None  # "level" | "sequential" | None when unlocked


def compute_path_gates(
    path: LearningPath,
    modules_by_slug: dict[str, LearningModule],
    progress_by_module: dict[str, ModuleProgress],
) -> list[ModuleGate]:
    """Lock state for every (resolvable) module in ``path``.

    Modules whose slug isn't in ``modules_by_slug`` are skipped (a stale
    path reference shouldn't crash the catalogue). Results come back in
    the path's declared order so the caller can render them as listed.
    """

    def _completed(slug: str) -> bool:
        progress = progress_by_module.get(slug)
        return progress is not None and progress.is_completed

    # (original_index, slug, module) for resolvable modules only.
    resolved = [
        (idx, slug, modules_by_slug[slug])
        for idx, slug in enumerate(path.module_slugs)
        if slug in modules_by_slug
    ]
    # Gating order: level first, then declared position within the level.
    gating_order = sorted(resolved, key=lambda t: (level_rank(t[2].level), t[0]))

    gates_by_slug: dict[str, ModuleGate] = {}
    blocker: tuple[str, str] | None = None  # (slug, level) of first incomplete predecessor
    for idx, slug, module in gating_order:
        completed = _completed(slug)
        if blocker is None:
            gates_by_slug[slug] = ModuleGate(
                module_slug=slug,
                level=module.level,
                position=idx,
                unlocked=True,
                completed=completed,
                blocked_by=None,
                reason=None,
            )
        else:
            blocker_slug, blocker_level = blocker
            reason = (
                "level" if level_rank(blocker_level) < level_rank(module.level) else "sequential"
            )
            gates_by_slug[slug] = ModuleGate(
                module_slug=slug,
                level=module.level,
                position=idx,
                unlocked=False,
                completed=completed,
                blocked_by=blocker_slug,
                reason=reason,
            )
        # The first incomplete module in gating order blocks everything
        # after it.
        if blocker is None and not completed:
            blocker = (slug, module.level)

    return [gates_by_slug[slug] for _, slug, _ in resolved]


def next_unlocked_module(gates: list[ModuleGate]) -> str | None:
    """The next module to work on: first unlocked-but-incomplete gate in
    gating order (not declared order)."""
    pending = [g for g in gates if g.unlocked and not g.completed]
    if not pending:
        return None
    # Re-derive gating order from (level_rank, position).
    pending.sort(key=lambda g: (level_rank(g.level), g.position))
    return pending[0].module_slug


def is_module_unlocked(slug: str, gates: list[ModuleGate]) -> bool:
    """Whether ``slug`` is unlocked among ``gates`` (False if unknown)."""
    return any(g.module_slug == slug and g.unlocked for g in gates)

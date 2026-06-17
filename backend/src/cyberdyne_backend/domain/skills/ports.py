"""Reader port for the skills context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.skills.entities import SkillInput


@runtime_checkable
class SkillMapReader(Protocol):
    async def skill_inputs_for_user(self, user_id: UUID) -> list[SkillInput]:
        """Per-skill (per-category) aggregates for the learner across
        published courses: lesson totals/progress, quiz best-scores, and a
        next-step suggestion. Mastery itself is computed in the domain."""
        ...

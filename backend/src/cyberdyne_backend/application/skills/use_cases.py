"""Use cases for the Skill Map (issue #165)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.skills import SkillMap, SkillMapReader, build_skill_map


@dataclass(slots=True)
class GetSkillMap:
    reader: SkillMapReader

    async def execute(self, user_id: UUID) -> SkillMap:
        inputs = await self.reader.skill_inputs_for_user(user_id)
        return build_skill_map(inputs)

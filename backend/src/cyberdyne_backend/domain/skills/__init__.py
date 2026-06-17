"""Skills bounded context.

Per-domain skill mastery + weak areas (the Profile Skill Map), derived
server-side from quiz performance + lesson/course completion rather than
the client's course-percent approximation. See issue #165.
"""

from cyberdyne_backend.domain.skills.entities import (
    MAX_SUGGESTIONS,
    WEAK_THRESHOLD,
    SkillInput,
    SkillMap,
    SkillMastery,
    build_skill_map,
)
from cyberdyne_backend.domain.skills.ports import SkillMapReader

__all__ = [
    "MAX_SUGGESTIONS",
    "WEAK_THRESHOLD",
    "SkillInput",
    "SkillMap",
    "SkillMapReader",
    "SkillMastery",
    "build_skill_map",
]

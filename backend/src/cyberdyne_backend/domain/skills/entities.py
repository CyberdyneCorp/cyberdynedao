"""Skill Map domain — per-domain mastery + weak areas (issue #165).

A *skill* maps to a course category; its *domain* is the parent category
(or the skill itself when top-level). Mastery is derived server-side from
the learner's lesson completion blended with quiz performance — a more
faithful signal than averaging raw course percent, which the client used
to approximate.

This module is pure: the reader supplies raw per-skill aggregates
(``SkillInput``) and ``build_skill_map`` folds them into the response
model. All thresholds/weights live here so the rule is one documented
place.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Mastery blend: lesson completion dominates, quiz performance refines it.
# When the learner has attempted no quiz in a skill, mastery is lesson
# completion alone (the quiz term is dropped, not treated as zero).
_LESSON_WEIGHT = 0.6
_QUIZ_WEIGHT = 0.4

# A skill the learner has engaged with but scores below this is "weak".
WEAK_THRESHOLD = 40

# Cap on next-step course suggestions returned.
MAX_SUGGESTIONS = 5


@dataclass(frozen=True, slots=True)
class SkillInput:
    """Raw per-skill aggregate assembled by the reader for one learner."""

    slug: str
    name: str
    domain: str
    course_count: int
    total_lessons: int
    # Sum of per-lesson percent (0..100) across the skill's lessons, with
    # un-started lessons contributing 0.
    lesson_percent_sum: int
    # Best score (0..100) per quiz the learner attempted in this skill.
    quiz_best_scores: tuple[int, ...] = ()
    # Lowest-progress incomplete course in the skill, if any — the
    # natural next step to study.
    suggestion_slug: str | None = None


@dataclass(frozen=True, slots=True)
class SkillMastery:
    id: str  # the category slug
    name: str
    domain: str
    mastery: int  # 0..100
    course_count: int
    weak: bool


@dataclass(frozen=True, slots=True)
class SkillMap:
    skills: list[SkillMastery] = field(default_factory=list)
    weak_areas: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def _lesson_completion(inp: SkillInput) -> float:
    if inp.total_lessons <= 0:
        return 0.0
    return inp.lesson_percent_sum / (100 * inp.total_lessons)


def _mastery_percent(inp: SkillInput) -> int:
    completion = _lesson_completion(inp)
    if inp.quiz_best_scores:
        quiz = sum(inp.quiz_best_scores) / len(inp.quiz_best_scores) / 100
        frac = _LESSON_WEIGHT * completion + _QUIZ_WEIGHT * quiz
    else:
        frac = completion
    return round(100 * max(0.0, min(frac, 1.0)))


def build_skill_map(inputs: list[SkillInput]) -> SkillMap:
    """Fold raw per-skill aggregates into the Skill Map response model."""
    skills: list[SkillMastery] = []
    weak_inputs: list[SkillInput] = []
    for inp in inputs:
        mastery = _mastery_percent(inp)
        weak = inp.course_count > 0 and mastery < WEAK_THRESHOLD
        if weak:
            weak_inputs.append(inp)
        skills.append(
            SkillMastery(
                id=inp.slug,
                name=inp.name,
                domain=inp.domain,
                mastery=mastery,
                course_count=inp.course_count,
                weak=weak,
            )
        )

    # Stable, client-friendly ordering: group by domain, then skill name.
    skills.sort(key=lambda s: (s.domain.lower(), s.name.lower()))

    # Suggest next-step courses from the weakest skills first.
    weak_inputs.sort(key=_mastery_percent)
    suggestions: list[str] = []
    for inp in weak_inputs:
        if inp.suggestion_slug and inp.suggestion_slug not in suggestions:
            suggestions.append(inp.suggestion_slug)
        if len(suggestions) >= MAX_SUGGESTIONS:
            break

    return SkillMap(
        skills=skills,
        weak_areas=[s.id for s in skills if s.weak],
        suggestions=suggestions,
    )

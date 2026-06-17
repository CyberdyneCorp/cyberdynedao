"""Unit tests for the Skill Map mastery formula (issue #165)."""

from __future__ import annotations

from cyberdyne_backend.domain.skills import (
    WEAK_THRESHOLD,
    SkillInput,
    build_skill_map,
)


def _inp(
    slug: str,
    *,
    name: str = "",
    domain: str = "General",
    course_count: int = 1,
    total_lessons: int = 0,
    lesson_percent_sum: int = 0,
    quiz_best_scores: tuple[int, ...] = (),
    suggestion_slug: str | None = None,
) -> SkillInput:
    return SkillInput(
        slug=slug,
        name=name or slug,
        domain=domain,
        course_count=course_count,
        total_lessons=total_lessons,
        lesson_percent_sum=lesson_percent_sum,
        quiz_best_scores=quiz_best_scores,
        suggestion_slug=suggestion_slug,
    )


def test_mastery_lesson_only_when_no_quiz() -> None:
    # 2 lessons, 50% avg completion, no quizzes -> mastery 50.
    sm = build_skill_map([_inp("calc", total_lessons=2, lesson_percent_sum=100)])
    assert sm.skills[0].mastery == 50


def test_mastery_blends_quiz_and_lessons() -> None:
    # completion = 200/(100*2) = 1.0 ; quiz avg = 50 -> 0.5
    # frac = 0.6*1.0 + 0.4*0.5 = 0.8 -> 80
    sm = build_skill_map(
        [_inp("calc", total_lessons=2, lesson_percent_sum=200, quiz_best_scores=(40, 60))]
    )
    assert sm.skills[0].mastery == 80


def test_weak_flagged_below_threshold() -> None:
    sm = build_skill_map(
        [
            _inp("strong", total_lessons=1, lesson_percent_sum=90),  # 90
            _inp("weak", total_lessons=1, lesson_percent_sum=30),  # 30
        ]
    )
    by_id = {s.id: s for s in sm.skills}
    assert by_id["strong"].weak is False
    assert by_id["weak"].weak is True
    assert by_id["weak"].mastery < WEAK_THRESHOLD
    assert sm.weak_areas == ["weak"]


def test_empty_skill_not_weak() -> None:
    # A category with courses but no lessons/quizzes is 0% — but only
    # flagged weak if it has courses; here course_count=0 means no signal.
    sm = build_skill_map([_inp("ghost", course_count=0, total_lessons=0)])
    assert sm.skills[0].weak is False
    assert sm.weak_areas == []


def test_suggestions_come_from_weak_skills_weakest_first() -> None:
    sm = build_skill_map(
        [
            _inp(
                "a", total_lessons=1, lesson_percent_sum=35, suggestion_slug="course-a"
            ),  # 35
            _inp(
                "b", total_lessons=1, lesson_percent_sum=10, suggestion_slug="course-b"
            ),  # 10 (weaker)
            _inp(
                "c", total_lessons=1, lesson_percent_sum=90, suggestion_slug="course-c"
            ),  # strong, no suggestion
        ]
    )
    # weakest first: b then a; c excluded (not weak).
    assert sm.suggestions == ["course-b", "course-a"]


def test_skills_sorted_by_domain_then_name() -> None:
    sm = build_skill_map(
        [
            _inp("z", name="Zeta", domain="Math"),
            _inp("a", name="Alpha", domain="Physics"),
            _inp("m", name="Mu", domain="Math"),
        ]
    )
    assert [s.id for s in sm.skills] == ["m", "z", "a"]  # Math(Mu,Zeta), Physics(Alpha)

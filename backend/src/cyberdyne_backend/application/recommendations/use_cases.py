"""Course recommendations for a signed-in learner.

A thin cross-context read: rank the published course catalogue against
the learner's own dashboard signals (modules completed, quizzes passed,
certificates earned) with a deterministic heuristic, then ask the chat
LLM for a short personalized intro on top of that fixed shortlist. The
*which courses* decision is pure code (so it's testable and stable); the
LLM only adds the narrative framing. One LLM call per request, skipped
entirely when the catalogue is empty.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import ChatLLMPort, ChatMessage, ChatRole
from cyberdyne_backend.domain.analytics import (
    AnalyticsRepository,
    LearnerDashboard,
    build_learner_dashboard,
)
from cyberdyne_backend.domain.courses import Course, CourseLevel, CourseRepository

_LEVEL_ORDINAL = {
    CourseLevel.BEGINNER: 0,
    CourseLevel.INTERMEDIATE: 1,
    CourseLevel.ADVANCED: 2,
}

_ADVISOR_SYSTEM_PROMPT = (
    "You are an encouraging learning advisor for Cyberdyne Academy. Given a learner's progress "
    "and a shortlist of recommended courses, write a warm 2-3 sentence intro that motivates them "
    "to start the shortlist. Do not invent courses beyond the ones listed, do not ask questions, "
    "and do not mention that you are an AI."
)

_EMPTY_SUMMARY = (
    "There are no published courses yet - check back soon as the Academy catalogue grows."
)


@dataclass(frozen=True, slots=True)
class CourseRecommendation:
    slug: str
    title: str
    level: str
    reason: str


@dataclass(frozen=True, slots=True)
class LearningRecommendations:
    summary: str
    courses: list[CourseRecommendation]


@dataclass(slots=True)
class RecommendCourses:
    courses: CourseRepository
    analytics: AnalyticsRepository
    llm: ChatLLMPort
    max_courses: int = field(default=3)

    async def execute(self, *, user_id: UUID) -> LearningRecommendations:
        dashboard = build_learner_dashboard(await self.analytics.learner_counts(user_id))
        catalogue = await self.courses.list_courses()  # published only
        ranked = self._rank(catalogue, dashboard)[: self.max_courses]
        recs = [
            CourseRecommendation(
                slug=course.slug,
                title=course.title,
                level=course.level.value,
                reason=self._reason(course, dashboard),
            )
            for course in ranked
        ]
        if not recs:
            return LearningRecommendations(summary=_EMPTY_SUMMARY, courses=[])
        summary = await self._summarize(dashboard, recs)
        return LearningRecommendations(summary=summary, courses=recs)

    def _target_level(self, dashboard: LearnerDashboard) -> int:
        """Where the learner sits on the Beginner->Advanced ladder.

        No completions at all -> Beginner. Some module/quiz progress ->
        Intermediate. A finished path or earned certificate -> Advanced.
        """
        if dashboard.certificates > 0 or dashboard.completed_paths > 0:
            return _LEVEL_ORDINAL[CourseLevel.ADVANCED]
        if dashboard.completed_modules > 0 or dashboard.quizzes_passed > 0:
            return _LEVEL_ORDINAL[CourseLevel.INTERMEDIATE]
        return _LEVEL_ORDINAL[CourseLevel.BEGINNER]

    def _rank(self, catalogue: list[Course], dashboard: LearnerDashboard) -> list[Course]:
        target = self._target_level(dashboard)

        def key(course: Course) -> tuple[bool, int, int, int]:
            ordinal = _LEVEL_ORDINAL[course.level]
            # Mandatory first; then nearest to the target level; then the
            # easier level; then catalogue order. ``not mandatory`` makes
            # mandatory courses sort ahead (False < True).
            return (not course.mandatory, abs(ordinal - target), ordinal, course.sort_order)

        return sorted(catalogue, key=key)

    def _reason(self, course: Course, dashboard: LearnerDashboard) -> str:
        if course.mandatory:
            return "Required course"
        ordinal = _LEVEL_ORDINAL[course.level]
        target = self._target_level(dashboard)
        if ordinal == target:
            return "Matches your current level"
        if ordinal < target:
            return "A solid refresher at a level you have covered"
        return "A step up to stretch your skills"

    async def _summarize(
        self, dashboard: LearnerDashboard, recs: list[CourseRecommendation]
    ) -> str:
        shortlist = "; ".join(f"{r.title} ({r.level})" for r in recs)
        prompt = (
            "Learner progress: "
            f"{dashboard.completed_modules} modules completed, "
            f"{dashboard.quizzes_passed}/{dashboard.quizzes_attempted} quizzes passed, "
            f"{dashboard.certificates} certificates earned.\n"
            f"Recommended courses: {shortlist}.\n"
            "Write the intro."
        )
        message = ChatMessage(
            id=uuid.uuid4(),
            session_id=uuid.uuid4(),
            role=ChatRole.USER,
            content=prompt,
        )
        response = await self.llm.complete(
            messages=[message], tools=[], system_prompt=_ADVISOR_SYSTEM_PROMPT
        )
        return response.content


__all__ = [
    "CourseRecommendation",
    "LearningRecommendations",
    "RecommendCourses",
]

"""Learner-context tools for the Global Agent Chat (issue #234).

A small, dedicated tool set — distinct from the Socratic tutor's
``CYBERDYNE_TOOLS`` — that exposes the *authenticated learner's own*
history so the answer agent can ground "what have I finished / what's
next" replies without dumping the whole history into the prompt.

Each tool reads ONLY the signed-in user's data: the ``user_id`` is held
on the dispatcher (taken from the request principal) and is never an LLM
argument. The dispatch surface mirrors ``ToolDispatcher.dispatch`` — every
result is JSON-stringified so the LLM gets a stable shape.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.application.courses import ListMyCourseProgress
from cyberdyne_backend.application.learning import GetMyLearningState
from cyberdyne_backend.application.recommendations import RecommendCourses
from cyberdyne_backend.domain.ai_chat import ToolCall, ToolSchema

logger = logging.getLogger("cyberdyne_backend.agent_chat.tools")


LEARNER_CONTEXT_TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="get_my_progress",
        description=(
            "The signed-in learner's progress across the courses they have started: "
            "each course's slug, completed-vs-total lesson counts, percent complete, and "
            "whether it's finished. Use this to answer 'what have I finished?', 'what am I "
            "studying?', or 'how far along am I?'."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="get_my_learning_state",
        description=(
            "The signed-in learner's active learning state: enrolled learning paths/tracks "
            "(with status), per-module progress, and earned certificates. Use this to ground "
            "answers about which track/path the learner is currently on."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="get_my_recommendations",
        description=(
            "Suggested next courses for the signed-in learner, ranked against their progress, "
            "plus a short motivating summary. Use this to answer 'what should I do next?' or "
            "'what do you recommend?'."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
]


@dataclass(slots=True)
class LearnerContextToolset:
    """The three use cases the learner-context tools read from, plus the
    authenticated ``user_id`` they are scoped to. Held by the dispatcher;
    the dispatcher only reads from it."""

    user_id: UUID
    list_my_progress: ListMyCourseProgress
    get_my_learning_state: GetMyLearningState
    recommend_courses: RecommendCourses


class LearnerContextDispatcher:
    """Runs one learner-context tool call to completion and returns a string
    the LLM can consume next. Every result is JSON-stringified. Every tool
    reads ONLY ``ctx.user_id`` — the user id is never taken from the call's
    arguments, so the agent can't read another learner's data."""

    def __init__(self, ctx: LearnerContextToolset) -> None:
        self._ctx = ctx

    async def dispatch(self, call: ToolCall) -> str:
        try:
            if call.name == "get_my_progress":
                return await self._get_my_progress()
            if call.name == "get_my_learning_state":
                return await self._get_my_learning_state()
            if call.name == "get_my_recommendations":
                return await self._get_my_recommendations()
        except Exception as exc:  # never let a tool break the turn
            logger.exception("learner-context tool %s failed", call.name)
            return json.dumps({"error": "tool_failed", "detail": str(exc)})
        return json.dumps({"error": "unknown_tool", "tool": call.name})

    async def _get_my_progress(self) -> str:
        items = await self._ctx.list_my_progress.execute(user_id=self._ctx.user_id)
        return json.dumps(
            {
                "courses": [
                    {
                        "slug": p.slug,
                        "completedLessons": p.completed_lessons,
                        "totalLessons": p.total_lessons,
                        "percent": p.percent,
                        "completed": p.completed,
                    }
                    for p in items
                    if p.completed_lessons > 0
                ]
            }
        )

    async def _get_my_learning_state(self) -> str:
        state = await self._ctx.get_my_learning_state.execute(self._ctx.user_id)
        return json.dumps(
            {
                "enrollments": [
                    {"pathSlug": e.path_slug, "status": e.status.value} for e in state.enrollments
                ],
                "progress": [
                    {"moduleSlug": p.module_slug, "percent": p.percent}
                    for p in state.progress_by_module.values()
                ],
                "certificates": [
                    {"pathSlug": c.path_slug, "verificationHash": c.verification_hash}
                    for c in state.certificates
                ],
            }
        )

    async def _get_my_recommendations(self) -> str:
        recs = await self._ctx.recommend_courses.execute(user_id=self._ctx.user_id)
        return json.dumps(
            {
                "summary": recs.summary,
                "courses": [
                    {"slug": r.slug, "title": r.title, "level": r.level, "reason": r.reason}
                    for r in recs.courses
                ],
            }
        )


__all__ = [
    "LEARNER_CONTEXT_TOOLS",
    "LearnerContextDispatcher",
    "LearnerContextToolset",
]

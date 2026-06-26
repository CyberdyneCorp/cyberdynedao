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
from typing import Any, Literal
from uuid import UUID

from cyberdyne_backend.application.courses import ListMyCourseProgress
from cyberdyne_backend.application.learning import GetMyLearningState
from cyberdyne_backend.application.lesson_notes import ListUserNotes
from cyberdyne_backend.application.recommendations import RecommendCourses
from cyberdyne_backend.domain.ai_chat import ToolCall, ToolSchema
from cyberdyne_backend.domain.notebook import InvalidNoteError, NoteType, parse_note_type

logger = logging.getLogger("cyberdyne_backend.agent_chat.tools")

# Bound the notes payload fed to the LLM so a learner with a huge note corpus
# can't blow up the prompt: cap the count and truncate each body.
_MAX_NOTES = 50
_MAX_NOTE_BODY = 600
_NOTEBOOK_OPS = ("create", "append")


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
    ToolSchema(
        name="get_my_notes",
        description=(
            "The signed-in learner's own lesson notes — each note's course slug, lesson id, the "
            "highlighted quote, and the learner's note body. Optionally filter to one course by "
            "slug. Use this to synthesize the learner's notes (e.g. build a mindmap or summary) "
            "before proposing a Notebook entry."
        ),
        parameters={
            "type": "object",
            "properties": {
                "course_slug": {
                    "type": "string",
                    "description": "Restrict to one course by its slug; omit for all courses.",
                }
            },
            "required": [],
        },
    ),
]

# Action-proposal tool (not a read): the agent calls it to PROPOSE a Notebook
# write when the learner asks to save/synthesize their notes. The backend only
# records the proposal — it performs NO write. The client commits via the
# existing notebook endpoints after the learner confirms (issue #243).
NOTEBOOK_ACTION_TOOL = ToolSchema(
    name="propose_notebook_action",
    description=(
        "Propose saving the answer to the learner's Notebook. Call this ONLY when the learner "
        "asks to save or synthesize something into the Notebook (e.g. 'make a mindmap of my "
        "Algorithms notes and save it as a new Notebook', 'add that to my X notebook'). Do NOT "
        "call it for ordinary questions. The system records the proposal; the learner confirms "
        "and the client performs the write — you never write yourself. Render mindmaps as a "
        "```mermaid mindmap block in `body`."
    ),
    parameters={
        "type": "object",
        "properties": {
            "op": {
                "type": "string",
                "enum": list(_NOTEBOOK_OPS),
                "description": "'create' a new Notebook entry, or 'append' to an existing one.",
            },
            "title": {"type": "string", "description": "Title for a 'create' op."},
            "type": {
                "type": "string",
                "enum": [t.value for t in NoteType],
                "description": "Notebook note type (e.g. 'theory').",
            },
            "target_note_id": {
                "type": "string",
                "description": "The existing Notebook note id to append to (required for 'append').",
            },
            "body": {
                "type": "string",
                "description": "The Markdown body to save (mindmaps as a ```mermaid block).",
            },
        },
        "required": ["op", "body"],
    },
)

# The full tool set the answer agent exposes: the read-only learner-context
# tools plus the write-proposal tool.
AGENT_TOOLS: list[ToolSchema] = [*LEARNER_CONTEXT_TOOLS, NOTEBOOK_ACTION_TOOL]


@dataclass(frozen=True, slots=True)
class NotebookActionProposal:
    """A PROPOSED Notebook write surfaced on the answer turn — never executed
    server-side. ``op`` is create/append; ``note_type`` is a ``NoteType`` raw
    value or ``None``; ``target_note_id`` is set for append."""

    op: Literal["create", "append"]
    body: str
    title: str | None = None
    note_type: str | None = None
    target_note_id: str | None = None


@dataclass(slots=True)
class LearnerContextToolset:
    """The three use cases the learner-context tools read from, plus the
    authenticated ``user_id`` they are scoped to. Held by the dispatcher;
    the dispatcher only reads from it."""

    user_id: UUID
    list_my_progress: ListMyCourseProgress
    get_my_learning_state: GetMyLearningState
    recommend_courses: RecommendCourses
    list_user_notes: ListUserNotes


class LearnerContextDispatcher:
    """Runs one learner-context tool call to completion and returns a string
    the LLM can consume next. Every result is JSON-stringified. Every tool
    reads ONLY ``ctx.user_id`` — the user id is never taken from the call's
    arguments, so the agent can't read another learner's data."""

    def __init__(self, ctx: LearnerContextToolset) -> None:
        self._ctx = ctx
        # The last Notebook action the LLM proposed this turn, if any. Captured
        # here (not executed) and read by the turn after the tool-call loop.
        self.proposed_action: NotebookActionProposal | None = None

    async def dispatch(self, call: ToolCall) -> str:
        try:
            if call.name == "get_my_progress":
                return await self._get_my_progress()
            if call.name == "get_my_learning_state":
                return await self._get_my_learning_state()
            if call.name == "get_my_recommendations":
                return await self._get_my_recommendations()
            if call.name == "get_my_notes":
                return await self._get_my_notes(_args(call))
            if call.name == "propose_notebook_action":
                return self._propose_notebook_action(_args(call))
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

    async def _get_my_notes(self, args: dict[str, Any]) -> str:
        raw_slug = args.get("course_slug")
        course_slug = raw_slug.strip() if isinstance(raw_slug, str) and raw_slug.strip() else None
        page = await self._ctx.list_user_notes.execute(
            user_id=self._ctx.user_id, course_slug=course_slug, limit=_MAX_NOTES
        )
        return json.dumps(
            {
                "notes": [
                    {
                        "courseSlug": n.course_slug,
                        "lessonId": n.lesson_id,
                        "quote": n.quote,
                        "body": n.body[:_MAX_NOTE_BODY],
                    }
                    for n in page.items
                ]
            }
        )

    def _propose_notebook_action(self, args: dict[str, Any]) -> str:
        """Record (do NOT execute) a proposed Notebook write. Returns an ack so
        the LLM knows the proposal was captured and can give its final answer."""
        op = args.get("op")
        if op not in _NOTEBOOK_OPS:
            return json.dumps({"error": "invalid_op", "expected": list(_NOTEBOOK_OPS)})
        body = args.get("body")
        if not isinstance(body, str) or not body.strip():
            return json.dumps({"error": "missing_body"})
        target = args.get("target_note_id")
        target_note_id = target.strip() if isinstance(target, str) and target.strip() else None
        if op == "append" and target_note_id is None:
            return json.dumps({"error": "append_requires_target_note_id"})
        note_type = _coerce_note_type(args.get("type"))
        title = args.get("title")
        self.proposed_action = NotebookActionProposal(
            op=op,
            body=body.strip(),
            title=title.strip() if isinstance(title, str) and title.strip() else None,
            note_type=note_type,
            target_note_id=target_note_id,
        )
        return json.dumps({"status": "proposed", "op": op})


def _args(call: ToolCall) -> dict[str, Any]:
    """Parse a tool call's JSON arguments into a dict; ``{}`` on anything
    unparseable so a malformed call degrades instead of breaking the turn."""
    if not call.arguments_json:
        return {}
    try:
        parsed = json.loads(call.arguments_json)
    except (ValueError, TypeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _coerce_note_type(raw: Any) -> str | None:
    """A valid ``NoteType`` raw value, or ``None`` for absent/unknown — an
    invalid type is dropped rather than failing the proposal."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return parse_note_type(raw.strip()).value
    except InvalidNoteError:
        return None


__all__ = [
    "AGENT_TOOLS",
    "LEARNER_CONTEXT_TOOLS",
    "NOTEBOOK_ACTION_TOOL",
    "LearnerContextDispatcher",
    "LearnerContextToolset",
    "NotebookActionProposal",
]

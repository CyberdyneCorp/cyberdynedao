"""Pydantic schemas for the Global Agent Chat endpoints (issue #234).

Reuses the chat ``ChatMessageResponse`` shape for the assistant message, and
adds the answer-agent extras: ``courseRefs`` (ranked, deep-linkable catalog
hits that cover the topic) and an optional ``unmatchedTopic`` (recorded to the
demand registry when nothing in the catalog covers the topic).
"""

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from cyberdyne_backend.adapters.inbound.api.ai_chat.schemas import (
    ChatHistoryResponse,
    ChatMessageResponse,
    StartSessionResponse,
)

__all__ = [
    "AgentMessageRequest",
    "AgentTurnResponse",
    "ChatHistoryResponse",
    "CourseRefView",
    "NotebookActionView",
    "StartSessionResponse",
    "UnmatchedTopicView",
]


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AgentMessageRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    content: str = Field(min_length=1, max_length=4000)
    # Upload UUIDs the learner attached (e.g. a photographed question). The
    # answer agent ingests each (text-extracted / vision-described) to ground
    # its answer. Optional — absent for plain text turns.
    attachments: list[str] = Field(default_factory=list, max_length=20)


class CourseRefView(_CamelModel):
    """A ranked catalog hit that covers the answered topic. ``lessonId`` is set
    for a deep-linkable lesson entry; ``None`` for a course-level entry."""

    course_slug: str
    lesson_id: UUID | None = None
    score: float
    match_reason: str


class UnmatchedTopicView(_CamelModel):
    """The out-of-catalog topic the agent answered, recorded to the demand
    registry so it can be authored later."""

    topic: str
    subject: str | None = None


class NotebookActionView(_CamelModel):
    """A PROPOSED Notebook write the client commits after the learner confirms
    (issue #243). Present only when the learner asked to save/synthesize to the
    Notebook; the backend never writes. ``type`` is a NotebookNoteType raw
    value; ``targetNoteId`` is set for ``append``."""

    op: Literal["create", "append"]
    body: str
    title: str | None = None
    note_type: str | None = Field(default=None, alias="type")
    target_note_id: str | None = None


class AgentTurnResponse(_CamelModel):
    """One answer turn: the assistant message, the courses that cover the topic,
    an optional recorded demand topic (catalog miss), and an optional proposed
    Notebook action (when the learner asked to save to the Notebook)."""

    message: ChatMessageResponse
    course_refs: list[CourseRefView] = []
    unmatched_topic: UnmatchedTopicView | None = None
    notebook_action: NotebookActionView | None = None

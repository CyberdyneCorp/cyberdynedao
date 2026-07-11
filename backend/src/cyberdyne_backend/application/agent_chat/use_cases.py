"""Global Agent Chat use cases (issue #234).

A top-level assistant reachable with NO course open. Unlike the lesson-anchored
Socratic tutor it ANSWERS DIRECTLY, is aware of the learner's own history (via
the small :mod:`agent_chat.tools` learner-context tool set), accepts images, and
with each answer points to the course/lesson that covers the topic. When nothing
in the catalog covers it, the topic is logged to the demand registry (#232) for
future development.

Reuses the chat ``ChatRepository`` (sessions/messages) and ``ChatLLMPort`` — no
new sessions table. The turn shape mirrors ``ai_chat.RunChatTurn``: persist the
user message, run a bounded tool-call loop persisting assistant/tool messages,
return the final assistant message — then route to courses and (on a no-match)
record demand.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from uuid import UUID

from cyberdyne_backend.application.agent_chat.tools import (
    AGENT_TOOLS,
    LearnerContextDispatcher,
    NotebookActionProposal,
)
from cyberdyne_backend.application.ai_chat.use_cases import (
    build_uploaded_attachments_block,
    build_user_context_block,
)
from cyberdyne_backend.application.course_demand import SubmitCourseRequest
from cyberdyne_backend.application.course_finder import CatalogSearchIndex
from cyberdyne_backend.domain.ai_chat import (
    AttachmentIngestorPort,
    AttachmentRef,
    ChatLLMPort,
    ChatMessage,
    ChatRepository,
    new_assistant_message,
    new_tool_message,
    new_user_message,
)
from cyberdyne_backend.domain.auth_identity import UserProfile
from cyberdyne_backend.domain.course_demand import RequestSource
from cyberdyne_backend.domain.course_finder import CourseMatch

logger = logging.getLogger("cyberdyne_backend.agent_chat")

# Answer-mode persona — direct, concise, correct. Deliberately NOT the Socratic
# tutor prompt: this agent gives the answer, then points to where it's covered.
ANSWER_AGENT_SYSTEM_PROMPT = """\
You are the Cyberdyne Academy assistant — a top-level helper a signed-in
learner can ask anything, with no course open.

# How to answer
  - ANSWER DIRECTLY and correctly. You are NOT a Socratic tutor here — give
    the actual answer, worked clearly and concisely. No emoji, no fluff.
  - When the learner asks about their OWN learning — "what have I finished?",
    "what am I studying?", "what's next?", "what do you recommend?" — call the
    learner-context tools to ground your answer in their real data:
      * `get_my_progress` — courses they've started (completed vs total, %).
      * `get_my_learning_state` — their active tracks/paths + certificates.
      * `get_my_recommendations` — suggested next courses.
      * `get_my_notes` — their own lesson notes (optionally one course), to
        synthesize (e.g. build a mindmap or summary) before saving.
    Never invent progress, course names, or notes; read them from the tools.
  - For the OUTSIDE world — current events, external facts, people, anything
    beyond Cyberdyne's own content — call `web_search` and cite the result
    URLs. When the learner shares a YouTube link or asks about a video, call
    `youtube_transcript`; for a playlist link, call `youtube_playlist`. Ground
    your answer in what the tools return; never invent web facts.
  - When (and ONLY when) the learner asks to SAVE or SYNTHESIZE something into
    their Notebook ("make a mindmap of my <course> notes and save it", "add
    that to my <X> notebook"), call `propose_notebook_action` with the content
    — `op:"create"` for a new entry (with a `title` + `type`) or `op:"append"`
    to an existing one (with `target_note_id`). Render a mindmap as a
    ```mermaid mindmap block in `body`. You only PROPOSE; the learner confirms
    and the app saves it. Do NOT call it for ordinary questions.
  - If the learner attached an image or document (e.g. a photographed
    question), it is provided to you below as extracted text / a vision
    description. Answer grounded in that content; do not ask them to retype it.
  - Math typesets as LaTeX: wrap inline math in \\( … \\) and display math in
    \\[ … \\] (or $$ … $$). Do NOT use single $…$.
  - After answering, the system itself points the learner to the course/lesson
    that covers the topic — you do not need to name a specific course slug
    yourself unless a learner-context tool told you one.
"""

MAX_TOOL_ROUNDS = 4
# Cap on how much of the answer text we fold into the catalog-routing query —
# enough to capture the topic without drowning the original question.
_ANSWER_QUERY_CHARS = 600


@dataclass(frozen=True, slots=True)
class UnmatchedTopic:
    """The topic the agent answered that no catalog course covers — recorded to
    the demand registry and echoed back so the client can confirm it."""

    topic: str
    subject: str | None = None


@dataclass(frozen=True, slots=True)
class AnswerTurnResult:
    """One answer turn: the assistant message, the ranked courses that cover the
    topic (deep-linkable), an optional recorded demand topic (catalog miss), and
    an optional proposed Notebook action (when the learner asked to save to the
    Notebook — proposed only, never executed server-side, issue #243)."""

    message: ChatMessage
    course_refs: list[CourseMatch]
    unmatched_topic: UnmatchedTopic | None = None
    notebook_action: NotebookActionProposal | None = None


@dataclass(slots=True)
class AnswerAgentTurn:
    """Runs one answer turn end-to-end for a signed-in learner: persist the user
    message (with any ingested attachments), run the LLM in a bounded tool-call
    loop over the learner-context tools, persist intermediate tool results and
    the final assistant message, then route the topic to the course catalog —
    recording unmatched topics to the demand registry."""

    repo: ChatRepository
    llm: ChatLLMPort
    learner_tools: LearnerContextDispatcher
    catalog_index: CatalogSearchIndex
    submit_course_request: SubmitCourseRequest
    user_id: UUID
    user: UserProfile | None = None
    ingestor: AttachmentIngestorPort | None = None
    system_prompt: str = ANSWER_AGENT_SYSTEM_PROMPT
    max_tool_rounds: int = MAX_TOOL_ROUNDS
    top_k: int = field(default=5)

    async def execute(
        self,
        *,
        session_id: UUID,
        user_content: str,
        attachments: tuple[str, ...] = (),
    ) -> AnswerTurnResult:
        # Raises ChatSessionNotFoundError if missing.
        await self.repo.get_session(session_id)

        attach_suffix, refs = await self._resolve_attachments(attachments)
        await self.repo.append_message(
            new_user_message(session_id=session_id, content=user_content, attachments=refs)
        )

        effective_prompt = self.system_prompt + build_user_context_block(self.user)
        effective_prompt += attach_suffix

        answer = await self._run_loop(session_id=session_id, system_prompt=effective_prompt)

        course_refs, unmatched = await self._route(
            question=user_content, answer_text=answer.content
        )
        # A Notebook write the LLM proposed via the tool, if any — surfaced for
        # the client to commit after confirmation; never executed here (#243).
        return AnswerTurnResult(
            message=answer,
            course_refs=course_refs,
            unmatched_topic=unmatched,
            notebook_action=self.learner_tools.proposed_action,
        )

    async def _resolve_attachments(
        self, attachments: tuple[str, ...]
    ) -> tuple[str, tuple[AttachmentRef, ...]]:
        """Ingest attached upload UUIDs (text-extracted / vision-described) and
        inline them as a grounding block, returning the prompt suffix and the
        resolved refs to persist on the user message. Non-UUID tokens are
        ignored — this agent has no interpreter workspace."""
        upload_ids: list[UUID] = []
        for token in attachments:
            try:
                upload_ids.append(UUID(token))
            except ValueError:
                continue
        if not upload_ids or self.ingestor is None:
            return "", ()
        ingested = await self.ingestor.ingest(tuple(upload_ids))
        suffix = build_uploaded_attachments_block(ingested)
        return suffix, tuple(item.ref for item in ingested)

    async def _run_loop(self, *, session_id: UUID, system_prompt: str) -> ChatMessage:
        for _ in range(self.max_tool_rounds):
            transcript = await self.repo.list_messages(session_id)
            response = await self.llm.complete(
                messages=transcript,
                tools=AGENT_TOOLS,
                system_prompt=system_prompt,
            )
            assistant_msg = new_assistant_message(
                session_id=session_id,
                content=response.content,
                tool_calls=response.tool_calls,
                tokens_in=response.tokens_in,
                tokens_out=response.tokens_out,
                model=response.model,
            )
            await self.repo.append_message(assistant_msg)
            if not response.tool_calls:
                return assistant_msg
            for call in response.tool_calls:
                result_text = await self.learner_tools.dispatch(call)
                await self.repo.append_message(
                    new_tool_message(
                        session_id=session_id, tool_call_id=call.id, content=result_text
                    )
                )
        # Hit the cap — return the last assistant turn we wrote.
        transcript = await self.repo.list_messages(session_id)
        return transcript[-1]

    async def _route(
        self, *, question: str, answer_text: str
    ) -> tuple[list[CourseMatch], UnmatchedTopic | None]:
        """Rank the catalog against the question (+ a slice of the answer). A
        hit is returned as ``courseRefs``; a miss is recorded to the demand
        registry as an AGENT-sourced request and echoed back."""
        query = _routing_query(question, answer_text)
        matches = await self.catalog_index.search(query, top_k=self.top_k)
        if matches:
            return matches, None
        topic = (question or answer_text).strip()[:256]
        if not topic:
            return [], None
        unmatched = UnmatchedTopic(topic=topic, subject=None)
        await self.submit_course_request.execute(
            user_id=self.user_id,
            topic=topic,
            source=RequestSource.AGENT,
            source_question_text=question or None,
        )
        return [], unmatched


def _routing_query(question: str, answer_text: str) -> str:
    """Fold the learner's question + a slice of the answer into one search
    string, so routing reflects the actual topic discussed."""
    parts = [question.strip(), answer_text.strip()[:_ANSWER_QUERY_CHARS]]
    return " ".join(p for p in parts if p).strip()


__all__ = [
    "ANSWER_AGENT_SYSTEM_PROMPT",
    "AnswerAgentTurn",
    "AnswerTurnResult",
    "UnmatchedTopic",
]

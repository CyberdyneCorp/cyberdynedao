"""Unit tests for the Global Agent Chat (issue #234).

Covers the AnswerAgentTurn use case and the LearnerContextDispatcher with
fakes (fake ChatRepository, fake LLM, fake CatalogSearchIndex, fake
SubmitCourseRequest, fake ingestor, fake learner-context use cases):

  * answer turn returns the answer + courseRefs when the index matches;
  * an index miss records an AGENT-sourced demand request AND returns the topic;
  * a learner-context tool round calls the right use case scoped to the user,
    and the result feeds the next LLM round;
  * attachments (upload UUIDs) are ingested and grounded;
  * each learner-context tool returns the user's data as JSON, scoped to the
    authenticated user (a tool never reads another user's data).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import cast

import pytest

from cyberdyne_backend.application.agent_chat import (
    AnswerAgentTurn,
    LearnerContextDispatcher,
    LearnerContextToolset,
)
from cyberdyne_backend.application.agent_chat.use_cases import _routing_query
from cyberdyne_backend.domain.ai_chat import (
    AttachmentRef,
    ChatMessage,
    ChatRole,
    ChatSession,
    ChatSessionNotFoundError,
    IngestedAttachment,
    LLMResponse,
    ToolCall,
)
from cyberdyne_backend.domain.course_demand import RequestSource
from cyberdyne_backend.domain.course_finder import CourseMatch

# ── Fakes ────────────────────────────────────────────────────────────


class _FakeChatRepo:
    def __init__(self) -> None:
        self.sessions: dict[uuid.UUID, ChatSession] = {}
        self.messages: list[ChatMessage] = []

    async def save_session(self, session: ChatSession) -> None:
        self.sessions[session.id] = session

    async def get_session(self, session_id: uuid.UUID) -> ChatSession:
        if session_id not in self.sessions:
            raise ChatSessionNotFoundError(session_id)
        return self.sessions[session_id]

    async def append_message(self, message: ChatMessage) -> None:
        self.messages.append(message)

    async def list_messages(
        self,
        session_id: uuid.UUID,
        *,
        limit: int | None = None,
        before: tuple[datetime, uuid.UUID] | None = None,
    ) -> list[ChatMessage]:
        msgs = [m for m in self.messages if m.session_id == session_id]
        msgs.sort(key=lambda m: (m.created_at, m.id))
        if before is not None:
            msgs = [m for m in msgs if (m.created_at, m.id) < before]
        if limit is not None:
            msgs = msgs[-limit:]
        return msgs


class _ScriptedLLM:
    def __init__(self, replies: list[LLMResponse]) -> None:
        self._replies = list(replies)
        self.calls = 0
        self.last_system_prompt = ""

    async def complete(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        self.calls += 1
        self.last_system_prompt = system_prompt
        self.last_tools = tools
        if not self._replies:
            return LLMResponse(content="(no more scripted replies)")
        return self._replies.pop(0)

    async def stream(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        raise NotImplementedError


class _FakeIndex:
    """Returns canned matches; records the query it was searched with."""

    def __init__(self, matches: list[CourseMatch]) -> None:
        self._matches = matches
        self.queries: list[str] = []

    async def search(self, query_text: str, *, top_k: int = 5) -> list[CourseMatch]:
        self.queries.append(query_text)
        return list(self._matches)


class _FakeSubmitCourseRequest:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def execute(self, **kwargs):  # type: ignore[no-untyped-def]
        self.calls.append(kwargs)
        return kwargs


class _FakeIngestor:
    def __init__(self, ingested: tuple[IngestedAttachment, ...]) -> None:
        self._ingested = ingested
        self.seen: tuple[uuid.UUID, ...] | None = None

    async def ingest(self, upload_ids: tuple[uuid.UUID, ...]) -> tuple[IngestedAttachment, ...]:
        self.seen = upload_ids
        return self._ingested


class _RecordingProgressUC:
    """Stands in for ListMyCourseProgress — records the user_id it's called
    with, returns canned per-course progress rows."""

    def __init__(self, rows) -> None:  # type: ignore[no-untyped-def]
        self._rows = rows
        self.seen_user_id: uuid.UUID | None = None

    async def execute(self, *, user_id):  # type: ignore[no-untyped-def]
        self.seen_user_id = user_id
        return self._rows


class _RecordingLearningStateUC:
    def __init__(self, state) -> None:  # type: ignore[no-untyped-def]
        self._state = state
        self.seen_user_id: uuid.UUID | None = None

    async def execute(self, user_id):  # type: ignore[no-untyped-def]
        self.seen_user_id = user_id
        return self._state


class _RecordingRecommendUC:
    def __init__(self, recs) -> None:  # type: ignore[no-untyped-def]
        self._recs = recs
        self.seen_user_id: uuid.UUID | None = None

    async def execute(self, *, user_id):  # type: ignore[no-untyped-def]
        self.seen_user_id = user_id
        return self._recs


class _RecordingNotesUC:
    """Stands in for ListUserNotes — records the (user_id, course_slug, limit)
    it was called with, returns a canned page."""

    def __init__(self, items) -> None:  # type: ignore[no-untyped-def]
        self._items = items
        self.seen_user_id: uuid.UUID | None = None
        self.seen_course_slug: str | None = None
        self.seen_limit: int | None = None

    async def execute(self, *, user_id, course_slug=None, limit=50):  # type: ignore[no-untyped-def]
        self.seen_user_id = user_id
        self.seen_course_slug = course_slug
        self.seen_limit = limit
        return type("Page", (), {"items": self._items, "next_cursor": None})()


class _NoteRow:
    def __init__(self, course_slug, lesson_id, quote, body) -> None:  # type: ignore[no-untyped-def]
        self.course_slug = course_slug
        self.lesson_id = lesson_id
        self.quote = quote
        self.body = body


# Lightweight data holders matching the duck-typed shapes the dispatcher reads.
class _Row:
    def __init__(self, slug, completed_lessons, total_lessons, percent, completed):  # type: ignore[no-untyped-def]
        self.slug = slug
        self.completed_lessons = completed_lessons
        self.total_lessons = total_lessons
        self.percent = percent
        self.completed = completed


class _Enrollment:
    def __init__(self, path_slug, status) -> None:  # type: ignore[no-untyped-def]
        self.path_slug = path_slug
        self.status = type("S", (), {"value": status})()


class _ModuleProgress:
    def __init__(self, module_slug, percent) -> None:  # type: ignore[no-untyped-def]
        self.module_slug = module_slug
        self.percent = percent


class _Cert:
    def __init__(self, path_slug, verification_hash) -> None:  # type: ignore[no-untyped-def]
        self.path_slug = path_slug
        self.verification_hash = verification_hash


class _LearningState:
    def __init__(self, enrollments, progress_by_module, certificates) -> None:  # type: ignore[no-untyped-def]
        self.enrollments = enrollments
        self.progress_by_module = progress_by_module
        self.certificates = certificates


class _Rec:
    def __init__(self, slug, title, level, reason) -> None:  # type: ignore[no-untyped-def]
        self.slug = slug
        self.title = title
        self.level = level
        self.reason = reason


class _Recommendations:
    def __init__(self, summary, courses) -> None:  # type: ignore[no-untyped-def]
        self.summary = summary
        self.courses = courses


# ── Helpers ──────────────────────────────────────────────────────────


def _seeded_session(repo: _FakeChatRepo) -> uuid.UUID:
    session = ChatSession(id=uuid.uuid4(), user_id=uuid.uuid4(), created_at=_now())
    repo.sessions[session.id] = session
    return session.id


def _now():  # type: ignore[no-untyped-def]
    from datetime import UTC, datetime

    return datetime.now(tz=UTC)


def _toolset(user_id: uuid.UUID, **overrides):  # type: ignore[no-untyped-def]
    progress = overrides.get("progress", _RecordingProgressUC([]))
    learning = overrides.get("learning", _RecordingLearningStateUC(_LearningState([], {}, [])))
    recommend = overrides.get("recommend", _RecordingRecommendUC(_Recommendations("go", [])))
    notes = overrides.get("notes", _RecordingNotesUC([]))
    return LearnerContextDispatcher(
        LearnerContextToolset(
            user_id=user_id,
            list_my_progress=cast("object", progress),  # type: ignore[arg-type]
            get_my_learning_state=cast("object", learning),  # type: ignore[arg-type]
            recommend_courses=cast("object", recommend),  # type: ignore[arg-type]
            list_user_notes=cast("object", notes),  # type: ignore[arg-type]
        )
    )


def _turn(repo, llm, *, index, submit, user_id, ingestor=None):  # type: ignore[no-untyped-def]
    return AnswerAgentTurn(
        repo=repo,
        llm=cast("object", llm),  # type: ignore[arg-type]
        learner_tools=_toolset(user_id),
        catalog_index=cast("object", index),  # type: ignore[arg-type]
        submit_course_request=cast("object", submit),  # type: ignore[arg-type]
        user_id=user_id,
        ingestor=ingestor,
    )


# ── AnswerAgentTurn ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_answer_turn_returns_course_refs_when_index_matches() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    llm = _ScriptedLLM([LLMResponse(content="The eigenvalues are the roots of det(A-λI)=0.")])
    match = CourseMatch(
        course_slug="linear-algebra",
        lesson_id=uuid.uuid4(),
        score=0.9,
        match_reason="matched lesson: eigenvalues",
    )
    submit = _FakeSubmitCourseRequest()
    turn = _turn(repo, llm, index=_FakeIndex([match]), submit=submit, user_id=user_id)

    result = await turn.execute(session_id=session_id, user_content="What is an eigenvalue?")

    assert result.message.role is ChatRole.ASSISTANT
    assert result.course_refs == [match]
    assert result.unmatched_topic is None
    assert submit.calls == []  # nothing recorded when the catalog covers it


@pytest.mark.asyncio
async def test_answer_turn_records_unmatched_topic_on_index_miss() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    llm = _ScriptedLLM([LLMResponse(content="Roman legions used the testudo formation.")])
    submit = _FakeSubmitCourseRequest()
    turn = _turn(repo, llm, index=_FakeIndex([]), submit=submit, user_id=user_id)

    result = await turn.execute(
        session_id=session_id, user_content="Explain Roman siege warfare tactics"
    )

    assert result.course_refs == []
    assert result.unmatched_topic is not None
    assert result.unmatched_topic.topic == "Explain Roman siege warfare tactics"
    # Recorded to the demand registry as an AGENT-sourced request, scoped to user.
    assert len(submit.calls) == 1
    call = submit.calls[0]
    assert call["user_id"] == user_id
    assert call["source"] is RequestSource.AGENT
    assert call["topic"] == "Explain Roman siege warfare tactics"


@pytest.mark.asyncio
async def test_learner_context_tool_round_feeds_next_llm_round() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    # Round 1: the LLM asks for the learner's progress. Round 2: it answers.
    llm = _ScriptedLLM(
        [
            LLMResponse(
                content="",
                tool_calls=(ToolCall(id="c1", name="get_my_progress", arguments_json="{}"),),
            ),
            LLMResponse(content="You've finished 1 of 2 lessons in Linear Algebra."),
        ]
    )
    progress = _RecordingProgressUC(
        [_Row("linear-algebra", completed_lessons=1, total_lessons=2, percent=50, completed=False)]
    )
    turn = AnswerAgentTurn(
        repo=repo,
        llm=cast("object", llm),  # type: ignore[arg-type]
        learner_tools=_toolset(user_id, progress=progress),
        catalog_index=cast("object", _FakeIndex([])),  # type: ignore[arg-type]
        submit_course_request=cast("object", _FakeSubmitCourseRequest()),  # type: ignore[arg-type]
        user_id=user_id,
    )

    result = await turn.execute(session_id=session_id, user_content="What have I finished?")

    assert llm.calls == 2  # tool round, then the answer round
    assert progress.seen_user_id == user_id  # scoped to the authenticated user
    assert "finished 1 of 2" in result.message.content
    # The tool result was persisted as a TOOL message between the two rounds.
    tool_msgs = [m for m in repo.messages if m.role is ChatRole.TOOL]
    assert len(tool_msgs) == 1
    assert "linear-algebra" in tool_msgs[0].content


@pytest.mark.asyncio
async def test_answer_turn_ingests_and_grounds_attachments() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    upload_id = uuid.uuid4()
    ref = AttachmentRef(id=upload_id, filename="question.png", content_type="image/png")
    ingestor = _FakeIngestor((IngestedAttachment(ref=ref, text="A photo of: solve 2x + 3 = 7"),))
    llm = _ScriptedLLM([LLMResponse(content="x = 2.")])
    turn = _turn(
        repo,
        llm,
        index=_FakeIndex([]),
        submit=_FakeSubmitCourseRequest(),
        user_id=user_id,
        ingestor=ingestor,
    )

    result = await turn.execute(
        session_id=session_id,
        user_content="Solve the attached problem",
        attachments=(str(upload_id),),
    )

    assert ingestor.seen == (upload_id,)
    # The extracted text was inlined into the system prompt as grounding.
    assert "solve 2x + 3 = 7" in llm.last_system_prompt
    # The resolved ref echoes back on the persisted user message.
    user_msg = next(m for m in repo.messages if m.role is ChatRole.USER)
    assert user_msg.attachments == (ref,)
    assert result.message.content == "x = 2."


@pytest.mark.asyncio
async def test_answer_turn_raises_for_missing_session() -> None:
    repo = _FakeChatRepo()
    turn = _turn(
        repo,
        _ScriptedLLM([LLMResponse(content="hi")]),
        index=_FakeIndex([]),
        submit=_FakeSubmitCourseRequest(),
        user_id=uuid.uuid4(),
    )
    with pytest.raises(ChatSessionNotFoundError):
        await turn.execute(session_id=uuid.uuid4(), user_content="hi")


def test_routing_query_folds_question_and_answer() -> None:
    q = _routing_query("What is an eigenvalue?", "An eigenvalue is a scalar λ such that ...")
    assert "eigenvalue" in q
    assert q.startswith("What is an eigenvalue?")


# ── LearnerContextDispatcher (user-scoping) ──────────────────────────


@pytest.mark.asyncio
async def test_get_my_progress_returns_user_data_scoped() -> None:
    user_id = uuid.uuid4()
    progress = _RecordingProgressUC(
        [
            _Row("started", completed_lessons=1, total_lessons=4, percent=25, completed=False),
            _Row("not-started", completed_lessons=0, total_lessons=3, percent=0, completed=False),
        ]
    )
    dispatcher = _toolset(user_id, progress=progress)
    out = json.loads(
        await dispatcher.dispatch(ToolCall(id="c", name="get_my_progress", arguments_json="{}"))
    )
    assert progress.seen_user_id == user_id
    # Only started courses surface, and the user id was never an argument.
    assert [c["slug"] for c in out["courses"]] == ["started"]
    assert out["courses"][0]["percent"] == 25


@pytest.mark.asyncio
async def test_get_my_learning_state_returns_user_data() -> None:
    user_id = uuid.uuid4()
    learning = _RecordingLearningStateUC(
        _LearningState(
            enrollments=[_Enrollment("data-track", "active")],
            progress_by_module={"m1": _ModuleProgress("m1", 80)},
            certificates=[_Cert("data-track", "hash123")],
        )
    )
    dispatcher = _toolset(user_id, learning=learning)
    out = json.loads(
        await dispatcher.dispatch(
            ToolCall(id="c", name="get_my_learning_state", arguments_json="{}")
        )
    )
    assert learning.seen_user_id == user_id
    assert out["enrollments"][0]["pathSlug"] == "data-track"
    assert out["progress"][0]["percent"] == 80
    assert out["certificates"][0]["verificationHash"] == "hash123"


@pytest.mark.asyncio
async def test_get_my_recommendations_returns_user_data() -> None:
    user_id = uuid.uuid4()
    recommend = _RecordingRecommendUC(
        _Recommendations("Start here", [_Rec("intro", "Intro", "Beginner", "Required course")])
    )
    dispatcher = _toolset(user_id, recommend=recommend)
    out = json.loads(
        await dispatcher.dispatch(
            ToolCall(id="c", name="get_my_recommendations", arguments_json="{}")
        )
    )
    assert recommend.seen_user_id == user_id
    assert out["summary"] == "Start here"
    assert out["courses"][0]["slug"] == "intro"


@pytest.mark.asyncio
async def test_dispatcher_unknown_tool_returns_error() -> None:
    out = json.loads(
        await _toolset(uuid.uuid4()).dispatch(
            ToolCall(id="c", name="get_other_user_data", arguments_json="{}")
        )
    )
    assert out["error"] == "unknown_tool"


# ── get_my_notes + notebook action proposal (issue #243) ─────────────


@pytest.mark.asyncio
async def test_get_my_notes_returns_user_notes_scoped_and_bounded() -> None:
    user_id = uuid.uuid4()
    long_body = "x" * 1000
    notes = _RecordingNotesUC(
        [_NoteRow("algorithms", "l1", "big-O", long_body)],
    )
    dispatcher = _toolset(user_id, notes=notes)
    out = json.loads(
        await dispatcher.dispatch(
            ToolCall(
                id="c",
                name="get_my_notes",
                arguments_json=json.dumps({"course_slug": "algorithms"}),
            )
        )
    )
    assert notes.seen_user_id == user_id  # scoped to the authenticated user
    assert notes.seen_course_slug == "algorithms"  # filter forwarded
    assert out["notes"][0]["courseSlug"] == "algorithms"
    assert out["notes"][0]["lessonId"] == "l1"
    assert out["notes"][0]["quote"] == "big-O"
    assert len(out["notes"][0]["body"]) == 600  # truncated to the cap


@pytest.mark.asyncio
async def test_propose_notebook_action_create_is_recorded() -> None:
    dispatcher = _toolset(uuid.uuid4())
    ack = json.loads(
        await dispatcher.dispatch(
            ToolCall(
                id="c",
                name="propose_notebook_action",
                arguments_json=json.dumps(
                    {
                        "op": "create",
                        "title": "Mindmap — My Algorithms Notes",
                        "type": "theory",
                        "body": "```mermaid\nmindmap\n  root((Algorithms))\n```",
                    }
                ),
            )
        )
    )
    assert ack["status"] == "proposed"
    action = dispatcher.proposed_action
    assert action is not None
    assert action.op == "create"
    assert action.title == "Mindmap — My Algorithms Notes"
    assert action.note_type == "theory"
    assert "mermaid" in action.body


@pytest.mark.asyncio
async def test_propose_notebook_action_append_requires_target() -> None:
    dispatcher = _toolset(uuid.uuid4())
    out = json.loads(
        await dispatcher.dispatch(
            ToolCall(
                id="c",
                name="propose_notebook_action",
                arguments_json=json.dumps({"op": "append", "body": "more"}),
            )
        )
    )
    assert out["error"] == "append_requires_target_note_id"
    assert dispatcher.proposed_action is None


@pytest.mark.asyncio
async def test_propose_notebook_action_rejects_bad_op_and_empty_body() -> None:
    dispatcher = _toolset(uuid.uuid4())
    bad_op = json.loads(
        await dispatcher.dispatch(
            ToolCall(
                id="c",
                name="propose_notebook_action",
                arguments_json=json.dumps({"op": "delete", "body": "x"}),
            )
        )
    )
    assert bad_op["error"] == "invalid_op"
    empty_body = json.loads(
        await dispatcher.dispatch(
            ToolCall(
                id="c",
                name="propose_notebook_action",
                arguments_json=json.dumps({"op": "create", "body": "  "}),
            )
        )
    )
    assert empty_body["error"] == "missing_body"
    assert dispatcher.proposed_action is None  # nothing recorded on either error


@pytest.mark.asyncio
async def test_propose_notebook_action_drops_unknown_type() -> None:
    dispatcher = _toolset(uuid.uuid4())
    await dispatcher.dispatch(
        ToolCall(
            id="c",
            name="propose_notebook_action",
            arguments_json=json.dumps({"op": "create", "type": "nonsense", "body": "ok"}),
        )
    )
    assert dispatcher.proposed_action is not None
    assert dispatcher.proposed_action.note_type is None  # invalid type dropped, not fatal


@pytest.mark.asyncio
async def test_answer_turn_surfaces_proposed_notebook_action() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    notes = _RecordingNotesUC([_NoteRow("algorithms", "l1", "q", "sorting is O(n log n)")])
    # Round 1: read notes. Round 2: propose the notebook write. Round 3: answer.
    llm = _ScriptedLLM(
        [
            LLMResponse(
                content="",
                tool_calls=(
                    ToolCall(
                        id="t1",
                        name="get_my_notes",
                        arguments_json=json.dumps({"course_slug": "algorithms"}),
                    ),
                ),
            ),
            LLMResponse(
                content="",
                tool_calls=(
                    ToolCall(
                        id="t2",
                        name="propose_notebook_action",
                        arguments_json=json.dumps(
                            {
                                "op": "create",
                                "title": "Mindmap — Algorithms",
                                "type": "theory",
                                "body": "```mermaid\nmindmap\n  root((Algorithms))\n```",
                            }
                        ),
                    ),
                ),
            ),
            LLMResponse(content="Saved a mindmap of your Algorithms notes."),
        ]
    )
    turn = AnswerAgentTurn(
        repo=repo,
        llm=cast("object", llm),  # type: ignore[arg-type]
        learner_tools=_toolset(user_id, notes=notes),
        catalog_index=cast("object", _FakeIndex([])),  # type: ignore[arg-type]
        submit_course_request=cast("object", _FakeSubmitCourseRequest()),  # type: ignore[arg-type]
        user_id=user_id,
    )

    result = await turn.execute(
        session_id=session_id,
        user_content="Make a mindmap of my algorithms notes and save it as a new notebook",
    )

    assert llm.calls == 3
    assert result.notebook_action is not None
    assert result.notebook_action.op == "create"
    assert "mermaid" in result.notebook_action.body


@pytest.mark.asyncio
async def test_ordinary_turn_has_no_notebook_action() -> None:
    repo = _FakeChatRepo()
    session_id = _seeded_session(repo)
    user_id = repo.sessions[session_id].user_id
    llm = _ScriptedLLM([LLMResponse(content="An eigenvalue is a scalar λ.")])
    turn = _turn(
        repo, llm, index=_FakeIndex([]), submit=_FakeSubmitCourseRequest(), user_id=user_id
    )
    result = await turn.execute(session_id=session_id, user_content="What is an eigenvalue?")
    assert result.notebook_action is None

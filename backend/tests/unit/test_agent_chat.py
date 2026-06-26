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

    async def list_messages(self, session_id: uuid.UUID) -> list[ChatMessage]:
        return [m for m in self.messages if m.session_id == session_id]


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
    return LearnerContextDispatcher(
        LearnerContextToolset(
            user_id=user_id,
            list_my_progress=cast("object", progress),  # type: ignore[arg-type]
            get_my_learning_state=cast("object", learning),  # type: ignore[arg-type]
            recommend_courses=cast("object", recommend),  # type: ignore[arg-type]
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

"""Integration tests for the Global Agent Chat (issue #234).

Drives router -> AnswerAgentTurn over the real SqlAlchemy chat repo + course
demand repo (in-memory sqlite), with a fake LLM (no network) and an injected
CatalogSearchIndex. Exercises the real EnforceQuota so TUTOR_MESSAGES is metered
end-to-end.

  * an in-catalog topic returns 200 with courseRefs (acceptance #2 — simulated
    with an attachment standing in for the photographed question);
  * an out-of-catalog topic returns 200 with unmatchedTopic AND records an
    AGENT-sourced demand request (visible in the admin clusters);
  * the history endpoint returns the turn;
  * an unauthenticated request is 401/403;
  * a free user over the cap is 402.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.agent_chat.router import (
    get_agent_history_uc,
    get_agent_start_session_uc,
    get_agent_turn_uc,
)
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import get_enforce_quota_uc
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    optional_principal,
    require_editor,
    require_principal,
)
from cyberdyne_backend.adapters.outbound.persistence.ai_chat.repository import (
    SqlAlchemyChatRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.course_demand.repository import (
    SqlAlchemyCourseRequestRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quota.repository import (
    SqlAlchemyUsageCounterRepository,
)
from cyberdyne_backend.application.agent_chat import (
    AnswerAgentTurn,
    LearnerContextDispatcher,
    LearnerContextToolset,
)
from cyberdyne_backend.application.ai_chat import GetChatHistory, StartChatSession
from cyberdyne_backend.application.course_demand import SubmitCourseRequest
from cyberdyne_backend.application.quota import EnforceQuota
from cyberdyne_backend.domain.ai_chat import IngestedAttachment, LLMResponse, ToolCall
from cyberdyne_backend.domain.ai_chat.entities import AttachmentRef
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.course_finder import CourseMatch
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration


def _user(uid: str, *, pro: bool = False) -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.UUID(uid),
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
        entitlements=frozenset({"pro:annual"}) if pro else frozenset(),
    )


_LEARNER = _user("44444444-4444-4444-4444-444444444444")
_EDITOR = UserPrincipal(
    user_id=uuid.uuid4(),
    username="editor",
    scopes=frozenset({"editor"}),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


class _FakeLLM:
    """Returns a fixed direct answer; never reaches the network."""

    def __init__(self, content: str) -> None:
        self._content = content

    async def complete(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        return LLMResponse(content=self._content, model="fake")

    async def stream(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        raise NotImplementedError


class _FakeIndex:
    def __init__(self, matches: list[CourseMatch]) -> None:
        self._matches = matches

    async def search(self, query_text: str, *, top_k: int = 5) -> list[CourseMatch]:
        return list(self._matches)


class _FakeIngestor:
    """Grounds an attachment as if a photographed question were read by vision."""

    def __init__(self, text: str) -> None:
        self._text = text

    async def ingest(self, upload_ids: tuple[uuid.UUID, ...]) -> tuple[IngestedAttachment, ...]:
        return tuple(
            IngestedAttachment(
                ref=AttachmentRef(id=uid, filename="question.png", content_type="image/png"),
                text=self._text,
            )
            for uid in upload_ids
        )


async def _real_enforcer() -> AsyncIterator[EnforceQuota]:
    async with session_scope() as session:
        yield EnforceQuota(repo=SqlAlchemyUsageCounterRepository(session))


async def _start_session_dep() -> AsyncIterator[StartChatSession]:
    async with session_scope() as session:
        yield StartChatSession(repo=SqlAlchemyChatRepository(session))


async def _history_dep() -> AsyncIterator[GetChatHistory]:
    async with session_scope() as session:
        yield GetChatHistory(repo=SqlAlchemyChatRepository(session))


def _learner_tools(session, user_id):  # type: ignore[no-untyped-def]
    # The learner-context tools aren't exercised here (the fake LLM doesn't
    # call them); a minimal toolset keeps the wiring honest.
    class _Empty:
        async def execute(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            return []

    return LearnerContextDispatcher(
        LearnerContextToolset(
            user_id=user_id,
            list_my_progress=_Empty(),  # type: ignore[arg-type]
            get_my_learning_state=_Empty(),  # type: ignore[arg-type]
            recommend_courses=_Empty(),  # type: ignore[arg-type]
            list_user_notes=_Empty(),  # type: ignore[arg-type]
        )
    )


def _turn_dep(*, answer: str, matches: list[CourseMatch], ingest_text: str | None = None):  # type: ignore[no-untyped-def]
    async def _dep() -> AsyncIterator[AnswerAgentTurn]:
        async with session_scope() as session:
            yield AnswerAgentTurn(
                repo=SqlAlchemyChatRepository(session),
                llm=_FakeLLM(answer),  # type: ignore[arg-type]
                learner_tools=_learner_tools(session, _LEARNER.user_id),
                catalog_index=_FakeIndex(matches),  # type: ignore[arg-type]
                submit_course_request=SubmitCourseRequest(
                    repo=SqlAlchemyCourseRequestRepository(session)
                ),
                user_id=_LEARNER.user_id,
                ingestor=_FakeIngestor(ingest_text) if ingest_text is not None else None,
            )

    return _dep


def _client(app: FastAPI, *, answer: str, matches, ingest_text=None) -> TestClient:  # type: ignore[no-untyped-def]
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    app.dependency_overrides[optional_principal] = lambda: _LEARNER
    app.dependency_overrides[require_editor] = lambda: _EDITOR
    app.dependency_overrides[get_enforce_quota_uc] = _real_enforcer
    app.dependency_overrides[get_agent_start_session_uc] = _start_session_dep
    app.dependency_overrides[get_agent_history_uc] = _history_dep
    app.dependency_overrides[get_agent_turn_uc] = _turn_dep(
        answer=answer, matches=matches, ingest_text=ingest_text
    )
    return TestClient(app)


def _start(client: TestClient) -> str:
    resp = client.post("/api/v1/agent/sessions")
    assert resp.status_code == 201, resp.text
    return resp.json()["sessionId"]


@pytest.mark.usefixtures("_prepared_schema")
def test_in_catalog_topic_returns_course_refs(app: FastAPI) -> None:
    match = CourseMatch(
        course_slug="linear-algebra",
        lesson_id=uuid.uuid4(),
        score=0.91,
        match_reason="matched lesson: eigenvalues",
    )
    client = _client(
        app,
        answer="The eigenvalues are the roots of det(A - lambda I) = 0.",
        matches=[match],
        ingest_text="Photo: find the eigenvalues of matrix A",
    )
    session_id = _start(client)
    resp = client.post(
        f"/api/v1/agent/sessions/{session_id}/messages",
        json={"content": "Solve the attached question", "attachments": [str(uuid.uuid4())]},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["message"]["role"] == "assistant"
    assert body["message"]["content"].startswith("The eigenvalues")
    assert body["courseRefs"]
    assert body["courseRefs"][0]["courseSlug"] == "linear-algebra"
    assert body["courseRefs"][0]["lessonId"]
    assert body.get("unmatchedTopic") is None
    assert resp.headers["X-Quota-Meter"] == "tutor_messages"


@pytest.mark.usefixtures("_prepared_schema")
def test_out_of_catalog_topic_records_demand(app: FastAPI) -> None:
    client = _client(
        app,
        answer="Roman legions used the testudo formation during sieges.",
        matches=[],
    )
    session_id = _start(client)
    resp = client.post(
        f"/api/v1/agent/sessions/{session_id}/messages",
        json={"content": "Explain Roman siege warfare tactics"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["courseRefs"] == []
    assert body["unmatchedTopic"]["topic"] == "Explain Roman siege warfare tactics"

    # The demand was recorded as an AGENT-sourced request — it surfaces in the
    # admin clusters (which aggregate every source).
    clusters = client.get("/api/v1/admin/learning/course-requests")
    assert clusters.status_code == 200, clusters.text
    topics = [c["topic"] for c in clusters.json()]
    assert "Explain Roman siege warfare tactics" in topics


@pytest.mark.usefixtures("_prepared_schema")
def test_history_endpoint_returns_the_turn(app: FastAPI) -> None:
    client = _client(app, answer="42.", matches=[])
    session_id = _start(client)
    client.post(
        f"/api/v1/agent/sessions/{session_id}/messages",
        json={"content": "What is 6 times 7?"},
    )
    hist = client.get(f"/api/v1/agent/sessions/{session_id}")
    assert hist.status_code == 200, hist.text
    roles = [m["role"] for m in hist.json()["messages"]]
    assert "user" in roles
    assert "assistant" in roles


@pytest.mark.usefixtures("_prepared_schema")
def test_unauthenticated_is_rejected(app: FastAPI) -> None:
    # No principal override → the auth middleware leaves the request anonymous.
    resp = TestClient(app).post(
        f"/api/v1/agent/sessions/{uuid.uuid4()}/messages",
        json={"content": "hi"},
    )
    assert resp.status_code in (401, 403)


class _ScriptedLLM:
    """Plays scripted replies (a tool-call round, then a final answer)."""

    def __init__(self, replies: list[LLMResponse]) -> None:
        self._replies = list(replies)

    async def complete(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        if self._replies:
            return self._replies.pop(0)
        return LLMResponse(content="done", model="fake")

    async def stream(self, *, messages, tools, system_prompt):  # type: ignore[no-untyped-def]
        raise NotImplementedError


@pytest.mark.usefixtures("_prepared_schema")
def test_notebook_action_is_proposed(app: FastAPI) -> None:
    # The agent proposes a Notebook write via the tool; the backend surfaces it
    # for the client to commit (it performs NO write itself).
    propose = ToolCall(
        id="t1",
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
    llm = _ScriptedLLM(
        [
            LLMResponse(content="", tool_calls=(propose,), model="fake"),
            LLMResponse(content="Saved a mindmap of your Algorithms notes.", model="fake"),
        ]
    )

    async def _dep() -> AsyncIterator[AnswerAgentTurn]:
        async with session_scope() as session:
            yield AnswerAgentTurn(
                repo=SqlAlchemyChatRepository(session),
                llm=llm,  # type: ignore[arg-type]
                learner_tools=_learner_tools(session, _LEARNER.user_id),
                catalog_index=_FakeIndex([]),  # type: ignore[arg-type]
                submit_course_request=SubmitCourseRequest(
                    repo=SqlAlchemyCourseRequestRepository(session)
                ),
                user_id=_LEARNER.user_id,
            )

    app.dependency_overrides[require_principal] = lambda: _LEARNER
    app.dependency_overrides[optional_principal] = lambda: _LEARNER
    app.dependency_overrides[get_enforce_quota_uc] = _real_enforcer
    app.dependency_overrides[get_agent_start_session_uc] = _start_session_dep
    app.dependency_overrides[get_agent_turn_uc] = _dep
    client = TestClient(app)
    session_id = _start(client)

    resp = client.post(
        f"/api/v1/agent/sessions/{session_id}/messages",
        json={"content": "Make a mindmap of my algorithms notes and save it as a new notebook"},
    )
    assert resp.status_code == 200, resp.text
    action = resp.json()["notebookAction"]
    assert action["op"] == "create"
    assert action["type"] == "theory"  # NotebookNoteType raw value, aliased to "type"
    assert "mermaid" in action["body"]


@pytest.mark.usefixtures("_prepared_schema")
def test_free_user_blocked_over_quota(app: FastAPI) -> None:
    client = _client(app, answer="ok", matches=[])
    session_id = _start(client)
    # Free TUTOR_MESSAGES cap is 10 / month.
    for _ in range(10):
        ok = client.post(f"/api/v1/agent/sessions/{session_id}/messages", json={"content": "hi"})
        assert ok.status_code == 200, ok.text
    blocked = client.post(f"/api/v1/agent/sessions/{session_id}/messages", json={"content": "more"})
    assert blocked.status_code == 402, blocked.text
    assert blocked.json()["detail"]["code"] == "quota_exceeded"

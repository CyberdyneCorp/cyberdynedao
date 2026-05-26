"""Tests for AI chat domain + use cases + tool dispatcher."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.ai_chat import (
    GetChatHistory,
    RunChatTurn,
    StartChatSession,
    ToolContext,
    ToolDispatcher,
)
from cyberdyne_backend.application.content.use_cases import ListProjects
from cyberdyne_backend.application.learning import ListPaths
from cyberdyne_backend.application.marketplace.use_cases import GetProduct
from cyberdyne_backend.domain.ai_chat import (
    ChatLLMPort,
    ChatMessage,
    ChatRole,
    ChatSession,
    ChatSessionNotFoundError,
    LLMResponse,
    ToolCall,
)
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema
from cyberdyne_backend.domain.content import Project
from cyberdyne_backend.domain.learning import LearningModule, LearningPath
from cyberdyne_backend.domain.marketplace import Product, ProductType

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
    """Returns canned responses in order, one per call."""

    def __init__(self, replies: list[LLMResponse]) -> None:
        self._replies = list(replies)
        self.calls = 0

    async def complete(self, *, messages, tools, system_prompt):
        self.calls += 1
        if not self._replies:
            return LLMResponse(content="(no more scripted replies)")
        return self._replies.pop(0)


class _FakeContentRepo:
    async def list_team(self):
        return []

    async def get_cyberdyne_page(self):
        raise NotImplementedError

    async def list_projects(self):
        return [
            Project(
                id="cyberstac",
                name="CyberSTAC",
                icon="🛰",
                description="Geospatial intelligence",
                features=("STAC API",),
                extra_features=None,
                palette="blue",
                status="active",
                full_width=False,
            )
        ]

    async def get_services_page(self):
        raise NotImplementedError

    async def get_contact_page(self):
        raise NotImplementedError

    async def list_resources(self):
        return []


class _FakeLearningRepo:
    async def list_modules(self):
        return [
            LearningModule(
                slug="mcp-servers",
                title="MCP Servers",
                category="Development",
                description="MCP backends",
                level="Intermediate",
                duration="1h 15min",
                icon="🔌",
                topics=("MCP", "FastMCP"),
            )
        ]

    async def list_paths(self):
        return [
            LearningPath(
                slug="cyberdyne-stack",
                title="Build Like Cyberdyne",
                description="Hexagonal cores + MCP.",
                module_slugs=("mcp-servers",),
                estimated_time="10w",
                icon="⚡",
            )
        ]

    async def get_path(self, slug: str):
        raise NotImplementedError

    async def upsert_enrollment(self, e):
        return e

    async def list_enrollments_for_user(self, user_id):
        return []

    async def upsert_progress(self, p):
        return p

    async def get_progress_map_for_user(self, user_id):
        return {}

    async def save_certificate(self, c):
        pass

    async def get_certificate_for_user_and_path(self, u, p):
        return None


class _FakeMarketplaceRepo:
    def __init__(self) -> None:
        self.product = Product(
            slug="train",
            type=ProductType.TRAINING,
            title="Course",
            description_md="",
            price_cents=29900,
            currency="USD",
            duration_label="40h",
            features=("Video",),
            category="Training Material",
            stripe_price_id="price_x",
        )

    async def list_products(self, **_kw):
        return [self.product]

    async def get_product(self, slug: str):
        if slug != self.product.slug:
            from cyberdyne_backend.domain.marketplace import ProductNotFoundError

            raise ProductNotFoundError(slug)
        return self.product

    async def save_order(self, o):
        pass

    async def get_order(self, oid):
        raise NotImplementedError

    async def get_order_by_session_id(self, sid):
        return None

    async def get_order_by_payment_intent(self, pi):
        return None

    async def list_orders_for_user(self, u):
        return []

    async def save_license(self, lic):
        pass

    async def get_license(self, lid):
        raise NotImplementedError

    async def list_licenses_for_user(self, u):
        return []

    async def record_webhook_event(self, e):
        return True


class _FakeAskRepo:
    def __init__(self) -> None:
        self.saved: list[object] = []

    async def save(self, ask):
        self.saved.append(ask)

    async def get(self, ask_id):
        raise NotImplementedError

    async def list_admin(self, **kw):
        return [], 0


class _AlwaysPassCaptcha:
    async def verify(self, token: str) -> bool:
        return True


class _RecordingAskNotifier:
    def __init__(self) -> None:
        self.sent: list[object] = []

    async def send_new_ask_notification(self, ask) -> None:
        self.sent.append(ask)


class _StubKnowledge:
    async def search(self, query: str, *, mode: str = "hybrid") -> str:
        return f"stub:{query}"


def _build_ctx(
    *,
    ask_repo: _FakeAskRepo | None = None,
    ask_notifier: _RecordingAskNotifier | None = None,
) -> ToolContext:
    content = _FakeContentRepo()
    learning = _FakeLearningRepo()
    market = _FakeMarketplaceRepo()
    return ToolContext(
        list_projects=ListProjects(repo=content),
        list_paths=ListPaths(repo=learning),
        get_product=GetProduct(repo=market),
        learning_repo=learning,
        knowledge=_StubKnowledge(),
        ask_repo=ask_repo or _FakeAskRepo(),
        captcha=_AlwaysPassCaptcha(),
        ask_notifier=ask_notifier or _RecordingAskNotifier(),
    )


# ── StartChatSession + GetChatHistory ────────────────────────────────


class TestStartChatSession:
    async def test_anonymous_session_persists(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        assert session.user_id is None
        assert session.id in repo.sessions

    async def test_authenticated_session_carries_user_id(self) -> None:
        repo = _FakeChatRepo()
        user_id = uuid.uuid4()
        session = await StartChatSession(repo=repo).execute(user_id=user_id)
        assert session.user_id == user_id


class TestGetChatHistory:
    async def test_returns_messages_in_order(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        from cyberdyne_backend.domain.ai_chat import (
            new_assistant_message,
            new_user_message,
        )

        await repo.append_message(new_user_message(session_id=session.id, content="hi"))
        await repo.append_message(new_assistant_message(session_id=session.id, content="hello"))
        history = await GetChatHistory(repo=repo).execute(session.id)
        assert [m.role for m in history] == [ChatRole.USER, ChatRole.ASSISTANT]

    async def test_missing_session_raises(self) -> None:
        with pytest.raises(ChatSessionNotFoundError):
            await GetChatHistory(repo=_FakeChatRepo()).execute(uuid.uuid4())


# ── RunChatTurn (tool loop) ──────────────────────────────────────────


class TestRunChatTurn:
    async def test_simple_reply_no_tools(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM([LLMResponse(content="Hi there.", model="m")])
        dispatcher = ToolDispatcher(_build_ctx())
        msg = await RunChatTurn(repo=repo, llm=llm, dispatcher=dispatcher).execute(
            session_id=session.id, user_content="hello"
        )
        assert msg.role is ChatRole.ASSISTANT
        assert msg.content == "Hi there."

    async def test_tool_call_round_dispatches_and_loops(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        # First turn: assistant calls list_projects. Second turn: final answer.
        llm = _ScriptedLLM(
            [
                LLMResponse(
                    content="",
                    tool_calls=(
                        ToolCall(
                            id="call_1",
                            name="list_projects",
                            arguments_json="{}",
                        ),
                    ),
                ),
                LLMResponse(content="Cyberdyne builds CyberSTAC and more."),
            ]
        )
        dispatcher = ToolDispatcher(_build_ctx())
        msg = await RunChatTurn(repo=repo, llm=llm, dispatcher=dispatcher).execute(
            session_id=session.id, user_content="what do you build?"
        )
        # 2 LLM calls, 4 stored messages: user, assistant(tool_call),
        # tool(result), assistant(final).
        assert llm.calls == 2
        assert msg.content.startswith("Cyberdyne")
        roles = [m.role for m in repo.messages]
        assert roles == [
            ChatRole.USER,
            ChatRole.ASSISTANT,
            ChatRole.TOOL,
            ChatRole.ASSISTANT,
        ]

    async def test_stops_at_max_tool_rounds(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        # LLM keeps requesting the same tool forever.
        llm = _ScriptedLLM(
            [
                LLMResponse(
                    content="",
                    tool_calls=(ToolCall(id=f"c{i}", name="list_projects", arguments_json="{}"),),
                )
                for i in range(10)
            ]
        )
        dispatcher = ToolDispatcher(_build_ctx())
        uc = RunChatTurn(repo=repo, llm=llm, dispatcher=dispatcher, max_tool_rounds=3)
        await uc.execute(session_id=session.id, user_content="loop me")
        # 3 rounds + the final loop-cap fallback.
        assert llm.calls == 3


# ── ToolDispatcher unit ──────────────────────────────────────────────


class TestToolDispatcher:
    async def test_list_projects(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_projects", arguments_json="{}")
        )
        data = json.loads(result)
        assert data[0]["id"] == "cyberstac"

    async def test_lookup_module_hit(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="lookup_module",
                arguments_json=json.dumps({"slug": "mcp-servers"}),
            )
        )
        data = json.loads(result)
        assert data["title"] == "MCP Servers"

    async def test_lookup_module_miss(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="lookup_module",
                arguments_json=json.dumps({"slug": "nope"}),
            )
        )
        assert json.loads(result)["error"] == "not_found"

    async def test_lookup_product_hit(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="lookup_product",
                arguments_json=json.dumps({"slug": "train"}),
            )
        )
        assert json.loads(result)["slug"] == "train"

    async def test_lookup_product_miss(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="lookup_product",
                arguments_json=json.dumps({"slug": "missing"}),
            )
        )
        assert json.loads(result)["error"] == "not_found"

    async def test_list_paths(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_paths", arguments_json="{}")
        )
        assert json.loads(result)[0]["slug"] == "cyberdyne-stack"

    async def test_search_returns_stub(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="search_cyberdyne_knowledge",
                arguments_json=json.dumps({"query": "agent"}),
            )
        )
        assert "stub:agent" in json.loads(result)["summary"]

    async def test_search_empty_query_rejected(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="search_cyberdyne_knowledge",
                arguments_json=json.dumps({"query": "   "}),
            )
        )
        assert json.loads(result)["error"] == "empty_query"

    async def test_create_ask_validates_required_fields(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="create_ask_for_handoff",
                arguments_json=json.dumps({"name": "", "email": "", "body": ""}),
            )
        )
        assert json.loads(result)["error"] == "missing_required_fields"

    async def test_create_ask_persists(self) -> None:
        ask_repo = _FakeAskRepo()
        notifier = _RecordingAskNotifier()
        ctx = _build_ctx(ask_repo=ask_repo, ask_notifier=notifier)
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_ask_for_handoff",
                arguments_json=json.dumps(
                    {
                        "name": "Alice",
                        "email": "alice@x.io",
                        "body": "I want a demo of CyberSTAC",
                        "product_slug": "cyberstac",
                    }
                ),
            )
        )
        assert json.loads(result)["ok"] is True
        assert len(ask_repo.saved) == 1
        assert len(notifier.sent) == 1

    async def test_unknown_tool_returns_error(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="does_not_exist", arguments_json="{}")
        )
        assert json.loads(result)["error"] == "unknown_tool"

    async def test_bad_arguments_json_returns_error(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_projects", arguments_json="{not json")
        )
        assert json.loads(result)["error"] == "invalid_arguments_json"


# Suppress unused-import warning.
_ = datetime.now(tz=UTC)
_ = ToolSchema(name="_", description="_")
_: ChatLLMPort = _ScriptedLLM([])

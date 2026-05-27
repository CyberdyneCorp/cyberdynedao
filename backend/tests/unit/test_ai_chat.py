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
        if slug == "cyberdyne-stack":
            return LearningPath(
                slug="cyberdyne-stack",
                title="Build Like Cyberdyne",
                description="Hexagonal cores + MCP.",
                module_slugs=("mcp-servers",),
                estimated_time="10w",
                icon="⚡",
            )
        from cyberdyne_backend.domain.learning import LearningContentNotFoundError

        raise LearningContentNotFoundError(slug)

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


class _FakeMatlab:
    """Records calls; returns a canned figure for plots."""

    def __init__(self) -> None:
        self.repl_calls: list[dict[str, object]] = []
        self.plot_calls: list[dict[str, object]] = []

    async def run_repl(self, *, source, session_id, bearer):
        from cyberdyne_backend.domain.ai_chat import MatlabRunResult

        self.repl_calls.append({"source": source, "session_id": session_id, "bearer": bearer})
        return MatlabRunResult(ok=True, stdout="ans = 4\n", stderr="", session_id=session_id)

    async def run_plot(self, *, source, session_id, bearer, fmt="png"):
        from cyberdyne_backend.domain.ai_chat import MatlabRunResult

        self.plot_calls.append({"source": source, "session_id": session_id, "bearer": bearer})
        return MatlabRunResult(
            ok=True,
            stdout="",
            stderr="",
            artifacts=("plot_abc.png",),
            session_id=session_id,
        )

    async def check(self, *, source, session_id, bearer):
        from cyberdyne_backend.domain.ai_chat import MatlabCheckResult, MatlabDiagnostic

        return MatlabCheckResult(
            ok=False,
            diagnostics=(MatlabDiagnostic(severity="error", message="undefined var", line=2),),
            stdout="",
            stderr="error",
        )

    async def codegen(self, *, source, target, session_id, bearer):
        from cyberdyne_backend.domain.ai_chat import MatlabCodegenResult

        return MatlabCodegenResult(
            ok=True, language=target, code="int main(){return 0;}", stderr=""
        )


class _FakeBlogRepo:
    def __init__(self, posts=None) -> None:
        self._posts = posts or []

    async def list_posts(self, **_kw):
        return self._posts, len(self._posts)

    async def get_by_slug(self, slug, *, include_drafts=False):
        for p in self._posts:
            if p.slug == slug:
                return p
        from cyberdyne_backend.domain.blog import BlogPostNotFoundError

        raise BlogPostNotFoundError(slug)

    async def save(self, post) -> None:
        self._posts.append(post)

    async def list_categories(self):
        return []


class _CapturingLLM:
    """Records the system_prompt of the last call, returns a fixed reply."""

    def __init__(self, reply: str = "ok") -> None:
        self.last_system_prompt: str | None = None
        self._reply = reply

    async def complete(self, *, messages, tools, system_prompt):
        self.last_system_prompt = system_prompt
        return LLMResponse(content=self._reply, model="m")


def _build_ctx(
    *,
    ask_repo: _FakeAskRepo | None = None,
    ask_notifier: _RecordingAskNotifier | None = None,
    user: object | None = None,
    matlab: object | None = None,
    bearer: str | None = None,
    blog_posts: list | None = None,
    dao: bool = False,
    user_id: object | None = None,
) -> ToolContext:
    from cyberdyne_backend.application.blog import GetBlogPost, ListBlogPosts
    from cyberdyne_backend.application.dao_treasury import GetDaoOverview
    from cyberdyne_backend.application.learning import (
        EnrollInPath,
        GetMyLearningState,
        UpdateModuleProgress,
    )

    content = _FakeContentRepo()
    learning = _FakeLearningRepo()
    market = _FakeMarketplaceRepo()
    blog = _FakeBlogRepo(blog_posts)
    dao_overview = None
    if dao:
        from cyberdyne_backend.adapters.outbound.chain.fake_reader import FakeChainReader

        dao_overview = GetDaoOverview(
            reader=FakeChainReader(), treasury_address="0xDA0", holders=42
        )
    return ToolContext(
        list_projects=ListProjects(repo=content),
        list_paths=ListPaths(repo=learning),
        get_product=GetProduct(repo=market),
        learning_repo=learning,
        knowledge=_StubKnowledge(),
        ask_repo=ask_repo or _FakeAskRepo(),
        captcha=_AlwaysPassCaptcha(),
        ask_notifier=ask_notifier or _RecordingAskNotifier(),
        user=user,  # type: ignore[arg-type]
        matlab=matlab,  # type: ignore[arg-type]
        bearer=bearer,
        dao_overview=dao_overview,
        list_blog_posts=ListBlogPosts(repo=blog),  # type: ignore[arg-type]
        get_blog_post=GetBlogPost(repo=blog),  # type: ignore[arg-type]
        enroll_in_path=EnrollInPath(repo=learning),
        get_my_learning=GetMyLearningState(repo=learning),
        update_progress=UpdateModuleProgress(repo=learning),
        user_id=user_id,  # type: ignore[arg-type]
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

    async def test_matlab_repl_runs_in_session_workspace(self) -> None:
        matlab = _FakeMatlab()
        ctx = _build_ctx(matlab=matlab, bearer="tok-123")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="matlab_repl", arguments_json=json.dumps({"source": "2+2"})),
            chat_session_id="sess-1",
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert "ans = 4" in data["stdout"]
        # stable per-conversation workspace + forwarded bearer
        assert matlab.repl_calls[0]["session_id"] == "agent-sess-1"
        assert matlab.repl_calls[0]["bearer"] == "tok-123"

    async def test_matlab_plot_returns_inline_image(self) -> None:
        matlab = _FakeMatlab()
        ctx = _build_ctx(matlab=matlab, bearer="tok")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="matlab_plot",
                arguments_json=json.dumps({"source": "plot(rand(10))"}),
            ),
            chat_session_id="sess-2",
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["has_figure"] is True
        assert data["figures"] == ["plot_abc.png"]
        assert data["session_id"] == "agent-sess-2"
        # No inline base64 — the frontend downloads via the proxy.
        assert "image_base64" not in data
        assert matlab.plot_calls[0]["session_id"] == "agent-sess-2"

    async def test_matlab_repl_on_plotting_source_routes_to_plot(self) -> None:
        # The agent often picks matlab_repl for "write a program that
        # plots…". Plain /v1/repl won't capture a figure, so drawing
        # code is routed through run_plot.
        matlab = _FakeMatlab()
        ctx = _build_ctx(matlab=matlab, bearer="tok")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="matlab_repl",
                arguments_json=json.dumps({"source": "x=linspace(0,1); plot(x, sin(x))"}),
            ),
            chat_session_id="sess-3",
        )
        data = json.loads(result)
        assert data["has_figure"] is True
        assert len(matlab.plot_calls) == 1
        assert len(matlab.repl_calls) == 0

    async def test_matlab_repl_non_plot_stays_repl(self) -> None:
        matlab = _FakeMatlab()
        ctx = _build_ctx(matlab=matlab, bearer="tok")
        await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x", name="matlab_repl", arguments_json=json.dumps({"source": "A = magic(5)"})
            ),
            chat_session_id="s",
        )
        assert len(matlab.repl_calls) == 1
        assert len(matlab.plot_calls) == 0

    async def test_matlab_empty_source_rejected(self) -> None:
        ctx = _build_ctx(matlab=_FakeMatlab())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="matlab_repl", arguments_json=json.dumps({"source": "  "})),
            chat_session_id="s",
        )
        assert json.loads(result)["error"] == "empty_source"

    async def test_matlab_check_returns_diagnostics(self) -> None:
        ctx = _build_ctx(matlab=_FakeMatlab())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="matlab_check", arguments_json=json.dumps({"source": "x="})),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["ok"] is False
        assert data["diagnostics"][0]["message"] == "undefined var"
        assert data["diagnostics"][0]["line"] == 2

    async def test_matlab_codegen_returns_code(self) -> None:
        ctx = _build_ctx(matlab=_FakeMatlab())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="matlab_codegen",
                arguments_json=json.dumps({"source": "function y=f(x)\ny=x;\nend", "target": "c"}),
            ),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["language"] == "c"
        assert "int main" in data["code"]

    async def test_get_dao_treasury(self) -> None:
        ctx = _build_ctx(dao=True)
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_dao_treasury", arguments_json="{}")
        )
        data = json.loads(result)
        assert data["holders"] == 42
        assert isinstance(data["total_usd_value"], (int, float))
        assert "token_balances" in data

    async def test_list_and_lookup_blog_posts(self) -> None:
        from datetime import UTC, datetime
        from uuid import uuid4

        from cyberdyne_backend.domain.blog import BlogPost, BlogPostStatus

        post = BlogPost(
            id=uuid4(),
            slug="hello-web3",
            title="Hello Web3",
            body_md="# Hi\n\nbody",
            excerpt="intro",
            category_slug="defi",
            author_user_id=None,
            status=BlogPostStatus.PUBLISHED,
            tags=("web3",),
            created_at=datetime(2026, 5, 1, tzinfo=UTC),
            published_at=datetime(2026, 5, 2, tzinfo=UTC),
        )
        ctx = _build_ctx(blog_posts=[post])
        listed = json.loads(
            await ToolDispatcher(ctx).dispatch(
                ToolCall(id="x", name="list_blog_posts", arguments_json="{}")
            )
        )
        assert listed["total"] == 1
        assert listed["posts"][0]["slug"] == "hello-web3"

        looked = json.loads(
            await ToolDispatcher(ctx).dispatch(
                ToolCall(
                    id="x",
                    name="lookup_blog_post",
                    arguments_json=json.dumps({"slug": "hello-web3"}),
                )
            )
        )
        assert "body" in looked["body_md"]

        miss = json.loads(
            await ToolDispatcher(ctx).dispatch(
                ToolCall(
                    id="x", name="lookup_blog_post", arguments_json=json.dumps({"slug": "nope"})
                )
            )
        )
        assert miss["error"] == "not_found"

    async def test_enroll_requires_sign_in(self) -> None:
        ctx = _build_ctx(user_id=None)
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="enroll_in_path",
                arguments_json=json.dumps({"path_slug": "cyberdyne-stack"}),
            )
        )
        assert json.loads(result)["error"] == "sign_in_required"

    async def test_enroll_in_path_for_signed_in_user(self) -> None:
        ctx = _build_ctx(user_id=uuid.uuid4())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="enroll_in_path",
                arguments_json=json.dumps({"path_slug": "cyberdyne-stack"}),
            )
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["path_slug"] == "cyberdyne-stack"

    async def test_enroll_unknown_path(self) -> None:
        ctx = _build_ctx(user_id=uuid.uuid4())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x", name="enroll_in_path", arguments_json=json.dumps({"path_slug": "ghost"})
            )
        )
        assert json.loads(result)["error"] == "not_found"

    async def test_set_module_progress(self) -> None:
        ctx = _build_ctx(user_id=uuid.uuid4())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="set_module_progress",
                arguments_json=json.dumps({"module_slug": "mcp-servers", "percent": 100}),
            )
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["percent"] == 100

    async def test_get_my_learning_signed_in(self) -> None:
        ctx = _build_ctx(user_id=uuid.uuid4())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_learning", arguments_json="{}")
        )
        data = json.loads(result)
        assert "enrollments" in data and "progress" in data and "certificates" in data

    async def test_matlab_unavailable_when_no_port(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="matlab_plot", arguments_json=json.dumps({"source": "plot(1)"})),
            chat_session_id="s",
        )
        assert json.loads(result)["error"] == "matlab_unavailable"

    async def test_capture_project_idea_persists_structured_body(self) -> None:
        ask_repo = _FakeAskRepo()
        notifier = _RecordingAskNotifier()
        ctx = _build_ctx(ask_repo=ask_repo, ask_notifier=notifier)
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="capture_project_idea",
                arguments_json=json.dumps(
                    {
                        "name": "Bob",
                        "email": "bob@x.io",
                        "project_title": "Geospatial risk dashboard for orchards",
                        "description": "Need a STAC-backed dashboard showing parametric risk for fruit growers.",
                        "scope": "one_time",
                        "budget_range": "$10k-$25k",
                        "timeline": "Q3 2026",
                        "domain": "geospatial",
                    }
                ),
            )
        )
        parsed = json.loads(result)
        assert parsed["ok"] is True
        assert parsed["captured"]["project_title"].startswith("Geospatial")
        assert parsed["captured"]["scope"] == "one_time"
        assert parsed["captured"]["budget_range"] == "$10k-$25k"
        assert len(ask_repo.saved) == 1
        # Body is structured-markdown so admins see fields at a glance.
        saved = ask_repo.saved[0]
        assert "Geospatial risk dashboard" in saved.body
        assert "Scope:** one_time" in saved.body
        assert "Budget:** $10k" in saved.body
        assert "Timeline:** Q3 2026" in saved.body
        assert "Domain:** geospatial" in saved.body
        assert len(notifier.sent) == 1

    async def test_capture_project_idea_validates_required_fields(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="capture_project_idea",
                arguments_json=json.dumps(
                    {
                        "name": "Bob",
                        "email": "bob@x.io",
                        "project_title": "",
                        "description": "",
                    }
                ),
            )
        )
        assert json.loads(result)["error"] == "missing_required_fields"

    async def test_capture_project_idea_omits_blank_optional_fields(self) -> None:
        ask_repo = _FakeAskRepo()
        ctx = _build_ctx(ask_repo=ask_repo)
        await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="capture_project_idea",
                arguments_json=json.dumps(
                    {
                        "name": "Bob",
                        "email": "bob@x.io",
                        "project_title": "Foo",
                        "description": "Bar.",
                    }
                ),
            )
        )
        saved = ask_repo.saved[0]
        assert "Budget" not in saved.body
        assert "Timeline" not in saved.body
        assert "Domain" not in saved.body
        # Scope defaults to 'unknown' so it's always listed.
        assert "Scope:** unknown" in saved.body

    async def test_bad_arguments_json_returns_error(self) -> None:
        result = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_projects", arguments_json="{not json")
        )
        assert json.loads(result)["error"] == "invalid_arguments_json"


class TestUserPersonalization:
    def _profile(self, **kw):
        from cyberdyne_backend.domain.auth_identity import UserProfile

        base = dict(
            user_id=uuid.uuid4(),
            email="leo@amini.ai",
            wallet_address="0xABCDEF0000000000000000000000000000001234",
            organization_id=None,
            is_email_verified=True,
        )
        base.update(kw)
        return UserProfile(**base)  # type: ignore[arg-type]

    def test_context_block_empty_for_anonymous(self) -> None:
        from cyberdyne_backend.application.ai_chat.use_cases import build_user_context_block

        assert build_user_context_block(None) == ""

    def test_context_block_includes_email_wallet_handle(self) -> None:
        from cyberdyne_backend.application.ai_chat.use_cases import build_user_context_block

        block = build_user_context_block(self._profile())
        assert "leo@amini.ai" in block
        assert "verified" in block
        assert "0xABCDEF" in block
        assert "leo" in block  # display_name = email local part

    async def test_run_turn_injects_profile_into_prompt(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _CapturingLLM()
        uc = RunChatTurn(
            repo=repo,
            llm=llm,
            dispatcher=ToolDispatcher(_build_ctx()),
            user=self._profile(),
        )
        await uc.execute(session_id=session.id, user_content="hi")
        assert llm.last_system_prompt is not None
        assert "leo@amini.ai" in llm.last_system_prompt
        # The static persona is still present — we append, not replace.
        assert "Cyberdyne terminal assistant" in llm.last_system_prompt

    async def test_run_turn_anonymous_prompt_unchanged(self) -> None:
        from cyberdyne_backend.application.ai_chat.use_cases import SYSTEM_PROMPT

        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _CapturingLLM()
        uc = RunChatTurn(repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx()))
        await uc.execute(session_id=session.id, user_content="hi")
        assert llm.last_system_prompt == SYSTEM_PROMPT

    async def test_capture_project_idea_prefills_email_from_profile(self) -> None:
        ask_repo = _FakeAskRepo()
        ctx = _build_ctx(ask_repo=ask_repo, user=self._profile())
        # LLM omits email entirely — should fall back to the profile.
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="capture_project_idea",
                arguments_json=json.dumps(
                    {
                        "name": "",
                        "email": "",
                        "project_title": "RAG for docs",
                        "description": "Index our PDFs.",
                    }
                ),
            )
        )
        assert json.loads(result)["ok"] is True
        saved = ask_repo.saved[0]
        assert saved.email == "leo@amini.ai"
        assert saved.name == "leo"  # display_name fallback

    async def test_create_ask_prefills_email_from_profile(self) -> None:
        ask_repo = _FakeAskRepo()
        ctx = _build_ctx(ask_repo=ask_repo, user=self._profile())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_ask_for_handoff",
                arguments_json=json.dumps({"name": "", "email": "", "body": "call me"}),
            )
        )
        assert json.loads(result)["ok"] is True
        assert ask_repo.saved[0].email == "leo@amini.ai"

    async def test_explicit_email_arg_overrides_profile(self) -> None:
        ask_repo = _FakeAskRepo()
        ctx = _build_ctx(ask_repo=ask_repo, user=self._profile())
        await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_ask_for_handoff",
                arguments_json=json.dumps({"name": "Pat", "email": "pat@other.io", "body": "hi"}),
            )
        )
        assert ask_repo.saved[0].email == "pat@other.io"
        assert ask_repo.saved[0].name == "Pat"


class TestSystemPrompt:
    def test_includes_cyberdyne_identity_and_tool_guidance(self) -> None:
        from cyberdyne_backend.application.ai_chat.use_cases import SYSTEM_PROMPT

        # Persona + identity is baked in so the agent doesn't burn a
        # list_projects round just to introduce itself.
        assert "Cyberdyne" in SYSTEM_PROMPT
        assert "five domains" in SYSTEM_PROMPT.lower()
        # Behavioral rails for lead capture.
        assert "capture_project_idea" in SYSTEM_PROMPT
        assert "create_ask_for_handoff" in SYSTEM_PROMPT
        # Operational guidance the agent must follow at runtime.
        assert "confirm" in SYSTEM_PROMPT.lower()  # email confirmation rule
        assert "lookup" in SYSTEM_PROMPT.lower()
        assert "search_cyberdyne_knowledge" in SYSTEM_PROMPT


# Suppress unused-import warning.
_ = datetime.now(tz=UTC)
_ = ToolSchema(name="_", description="_")
_: ChatLLMPort = _ScriptedLLM([])

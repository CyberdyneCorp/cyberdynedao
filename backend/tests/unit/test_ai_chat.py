"""Tests for AI chat domain + use cases + tool dispatcher."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import cast

import pytest

from cyberdyne_backend.application.ai_chat import (
    CYBERDYNE_TOOLS,
    GetChatHistory,
    RunChatTurn,
    StartChatSession,
    StreamChatTurn,
    ToolContext,
    ToolDispatcher,
)
from cyberdyne_backend.application.content.use_cases import ListProjects
from cyberdyne_backend.application.learning import ListPaths
from cyberdyne_backend.application.marketplace.use_cases import GetProduct
from cyberdyne_backend.domain.ai_chat import (
    AttachmentRef,
    ChatLLMPort,
    ChatMessage,
    ChatRole,
    ChatSession,
    ChatSessionNotFoundError,
    IngestedAttachment,
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
            msgs = msgs[-limit:]  # most-recent N, still chronological
        return msgs


class _FakeIngestor:
    """Returns canned IngestedAttachments; records the ids it was asked for."""

    def __init__(self, ingested: tuple[IngestedAttachment, ...]) -> None:
        self._ingested = ingested
        self.seen: tuple[uuid.UUID, ...] | None = None

    async def ingest(self, upload_ids: tuple[uuid.UUID, ...]) -> tuple[IngestedAttachment, ...]:
        self.seen = upload_ids
        return self._ingested


class _ScriptedLLM:
    """Returns canned responses in order, one per call."""

    def __init__(self, replies: list[LLMResponse]) -> None:
        self._replies = list(replies)
        self.calls = 0
        self.last_system_prompt = ""

    async def complete(self, *, messages, tools, system_prompt):
        self.calls += 1
        self.last_system_prompt = system_prompt
        if not self._replies:
            return LLMResponse(content="(no more scripted replies)")
        return self._replies.pop(0)

    async def stream(self, *, messages, tools, system_prompt):
        from cyberdyne_backend.domain.ai_chat import LLMStreamChunk

        self.calls += 1
        self.last_system_prompt = system_prompt
        reply = self._replies.pop(0) if self._replies else LLMResponse(content="(no more replies)")
        if reply.content:
            yield LLMStreamChunk(content_delta=reply.content)
        yield LLMStreamChunk(response=reply)


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
    async def list_modules(self, *, locale: str = "en"):
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

    async def list_paths(self, *, locale: str = "en"):
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


class _FakeCourseRepo:
    def __init__(self) -> None:
        from cyberdyne_backend.domain.courses import new_course, new_lesson

        c = new_course(title="Intro to MCP", description="MCP basics", level="Beginner")
        c.publish()
        c.lessons.append(
            new_lesson(course_id=c.id, title="What is MCP", lesson_type="text", text_body="hi")
        )
        self._course = c

    async def list_courses(
        self,
        *,
        level=None,
        include_drafts=False,
        locale="en",
        limit=None,
        offset=0,
        include_lessons=True,
    ):
        items = [self._course]
        if level is not None:
            items = [x for x in items if x.level is level]
        if offset:
            items = items[offset:]
        if limit is not None:
            items = items[:limit]
        return items

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False, locale: str = "en"):
        from cyberdyne_backend.domain.courses import CourseNotFoundError

        if slug == self._course.slug:
            return self._course
        raise CourseNotFoundError(slug)

    async def save(self, course) -> None:
        pass

    async def delete(self, course_id) -> None:
        pass

    async def get_by_id(self, course_id):
        return self._course if self._course.id == course_id else None


class _FakeCourseProgressRepo:
    """No progress recorded — every course reads as 0% / not started."""

    async def get_lesson_progress(self, *, user_id, lesson_id):
        return None

    async def upsert_lesson_progress(self, progress) -> None:
        pass

    async def list_course_progress(self, *, user_id, course_id):
        return []

    async def get_lesson_course_id(self, lesson_id):
        return None


class _FakeAnalyticsRepo:
    async def learner_counts(self, user_id):
        from cyberdyne_backend.domain.analytics import LearnerCounts

        return LearnerCounts(
            enrolled_paths=2,
            completed_paths=1,
            active_paths=1,
            best_quiz_scores=[80, 100],
            quizzes_passed=2,
            total_quiz_attempts=3,
            certificates=1,
            completed_courses=1,
            in_progress_courses=2,
        )

    async def platform_counts(self):
        from cyberdyne_backend.domain.analytics import PlatformCounts

        return PlatformCounts()


class _FakeQuizRepo:
    LESSON_ID = uuid.UUID("aaaaaaaa-0000-0000-0000-000000000001")

    def __init__(self) -> None:
        from cyberdyne_backend.domain.quizzes import build_question, new_quiz

        self._quiz = new_quiz(
            lesson_id=self.LESSON_ID,
            questions=[
                build_question(
                    prompt="2 + 2 = ?",
                    explanation="basic addition",
                    options=[("3", False), ("4", True)],
                )
            ],
        )

    async def get_by_lesson(self, lesson_id, *, locale="en"):
        from cyberdyne_backend.domain.quizzes import QuizNotFoundError

        if lesson_id == self.LESSON_ID:
            return self._quiz
        raise QuizNotFoundError(str(lesson_id))

    async def upsert(self, quiz) -> None:
        pass

    async def delete_by_lesson(self, lesson_id) -> None:
        pass

    async def add_attempt(self, attempt):
        return attempt

    async def list_attempts(self, *, user_id, quiz_id):
        return []

    async def count_attempts(self, *, user_id, quiz_id):
        return 0


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


class _FakePython:
    """Records create_session + execute calls; returns canned stdout."""

    def __init__(
        self,
        artifacts: tuple[str, ...] = (),
        manim_artifacts: tuple[str, ...] = ("Scene.gif",),
        manim_status: str = "succeeded",
        rich_outputs=(),
    ) -> None:
        self.calls: list[dict[str, object]] = []
        self.uploads: list[dict[str, object]] = []
        self.manim_calls: list[dict[str, object]] = []
        self.created = 0
        self._artifacts = artifacts
        self._manim_artifacts = manim_artifacts
        self._manim_status = manim_status
        self._rich_outputs = rich_outputs

    async def create_session(self, *, bearer):
        self.created += 1
        return f"srv-session-{self.created}"

    async def upload_file(self, *, session_id, filename, content, content_type, bearer):
        self.uploads.append(
            {
                "session_id": session_id,
                "filename": filename,
                "content": content,
                "content_type": content_type,
                "bearer": bearer,
            }
        )
        return filename

    async def execute(self, *, code, session_id, bearer, restricted=True):
        from cyberdyne_backend.domain.ai_chat import PythonExecResult

        self.calls.append(
            {
                "code": code,
                "session_id": session_id,
                "bearer": bearer,
                "restricted": restricted,
            }
        )
        return PythonExecResult(
            ok=True,
            stdout="45\n",
            stderr="",
            result="45",
            artifacts=self._artifacts,
            session_id=session_id,
            rich_outputs=self._rich_outputs,
        )

    async def render_manim(
        self, *, code, scene, session_id, bearer, quality="medium", output_format="gif"
    ):
        from cyberdyne_backend.domain.ai_chat import ManimRenderResult

        self.manim_calls.append(
            {
                "code": code,
                "scene": scene,
                "session_id": session_id,
                "bearer": bearer,
                "quality": quality,
                "output_format": output_format,
            }
        )
        artifacts = self._manim_artifacts if self._manim_status == "succeeded" else ()
        return ManimRenderResult(
            ok=self._manim_status == "succeeded" and bool(artifacts),
            scene=scene,
            status=self._manim_status,
            artifacts=artifacts,
            session_id=session_id,
            error=None if self._manim_status == "succeeded" else "Manim render failed",
            # The real renderer merges stderr into stdout, so a failed scene's
            # traceback arrives in stdout while stderr stays empty.
            stdout=""
            if self._manim_status == "succeeded"
            else (
                "Traceback (most recent call last):\n"
                "TypeError: get_area() got an unexpected keyword argument 'x_min'"
            ),
            stderr="",
        )


class _FakeDocs:
    """Records render_pdf calls; returns a tiny PDF-looking byte string."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def render_pdf(self, *, content, title=None):
        self.calls.append({"content": content, "title": title})
        return b"%PDF-1.4 fake"


class _FakeCyberflies:
    """Records ask/list/get calls; returns canned meeting data."""

    def __init__(self, *, found: bool = True) -> None:
        self.ask_calls: list[dict[str, object]] = []
        self.list_calls = 0
        self.get_calls: list[dict[str, object]] = []
        self._found = found

    async def ask_meetings(self, *, question, bearer):
        self.ask_calls.append({"question": question, "bearer": bearer})
        return "You discussed the Q3 budget."

    async def list_meetings(self, *, bearer):
        from cyberdyne_backend.domain.ai_chat import MeetingSummary

        self.list_calls += 1
        return (
            MeetingSummary(
                id="rec-1", headline="Standup", status="completed", created_at="2026-06-01"
            ),
        )

    async def get_meeting(self, *, meeting_id, bearer):
        from cyberdyne_backend.domain.ai_chat import MeetingDetail

        self.get_calls.append({"meeting_id": meeting_id, "bearer": bearer})
        if not self._found:
            return None
        return MeetingDetail(
            id=meeting_id,
            headline="Standup",
            abstract="The team synced on the Q3 budget.",
            bullets=("Approve budget", "Ship the agent"),
            transcript="Alice: budget looks good. Bob: I'll ship the agent Friday.",
            status="completed",
            created_at="2026-06-01",
            word_count=12,
            duration_seconds=320.0,
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
    python: object | None = None,
    cyberflies: object | None = None,
    documents: object | None = None,
    bearer: str | None = None,
    blog_posts: list | None = None,
    dao: bool = False,
    user_id: object | None = None,
    list_user_notes: object | None = None,
    list_notebook_notes: object | None = None,
    list_note_flashcards: object | None = None,
    wallet_access: object | None = None,
) -> ToolContext:
    from cyberdyne_backend.application.analytics import GetLearnerDashboard
    from cyberdyne_backend.application.blog import GetBlogPost, ListBlogPosts
    from cyberdyne_backend.application.courses import (
        GetCourse,
        GetMyCourseProgress,
        ListCourses,
    )
    from cyberdyne_backend.application.dao_treasury import GetDaoOverview
    from cyberdyne_backend.application.learning import (
        EnrollInPath,
        GetMyDeadlines,
        GetMyLearningState,
        GetPathGating,
        UpdateModuleProgress,
    )
    from cyberdyne_backend.application.quizzes import GetQuiz

    content = _FakeContentRepo()
    learning = _FakeLearningRepo()
    courses = _FakeCourseRepo()
    quizzes = _FakeQuizRepo()
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
        python=python,  # type: ignore[arg-type]
        cyberflies=cyberflies,  # type: ignore[arg-type]
        documents=documents,  # type: ignore[arg-type]
        bearer=bearer,
        dao_overview=dao_overview,
        list_blog_posts=ListBlogPosts(repo=blog),  # type: ignore[arg-type]
        get_blog_post=GetBlogPost(repo=blog),  # type: ignore[arg-type]
        enroll_in_path=EnrollInPath(repo=learning),
        get_my_learning=GetMyLearningState(repo=learning),
        update_progress=UpdateModuleProgress(repo=learning),
        list_courses=ListCourses(repo=courses),  # type: ignore[arg-type]
        get_course=GetCourse(repo=courses),  # type: ignore[arg-type]
        get_my_course_progress=GetMyCourseProgress(
            courses=courses,  # type: ignore[arg-type]
            progress=_FakeCourseProgressRepo(),  # type: ignore[arg-type]
        ),
        get_my_deadlines=GetMyDeadlines(repo=learning),
        path_gating=GetPathGating(repo=learning),
        get_quiz=GetQuiz(repo=quizzes),  # type: ignore[arg-type]
        learner_dashboard=GetLearnerDashboard(repo=_FakeAnalyticsRepo()),  # type: ignore[arg-type]
        list_user_notes=list_user_notes,  # type: ignore[arg-type]
        list_notebook_notes=list_notebook_notes,  # type: ignore[arg-type]
        list_note_flashcards=list_note_flashcards,  # type: ignore[arg-type]
        get_wallet_access=wallet_access,  # type: ignore[arg-type]
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
        page = await GetChatHistory(repo=repo).execute(session.id)
        # Default (no limit): whole history, no cursor — backward-compatible.
        assert [m.role for m in page.messages] == [ChatRole.USER, ChatRole.ASSISTANT]
        assert page.next_cursor is None

    async def test_missing_session_raises(self) -> None:
        with pytest.raises(ChatSessionNotFoundError):
            await GetChatHistory(repo=_FakeChatRepo()).execute(uuid.uuid4())

    async def _seed_messages(self, repo: _FakeChatRepo, session_id: uuid.UUID, n: int) -> None:
        from cyberdyne_backend.domain.ai_chat import new_user_message

        base = datetime(2026, 1, 1, tzinfo=UTC)
        for i in range(n):
            msg = new_user_message(session_id=session_id, content=f"m{i:02d}")
            # Deterministic, strictly increasing timestamps for stable paging.
            msg.created_at = base.replace(minute=i)
            await repo.append_message(msg)

    async def test_limit_returns_most_recent_with_cursor(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        await self._seed_messages(repo, session.id, 5)
        page = await GetChatHistory(repo=repo).execute(session.id, limit=2)
        # Most-recent 2, still chronological.
        assert [m.content for m in page.messages] == ["m03", "m04"]
        assert page.next_cursor is not None  # older messages remain

    async def test_cursor_pages_backwards(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        await self._seed_messages(repo, session.id, 5)
        uc = GetChatHistory(repo=repo)
        first = await uc.execute(session.id, limit=2)
        second = await uc.execute(session.id, limit=2, before=first.next_cursor)
        assert [m.content for m in second.messages] == ["m01", "m02"]
        third = await uc.execute(session.id, limit=2, before=second.next_cursor)
        assert [m.content for m in third.messages] == ["m00"]
        assert third.next_cursor is None  # reached the oldest message

    async def test_limit_at_or_above_total_has_no_cursor(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        await self._seed_messages(repo, session.id, 3)
        page = await GetChatHistory(repo=repo).execute(session.id, limit=10)
        assert [m.content for m in page.messages] == ["m00", "m01", "m02"]
        assert page.next_cursor is None

    async def test_malformed_cursor_treated_as_most_recent(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        await self._seed_messages(repo, session.id, 3)
        page = await GetChatHistory(repo=repo).execute(session.id, limit=2, before="not-a-cursor")
        assert [m.content for m in page.messages] == ["m01", "m02"]


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

    async def test_interpreter_session_and_attachments_thread_to_dispatch(self) -> None:
        # Upload-and-analyze end to end: the request's interpreter session is
        # used by python_exec, and the attachment filenames reach the agent via
        # the system prompt.
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        python = _FakePython()
        llm = _ScriptedLLM(
            [
                LLMResponse(
                    content="",
                    tool_calls=(
                        ToolCall(
                            id="call_1",
                            name="python_exec",
                            arguments_json=json.dumps({"code": "open('scores.csv')"}),
                        ),
                    ),
                ),
                LLMResponse(content="The average score is 83."),
            ]
        )
        dispatcher = ToolDispatcher(_build_ctx(python=python, bearer="tok"))
        await RunChatTurn(repo=repo, llm=llm, dispatcher=dispatcher).execute(
            session_id=session.id,
            user_content="analyze my file",
            interpreter_session_id="uploaded-7",
            attachments=("scores.csv",),
        )
        # python_exec ran in the uploaded workspace, no new session created.
        assert python.created == 0
        assert python.calls[0]["session_id"] == "uploaded-7"
        # The agent was told what file is attached.
        assert "scores.csv" in llm.last_system_prompt

    async def test_no_attachment_block_without_attachments(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM([LLMResponse(content="hi")])
        await RunChatTurn(repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx())).execute(
            session_id=session.id, user_content="hello"
        )
        assert "Attached files" not in llm.last_system_prompt

    async def test_upload_uuid_grounds_prompt_and_persists_ref(self) -> None:
        # An attachment that parses as a UUID is an upload id: the ingestor
        # resolves it, the grounding block lands in the prompt, and the
        # resolved AttachmentRef is persisted on the user message.
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM([LLMResponse(content="ok")])
        ref = AttachmentRef(id=uuid.uuid4(), filename="notes.pdf", content_type="application/pdf")
        ingestor = _FakeIngestor((IngestedAttachment(ref=ref, text="grounding-text-here"),))
        await RunChatTurn(
            repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx()), ingestor=ingestor
        ).execute(
            session_id=session.id,
            user_content="summarize this",
            attachments=(str(ref.id),),
        )
        assert ingestor.seen == (ref.id,)
        assert "# Attached files (contents)" in llm.last_system_prompt
        assert "notes.pdf" in llm.last_system_prompt
        assert "grounding-text-here" in llm.last_system_prompt
        user_msg = next(m for m in repo.messages if m.role is ChatRole.USER)
        assert user_msg.attachments == (ref,)

    async def test_non_uuid_attachment_uses_interpreter_block(self) -> None:
        # A non-UUID attachment is an interpreter filename: it must keep using
        # the python_exec-workspace block, not the ingestor.
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM([LLMResponse(content="ok")])
        ingestor = _FakeIngestor(())
        await RunChatTurn(
            repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx()), ingestor=ingestor
        ).execute(
            session_id=session.id,
            user_content="analyze",
            attachments=("scores.csv",),
        )
        assert ingestor.seen is None  # never called
        assert "python_exec workspace" in llm.last_system_prompt
        assert "scores.csv" in llm.last_system_prompt
        assert "# Attached files (contents)" not in llm.last_system_prompt


class TestStreamChatTurn:
    async def test_streams_content_deltas_then_done(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM([LLMResponse(content="Hello world", model="m")])
        uc = StreamChatTurn(repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx()))
        events = [ev async for ev in uc.execute(session_id=session.id, user_content="hi")]
        kinds = [e.kind for e in events]
        assert "delta" in kinds
        assert kinds[-1] == "done"
        assert "".join(e.text for e in events if e.kind == "delta") == "Hello world"
        assert events[-1].message is not None
        assert events[-1].message.content == "Hello world"

    async def test_tool_round_emits_status_then_final(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        llm = _ScriptedLLM(
            [
                LLMResponse(
                    content="",
                    tool_calls=(ToolCall(id="c1", name="list_projects", arguments_json="{}"),),
                ),
                LLMResponse(content="We build CyberSTAC."),
            ]
        )
        uc = StreamChatTurn(repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx()))
        events = [ev async for ev in uc.execute(session_id=session.id, user_content="what?")]
        status = [e for e in events if e.kind == "status"]
        assert status and status[0].text == "list_projects"
        assert events[-1].kind == "done"
        assert events[-1].message is not None
        assert events[-1].message.content == "We build CyberSTAC."
        # Persisted: user, assistant(tool_call), tool(result), assistant(final).
        roles = [m.role for m in repo.messages]
        assert roles == [
            ChatRole.USER,
            ChatRole.ASSISTANT,
            ChatRole.TOOL,
            ChatRole.ASSISTANT,
        ]

    async def test_stream_threads_interpreter_session_and_attachments(self) -> None:
        repo = _FakeChatRepo()
        session = await StartChatSession(repo=repo).execute()
        python = _FakePython()
        llm = _ScriptedLLM(
            [
                LLMResponse(
                    content="",
                    tool_calls=(
                        ToolCall(
                            id="c1",
                            name="python_exec",
                            arguments_json=json.dumps({"code": "open('f.csv')"}),
                        ),
                    ),
                ),
                LLMResponse(content="done"),
            ]
        )
        uc = StreamChatTurn(
            repo=repo, llm=llm, dispatcher=ToolDispatcher(_build_ctx(python=python, bearer="t"))
        )
        _ = [
            ev
            async for ev in uc.execute(
                session_id=session.id,
                user_content="analyze",
                interpreter_session_id="up-1",
                attachments=("f.csv",),
            )
        ]
        assert python.created == 0
        assert python.calls[0]["session_id"] == "up-1"
        assert "f.csv" in llm.last_system_prompt


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

    async def test_python_exec_runs_in_server_session(self) -> None:
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="tok-9")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="python_exec",
                arguments_json=json.dumps({"code": "print(sum(range(10)))"}),
            ),
            chat_session_id="sess-7",
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert "45" in data["stdout"]
        assert data["result"] == "45"
        # A server-issued session is created (never a client-invented id)
        # and the bearer + restricted sandbox are forwarded.
        assert python.created == 1
        assert python.calls[0]["session_id"] == "srv-session-1"
        assert python.calls[0]["bearer"] == "tok-9"
        assert python.calls[0]["restricted"] is True

    async def test_python_exec_reuses_one_session_within_a_turn(self) -> None:
        python = _FakePython()
        dispatcher = ToolDispatcher(_build_ctx(python=python, bearer="t"))
        for _ in range(3):
            await dispatcher.dispatch(
                ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": "1"})),
                chat_session_id="s",
            )
        # One session created, reused across the three calls.
        assert python.created == 1
        assert {c["session_id"] for c in python.calls} == {"srv-session-1"}

    async def test_python_exec_reports_figure_artifacts(self) -> None:
        python = _FakePython(artifacts=("plot.png", "data.csv"))
        ctx = _build_ctx(python=python, bearer="tok")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="python_exec",
                arguments_json=json.dumps({"code": "savefig('plot.png')"}),
            ),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["has_figure"] is True
        assert data["figures"] == ["plot.png"]
        assert data["artifacts"] == ["plot.png", "data.csv"]

    def test_python_tool_descriptions_do_not_promise_variable_persistence(self) -> None:
        # Regression: the interpreter's /execute path is stateless per call —
        # only workspace FILES persist, not the Python namespace. The tool
        # descriptions must not tell the model variables carry over (they
        # used to, which made the model write code that NameError'd).
        tools = {t.name: t for t in CYBERDYNE_TOOLS}
        py = tools["python_exec"].description.lower()
        assert "variables" in py and "do not carry over" in py
        assert "files" in py and "persist" in py
        # The old misleading phrasing must be gone.
        assert "variables and files persist" not in py

        manim = tools["render_manim"].description.lower()
        assert "variables do not carry over" in manim
        assert "stateful interpreter session" not in manim

    async def test_python_exec_detects_figure_from_rich_outputs(self) -> None:
        # The interpreter auto-captures a figure into an extensionless artifact
        # but flags it via rich_outputs (image/* mime type). The agent must
        # surface it even though the filename wouldn't sniff as an image.
        from cyberdyne_backend.domain.ai_chat import RichOutput

        python = _FakePython(
            artifacts=("fig-0",),
            rich_outputs=(RichOutput(mime_type="image/png", artifact="fig-0"),),
        )
        ctx = _build_ctx(python=python, bearer="tok")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="python_exec",
                arguments_json=json.dumps({"code": "plt.plot([1,2]); plt.show()"}),
            ),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["has_figure"] is True
        assert data["figures"] == ["fig-0"]

    async def test_render_manim_returns_animation_figure(self) -> None:
        python = _FakePython(manim_artifacts=("Demo.gif",))
        ctx = _build_ctx(python=python, bearer="tok-m")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="render_manim",
                arguments_json=json.dumps(
                    {
                        "code": "from manim import *\nclass Demo(Scene):\n    def construct(self):\n        self.play(Create(Circle()))",
                        "scene": "Demo",
                        "quality": "low",
                    }
                ),
            ),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["status"] == "succeeded"
        assert data["has_figure"] is True
        assert data["figures"] == ["Demo.gif"]
        # Rendered into a server-created session, as GIF, with the user's bearer.
        call = python.manim_calls[0]
        assert call["scene"] == "Demo"
        assert call["quality"] == "low"
        assert call["output_format"] == "gif"
        assert call["bearer"] == "tok-m"
        assert str(call["session_id"]).startswith("srv-session-")

    async def test_render_manim_reuses_python_session_within_turn(self) -> None:
        python = _FakePython()
        dispatcher = ToolDispatcher(_build_ctx(python=python, bearer="t"))
        await dispatcher.dispatch(
            ToolCall(id="a", name="python_exec", arguments_json=json.dumps({"code": "1"})),
            chat_session_id="s",
        )
        await dispatcher.dispatch(
            ToolCall(
                id="b",
                name="render_manim",
                arguments_json=json.dumps({"code": "from manim import *", "scene": "S"}),
            ),
            chat_session_id="s",
        )
        # One session for the whole turn — python_exec + render_manim share it.
        assert python.created == 1
        assert python.calls[0]["session_id"] == python.manim_calls[0]["session_id"]

    async def test_render_manim_surfaces_failure_traceback(self) -> None:
        # Regression: the renderer merges stderr into stdout, so a failed scene's
        # traceback lands in stdout — which the tool used to drop, leaving the
        # model with only the generic `error`. It must forward stdout so the
        # model can see the real cause (here, a bad get_area kwarg) and fix it.
        python = _FakePython(manim_status="failed")
        ctx = _build_ctx(python=python, bearer="tok")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="render_manim",
                arguments_json=json.dumps({"code": "from manim import *", "scene": "Bad"}),
            ),
            chat_session_id="s",
        )
        data = json.loads(result)
        assert data["ok"] is False
        assert data["status"] == "failed"
        assert data["has_figure"] is False
        assert "TypeError" in data["stdout"]
        assert "get_area" in data["stdout"]

    async def test_render_manim_rejects_empty_code_and_scene(self) -> None:
        ctx = _build_ctx(python=_FakePython(), bearer="t")
        empty_code = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="render_manim", arguments_json=json.dumps({"scene": "S"})),
            chat_session_id="s",
        )
        assert json.loads(empty_code)["error"] == "empty_code"
        no_scene = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="y",
                name="render_manim",
                arguments_json=json.dumps({"code": "from manim import *"}),
            ),
            chat_session_id="s",
        )
        assert json.loads(no_scene)["error"] == "missing_scene"

    async def test_render_manim_unavailable_when_port_missing(self) -> None:
        ctx = _build_ctx(python=None)
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="render_manim",
                arguments_json=json.dumps({"code": "from manim import *", "scene": "S"}),
            ),
            chat_session_id="s",
        )
        assert json.loads(result)["error"] == "python_unavailable"

    async def test_python_exec_auto_captures_matplotlib_without_savefig(self) -> None:
        # Regression: plt.show() in the headless sandbox saves nothing, so the
        # agent's plotting code must be auto-savefig'd or the user sees no plot.
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="tok")
        code = "import matplotlib.pyplot as plt\nplt.plot([1, 2, 3])\nplt.show()"
        await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": code})),
            chat_session_id="s",
        )
        sent = cast(str, python.calls[0]["code"])
        assert code in sent  # user's code is preserved verbatim
        assert "savefig" in sent  # capture epilogue appended
        assert 'savefig("figure_' in sent  # captured to a figure_<tag> file
        assert "_0_" in sent  # per-call sequence in the filename

    async def test_python_exec_does_not_auto_capture_when_savefig_present(self) -> None:
        # The agent saved its own figure — don't double-capture it.
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="tok")
        code = "import matplotlib.pyplot as plt\nplt.plot([1])\nplt.savefig('mine.png')"
        await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": code})),
            chat_session_id="s",
        )
        assert python.calls[0]["code"] == code  # unchanged

    async def test_python_exec_no_capture_for_non_plotting_code(self) -> None:
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="tok")
        code = "print(sum(range(10)))"
        await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": code})),
            chat_session_id="s",
        )
        assert python.calls[0]["code"] == code  # no epilogue for plain code

    async def test_python_exec_capture_sequence_is_unique_per_call(self) -> None:
        # Two plotting calls in one turn must capture to distinct filenames so
        # the second figure doesn't overwrite the first.
        python = _FakePython()
        dispatcher = ToolDispatcher(_build_ctx(python=python, bearer="tok"))
        for _ in range(2):
            await dispatcher.dispatch(
                ToolCall(
                    id="x",
                    name="python_exec",
                    arguments_json=json.dumps(
                        {"code": "import matplotlib.pyplot as plt\nplt.plot([1])"}
                    ),
                ),
                chat_session_id="s",
            )
        assert "_0_" in cast(str, python.calls[0]["code"])
        assert "_1_" in cast(str, python.calls[1]["code"])

    async def test_use_python_session_seeds_uploaded_workspace(self) -> None:
        # Upload-and-analyze: a pre-seeded session is reused (no new session
        # created) so python_exec runs where the user's files live.
        python = _FakePython()
        dispatcher = ToolDispatcher(_build_ctx(python=python, bearer="tok"))
        dispatcher.use_python_session("uploaded-session-1")
        await dispatcher.dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": "1"})),
            chat_session_id="s",
        )
        assert python.created == 0  # did NOT create a new session
        assert python.calls[0]["session_id"] == "uploaded-session-1"

    async def test_python_exec_empty_code_rejected(self) -> None:
        ctx = _build_ctx(python=_FakePython())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": "  "})),
            chat_session_id="s",
        )
        assert json.loads(result)["error"] == "empty_code"

    async def test_python_exec_unavailable_when_port_missing(self) -> None:
        ctx = _build_ctx()  # python defaults to None
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="python_exec", arguments_json=json.dumps({"code": "1+1"})),
            chat_session_id="s",
        )
        assert json.loads(result)["error"] == "python_unavailable"

    async def test_ask_meetings_forwards_question_and_bearer(self) -> None:
        cyberflies = _FakeCyberflies()
        ctx = _build_ctx(cyberflies=cyberflies, bearer="tok-m")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="ask_meetings",
                arguments_json=json.dumps({"question": "what did we decide on budget?"}),
            )
        )
        data = json.loads(result)
        assert "Q3 budget" in data["reply"]
        assert cyberflies.ask_calls[0]["question"] == "what did we decide on budget?"
        assert cyberflies.ask_calls[0]["bearer"] == "tok-m"

    async def test_ask_meetings_empty_question_rejected(self) -> None:
        ctx = _build_ctx(cyberflies=_FakeCyberflies())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="ask_meetings", arguments_json=json.dumps({"question": " "}))
        )
        assert json.loads(result)["error"] == "empty_question"

    async def test_list_meetings_returns_summaries(self) -> None:
        cyberflies = _FakeCyberflies()
        ctx = _build_ctx(cyberflies=cyberflies, bearer="t")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="list_meetings", arguments_json="{}")
        )
        data = json.loads(result)
        assert data["meetings"][0]["headline"] == "Standup"
        assert data["meetings"][0]["id"] == "rec-1"

    async def test_meetings_unavailable_when_port_missing(self) -> None:
        ctx = _build_ctx()  # cyberflies defaults to None
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="ask_meetings", arguments_json=json.dumps({"question": "hi"}))
        )
        assert json.loads(result)["error"] == "cyberflies_unavailable"

    async def test_get_meeting_returns_summary_and_transcript(self) -> None:
        cyberflies = _FakeCyberflies()
        ctx = _build_ctx(cyberflies=cyberflies, bearer="tok-g")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="get_meeting",
                arguments_json=json.dumps({"meeting_id": "rec-1"}),
            )
        )
        data = json.loads(result)
        assert data["id"] == "rec-1"
        assert data["headline"] == "Standup"
        assert data["bullets"] == ["Approve budget", "Ship the agent"]
        assert "ship the agent" in data["transcript"].lower()
        assert data["word_count"] == 12
        # id + bearer are forwarded to the port.
        assert cyberflies.get_calls[0] == {"meeting_id": "rec-1", "bearer": "tok-g"}

    async def test_get_meeting_missing_id_rejected(self) -> None:
        ctx = _build_ctx(cyberflies=_FakeCyberflies())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_meeting", arguments_json=json.dumps({"meeting_id": " "}))
        )
        assert json.loads(result)["error"] == "missing_meeting_id"

    async def test_get_meeting_not_found(self) -> None:
        ctx = _build_ctx(cyberflies=_FakeCyberflies(found=False), bearer="t")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_meeting", arguments_json=json.dumps({"meeting_id": "nope"}))
        )
        data = json.loads(result)
        assert data["error"] == "not_found"
        assert data["meeting_id"] == "nope"

    async def test_get_meeting_unavailable_when_port_missing(self) -> None:
        ctx = _build_ctx()  # cyberflies defaults to None
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_meeting", arguments_json=json.dumps({"meeting_id": "rec-1"}))
        )
        assert json.loads(result)["error"] == "cyberflies_unavailable"

    async def test_create_document_writes_markdown_to_workspace(self) -> None:
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="tok-d")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_document",
                arguments_json=json.dumps(
                    {"filename": "summary", "content": "# Notes\n- a\n- b", "format": "markdown"}
                ),
            )
        )
        data = json.loads(result)
        assert data["ok"] is True
        assert data["filename"] == "summary.md"
        assert data["session_id"] == "srv-session-1"
        up = python.uploads[0]
        assert up["filename"] == "summary.md"
        assert up["content"] == b"# Notes\n- a\n- b"
        assert up["content_type"] == "text/markdown"
        assert up["bearer"] == "tok-d"

    async def test_create_document_mermaid_uses_mmd_extension(self) -> None:
        python = _FakePython()
        ctx = _build_ctx(python=python, bearer="t")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_document",
                arguments_json=json.dumps(
                    {"filename": "flow", "content": "graph TD;A-->B", "format": "mermaid"}
                ),
            )
        )
        assert json.loads(result)["filename"] == "flow.mmd"

    async def test_create_document_pdf_renders_via_document_port(self) -> None:
        python = _FakePython()
        docs = _FakeDocs()
        ctx = _build_ctx(python=python, documents=docs, bearer="t")
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_document",
                arguments_json=json.dumps(
                    {"filename": "report.pdf", "content": "# Report", "format": "pdf"}
                ),
            )
        )
        data = json.loads(result)
        assert data["filename"] == "report.pdf"
        assert docs.calls[0]["content"] == "# Report"
        assert python.uploads[0]["content"] == b"%PDF-1.4 fake"
        assert python.uploads[0]["content_type"] == "application/pdf"

    async def test_create_document_empty_content_rejected(self) -> None:
        ctx = _build_ctx(python=_FakePython())
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_document",
                arguments_json=json.dumps({"filename": "x", "content": "  ", "format": "markdown"}),
            )
        )
        assert json.loads(result)["error"] == "empty_content"

    async def test_create_document_pdf_without_renderer_reports_unavailable(self) -> None:
        ctx = _build_ctx(python=_FakePython())  # documents=None
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="create_document",
                arguments_json=json.dumps({"filename": "x", "content": "hi", "format": "pdf"}),
            )
        )
        assert json.loads(result)["error"] == "documents_unavailable"

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


class TestLearningAwarenessTools:
    """The agent's awareness of the new learning surface (courses,
    deadlines, gating) so it can guide + recommend."""

    async def test_list_courses(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_courses", arguments_json="{}")
        )
        data = json.loads(out)
        assert any(c["slug"] == "intro-to-mcp" for c in data)
        assert data[0]["lesson_count"] == 1

    async def test_list_courses_level_filter_no_match(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="list_courses", arguments_json='{"level": "Advanced"}')
        )
        assert json.loads(out) == []

    async def test_get_course_hit(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_course", arguments_json='{"slug": "intro-to-mcp"}')
        )
        data = json.loads(out)
        assert data["title"] == "Intro to MCP"
        assert data["lessons"][0]["type"] == "text"

    async def test_get_course_miss(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_course", arguments_json='{"slug": "nope"}')
        )
        assert json.loads(out)["error"] == "not_found"

    async def test_deadlines_requires_auth(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_my_deadlines", arguments_json="{}")
        )
        assert json.loads(out)["error"] == "sign_in_required"

    async def test_deadlines_for_user(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(id="x", name="get_my_deadlines", arguments_json="{}")
        )
        assert json.loads(out) == []  # fake repo has no enrollments

    async def test_path_gating_for_user(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(
                id="x",
                name="get_path_gating",
                arguments_json='{"path_slug": "cyberdyne-stack"}',
            )
        )
        data = json.loads(out)
        assert data[0]["module_slug"] == "mcp-servers"
        assert data[0]["unlocked"] is True  # first module, nothing before it

    async def test_path_gating_requires_auth(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x", name="get_path_gating", arguments_json='{"path_slug": "cyberdyne-stack"}'
            )
        )
        assert json.loads(out)["error"] == "sign_in_required"

    async def test_get_lesson_quiz_player_view_no_answer_leak(self) -> None:
        lid = str(_FakeQuizRepo.LESSON_ID)
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="get_lesson_quiz",
                arguments_json=json.dumps({"lesson_id": lid}),
            )
        )
        # Player view present...
        data = json.loads(out)
        assert data["questions"][0]["prompt"] == "2 + 2 = ?"
        assert {k for k in data["questions"][0]["options"][0]} == {"id", "text"}
        # ...and the answer key is NOT leaked anywhere in the payload.
        assert "is_correct" not in out
        assert "explanation" not in out

    async def test_get_lesson_quiz_not_found(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="get_lesson_quiz",
                arguments_json=json.dumps({"lesson_id": str(uuid.uuid4())}),
            )
        )
        assert json.loads(out)["error"] == "not_found"

    async def test_get_lesson_quiz_invalid_id(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_lesson_quiz", arguments_json='{"lesson_id": "not-a-uuid"}')
        )
        assert json.loads(out)["error"] == "invalid_lesson_id"

    async def test_dashboard_requires_auth(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_my_dashboard", arguments_json="{}")
        )
        assert json.loads(out)["error"] == "sign_in_required"

    async def test_dashboard_for_user(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(id="x", name="get_my_dashboard", arguments_json="{}")
        )
        data = json.loads(out)
        assert data["enrolled_paths"] == 2
        assert data["avg_quiz_score"] == 90.0  # mean(best 80, 100)
        assert data["quiz_pass_rate"] == 100.0  # 2/2 attempted quizzes passed
        assert data["completed_courses"] == 1
        assert data["in_progress_courses"] == 2

    async def test_course_progress_requires_auth(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(
                id="x",
                name="get_my_course_progress",
                arguments_json='{"slug": "intro-to-mcp"}',
            )
        )
        assert json.loads(out)["error"] == "sign_in_required"

    async def test_course_progress_for_user(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(
                id="x",
                name="get_my_course_progress",
                arguments_json='{"slug": "intro-to-mcp"}',
            )
        )
        data = json.loads(out)
        assert data["slug"] == "intro-to-mcp"
        assert data["total_lessons"] == 1
        assert data["completed"] is False
        assert data["percent"] == 0

    async def test_course_progress_unknown_slug(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(id="x", name="get_my_course_progress", arguments_json='{"slug": "ghost"}')
        )
        assert json.loads(out)["error"] == "not_found"

    async def test_my_courses_requires_sign_in(self) -> None:
        out = await ToolDispatcher(_build_ctx()).dispatch(
            ToolCall(id="x", name="get_my_courses", arguments_json="{}")
        )
        assert json.loads(out)["error"] == "sign_in_required"

    async def test_my_courses_reports_progress_across_courses(self) -> None:
        out = await ToolDispatcher(_build_ctx(user_id=uuid.uuid4())).dispatch(
            ToolCall(id="x", name="get_my_courses", arguments_json="{}")
        )
        data = json.loads(out)
        assert "courses" in data
        intro = next(c for c in data["courses"] if c["slug"] == "intro-to-mcp")
        assert intro["total_lessons"] == 1
        assert intro["completed"] is False
        assert intro["percent"] == 0


class TestGetMyNotesTool:
    def _notes_uc(self, notes):
        from cyberdyne_backend.application.lesson_notes import ListUserNotes
        from cyberdyne_backend.domain.lesson_notes.entities import LessonNotePage

        class _FakeNotesRepo:
            async def list_for_user(self, *, user_id, course_slug=None, cursor=None, limit=50):
                items = [n for n in notes if course_slug is None or n.course_slug == course_slug]
                return LessonNotePage(items=items, next_cursor=None)

        return ListUserNotes(repo=_FakeNotesRepo())  # type: ignore[arg-type]

    def _note(self, course_slug="quantum-101", body="my note"):
        from cyberdyne_backend.domain.lesson_notes.entities import LessonNote

        return LessonNote(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            course_slug=course_slug,
            lesson_id="l1",
            body=body,
            quote="a highlighted line",
        )

    async def test_sign_in_required_when_anonymous(self) -> None:
        ctx = _build_ctx(list_user_notes=self._notes_uc([self._note()]))
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notes", arguments_json="{}")
        )
        assert json.loads(out) == {"error": "sign_in_required"}

    async def test_returns_user_notes(self) -> None:
        notes = [self._note(body="note A"), self._note(body="note B")]
        ctx = _build_ctx(user_id=uuid.uuid4(), list_user_notes=self._notes_uc(notes))
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notes", arguments_json="{}")
        )
        data = json.loads(out)
        assert [n["body"] for n in data["notes"]] == ["note A", "note B"]
        assert data["notes"][0]["quote"] == "a highlighted line"
        assert data["notes"][0]["lesson_id"] == "l1"

    async def test_filters_by_course_slug(self) -> None:
        notes = [self._note(course_slug="quantum-101"), self._note(course_slug="rust-201")]
        ctx = _build_ctx(user_id=uuid.uuid4(), list_user_notes=self._notes_uc(notes))
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notes", arguments_json='{"course_slug": "rust-201"}')
        )
        data = json.loads(out)
        assert [n["course_slug"] for n in data["notes"]] == ["rust-201"]


class TestGetMyNotebookTool:
    def _note(self, *, title="Newton's laws", note_type="theory", body="F = ma", cards=()):
        from cyberdyne_backend.domain.notebook.entities import Flashcard, Note, NoteType

        note = Note(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            title=title,
            type=NoteType(note_type),
            body=body,
        )
        flashcards = [
            Flashcard(id=uuid.uuid4(), note_id=note.id, question=q, answer=a) for q, a in cards
        ]
        return note, flashcards

    def _wire(self, pairs, *, expect_due=False, expect_query=None, expect_type=None):
        from cyberdyne_backend.application.notebook import ListFlashcards, ListNotes
        from cyberdyne_backend.domain.notebook.entities import NotePage

        notes = [n for n, _ in pairs]
        cards_by_note = {n.id: cards for n, cards in pairs}
        captured: dict = {}

        class _FakeNotebookRepo:
            async def list_for_user(
                self, *, user_id, type=None, query=None, due=False, cursor=None, limit=20
            ):
                captured.update({"type": type, "query": query, "due": due})
                return NotePage(items=notes, next_cursor=None)

            async def get(self, *, user_id, note_id):
                return next(n for n in notes if n.id == note_id)

            async def list_flashcards(self, note_id):
                return cards_by_note.get(note_id, [])

        repo = _FakeNotebookRepo()
        return (
            ListNotes(repo=repo),  # type: ignore[arg-type]
            ListFlashcards(repo=repo),  # type: ignore[arg-type]
            captured,
        )

    async def test_sign_in_required_when_anonymous(self) -> None:
        list_notes, list_cards, _ = self._wire([self._note()])
        ctx = _build_ctx(list_notebook_notes=list_notes, list_note_flashcards=list_cards)
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notebook", arguments_json="{}")
        )
        assert json.loads(out) == {"error": "sign_in_required"}

    async def test_returns_notes_with_flashcards(self) -> None:
        pairs = [self._note(cards=[("What is F?", "mass times acceleration")])]
        list_notes, list_cards, _ = self._wire(pairs)
        ctx = _build_ctx(
            user_id=uuid.uuid4(),
            list_notebook_notes=list_notes,
            list_note_flashcards=list_cards,
        )
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notebook", arguments_json="{}")
        )
        data = json.loads(out)
        note = data["notes"][0]
        assert note["title"] == "Newton's laws"
        assert note["type"] == "theory"
        assert note["flashcards"] == [
            {"question": "What is F?", "answer": "mass times acceleration"}
        ]

    async def test_passes_filters_through(self) -> None:
        list_notes, list_cards, captured = self._wire([self._note()])
        ctx = _build_ctx(
            user_id=uuid.uuid4(),
            list_notebook_notes=list_notes,
            list_note_flashcards=list_cards,
        )
        await ToolDispatcher(ctx).dispatch(
            ToolCall(
                id="x",
                name="get_my_notebook",
                arguments_json='{"query": "newton", "due": true, "type": "theory"}',
            )
        )
        assert captured["query"] == "newton"
        assert captured["due"] is True
        assert captured["type"] is not None
        assert captured["type"].value == "theory"

    async def test_ignores_unknown_type(self) -> None:
        list_notes, list_cards, captured = self._wire([self._note()])
        ctx = _build_ctx(
            user_id=uuid.uuid4(),
            list_notebook_notes=list_notes,
            list_note_flashcards=list_cards,
        )
        await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_my_notebook", arguments_json='{"type": "bogus"}')
        )
        assert captured["type"] is None


class TestGetUserTierTool:
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

    def _wallet_access(self, grants=None):
        from cyberdyne_backend.adapters.outbound.access.fake_reader import FakeAccessReader
        from cyberdyne_backend.application.access import GetWalletAccess

        return GetWalletAccess(reader=FakeAccessReader(grants or {}))

    async def test_no_wallet_linked_when_profile_has_no_wallet(self) -> None:
        ctx = _build_ctx(
            user=self._profile(wallet_address=None),
            wallet_access=self._wallet_access(),
        )
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_user_tier", arguments_json="{}")
        )
        assert json.loads(out) == {"error": "no_wallet_linked"}

    async def test_reports_no_access_for_unknown_wallet(self) -> None:
        ctx = _build_ctx(user=self._profile(), wallet_access=self._wallet_access())
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_user_tier", arguments_json="{}")
        )
        data = json.loads(out)
        assert data["has_access_nft"] is False
        assert data["token_count"] == 0
        assert all(v is False for v in data["traits"].values())

    async def test_surfaces_granted_traits(self) -> None:
        from cyberdyne_backend.domain.access import AccessTraits, WalletAccess

        addr = "0xabcdef0000000000000000000000000000001234"
        grant = WalletAccess(
            address=addr,
            has_access_nft=True,
            token_count=1,
            traits=AccessTraits(learning=True, admin=True),
        )
        ctx = _build_ctx(
            user=self._profile(),
            wallet_access=self._wallet_access({addr: grant}),
        )
        out = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="x", name="get_user_tier", arguments_json="{}")
        )
        data = json.loads(out)
        assert data["has_access_nft"] is True
        assert data["token_count"] == 1
        assert data["traits"]["learning"] is True
        assert data["traits"]["admin"] is True
        assert data["traits"]["marketplace"] is False


# Suppress unused-import warning.
_ = datetime.now(tz=UTC)
_ = ToolSchema(name="_", description="_")
_: ChatLLMPort = _ScriptedLLM([])

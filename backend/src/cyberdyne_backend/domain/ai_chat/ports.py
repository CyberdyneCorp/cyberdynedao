"""Ports for the AI chat context."""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.ai_chat.entities import ChatMessage, ChatSession, ToolCall


@dataclass(frozen=True, slots=True)
class LLMResponse:
    """One inference step. Either ``content`` is populated (final answer)
    or ``tool_calls`` is non-empty (more rounds needed)."""

    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    finish_reason: str = ""


@dataclass(frozen=True, slots=True)
class ToolSchema:
    """OpenAI-compatible tool descriptor."""

    name: str
    description: str
    parameters: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class LLMStreamChunk:
    """One streamed step. ``content_delta`` is text to append to the visible
    answer as it's generated; ``response`` is set exactly once, on the final
    chunk, with the fully-accumulated result (content + tool_calls + usage)."""

    content_delta: str = ""
    response: LLMResponse | None = None


@runtime_checkable
class ChatLLMPort(Protocol):
    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse: ...

    def stream(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> AsyncIterator[LLMStreamChunk]:
        """Stream one inference step. Yields content deltas as they arrive,
        then a final chunk carrying the complete LLMResponse. Tool-call rounds
        emit no content deltas (content is empty) — only the final chunk, whose
        response carries the tool_calls to dispatch."""
        ...


@runtime_checkable
class KnowledgeSearchPort(Protocol):
    """CyberRAG MCP client (or equivalent). v1 ships with a stub that
    returns "no semantic index configured"."""

    async def search(self, query: str, *, mode: str = "hybrid") -> str: ...


@dataclass(frozen=True, slots=True)
class MatlabRunResult:
    """One MATLAB-LLVM execution. Figures are referenced by ``artifacts``
    + ``session_id`` (NOT inlined) — the frontend downloads them through
    the authed /api/matlab proxy. Embedding the PNG here would feed it
    straight back into the next LLM round, bloating the prompt and
    risking the call."""

    ok: bool
    stdout: str
    stderr: str
    artifacts: tuple[str, ...] = ()
    session_id: str = ""
    timed_out: bool = False


@dataclass(frozen=True, slots=True)
class MatlabDiagnostic:
    severity: str
    message: str
    line: int | None = None
    col: int | None = None


@dataclass(frozen=True, slots=True)
class MatlabCheckResult:
    ok: bool
    diagnostics: tuple[MatlabDiagnostic, ...] = ()
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True, slots=True)
class MatlabCodegenResult:
    ok: bool
    language: str
    code: str
    diagnostics: tuple[MatlabDiagnostic, ...] = ()
    stderr: str = ""


@runtime_checkable
class MatlabPort(Protocol):
    """Thin client over the MATLAB-LLVM backend. The agent calls it as
    the signed-in user (``bearer`` is the user's CyberdyneAuth token),
    so figures land in that user's per-session workspace."""

    async def run_repl(
        self, *, source: str, session_id: str, bearer: str | None
    ) -> MatlabRunResult: ...

    async def run_plot(
        self, *, source: str, session_id: str, bearer: str | None, fmt: str = "png"
    ) -> MatlabRunResult: ...

    async def check(
        self, *, source: str, session_id: str, bearer: str | None
    ) -> MatlabCheckResult: ...

    async def codegen(
        self, *, source: str, target: str, session_id: str, bearer: str | None
    ) -> MatlabCodegenResult: ...


@dataclass(frozen=True, slots=True)
class PythonExecResult:
    """One Python interpreter execution. Like MATLAB, files written to the
    workspace are referenced by ``artifacts`` (filenames) + ``session_id``,
    not inlined — the frontend downloads them through the authed
    /api/interpreter proxy."""

    ok: bool
    stdout: str
    stderr: str
    result: str | None = None
    error: str | None = None
    artifacts: tuple[str, ...] = ()
    session_id: str = ""


@runtime_checkable
class PythonInterpreterPort(Protocol):
    """Thin client over the Python interpreter backend. The agent calls it
    as the signed-in user (``bearer`` is the user's CyberdyneAuth token),
    so files land in that user's per-session workspace.

    Sessions must be created server-side via ``create_session`` — the
    backend rejects client-invented ids ("invalid session id"). Execution
    runs under the RestrictedPython sandbox (``restricted=True``); the
    backend disables unrestricted execution by policy."""

    async def create_session(self, *, bearer: str | None) -> str: ...

    async def execute(
        self, *, code: str, session_id: str, bearer: str | None, restricted: bool = True
    ) -> PythonExecResult: ...

    async def upload_file(
        self,
        *,
        session_id: str,
        filename: str,
        content: bytes,
        content_type: str,
        bearer: str | None,
    ) -> str:
        """Write a file into the session workspace (no code execution).
        Returns the stored filename. Used by ``create_document`` to make a
        generated file downloadable via the same artifact path."""
        ...


@runtime_checkable
class DocumentRendererPort(Protocol):
    """Renders document bytes from text content (e.g. markdown → PDF)."""

    def render_pdf(self, *, content: str, title: str | None = None) -> bytes: ...


@dataclass(frozen=True, slots=True)
class MeetingSummary:
    """A one-line meeting/recording descriptor for the agent's
    ``list_meetings`` tool."""

    id: str
    headline: str
    status: str
    created_at: str


@dataclass(frozen=True, slots=True)
class MeetingDetail:
    """Full detail for one meeting/recording, for the ``get_meeting`` tool:
    the AI summary (headline / abstract / key points) plus the transcript
    text, so the agent can summarize it, extract action items, or draft a
    follow-up grounded in what was actually said."""

    id: str
    headline: str
    abstract: str
    bullets: tuple[str, ...]
    transcript: str
    status: str
    created_at: str
    word_count: int = 0
    duration_seconds: float | None = None


@runtime_checkable
class CyberfliesPort(Protocol):
    """Thin client over the Cyberflies (meetings) backend. The agent calls
    it as the signed-in user (``bearer`` is the user's CyberdyneAuth token)
    so it only ever sees that user's recordings."""

    async def ask_meetings(self, *, question: str, bearer: str | None) -> str: ...

    async def list_meetings(self, *, bearer: str | None) -> tuple[MeetingSummary, ...]: ...

    async def get_meeting(self, *, meeting_id: str, bearer: str | None) -> MeetingDetail | None: ...


@runtime_checkable
class ChatRepository(Protocol):
    async def save_session(self, session: ChatSession) -> None: ...
    async def get_session(self, session_id: UUID) -> ChatSession: ...
    async def append_message(self, message: ChatMessage) -> None: ...
    async def list_messages(self, session_id: UUID) -> list[ChatMessage]: ...

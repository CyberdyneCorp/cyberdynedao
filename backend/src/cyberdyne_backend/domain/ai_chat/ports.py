"""Ports for the AI chat context."""

from __future__ import annotations

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


@runtime_checkable
class ChatLLMPort(Protocol):
    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse: ...


@runtime_checkable
class KnowledgeSearchPort(Protocol):
    """CyberRAG MCP client (or equivalent). v1 ships with a stub that
    returns "no semantic index configured"."""

    async def search(self, query: str, *, mode: str = "hybrid") -> str: ...


@runtime_checkable
class ChatRepository(Protocol):
    async def save_session(self, session: ChatSession) -> None: ...
    async def get_session(self, session_id: UUID) -> ChatSession: ...
    async def append_message(self, message: ChatMessage) -> None: ...
    async def list_messages(self, session_id: UUID) -> list[ChatMessage]: ...

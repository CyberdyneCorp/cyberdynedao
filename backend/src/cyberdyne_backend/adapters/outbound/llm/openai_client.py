"""OpenAI Chat Completions adapter — ``httpx``-only (no ``openai`` dep).

Translates Cyberdyne ``ChatMessage``s into OpenAI's wire format and
back. v1 is non-streaming for simplicity; the SSE response endpoint
emits ``assistant`` and ``tool`` events as the dispatcher loop runs.
Streaming the *token deltas* themselves is a follow-up; the LLM call
finishes in one POST today.
"""

from __future__ import annotations

import logging
from typing import cast

import httpx

from cyberdyne_backend.domain.ai_chat import (
    ChatMessage,
    ChatProviderError,
    ChatRole,
    LLMResponse,
    ToolCall,
)
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema

logger = logging.getLogger("cyberdyne_backend.openai")

_DEFAULT_BASE_URL = "https://api.openai.com/v1"


class OpenAIChatClient:
    def __init__(
        self,
        *,
        api_key: str,
        http_client: httpx.AsyncClient,
        model: str = "gpt-4o-mini",
        base_url: str = _DEFAULT_BASE_URL,
        timeout_s: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self._api_key = api_key
        self._http = http_client
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse:
        wire_messages: list[dict[str, object]] = [{"role": "system", "content": system_prompt}]
        for m in messages:
            wire_messages.append(_message_to_openai(m))
        body: dict[str, object] = {
            "model": self._model,
            "messages": wire_messages,
        }
        if tools:
            body["tools"] = [_tool_to_openai(t) for t in tools]
        # Transient transport hiccups (a dropped keep-alive on the shared
        # httpx pool, a brief network blip) surface as httpx.HTTPError
        # with an often-empty message. One quick retry turns those from a
        # user-visible 502 into a non-event; a real outage still fails.
        last_exc: httpx.HTTPError | None = None
        for attempt in range(2):
            try:
                response = await self._http.post(
                    f"{self._base_url}/chat/completions",
                    json=body,
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=self._timeout_s,
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                logger.warning("openai transport error (attempt %d): %r", attempt + 1, exc)
                continue
            if response.status_code >= 400:
                raise ChatProviderError(
                    f"openai error {response.status_code}: {response.text[:500]}"
                )
            return _parse_openai_response(response.json(), default_model=self._model)
        raise ChatProviderError(f"openai transport error: {last_exc!r}")


def _message_to_openai(m: ChatMessage) -> dict[str, object]:
    if m.role is ChatRole.USER:
        return {"role": "user", "content": m.content}
    if m.role is ChatRole.ASSISTANT:
        payload: dict[str, object] = {"role": "assistant", "content": m.content}
        if m.tool_calls:
            payload["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": tc.arguments_json},
                }
                for tc in m.tool_calls
            ]
        return payload
    if m.role is ChatRole.TOOL:
        return {
            "role": "tool",
            "tool_call_id": m.tool_call_id or "",
            "content": m.content,
        }
    # SYSTEM messages from the transcript get suppressed — we send our
    # own system prompt up front instead.
    return {"role": "system", "content": m.content}


def _tool_to_openai(t: ToolSchema) -> dict[str, object]:
    return {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description,
            "parameters": t.parameters,
        },
    }


def _parse_openai_response(payload: object, *, default_model: str) -> LLMResponse:
    body = cast(dict[str, object], payload)
    choices = cast(list[dict[str, object]], body.get("choices") or [])
    if not choices:
        return LLMResponse(content="", model=default_model, finish_reason="empty")
    choice = choices[0]
    message = cast(dict[str, object], choice.get("message") or {})
    content = cast(str | None, message.get("content")) or ""
    raw_tool_calls = cast(list[dict[str, object]] | None, message.get("tool_calls"))
    tool_calls: tuple[ToolCall, ...] = ()
    if raw_tool_calls:
        parsed: list[ToolCall] = []
        for tc in raw_tool_calls:
            fn = cast(dict[str, object], tc.get("function") or {})
            parsed.append(
                ToolCall(
                    id=cast(str, tc.get("id", "")),
                    name=cast(str, fn.get("name", "")),
                    arguments_json=cast(str, fn.get("arguments", "{}")),
                )
            )
        tool_calls = tuple(parsed)
    usage = cast(dict[str, object], body.get("usage") or {})
    return LLMResponse(
        content=content,
        tool_calls=tool_calls,
        tokens_in=cast(int, usage.get("prompt_tokens", 0)),
        tokens_out=cast(int, usage.get("completion_tokens", 0)),
        model=cast(str, body.get("model", default_model)),
        finish_reason=cast(str, choice.get("finish_reason", "")),
    )


class StaticChatClient:
    """Mock LLM that returns a canned reply. Active when ``OPENAI_API_KEY``
    is unset — keeps the chat endpoint live in local dev without burning
    real tokens."""

    def __init__(self, *, reply: str | None = None) -> None:
        self._reply = (
            reply or "I'm running in offline mode — set OPENAI_API_KEY to enable the live model."
        )

    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse:
        return LLMResponse(content=self._reply, model="mock-offline")


class StubKnowledgeSearch:
    """v1 stub for the CyberRAG MCP client port."""

    async def search(self, query: str, *, mode: str = "hybrid") -> str:
        return (
            "Semantic knowledge search is not configured in this environment. "
            "Use lookup_module / lookup_product / list_projects for exact-slug lookups."
        )

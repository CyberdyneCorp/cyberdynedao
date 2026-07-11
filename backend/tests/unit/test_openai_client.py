"""Unit tests for the OpenAI streaming path.

Covers the SSE accumulator: content deltas are yielded as they arrive, and a
final chunk carries the fully-assembled LLMResponse (content, fragmented
tool_calls reassembled by index, and usage).
"""

from __future__ import annotations

import json

import httpx
import pytest

from cyberdyne_backend.adapters.outbound.llm.openai_client import OpenAIChatClient
from cyberdyne_backend.domain.ai_chat import ChatProviderError


def _sse(*chunks: dict) -> bytes:
    lines = [f"data: {json.dumps(c)}" for c in chunks]
    lines.append("data: [DONE]")
    return ("\n\n".join(lines) + "\n\n").encode()


def _client_with(body: bytes, status: int = 200) -> OpenAIChatClient:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, content=body)

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return OpenAIChatClient(api_key="sk-test", http_client=http, model="gpt-4o-mini")


class TestOpenAIStreaming:
    async def test_streams_content_deltas_then_final(self) -> None:
        body = _sse(
            {"model": "gpt-4o-mini", "choices": [{"delta": {"content": "Hel"}}]},
            {"choices": [{"delta": {"content": "lo"}}]},
            {"choices": [{"delta": {}, "finish_reason": "stop"}]},
            {"choices": [], "usage": {"prompt_tokens": 11, "completion_tokens": 2}},
        )
        client = _client_with(body)
        deltas: list[str] = []
        final = None
        async for chunk in client.stream(messages=[], tools=[], system_prompt="sys"):
            if chunk.content_delta:
                deltas.append(chunk.content_delta)
            if chunk.response is not None:
                final = chunk.response
        assert deltas == ["Hel", "lo"]
        assert final is not None
        assert final.content == "Hello"
        assert final.tool_calls == ()
        assert final.finish_reason == "stop"
        assert final.tokens_in == 11
        assert final.tokens_out == 2

    async def test_reassembles_fragmented_tool_calls(self) -> None:
        body = _sse(
            {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {"index": 0, "id": "call_1", "function": {"name": "get_meeting"}}
                            ]
                        }
                    }
                ]
            },
            {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {"index": 0, "function": {"arguments": '{"meeting_id":'}}
                            ]
                        }
                    }
                ]
            },
            {
                "choices": [
                    {"delta": {"tool_calls": [{"index": 0, "function": {"arguments": '"rec-1"}'}}]}}
                ]
            },
            {"choices": [{"delta": {}, "finish_reason": "tool_calls"}]},
        )
        client = _client_with(body)
        deltas: list[str] = []
        final = None
        async for chunk in client.stream(messages=[], tools=[], system_prompt="sys"):
            if chunk.content_delta:
                deltas.append(chunk.content_delta)
            if chunk.response is not None:
                final = chunk.response
        assert deltas == []  # tool-call rounds emit no visible content
        assert final is not None
        assert len(final.tool_calls) == 1
        tc = final.tool_calls[0]
        assert tc.id == "call_1"
        assert tc.name == "get_meeting"
        assert json.loads(tc.arguments_json) == {"meeting_id": "rec-1"}
        assert final.finish_reason == "tool_calls"

    async def test_http_error_raises_chat_provider_error(self) -> None:
        client = _client_with(b'{"error": "bad"}', status=429)
        with pytest.raises(ChatProviderError):
            async for _ in client.stream(messages=[], tools=[], system_prompt="sys"):
                pass


class TestReasoningEffort:
    def test_supports_reasoning_effort(self) -> None:
        from cyberdyne_backend.adapters.outbound.llm.openai_client import (
            supports_reasoning_effort,
        )

        assert supports_reasoning_effort("gpt-5-mini")
        assert supports_reasoning_effort("gpt-5")
        assert supports_reasoning_effort("gpt-5.4-nano")
        assert supports_reasoning_effort("o3-mini")
        # gpt-4o and the non-reasoning gpt-5-chat variant reject the field.
        assert not supports_reasoning_effort("gpt-4o-mini")
        assert not supports_reasoning_effort("gpt-5-chat-latest")

    @staticmethod
    def _capture_client(model: str, reasoning_effort: str | None) -> tuple[OpenAIChatClient, list]:
        seen: list[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen.append(json.loads(request.content))
            return httpx.Response(
                200,
                json={
                    "model": model,
                    "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1},
                },
            )

        http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        return (
            OpenAIChatClient(
                api_key="sk-test",
                http_client=http,
                model=model,
                reasoning_effort=reasoning_effort,
            ),
            seen,
        )

    async def test_sent_for_gpt5(self) -> None:
        client, seen = self._capture_client("gpt-5-mini", "minimal")
        await client.complete(messages=[], tools=[], system_prompt="sys")
        assert seen[0]["reasoning_effort"] == "minimal"

    async def test_omitted_for_gpt4o(self) -> None:
        # gpt-4o rejects the field; it must never be sent even when configured.
        client, seen = self._capture_client("gpt-4o-mini", "minimal")
        await client.complete(messages=[], tools=[], system_prompt="sys")
        assert "reasoning_effort" not in seen[0]

    async def test_omitted_when_unset(self) -> None:
        client, seen = self._capture_client("gpt-5-mini", None)
        await client.complete(messages=[], tools=[], system_prompt="sys")
        assert "reasoning_effort" not in seen[0]

    async def test_sent_on_stream_path(self) -> None:
        client, seen = self._capture_client("gpt-5-mini", "minimal")
        async for _ in client.stream(messages=[], tools=[], system_prompt="sys"):
            pass
        assert seen[0]["reasoning_effort"] == "minimal"
        assert seen[0]["stream"] is True

"""Unit tests for the vision question reader (issue #231).

A fake VisionPort returns canned text; we assert the reader parses strict JSON,
tolerates code fences + surrounding prose, and falls back to the raw text as the
question when no JSON can be recovered.
"""

from __future__ import annotations

import pytest

from cyberdyne_backend.adapters.outbound.llm.vision_question_reader import VisionQuestionReader

pytestmark = pytest.mark.asyncio


class _FakeVision:
    def __init__(self, reply: str) -> None:
        self._reply = reply
        self.calls = 0

    async def describe_image(self, *, image_bytes: bytes, content_type: str, prompt: str) -> str:
        self.calls += 1
        return self._reply


async def test_parses_strict_json() -> None:
    reply = '{"question": "What is 2+2?", "subject": "Arithmetic", "keywords": ["addition"]}'
    reader = VisionQuestionReader(vision=_FakeVision(reply))
    query = await reader.read_question(image_bytes=b"x", content_type="image/png")
    assert query.question == "What is 2+2?"
    assert query.subject == "Arithmetic"
    assert query.keywords == ("addition",)


async def test_strips_code_fences() -> None:
    reply = '```json\n{"question": "Solve x", "subject": null, "keywords": []}\n```'
    reader = VisionQuestionReader(vision=_FakeVision(reply))
    query = await reader.read_question(image_bytes=b"x", content_type="image/png")
    assert query.question == "Solve x"
    assert query.subject is None
    assert query.keywords == ()


async def test_recovers_json_embedded_in_prose() -> None:
    reply = 'Sure! Here it is: {"question": "Define entropy", "keywords": ["thermodynamics"]}'
    reader = VisionQuestionReader(vision=_FakeVision(reply))
    query = await reader.read_question(image_bytes=b"x", content_type="image/png")
    assert query.question == "Define entropy"
    assert query.keywords == ("thermodynamics",)


async def test_malformed_falls_back_to_raw_question() -> None:
    reply = "The image shows a calculus problem about limits."
    reader = VisionQuestionReader(vision=_FakeVision(reply))
    query = await reader.read_question(image_bytes=b"x", content_type="image/png")
    assert query.question == reply
    assert query.subject is None
    assert query.keywords == ()


async def test_drops_non_string_keywords_and_blank_subject() -> None:
    reply = '{"question": "Q", "subject": "  ", "keywords": ["a", 5, "", "b"]}'
    reader = VisionQuestionReader(vision=_FakeVision(reply))
    query = await reader.read_question(image_bytes=b"x", content_type="image/png")
    assert query.subject is None
    assert query.keywords == ("a", "b")

"""Ports the Scan-to-Learn (course_finder) context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.course_finder.entities import ScanQuery


@runtime_checkable
class EmbeddingPort(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed each input text into a vector, one per input, in input
        order. All returned vectors share a single dimensionality."""
        ...


@runtime_checkable
class VisionQuestionReaderPort(Protocol):
    async def read_question(self, *, image_bytes: bytes, content_type: str) -> ScanQuery:
        """Extract the question (plus optional subject + keywords) from a
        photographed question. Image bytes are analyzed only, never retained."""
        ...

"""Vision-backed question reader for Scan-to-Learn (issue #231).

Wraps the existing :class:`VisionPort` to extract a structured
``{question, subject, keywords}`` from a photographed question. The model is
asked for strict JSON; parsing is defensive (strips code fences, tolerates
extra prose) and falls back to treating the whole description as the question
when JSON can't be recovered. Image bytes stay in memory — never persisted.
"""

from __future__ import annotations

import json
import logging
import re
from typing import cast

from cyberdyne_backend.domain.ai_chat import VisionPort
from cyberdyne_backend.domain.course_finder import ScanQuery

logger = logging.getLogger("cyberdyne_backend.scan.vision")

_PROMPT = (
    "You are reading a photo of a study question (homework, exam, textbook). "
    "Extract the core question and classify it. Respond with STRICT JSON only, "
    "no prose, no code fences, in exactly this shape: "
    '{"question": "<the question text>", "subject": "<academic subject or null>", '
    '"keywords": ["<key topic>", ...]}. '
    "Keep keywords to the 3-6 most salient topical terms."
)

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


class VisionQuestionReader:
    def __init__(self, *, vision: VisionPort) -> None:
        self._vision = vision

    async def read_question(self, *, image_bytes: bytes, content_type: str) -> ScanQuery:
        raw = await self._vision.describe_image(
            image_bytes=image_bytes, content_type=content_type, prompt=_PROMPT
        )
        return _parse_scan_query(raw)


def _parse_scan_query(raw: str) -> ScanQuery:
    text = raw.strip()
    payload = _load_json_object(text)
    if payload is None:
        # Couldn't recover structured JSON — treat the whole description as the
        # question so a scan still searches on something sensible.
        return ScanQuery(question=text, subject=None, keywords=())
    question = _as_str(payload.get("question")) or text
    subject = _as_str(payload.get("subject"))
    keywords = _as_keywords(payload.get("keywords"))
    return ScanQuery(question=question, subject=subject, keywords=keywords)


def _load_json_object(text: str) -> dict[str, object] | None:
    candidate = _FENCE_RE.sub("", text).strip()
    for attempt in (candidate, _slice_braces(candidate)):
        if not attempt:
            continue
        try:
            parsed = json.loads(attempt)
        except (ValueError, TypeError):
            continue
        if isinstance(parsed, dict):
            return cast(dict[str, object], parsed)
    return None


def _slice_braces(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return ""
    return text[start : end + 1]


def _as_str(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _as_keywords(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    out = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    return tuple(out)

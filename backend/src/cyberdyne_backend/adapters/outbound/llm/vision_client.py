"""OpenAI vision adapter — describe / OCR image attachments (issue #220).

``httpx``-only, mirroring ``OpenAIChatClient``: one non-streaming POST to
chat-completions with a user message carrying the prompt plus the image as
a base64 ``data:`` URL, returning the model's text. ``StaticVisionClient``
is the offline fallback used when no OpenAI key is configured.
"""

from __future__ import annotations

import base64
import logging
from typing import cast

import httpx

from cyberdyne_backend.domain.ai_chat import ChatProviderError

logger = logging.getLogger("cyberdyne_backend.openai.vision")

_DEFAULT_BASE_URL = "https://api.openai.com/v1"
_UNAVAILABLE = "image description unavailable (vision model not configured)"


class OpenAIVisionClient:
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

    async def describe_image(self, *, image_bytes: bytes, content_type: str, prompt: str) -> str:
        encoded = base64.b64encode(image_bytes).decode("ascii")
        data_url = f"data:{content_type};base64,{encoded}"
        body: dict[str, object] = {
            "model": self._model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
        }
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
            raise ChatProviderError(f"openai vision transport error: {exc!r}") from exc
        if response.status_code >= 400:
            raise ChatProviderError(
                f"openai vision error {response.status_code}: {response.text[:500]}"
            )
        return _content_from(response.json())


def _content_from(payload: object) -> str:
    body = cast(dict[str, object], payload)
    choices = cast(list[dict[str, object]], body.get("choices") or [])
    if not choices:
        return ""
    message = cast(dict[str, object], choices[0].get("message") or {})
    return cast(str | None, message.get("content")) or ""


class StaticVisionClient:
    """Offline fallback — returns a fixed string when no OpenAI key is set,
    mirroring ``StaticChatClient``."""

    async def describe_image(self, *, image_bytes: bytes, content_type: str, prompt: str) -> str:
        return _UNAVAILABLE

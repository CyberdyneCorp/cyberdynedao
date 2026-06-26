"""Embedding adapters for Scan-to-Learn catalog matching (issue #231).

``OpenAIEmbeddingClient`` calls OpenAI's ``/v1/embeddings`` over ``httpx``
(mirroring ``OpenAIVisionClient``'s construction). ``StaticEmbeddingClient`` is
the offline fallback used when no OpenAI key is configured: a deterministic
set-of-words hashed embedding so cosine similarity approximates keyword overlap,
good enough for tests and key-less environments to return sensible matches.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import cast

import httpx

from cyberdyne_backend.domain.ai_chat import ChatProviderError

_DEFAULT_BASE_URL = "https://api.openai.com/v1"
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STATIC_DIM = 256

# Common connective words carry no topical signal but, counted, dilute the
# cosine between a short query and a longer catalog text. Dropping them sharpens
# the keyword-overlap signal the static embedder approximates.
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "do",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "the",
        "to",
        "what",
        "which",
        "with",
    }
)


class OpenAIEmbeddingClient:
    def __init__(
        self,
        *,
        api_key: str,
        http_client: httpx.AsyncClient,
        model: str = "text-embedding-3-small",
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

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        body: dict[str, object] = {"model": self._model, "input": texts}
        try:
            response = await self._http.post(
                f"{self._base_url}/embeddings",
                json=body,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self._timeout_s,
            )
        except httpx.HTTPError as exc:
            raise ChatProviderError(f"openai embeddings transport error: {exc!r}") from exc
        if response.status_code >= 400:
            raise ChatProviderError(
                f"openai embeddings error {response.status_code}: {response.text[:500]}"
            )
        return _vectors_from(response.json())


def _vectors_from(payload: object) -> list[list[float]]:
    body = cast(dict[str, object], payload)
    # OpenAI returns ``data`` ordered by an ``index`` field; sort defensively
    # so the order-preserving contract holds even if the API reorders.
    data = cast(list[dict[str, object]], body.get("data") or [])
    ordered = sorted(data, key=lambda item: cast(int, item.get("index", 0)))
    return [cast(list[float], item.get("embedding") or []) for item in ordered]


class StaticEmbeddingClient:
    """Deterministic offline embedding: hashed set-of-words, L2-normalized.

    Each distinct, non-stopword, lowercased alphanumeric token is hashed into
    one of ``dim`` buckets and sets that bucket to 1; the vector is then
    L2-normalized. With binary presence (not counts), cosine reduces to
    ``shared / sqrt(|a| * |b|)`` — i.e. keyword-overlap similarity — so related
    texts score well above unrelated ones. Stable across runs, no network,
    active when ``OPENAI_API_KEY`` is unset."""

    def __init__(self, *, dim: int = _STATIC_DIM) -> None:
        self._dim = dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vec = [0.0] * self._dim
        tokens = {t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS and len(t) > 1}
        for token in tokens:
            # sha1 here is a fast non-crypto hash to bucket tokens, not for security.
            digest = hashlib.sha1(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self._dim
            vec[bucket] = 1.0
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0.0:
            return vec
        return [v / norm for v in vec]

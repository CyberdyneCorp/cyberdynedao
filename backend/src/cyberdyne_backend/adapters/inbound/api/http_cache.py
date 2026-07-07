"""Conditional-request (ETag) helper for the public catalogue reads.

The catalogue list endpoints (courses, categories, learning modules/paths)
are polled repeatedly and return a large, rarely-changing body. This helper
serves them with a strong ``ETag`` plus a short ``Cache-Control: max-age`` so
a client can:

  * skip the request entirely for ``max-age`` seconds (its own cache), and
  * afterwards revalidate cheaply with ``If-None-Match`` — matching bodies
    come back as an empty ``304 Not Modified`` instead of re-transferring the
    payload.

The 200 body is the pydantic ``by_alias`` JSON of the response models — the
same camelCase shape ``response_model`` would emit — so existing clients (the
iOS app) are unaffected; keep ``response_model`` on the route decorator for
OpenAPI docs (FastAPI passes a returned ``Response`` through untouched).

Caching is ``private``, not ``public``: some of these reads vary by caller
(``/courses`` includes drafts for an editor's token) and by ``Accept-Language``.
``private`` keeps a shared/proxy cache from ever storing one caller's body and
serving it to another, while still letting each client cache its own copy and
revalidate via the ETag. See issue #260 for the shared-cache leak this avoids.
"""

from __future__ import annotations

import hashlib

from fastapi import Request, Response
from pydantic import BaseModel

# Bounds how often a polling client re-hits the endpoint. Short enough that an
# admin edit is visible within a minute; long enough to collapse tight polls.
_MAX_AGE_SECONDS = 60
_CACHE_CONTROL = f"private, max-age={_MAX_AGE_SECONDS}"


def _serialize(items: list[BaseModel]) -> bytes:
    # Join each model's own ``by_alias`` JSON into an array — byte-identical to
    # ``TypeAdapter(list[Model]).dump_json(items, by_alias=True)`` (pydantic
    # emits compact, space-free separators), and typed without a runtime type
    # variable.
    return b"[" + b",".join(m.model_dump_json(by_alias=True).encode() for m in items) + b"]"


def conditional_json_list(items: list[BaseModel], request: Request) -> Response:
    """Serve ``items`` as a cached JSON array.

    Returns ``304 Not Modified`` (empty body) when the request's
    ``If-None-Match`` equals the current ETag, otherwise a ``200`` carrying the
    serialized body. Both responses carry the ``ETag`` and ``Cache-Control``
    headers so a 304 can still be revalidated on the next poll.
    """
    body = _serialize(items)
    etag = '"' + hashlib.sha256(body).hexdigest() + '"'
    headers = {
        "ETag": etag,
        "Cache-Control": _CACHE_CONTROL,
        "Vary": "Accept-Language",
    }
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers=headers)
    return Response(content=body, media_type="application/json", headers=headers)

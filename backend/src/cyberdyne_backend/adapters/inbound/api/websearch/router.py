"""Web search endpoint — open-web search for the chat agents.

Given a query, returns organic search results (title, url, snippet) and,
when the engine surfaces one, a concise direct answer. Authentication is
required so the API cannot be used as an anonymous search proxy. Backed
by SERPAPI; returns 503 when no SERPAPI key is configured.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.websearch.schemas import (
    SearchResponse,
    SearchResultResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.websearch import SearchWeb
from cyberdyne_backend.domain.auth_identity import Principal
from cyberdyne_backend.domain.websearch import (
    DEFAULT_RESULTS,
    MAX_RESULTS,
    MIN_RESULTS,
    InvalidQueryError,
    SearchProviderError,
    SearchUnavailableError,
)
from cyberdyne_backend.domain.websearch import (
    SearchResponse as DomainSearchResponse,
)

router = APIRouter(prefix="/api/v1/search", tags=["search"])


async def get_search_web_uc() -> SearchWeb:  # pragma: no cover - override target
    raise NotImplementedError


def _response(result: DomainSearchResponse) -> SearchResponse:
    return SearchResponse(
        query=result.query,
        answer=result.answer,
        results=[
            SearchResultResponse(
                position=r.position,
                title=r.title,
                url=r.url,
                snippet=r.snippet,
                source=r.source,
            )
            for r in result.results
        ],
    )


@router.get("", response_model=SearchResponse, response_model_by_alias=True)
async def search(
    q: Annotated[str, Query(min_length=1, description="Search query")],
    use_case: Annotated[SearchWeb, Depends(get_search_web_uc)],
    _principal: Annotated[Principal, Depends(require_principal)],
    num: Annotated[
        int,
        Query(ge=MIN_RESULTS, le=MAX_RESULTS, description="Number of results"),
    ] = DEFAULT_RESULTS,
) -> SearchResponse:
    try:
        result = await use_case.execute(q, num_results=num)
    except InvalidQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SearchUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except SearchProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return _response(result)

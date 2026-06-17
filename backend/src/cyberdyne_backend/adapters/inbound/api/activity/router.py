"""Learner activity + stats endpoints (issue #164).

Records lightweight per-user activity events and derives the study streak
+ activity counts the redesigned Profile/Today surfaces show. All routes
are scoped to the authenticated user.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.activity.schemas import (
    ActivityEventResponse,
    LearnerStatsResponse,
    RecordActivityRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.activity import GetLearnerStats, RecordActivity
from cyberdyne_backend.domain.activity import (
    ActivityEvent,
    LearnerStats,
    parse_activity_kind,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal

public_router = APIRouter(prefix="/api/v1/me", tags=["me"])

# Day boundaries are computed at ±this many minutes from UTC at most
# (UTC-12:00 .. UTC+14:00). Documented so clients pass a sane offset.
_TZ_OFFSET_MIN = -12 * 60
_TZ_OFFSET_MAX = 14 * 60


# Dependency stubs — overridden in main.py.
async def get_record_activity_uc() -> RecordActivity:  # pragma: no cover - override target
    raise NotImplementedError


async def get_learner_stats_uc() -> GetLearnerStats:  # pragma: no cover - override target
    raise NotImplementedError


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


def _event_response(e: ActivityEvent) -> ActivityEventResponse:
    return ActivityEventResponse(
        id=e.id,
        kind=e.kind.value,
        ref=e.ref,
        occurred_at=e.occurred_at,
    )


def _stats_response(s: LearnerStats) -> LearnerStatsResponse:
    return LearnerStatsResponse(
        current_streak_days=s.current_streak_days,
        longest_streak_days=s.longest_streak_days,
        last_active_on=s.last_active_on,
        code_runs_count=s.code_runs_count,
        simulations_run=s.simulations_run,
        concepts_mastered=s.concepts_mastered,
    )


@public_router.post(
    "/activity",
    response_model=ActivityEventResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def record_activity(
    body: RecordActivityRequest,
    use_case: Annotated[RecordActivity, Depends(get_record_activity_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> ActivityEventResponse:
    user = _require_user(principal)
    event = await use_case.execute(
        user_id=user.user_id,
        kind=parse_activity_kind(body.kind),
        ref=body.ref,
    )
    return _event_response(event)


@public_router.get(
    "/stats",
    response_model=LearnerStatsResponse,
    response_model_by_alias=True,
)
async def get_my_stats(
    use_case: Annotated[GetLearnerStats, Depends(get_learner_stats_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    tz_offset_minutes: Annotated[
        int, Query(alias="tzOffsetMinutes", ge=_TZ_OFFSET_MIN, le=_TZ_OFFSET_MAX)
    ] = 0,
) -> LearnerStatsResponse:
    """Study streak + activity counts for the signed-in learner. The
    streak is computed from day-level activity; pass ``tzOffsetMinutes``
    (minutes east of UTC) to bucket days in the learner's timezone
    (default UTC)."""
    user = _require_user(principal)
    stats = await use_case.execute(user.user_id, tz_offset_minutes=tz_offset_minutes)
    return _stats_response(stats)

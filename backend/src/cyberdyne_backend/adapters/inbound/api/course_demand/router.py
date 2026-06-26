"""Course/topic demand registry endpoints (issue #232).

Learners request courses/topics we don't yet offer, from two entry points (a
typed request, or a Scan-to-Learn no-match). Requests land in one registry and
are clustered by normalized topic so authors see ranked demand. Demand capture
only — no authoring/publishing happens here.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.course_demand.schemas import (
    CourseRequestResponse,
    DemandClusterResponse,
    SubmitCourseRequestRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.course_demand import (
    ListCourseRequestClusters,
    SubmitCourseRequest,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.course_demand import (
    CourseRequest,
    DemandCluster,
    parse_request_source,
)

public_router = APIRouter(prefix="/api/v1/learning", tags=["learning"])
admin_router = APIRouter(prefix="/api/v1/admin/learning", tags=["admin-learning"])


# Dependency stubs — overridden in main.py.
async def get_submit_course_request_uc() -> SubmitCourseRequest:  # pragma: no cover - override
    raise NotImplementedError


async def get_list_clusters_uc() -> ListCourseRequestClusters:  # pragma: no cover - override
    raise NotImplementedError


def _request_response(r: CourseRequest) -> CourseRequestResponse:
    return CourseRequestResponse(
        id=r.id,
        topic=r.topic,
        topic_key=r.topic_key,
        subject=r.subject,
        source=r.source.value,
        created_at=r.created_at,
    )


def _cluster_response(c: DemandCluster) -> DemandClusterResponse:
    return DemandClusterResponse(
        topic_key=c.topic_key,
        topic=c.topic,
        subject=c.subject,
        count=c.count,
        last_requested_at=c.last_requested_at,
    )


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


@public_router.post(
    "/course-requests",
    response_model=CourseRequestResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def submit_course_request(
    body: SubmitCourseRequestRequest,
    use_case: Annotated[SubmitCourseRequest, Depends(get_submit_course_request_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CourseRequestResponse:
    user = _require_user(principal)
    created = await use_case.execute(
        user_id=user.user_id,
        topic=body.topic,
        source=parse_request_source(body.source),
        subject=body.subject,
        source_question_text=body.source_question_text,
        course_id=body.course_id,
        lesson_id=body.lesson_id,
    )
    return _request_response(created)


@admin_router.get(
    "/course-requests",
    response_model=list[DemandClusterResponse],
    response_model_by_alias=True,
)
async def list_course_request_clusters(
    use_case: Annotated[ListCourseRequestClusters, Depends(get_list_clusters_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[DemandClusterResponse]:
    clusters = await use_case.execute()
    return [_cluster_response(c) for c in clusters]

"""Use cases for the course/topic demand registry."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.course_demand.entities import (
    CourseRequest,
    DemandCluster,
    RequestSource,
    new_course_request,
)
from cyberdyne_backend.domain.course_demand.ports import CourseRequestRepository


@dataclass(slots=True)
class SubmitCourseRequest:
    """Capture a learner's request for a course/topic we don't yet offer.
    Open to every signed-in learner (not gated). Demand capture only — no
    authoring happens here."""

    repo: CourseRequestRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        topic: str,
        source: RequestSource,
        subject: str | None = None,
        source_question_text: str | None = None,
        course_id: str | None = None,
        lesson_id: str | None = None,
    ) -> CourseRequest:
        candidate = new_course_request(
            user_id=user_id,
            topic=topic,
            source=source,
            subject=subject,
            source_question_text=source_question_text,
            course_id=course_id,
            lesson_id=lesson_id,
        )
        return await self.repo.add(candidate)


@dataclass(slots=True)
class ListCourseRequestClusters:
    """Ranked demand for the authoring backlog — clusters ordered by how many
    learners requested each topic."""

    repo: CourseRequestRepository

    async def execute(self) -> list[DemandCluster]:
        return await self.repo.list_clusters()

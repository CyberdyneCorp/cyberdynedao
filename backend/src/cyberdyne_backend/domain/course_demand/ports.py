"""Repository port for the course-demand context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.course_demand.entities import CourseRequest, DemandCluster


@runtime_checkable
class CourseRequestRepository(Protocol):
    async def add(self, request: CourseRequest) -> CourseRequest:
        """Persist a course request and return it."""
        ...

    async def list_clusters(self) -> list[DemandCluster]:
        """Demand clusters (one per normalized topic key), ranked by request
        count (most-wanted first), then by most-recent request."""
        ...

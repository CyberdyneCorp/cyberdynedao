"""Unit tests for the course/topic demand registry (issue #232)."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from cyberdyne_backend.application.course_demand import (
    ListCourseRequestClusters,
    SubmitCourseRequest,
)
from cyberdyne_backend.domain.course_demand import (
    CourseRequest,
    DemandCluster,
    RequestSource,
    normalize_topic,
)

pytestmark = pytest.mark.unit


class _FakeRepo:
    def __init__(self) -> None:
        self.items: list[CourseRequest] = []

    async def add(self, request: CourseRequest) -> CourseRequest:
        self.items.append(request)
        return request

    async def list_clusters(self) -> list[DemandCluster]:
        clusters: dict[str, DemandCluster] = {}
        for r in sorted(self.items, key=lambda x: x.created_at, reverse=True):
            existing = clusters.get(r.topic_key)
            if existing is None:
                clusters[r.topic_key] = DemandCluster(
                    topic_key=r.topic_key,
                    topic=r.topic,
                    subject=r.subject,
                    count=1,
                    last_requested_at=r.created_at,
                )
            else:
                existing.count += 1
        return sorted(clusters.values(), key=lambda c: (c.count, c.last_requested_at), reverse=True)


def test_normalize_topic_clusters_equivalent_text() -> None:
    # Punctuation, case, and spacing differences collapse to one key.
    assert normalize_topic("Linear Algebra: eigenvalues") == "linear algebra eigenvalues"
    assert normalize_topic("  linear algebra   eigenvalues!! ") == "linear algebra eigenvalues"
    assert normalize_topic("Eigenvalues?") == normalize_topic("eigenvalues")


def test_typed_and_scan_same_topic_cluster_together() -> None:
    repo = _FakeRepo()
    submit = SubmitCourseRequest(repo=repo)
    # A typed request and a scan no-match for the same topic (different casing).
    asyncio.run(
        submit.execute(user_id=uuid.uuid4(), topic="Eigenvalues", source=RequestSource.TYPED)
    )
    asyncio.run(
        submit.execute(
            user_id=uuid.uuid4(),
            topic="eigenvalues?",
            source=RequestSource.SCAN,
            source_question_text="Find the eigenvalues of A",
        )
    )

    clusters = asyncio.run(ListCourseRequestClusters(repo=repo).execute())
    assert len(clusters) == 1
    assert clusters[0].count == 2
    assert clusters[0].topic_key == "eigenvalues"


def test_clusters_ranked_by_demand() -> None:
    repo = _FakeRepo()
    submit = SubmitCourseRequest(repo=repo)
    for _ in range(3):
        asyncio.run(
            submit.execute(user_id=uuid.uuid4(), topic="Calculus", source=RequestSource.TYPED)
        )
    asyncio.run(submit.execute(user_id=uuid.uuid4(), topic="Topology", source=RequestSource.TYPED))

    clusters = asyncio.run(ListCourseRequestClusters(repo=repo).execute())
    assert [(c.topic_key, c.count) for c in clusters] == [("calculus", 3), ("topology", 1)]

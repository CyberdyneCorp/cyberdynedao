"""Unit tests for the learner-feedback use cases (issue #233)."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from cyberdyne_backend.application.feedback import ListFeedback, SubmitFeedback
from cyberdyne_backend.domain.feedback import (
    Feedback,
    FeedbackKind,
    FeedbackStatus,
)

pytestmark = pytest.mark.unit


class _FakeRepo:
    def __init__(self) -> None:
        self.items: list[Feedback] = []

    async def add(self, feedback: Feedback) -> Feedback:
        self.items.append(feedback)
        return feedback

    async def list_all(
        self,
        *,
        kind: FeedbackKind | None = None,
        status: FeedbackStatus | None = None,
    ) -> list[Feedback]:
        rows = list(reversed(self.items))  # newest first
        if kind is not None:
            rows = [r for r in rows if r.kind == kind]
        if status is not None:
            rows = [r for r in rows if r.status == status]
        return rows


def test_submit_feedback_persists_new_item() -> None:
    repo = _FakeRepo()
    uc = SubmitFeedback(repo=repo)
    user_id = uuid.uuid4()

    feedback = asyncio.run(
        uc.execute(
            user_id=user_id,
            kind=FeedbackKind.PROBLEM,
            message="The video player stalls on lesson 3.",
            course_id="r-data-analysis-advanced",
            lesson_id="9dc76395-22a5-4204-9a44-9fd2a609d8bc",
            app_version="1.4.2",
            platform="ios",
        )
    )

    assert feedback.user_id == user_id
    assert feedback.kind == FeedbackKind.PROBLEM
    assert feedback.status == FeedbackStatus.NEW  # new items start in triage queue
    assert feedback.course_id == "r-data-analysis-advanced"
    assert repo.items == [feedback]


def test_list_feedback_filters_by_kind_and_status() -> None:
    repo = _FakeRepo()
    submit = SubmitFeedback(repo=repo)
    user_id = uuid.uuid4()
    asyncio.run(submit.execute(user_id=user_id, kind=FeedbackKind.PROBLEM, message="bug"))
    asyncio.run(submit.execute(user_id=user_id, kind=FeedbackKind.FEATURE, message="please add X"))

    list_uc = ListFeedback(repo=repo)
    assert len(asyncio.run(list_uc.execute())) == 2
    problems = asyncio.run(list_uc.execute(kind=FeedbackKind.PROBLEM))
    assert [f.kind for f in problems] == [FeedbackKind.PROBLEM]
    new_features = asyncio.run(
        list_uc.execute(kind=FeedbackKind.FEATURE, status=FeedbackStatus.NEW)
    )
    assert [f.kind for f in new_features] == [FeedbackKind.FEATURE]
    assert asyncio.run(list_uc.execute(status=FeedbackStatus.CLOSED)) == []

"""Unit tests for the ListQuizCatalog use case (issue #169)."""

from __future__ import annotations

import asyncio
import uuid

from cyberdyne_backend.application.quizzes import ListQuizCatalog
from cyberdyne_backend.domain.quizzes import QuizCatalogPage


class _FakeReader:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def list_quizzes(
        self,
        *,
        user_id,
        course_slug=None,
        category_slug=None,
        cursor=None,
        limit=20,
    ) -> QuizCatalogPage:
        self.calls.append(
            {
                "user_id": user_id,
                "course_slug": course_slug,
                "category_slug": category_slug,
                "cursor": cursor,
                "limit": limit,
            }
        )
        return QuizCatalogPage(items=[], next_cursor=None)


def test_limit_is_clamped_into_range() -> None:
    reader = _FakeReader()
    uc = ListQuizCatalog(reader=reader)
    user = uuid.uuid4()

    asyncio.run(uc.execute(user_id=user, limit=9999))
    asyncio.run(uc.execute(user_id=user, limit=0))

    assert reader.calls[0]["limit"] == 100  # MAX_CATALOG_LIMIT
    assert reader.calls[1]["limit"] == 1  # floor of 1


def test_filters_pass_through() -> None:
    reader = _FakeReader()
    uc = ListQuizCatalog(reader=reader)
    user = uuid.uuid4()

    asyncio.run(
        uc.execute(
            user_id=user,
            course_slug="python-101",
            category_slug="programming",
            cursor="abc",
        )
    )

    call = reader.calls[0]
    assert call["course_slug"] == "python-101"
    assert call["category_slug"] == "programming"
    assert call["cursor"] == "abc"
    assert call["user_id"] == user
    assert call["limit"] == 20  # default

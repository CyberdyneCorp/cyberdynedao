"""Use-case tests for course recommendations, with fakes for the course
catalogue, the analytics dashboard, and a scripted LLM."""

from __future__ import annotations

import uuid
from uuid import UUID

from cyberdyne_backend.application.recommendations import RecommendCourses
from cyberdyne_backend.domain.ai_chat import ChatMessage, LLMResponse, ToolSchema
from cyberdyne_backend.domain.analytics import AnalyticsRepository, LearnerCounts
from cyberdyne_backend.domain.courses import (
    Course,
    CourseLevel,
    CourseRepository,
    new_course,
)


class FakeCourseRepo:
    def __init__(self, courses: list[Course]) -> None:
        self._courses = courses

    async def save(self, course: Course) -> None:  # pragma: no cover - unused
        raise NotImplementedError

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        raise NotImplementedError  # pragma: no cover - unused

    async def get_by_id(self, course_id: UUID) -> Course | None:
        raise NotImplementedError  # pragma: no cover - unused

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
    ) -> list[Course]:
        return list(self._courses)

    async def delete(self, course_id: UUID) -> None:  # pragma: no cover - unused
        raise NotImplementedError

    async def set_category(  # pragma: no cover - unused
        self, course_id: UUID, category_id: UUID | None
    ) -> None:
        raise NotImplementedError


class FakeAnalyticsRepo:
    def __init__(self, learner: LearnerCounts) -> None:
        self._learner = learner

    async def learner_counts(self, user_id: UUID) -> LearnerCounts:
        return self._learner

    async def platform_counts(self) -> object:  # pragma: no cover - unused
        raise NotImplementedError


class ScriptedLLM:
    def __init__(self) -> None:
        self.prompts: list[str] = []
        self.system_prompts: list[str] = []

    async def complete(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolSchema],
        system_prompt: str,
    ) -> LLMResponse:
        self.prompts.append(messages[-1].content)
        self.system_prompts.append(system_prompt)
        return LLMResponse(content="Great progress! Here is what to try next.")


def test_fakes_match_ports() -> None:
    assert isinstance(FakeCourseRepo([]), CourseRepository)
    assert isinstance(FakeAnalyticsRepo(LearnerCounts()), AnalyticsRepository)


def _course(title: str, level: str, *, mandatory: bool = False, sort_order: int = 0) -> Course:
    course = new_course(
        title=title, description="d", level=level, mandatory=mandatory, sort_order=sort_order
    )
    course.publish()
    return course


def _uc(courses: list[Course], learner: LearnerCounts, llm: ScriptedLLM) -> RecommendCourses:
    return RecommendCourses(
        courses=FakeCourseRepo(courses),
        analytics=FakeAnalyticsRepo(learner),
        llm=llm,
    )


class TestRecommendCourses:
    async def test_beginner_gets_beginner_first_and_one_llm_call(self) -> None:
        catalogue = [
            _course("Adv", "Advanced", sort_order=0),
            _course("Beg", "Beginner", sort_order=1),
            _course("Int", "Intermediate", sort_order=2),
        ]
        llm = ScriptedLLM()
        # Brand-new learner (no progress) -> target Beginner.
        result = await _uc(catalogue, LearnerCounts(), llm).execute(user_id=uuid.uuid4())

        assert [c.title for c in result.courses] == ["Beg", "Int", "Adv"]
        assert result.courses[0].reason == "Matches your current level"
        assert result.summary == "Great progress! Here is what to try next."
        assert len(llm.prompts) == 1
        assert llm.system_prompts[0].startswith("You are an encouraging learning advisor")

    async def test_max_courses_caps_the_shortlist(self) -> None:
        catalogue = [_course(f"C{i}", "Beginner", sort_order=i) for i in range(6)]
        llm = ScriptedLLM()
        uc = RecommendCourses(
            courses=FakeCourseRepo(catalogue),
            analytics=FakeAnalyticsRepo(LearnerCounts()),
            llm=llm,
            max_courses=2,
        )
        result = await uc.execute(user_id=uuid.uuid4())
        assert len(result.courses) == 2

    async def test_mandatory_course_ranks_first(self) -> None:
        catalogue = [
            _course("Beg", "Beginner", sort_order=0),
            _course("Mandatory Adv", "Advanced", mandatory=True, sort_order=1),
        ]
        result = await _uc(catalogue, LearnerCounts(), ScriptedLLM()).execute(user_id=uuid.uuid4())
        assert result.courses[0].title == "Mandatory Adv"
        assert result.courses[0].reason == "Required course"

    async def test_advanced_learner_targets_advanced(self) -> None:
        catalogue = [
            _course("Beg", "Beginner", sort_order=0),
            _course("Adv", "Advanced", sort_order=1),
        ]
        # A certificate earned -> target Advanced.
        learner = LearnerCounts(certificates=1)
        result = await _uc(catalogue, learner, ScriptedLLM()).execute(user_id=uuid.uuid4())
        assert result.courses[0].title == "Adv"
        assert result.courses[0].reason == "Matches your current level"
        # The beginner course is a refresher relative to the advanced target.
        assert result.courses[1].reason == "A solid refresher at a level you have covered"

    async def test_step_up_reason_for_higher_level(self) -> None:
        catalogue = [_course("Int", "Intermediate", sort_order=0)]
        result = await _uc(catalogue, LearnerCounts(), ScriptedLLM()).execute(user_id=uuid.uuid4())
        assert result.courses[0].reason == "A step up to stretch your skills"

    async def test_empty_catalogue_skips_llm(self) -> None:
        llm = ScriptedLLM()
        result = await _uc([], LearnerCounts(), llm).execute(user_id=uuid.uuid4())
        assert result.courses == []
        assert "no published courses" in result.summary.lower()
        assert llm.prompts == []  # no LLM call when there is nothing to recommend

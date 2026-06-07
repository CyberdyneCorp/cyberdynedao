"""Tests for the Academy course seed: it provisions the curated MATLAB and
Python courses, is idempotent, and never clobbers hand-authored lessons."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed import (
    ACADEMY_COURSES,
    SeedCourse,
    SeedLesson,
    seed_courses,
)
from cyberdyne_backend.domain.courses import Course, CourseNotFoundError, new_course, new_lesson


class FakeCourseRepo:
    def __init__(self, seed: list[Course] | None = None) -> None:
        self._by_slug: dict[str, Course] = {c.slug: c for c in (seed or [])}

    async def save(self, course: Course) -> None:
        self._by_slug[course.slug] = course

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        course = self._by_slug.get(slug)
        if course is None:
            raise CourseNotFoundError(slug)
        if not include_drafts and not course.is_visible_to_anonymous():
            raise CourseNotFoundError(slug)
        return course


class TestSeedCourses:
    async def test_creates_both_courses_published_with_lessons(self) -> None:
        repo = FakeCourseRepo()
        summary = await seed_courses(repo)

        assert len(summary) == 4
        matlab = await repo.get_by_slug("matlab-basics", include_drafts=True)
        python = await repo.get_by_slug("python-course", include_drafts=True)
        assert matlab.status.value == "published"
        assert python.status.value == "published"
        # MATLAB keeps the titles learners already see, with rich bodies now.
        titles = [lesson.title for lesson in matlab.lessons]
        assert "Welcome to MATLAB" in titles
        assert "Run your first script" in titles
        welcome = next(le for le in matlab.lessons if le.title == "Welcome to MATLAB")
        assert welcome.text_body and "Command Window" in welcome.text_body
        code = next(le for le in matlab.lessons if le.lesson_type.value == "code")
        assert code.text_body and "trace" in code.text_body
        # Python course aligns to the live titles + gains a runnable code lesson.
        py_titles = [le.title for le in python.lessons]
        assert "Welcome to Python" in py_titles
        assert "Run your first Python script" in py_titles
        py_code = next(le for le in python.lessons if le.lesson_type.value == "code")
        assert py_code.text_body and "scores" in py_code.text_body
        # Both courses carry a control-flow lesson covering if/for/while/
        # break/continue, with a Mermaid diagram.
        for course in (matlab, python):
            cf = next(le for le in course.lessons if le.title.startswith("Control flow"))
            body = cf.text_body or ""
            for kw in ("if", "for", "while", "break", "continue", "```mermaid"):
                assert kw in body, f"{course.slug} control-flow lesson missing {kw!r}"

    async def test_is_idempotent(self) -> None:
        repo = FakeCourseRepo()
        await seed_courses(repo)
        matlab_first = await repo.get_by_slug("matlab-basics", include_drafts=True)
        ids_first = [le.id for le in matlab_first.lessons]
        counts_first = len(matlab_first.lessons)

        summary = await seed_courses(repo)  # second run
        matlab_second = await repo.get_by_slug("matlab-basics", include_drafts=True)
        # No new lessons, same ids, same count — a pure no-op content-wise.
        assert [le.id for le in matlab_second.lessons] == ids_first
        assert len(matlab_second.lessons) == counts_first
        assert all("+0 lessons" in line for line in summary)

    async def test_updates_in_place_and_preserves_unmentioned_quiz(self) -> None:
        # Simulate the live course: an old Welcome text lesson + a hand-authored
        # quiz the seed never mentions.
        course = new_course(
            title="MATLAB Basics", description="old", level="Beginner", slug="matlab-basics"
        )
        welcome = new_lesson(
            course_id=course.id,
            title="Welcome to MATLAB",
            lesson_type="text",
            text_body="old body",
            sort_order=0,
        )
        quiz = new_lesson(
            course_id=course.id, title="Check your knowledge", lesson_type="quiz", sort_order=99
        )
        course.lessons.extend([welcome, quiz])
        repo = FakeCourseRepo([course])

        await seed_courses(repo)
        updated = await repo.get_by_slug("matlab-basics", include_drafts=True)

        # The existing Welcome lesson is updated in place (same id, new body).
        new_welcome = next(le for le in updated.lessons if le.title == "Welcome to MATLAB")
        assert new_welcome.id == welcome.id
        assert new_welcome.text_body != "old body"
        # The quiz the seed doesn't mention survives untouched.
        kept_quiz = next((le for le in updated.lessons if le.id == quiz.id), None)
        assert kept_quiz is not None
        assert kept_quiz.lesson_type.value == "quiz"
        # Description refreshed from the curated copy.
        assert updated.description != "old"

    async def test_skips_title_match_of_different_type(self) -> None:
        # A quiz titled like a curated text lesson must NOT be overwritten.
        spec = SeedCourse(
            slug="c1",
            title="C1",
            description="d",
            level="Beginner",
            lessons=(SeedLesson(title="Intro", lesson_type="text", text_body="new"),),
        )
        course = new_course(title="C1", description="d", level="Beginner", slug="c1")
        clash = new_lesson(course_id=course.id, title="Intro", lesson_type="quiz", sort_order=0)
        course.lessons.append(clash)
        repo = FakeCourseRepo([course])

        await seed_courses(repo, courses=(spec,))
        updated = await repo.get_by_slug("c1", include_drafts=True)
        intro_quiz = next(le for le in updated.lessons if le.id == clash.id)
        assert intro_quiz.lesson_type.value == "quiz"  # untouched
        assert intro_quiz.text_body is None

    def test_curated_content_covers_all_courses(self) -> None:
        slugs = {c.slug for c in ACADEMY_COURSES}
        assert slugs == {
            "matlab-basics",
            "python-course",
            "blockchain-basics",
            "blockchain-beyond-basics",
        }
        for course in ACADEMY_COURSES:
            assert course.lessons  # non-empty
            for lesson in course.lessons:
                if lesson.lesson_type in {"text", "code"}:
                    assert lesson.text_body, f"{course.slug}/{lesson.title} missing body"

    def test_blockchain_course_covers_idea_pow_and_bitcoin(self) -> None:
        bc = next(c for c in ACADEMY_COURSES if c.slug == "blockchain-basics")
        titles = " | ".join(le.title for le in bc.lessons)
        for needle in ("blockchain", "Hashing", "Proof of Work", "Mine a block", "Bitcoin"):
            assert needle in titles, f"missing lesson about {needle!r}"
        # The runnable miner is a Python code lesson with a working toy PoW.
        code = next(le for le in bc.lessons if le.lesson_type == "code")
        assert code.text_body and "toy_hash" in code.text_body and "nonce" in code.text_body
        # It must avoid hashlib (blocked in the restricted interpreter sandbox).
        assert "hashlib" not in (code.text_body or "")

    def test_advanced_blockchain_course_covers_requested_topics(self) -> None:
        bc = next(c for c in ACADEMY_COURSES if c.slug == "blockchain-beyond-basics")
        titles = " | ".join(le.title for le in bc.lessons)
        for needle in ("Bitcoin Script", "Consensus", "Cold wallets", "Ethereum", "Solidity"):
            assert needle in titles, f"missing lesson about {needle!r}"
        # The runnable Bitcoin Script toy avoids imports (restricted sandbox).
        code = next(le for le in bc.lessons if le.lesson_type == "code")
        assert code.text_body and "stack" in code.text_body and "import" not in code.text_body

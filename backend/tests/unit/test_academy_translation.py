"""Unit tests for the Academy translation pipeline.

The headline guard is *content preservation*: code fences, ```plot JSON,
and LaTeX math must survive translation byte-for-byte. Silent corruption
of those spans is the worst failure mode, so it gets the most coverage.
"""

from __future__ import annotations

import uuid

import pytest

from cyberdyne_backend.application.academy.translation import (
    _RICH_CHUNK_BUDGET,
    MarkdownAwareTranslator,
    TranslateAcademy,
    TranslationError,
    content_hash,
)
from cyberdyne_backend.domain.ai_chat import LLMResponse
from cyberdyne_backend.domain.courses import new_course, new_lesson
from cyberdyne_backend.domain.quizzes import build_question, new_quiz

pytestmark = pytest.mark.unit


class EchoLLM:
    """Returns the (masked) prompt unchanged, prefixed so we can prove the
    prose path ran. Placeholders survive, so restore round-trips."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        content = messages[-1].content
        self.calls.append(content)
        return LLMResponse(content=f"[T] {content}")


class PromptCaptureLLM:
    """Records the system prompt passed for each call."""

    def __init__(self) -> None:
        self.system_prompts: list[str] = []

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        self.system_prompts.append(system_prompt)
        return LLMResponse(content=messages[-1].content)


class DroppingLLM:
    """Strips every protected placeholder — simulates a model that mangles
    the sentinels, which must be caught rather than silently corrupt."""

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        content = messages[-1].content
        for token in ("[[KEEP0]]", "[[KEEP1]]", "[[KEEP2]]", "[[KEEP3]]"):
            content = content.replace(token, "")
        return LLMResponse(content=content)


LESSON_MD = """# Sets and functions

A **set** is a collection: $A = \\{1, 2, 3\\}$. The union is `A | B`.

```python
result = union(a, b)
```

```plot
{"expr": "x^2", "label": "f(x)"}
```

Display math:

$$y = A\\sin(\\omega x) + c$$
"""


async def test_preserves_code_math_and_plot_blocks() -> None:
    translator = MarkdownAwareTranslator(llm=EchoLLM())
    out = await translator.translate(LESSON_MD, language="pt-BR")
    # Every must-not-translate span comes back verbatim.
    assert "```python\nresult = union(a, b)\n```" in out
    assert '```plot\n{"expr": "x^2", "label": "f(x)"}\n```' in out
    assert "$$y = A\\sin(\\omega x) + c$$" in out
    assert "$A = \\{1, 2, 3\\}$" in out
    assert "`A | B`" in out
    # The prose path ran (marker present) and no sentinels leaked.
    assert "[T]" in out
    assert "[[KEEP" not in out


async def test_preserves_keep_marked_spans() -> None:
    # A language course wraps the target-language text in [[keep]]…[[/keep]];
    # it must survive translation byte-for-byte (markers included).
    translator = MarkdownAwareTranslator(llm=EchoLLM())
    src = "En inglés se dice [[keep]]the deployment pipeline[[/keep]] para esto."
    out = await translator.translate(src, language="es")
    assert "[[keep]]the deployment pipeline[[/keep]]" in out
    assert "[[KEEP" not in out  # internal sentinels fully restored


async def test_blank_text_is_returned_unchanged() -> None:
    translator = MarkdownAwareTranslator(llm=EchoLLM())
    assert await translator.translate("", language="fr") == ""
    assert await translator.translate(None, language="fr") == ""


async def test_plain_vs_rich_prompt_selection() -> None:
    # Plain (rich=False) must NOT invite the model to add Markdown structure —
    # that's what expanded a short title into a paragraph. Rich keeps it.
    llm = PromptCaptureLLM()
    translator = MarkdownAwareTranslator(llm=llm)
    await translator.translate("DAC architectures", language="fr", rich=False)
    await translator.translate("# Body\n\nprose", language="fr", rich=True)
    plain, rich = llm.system_prompts
    assert "do NOT add headings" in plain
    assert "Keep all Markdown structure" not in plain
    assert "Keep all Markdown structure" in rich


async def test_dropped_placeholder_raises_rather_than_corrupt() -> None:
    translator = MarkdownAwareTranslator(llm=DroppingLLM())
    with pytest.raises(TranslationError):
        await translator.translate(LESSON_MD, language="es")


# ── Chunking of long, code-heavy bodies (issue #235) ─────────────────


class SizeSensitiveDroppingLLM:
    """Models output truncation: a single oversized prompt comes back with
    every sentinel dropped (as a too-long generation loses its tail), while a
    prompt within ``limit`` echoes faithfully. Records the call count so a
    test can prove the body was split."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.calls = 0

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        content = messages[-1].content
        self.calls += 1
        if len(content) > self.limit:
            for token in [f"[[KEEP{i}]]" for i in range(500)]:
                content = content.replace(token, "")
        return LLMResponse(content=content)


def _long_code_heavy_body() -> str:
    # Many prose paragraphs, each carrying an inline-code span (a sentinel),
    # so the masked body comfortably exceeds the chunk budget — the shape that
    # made the real pt-BR jobs never finish.
    paragraphs = [
        f"## Section {i}\n\nThis paragraph {i} explains a concept and uses `value_{i}` inline."
        for i in range(200)
    ]
    return "\n\n".join(paragraphs)


async def test_long_rich_body_is_chunked_and_survives_truncation() -> None:
    body = _long_code_heavy_body()
    assert len(body) > _RICH_CHUNK_BUDGET  # guard: the body must actually be long
    llm = SizeSensitiveDroppingLLM(limit=_RICH_CHUNK_BUDGET)
    out = await MarkdownAwareTranslator(llm=llm).translate(body, language="pt-BR", rich=True)
    # Split into several bounded calls, none oversized → no sentinel dropped.
    assert llm.calls > 1
    assert "[[KEEP" not in out
    # Every protected span is restored verbatim, including the first and last.
    assert "`value_0`" in out
    assert "`value_199`" in out


async def test_short_body_takes_single_call_path() -> None:
    # Below the budget the body is translated in one call — unchanged behavior.
    llm = SizeSensitiveDroppingLLM(limit=_RICH_CHUNK_BUDGET)
    await MarkdownAwareTranslator(llm=llm).translate(LESSON_MD, language="pt-BR", rich=True)
    assert llm.calls == 1


async def test_failures_capture_field_context() -> None:
    # A dropped sentinel records WHICH field failed and why, so the worker can
    # surface it (issue #235) instead of a silent counter bump.
    repo = FakeTranslationRepo()
    orch = TranslateAcademy(translator=MarkdownAwareTranslator(llm=DroppingLLM()), repo=repo)
    course = new_course(title="T", description="d", level="Beginner", slug="t")
    lesson = new_lesson(
        course_id=course.id,
        title="Machine learning on omics",
        lesson_type="text",
        text_body="prose `code` and $x$ more",
    )
    course.lessons.append(lesson)

    stats = await orch.run(courses=[course], quizzes=[], languages=["pt-BR"])

    lesson_failures = [f for f in stats.failures if f.kind == "lesson"]
    assert len(lesson_failures) == 1
    failure = lesson_failures[0]
    assert failure.ref_id == lesson.id
    assert failure.language == "pt-BR"
    assert failure.label == "Machine learning on omics"
    assert "protected span" in failure.error


# ── TranslateAcademy orchestration ───────────────────────────────────


class FakeTranslationRepo:
    def __init__(self, *, course_h=None, lesson_h=None, q_h=None, o_h=None) -> None:
        self._course_h = course_h or {}
        self._lesson_h = lesson_h or {}
        self._q_h = q_h or {}
        self._o_h = o_h or {}
        self.courses: list[tuple] = []
        self.lessons: list[tuple] = []
        self.questions: list[tuple] = []
        self.options: list[tuple] = []

    async def course_hashes(self, language):
        return dict(self._course_h)

    async def lesson_hashes(self, language):
        return dict(self._lesson_h)

    async def question_hashes(self, language):
        return dict(self._q_h)

    async def option_hashes(self, language):
        return dict(self._o_h)

    async def upsert_course_translation(self, **kw):
        self.courses.append(kw)

    async def upsert_lesson_translation(self, **kw):
        self.lessons.append(kw)

    async def upsert_question_translation(self, **kw):
        self.questions.append(kw)

    async def upsert_option_translation(self, **kw):
        self.options.append(kw)


def _course_with_lesson():
    course = new_course(title="Algebra", description="Learn algebra", level="Beginner", slug="alg")
    lesson = new_lesson(
        course_id=course.id, title="Intro", lesson_type="text", text_body="Some prose."
    )
    course.lessons.append(lesson)
    return course


async def test_run_translates_every_field_and_persists() -> None:
    course = _course_with_lesson()
    quiz = new_quiz(
        lesson_id=uuid.uuid4(),
        questions=[
            build_question(prompt="Q?", explanation="because", options=[("a", True), ("b", False)])
        ],
        passing_score=70,
    )
    repo = FakeTranslationRepo()
    orch = TranslateAcademy(translator=MarkdownAwareTranslator(llm=EchoLLM()), repo=repo)

    stats = await orch.run(courses=[course], quizzes=[quiz], languages=["pt-BR"])

    assert len(repo.courses) == 1
    assert len(repo.lessons) == 1
    assert len(repo.questions) == 1
    assert len(repo.options) == 2  # two options
    assert stats.translated == 5  # course + lesson + question + 2 options
    assert stats.failed == 0


async def test_run_skips_unchanged_content_by_hash() -> None:
    course = _course_with_lesson()
    lesson = course.lessons[0]
    # Pre-seed hashes matching the current English source → all skipped.
    repo = FakeTranslationRepo(
        course_h={course.id: content_hash(course.title, course.description)},
        lesson_h={lesson.id: content_hash(lesson.title, lesson.text_body)},
    )
    orch = TranslateAcademy(translator=MarkdownAwareTranslator(llm=EchoLLM()), repo=repo)

    stats = await orch.run(courses=[course], quizzes=[], languages=["pt-BR"])

    assert repo.courses == []
    assert repo.lessons == []
    assert stats.translated == 0
    assert stats.skipped == 2


async def test_run_ignores_english() -> None:
    repo = FakeTranslationRepo()
    orch = TranslateAcademy(translator=MarkdownAwareTranslator(llm=EchoLLM()), repo=repo)
    stats = await orch.run(courses=[_course_with_lesson()], quizzes=[], languages=["en"])
    assert stats.translated == 0
    assert repo.courses == []


async def test_run_counts_failures_without_persisting() -> None:
    repo = FakeTranslationRepo()
    orch = TranslateAcademy(translator=MarkdownAwareTranslator(llm=DroppingLLM()), repo=repo)
    # text_body has protected spans the dropping LLM mangles → failure.
    course = new_course(title="T", description="d", level="Beginner", slug="t")
    course.lessons.append(
        new_lesson(
            course_id=course.id,
            title="L",
            lesson_type="text",
            text_body="prose `code` and $x$ more",
        )
    )
    stats = await orch.run(courses=[course], quizzes=[], languages=["fr"])
    # The course title/description translate fine (no protected spans); the
    # lesson body fails and is not persisted.
    assert stats.failed >= 1
    assert repo.lessons == []

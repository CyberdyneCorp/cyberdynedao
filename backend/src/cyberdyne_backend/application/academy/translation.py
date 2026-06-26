"""AI translation of Academy content (courses, lessons, quizzes).

Runs at seed time to populate the ``*_translations`` tables from the
English source. Two pieces:

* :class:`MarkdownAwareTranslator` — translates a single string while
  preserving everything that must stay verbatim (fenced code, ```plot /
  ```mermaid blocks, inline code, and LaTeX math). It masks those spans
  with sentinels, asks the LLM to translate only the prose around them,
  then restores them. If the model drops a sentinel it raises rather than
  return corrupted content, so the field is retried on the next run.
* :class:`TranslateAcademy` — orchestrates translating every translatable
  field for a set of languages, skipping anything whose English source
  hasn't changed since last time (``source_hash``).

The LLM is the existing :class:`ChatLLMPort` (OpenAI), reused exactly as
the quiz tutor feature does. ``TranslationRepository`` is the outbound
port this service needs; the SQLAlchemy adapter implements it.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from collections.abc import Awaitable
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import ChatLLMPort, ChatMessage, ChatRole
from cyberdyne_backend.domain.courses import Course, Lesson
from cyberdyne_backend.domain.quizzes import Question, QuestionOption, Quiz

# Languages the Academy content is offered in. ``en`` is the source of
# truth (base rows); the rest live in the translation tables. Canonical
# home for the supported set — the inbound API locale resolver imports it.
SUPPORTED_LANGUAGES: tuple[str, ...] = ("en", "pt-BR", "es", "fr")

# Human-readable language names for the translation prompt.
LANGUAGE_NAMES: dict[str, str] = {
    "pt-BR": "Brazilian Portuguese",
    "es": "Spanish",
    "fr": "French",
}


def content_hash(*parts: str | None) -> str:
    """Stable hash of an English source field (or fields). Used to skip
    re-translating content that hasn't changed."""
    joined = "\x00".join(p or "" for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


class TranslationError(RuntimeError):
    """Raised when a translation can't be trusted (e.g. the model dropped a
    protected placeholder). The caller skips the field so it retries later."""


# Spans that must survive translation untouched, matched in priority order
# (fenced blocks before inline). Each becomes a sentinel the model is told
# to keep verbatim.
_PROTECT_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Author-marked do-not-translate spans — e.g. the target-language text in a
    # *language* course ([[keep]]the deployment pipeline[[/keep]]). Masked first,
    # whole span incl. markers, so its content survives untouched; renderers
    # strip the [[keep]]…[[/keep]] markers when displaying.
    re.compile(r"\[\[keep\]\].*?\[\[/keep\]\]", re.DOTALL),
    re.compile(r"```.*?```", re.DOTALL),  # fenced code / plot / mermaid
    re.compile(r"\$\$.*?\$\$", re.DOTALL),  # block LaTeX
    re.compile(r"`[^`\n]+`"),  # inline code
    re.compile(r"\$[^$\n]+\$"),  # inline LaTeX
)


# Max characters of masked Markdown to send in a single rich-body LLM call.
# A long, code-heavy lesson body otherwise yields an output the model
# truncates, silently dropping the trailing [[KEEPn]] sentinels — the
# deterministic failure behind a course that never reaches 100% translated
# (issue #235). Splitting the body into bounded chunks keeps each call's
# output well within limits and lowers the sentinel count per call.
_RICH_CHUNK_BUDGET = 6000


def _sentinel(index: int) -> str:
    # Bracketed, upper-case, no spaces — survives translation reliably and is
    # easy to validate. The model is explicitly told to preserve these.
    return f"[[KEEP{index}]]"


def _protect(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}
    masked = text
    for pattern in _PROTECT_PATTERNS:

        def repl(match: re.Match[str]) -> str:
            token = _sentinel(len(tokens))
            tokens[token] = match.group(0)
            return token

        masked = pattern.sub(repl, masked)
    return masked, tokens


def _restore(text: str, tokens: dict[str, str]) -> str:
    restored = text
    for token, original in tokens.items():
        restored = restored.replace(token, original)
    return restored


def _split_chunks(masked: str, budget: int) -> list[str]:
    """Split masked Markdown into chunks no larger than ``budget`` characters,
    breaking only on blank-line (paragraph) boundaries so a sentence — or a
    ``[[KEEPn]]`` sentinel — is never cut in half. A single paragraph larger
    than the budget is kept whole (we never split mid-paragraph). Chunks
    rejoin with ``\\n\\n``."""
    chunks: list[str] = []
    current = ""
    for para in masked.split("\n\n"):
        candidate = f"{current}\n\n{para}" if current else para
        if current and len(candidate) > budget:
            chunks.append(current)
            current = para
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


# Rich prompt for full Markdown bodies (lesson content): preserve structure.
_SYSTEM_PROMPT_RICH = (
    "You are a professional translator localizing technical course material for "
    "Cyberdyne Academy into {language}. Translate ONLY the natural-language prose. "
    "Rules:\n"
    "- Preserve every placeholder of the form [[KEEPn]] EXACTLY as written — never "
    "translate, reorder, renumber, or remove them.\n"
    "- Keep all Markdown structure (headings #, lists, tables, links) intact.\n"
    "- Do NOT translate code, mathematical notation, JSON keys, URLs, or product "
    "names (MATLAB, Python, Cyberdyne, etc.).\n"
    "- Return only the translated text, with no preamble or commentary."
)

# Plain prompt for short standalone fields (titles, descriptions, quiz text):
# translate in place WITHOUT inventing headings or padding the length — the
# rich prompt's "keep Markdown structure" line tempts the model to expand a
# bare title into a paragraph.
_SYSTEM_PROMPT_PLAIN = (
    "You are a professional translator. Translate the text into {language}.\n"
    "Rules:\n"
    "- Return ONLY the translated text — no preamble, quotes, or commentary.\n"
    "- Keep it roughly the same length and shape; do NOT add headings, lists, or "
    "extra sentences that were not in the original.\n"
    "- Preserve every placeholder of the form [[KEEPn]] EXACTLY.\n"
    "- Do NOT translate code, mathematical notation, URLs, or product names "
    "(MATLAB, Python, Cyberdyne, etc.)."
)


@dataclass(slots=True)
class MarkdownAwareTranslator:
    """Translates one string to a target language, preserving code/math."""

    llm: ChatLLMPort

    async def translate(self, text: str | None, *, language: str, rich: bool = True) -> str:
        """Translate ``text`` into ``language``.

        ``rich=True`` (default) is for full Markdown bodies; ``rich=False`` for
        short standalone fields (titles, descriptions, quiz prompts/options)
        where the model must not invent structure or pad the length.
        """
        if not text or not text.strip():
            return text or ""
        masked, tokens = _protect(text)
        language_name = LANGUAGE_NAMES.get(language, language)
        system_prompt = (_SYSTEM_PROMPT_RICH if rich else _SYSTEM_PROMPT_PLAIN).format(
            language=language_name
        )
        # Long rich bodies are translated in bounded chunks so the model never
        # truncates its output and drops trailing sentinels (issue #235). Short
        # fields and short bodies take the single-call path unchanged.
        if rich and len(masked) > _RICH_CHUNK_BUDGET:
            translated_segments: list[str] = []
            for segment in _split_chunks(masked, _RICH_CHUNK_BUDGET):
                translated_segments.append(
                    await self._complete(
                        segment,
                        expected={tok for tok in tokens if tok in segment},
                        system_prompt=system_prompt,
                        language=language,
                    )
                )
            out = "\n\n".join(translated_segments)
        else:
            out = await self._complete(
                masked, expected=set(tokens), system_prompt=system_prompt, language=language
            )
        return _restore(out, tokens)

    async def _complete(
        self, masked: str, *, expected: set[str], system_prompt: str, language: str
    ) -> str:
        """One LLM call over ``masked``, validating that every sentinel in
        ``expected`` survived. Raises :class:`TranslationError` on a dropped
        placeholder — better to retry than to silently lose a code/math
        block."""
        message = ChatMessage(
            id=uuid.uuid4(),
            session_id=uuid.uuid4(),
            role=ChatRole.USER,
            content=masked,
        )
        response = await self.llm.complete(
            messages=[message],
            tools=[],
            system_prompt=system_prompt,
        )
        out = response.content
        missing = [tok for tok in expected if tok not in out]
        if missing:
            raise TranslationError(
                f"translation dropped {len(missing)} protected span(s) for {language}"
            )
        return out


@runtime_checkable
class TranslationRepository(Protocol):
    """Outbound port: stores Academy translations + reports current hashes.

    Hash maps are returned per-language so the orchestrator can skip
    unchanged content in one round-trip per table.
    """

    async def course_languages(self, course_id: UUID) -> list[str]:
        """Non-English languages this course has a translation row for."""
        ...

    async def translated_lesson_counts(self, course_id: UUID) -> dict[str, int]:
        """Per-language count of this course's lessons that have a
        translation row. Lets a caller verify a language is *fully*
        translated (count == number of lessons) rather than relying on the
        presence of a course-level row alone."""
        ...

    async def translated_question_counts(self, course_id: UUID) -> dict[str, int]:
        """Per-language count of this course's quiz questions that have a
        translation row. A course translated before quiz support (or by an
        interrupted job) has its lessons translated but its quizzes still in
        English, so 'fully translated' must check questions too."""
        ...

    async def course_hashes(self, language: str) -> dict[UUID, str]: ...
    async def lesson_hashes(self, language: str) -> dict[UUID, str]: ...
    async def question_hashes(self, language: str) -> dict[UUID, str]: ...
    async def option_hashes(self, language: str) -> dict[UUID, str]: ...

    async def upsert_course_translation(
        self, *, course_id: UUID, language: str, title: str, description: str, source_hash: str
    ) -> None: ...

    async def upsert_lesson_translation(
        self,
        *,
        lesson_id: UUID,
        language: str,
        title: str,
        text_body: str | None,
        source_hash: str,
    ) -> None: ...

    async def upsert_question_translation(
        self,
        *,
        question_id: UUID,
        language: str,
        prompt: str,
        explanation: str,
        source_hash: str,
    ) -> None: ...

    async def upsert_option_translation(
        self, *, option_id: UUID, language: str, text: str, source_hash: str
    ) -> None: ...


@dataclass(slots=True)
class TranslationFailure:
    """A single field that failed to translate, captured so the worker can
    record *which* lesson/question broke and why — making the failure
    diagnosable through the job's ``error`` instead of only the logs."""

    kind: str  # "course" | "lesson" | "question" | "option"
    ref_id: UUID
    language: str
    label: str
    error: str


def _label(text: str, *, limit: int = 80) -> str:
    """A short, single-line identifier for a translated field (its title or
    the head of its prompt) for failure messages."""
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else f"{flat[:limit]}…"


@dataclass(slots=True)
class TranslationStats:
    translated: int = 0
    skipped: int = 0
    failed: int = 0
    failures: list[TranslationFailure] = field(default_factory=list)

    def merge(self, other: TranslationStats) -> None:
        self.translated += other.translated
        self.skipped += other.skipped
        self.failed += other.failed
        self.failures.extend(other.failures)


@dataclass(slots=True)
class TranslateAcademy:
    """Translate every translatable field of the given courses + quizzes
    into each target language, skipping unchanged content (by source hash).
    A field whose translation fails is left untranslated and retried next
    run (English fallback serves it meanwhile)."""

    translator: MarkdownAwareTranslator
    repo: TranslationRepository

    async def run(
        self, *, courses: list[Course], quizzes: list[Quiz], languages: list[str]
    ) -> TranslationStats:
        stats = TranslationStats()
        for language in languages:
            if language == "en":
                continue
            stats.merge(await self._run_language(courses, quizzes, language))
        return stats

    async def _run_language(
        self, courses: list[Course], quizzes: list[Quiz], language: str
    ) -> TranslationStats:
        stats = TranslationStats()
        course_hashes = await self.repo.course_hashes(language)
        lesson_hashes = await self.repo.lesson_hashes(language)
        question_hashes = await self.repo.question_hashes(language)
        option_hashes = await self.repo.option_hashes(language)

        for course in courses:
            src = content_hash(course.title, course.description)
            if course_hashes.get(course.id) != src:
                await self._guard(
                    stats,
                    kind="course",
                    ref_id=course.id,
                    language=language,
                    label=_label(course.title),
                    coro=self._translate_course(course, language, src),
                )
            else:
                stats.skipped += 1
            for lesson in course.lessons:
                lsrc = content_hash(lesson.title, lesson.text_body)
                if lesson_hashes.get(lesson.id) != lsrc:
                    await self._guard(
                        stats,
                        kind="lesson",
                        ref_id=lesson.id,
                        language=language,
                        label=_label(lesson.title),
                        coro=self._translate_lesson(lesson, language, lsrc),
                    )
                else:
                    stats.skipped += 1

        for quiz in quizzes:
            for question in quiz.questions:
                qsrc = content_hash(question.prompt, question.explanation)
                if question_hashes.get(question.id) != qsrc:
                    await self._guard(
                        stats,
                        kind="question",
                        ref_id=question.id,
                        language=language,
                        label=_label(question.prompt),
                        coro=self._translate_question(question, language, qsrc),
                    )
                else:
                    stats.skipped += 1
                for option in question.options:
                    osrc = content_hash(option.text)
                    if option_hashes.get(option.id) != osrc:
                        await self._guard(
                            stats,
                            kind="option",
                            ref_id=option.id,
                            language=language,
                            label=_label(option.text),
                            coro=self._translate_option(option, language, osrc),
                        )
                    else:
                        stats.skipped += 1
        return stats

    async def _guard(
        self,
        stats: TranslationStats,
        *,
        kind: str,
        ref_id: UUID,
        language: str,
        label: str,
        coro: Awaitable[None],
    ) -> None:
        try:
            await coro
            stats.translated += 1
        except TranslationError as exc:
            stats.failed += 1
            stats.failures.append(
                TranslationFailure(
                    kind=kind,
                    ref_id=ref_id,
                    language=language,
                    label=label,
                    error=str(exc),
                )
            )

    async def _translate_course(self, course: Course, language: str, src: str) -> None:
        title = await self.translator.translate(course.title, language=language, rich=False)
        description = await self.translator.translate(
            course.description, language=language, rich=False
        )
        await self.repo.upsert_course_translation(
            course_id=course.id,
            language=language,
            title=title,
            description=description,
            source_hash=src,
        )

    async def _translate_lesson(self, lesson: Lesson, language: str, src: str) -> None:
        title = await self.translator.translate(lesson.title, language=language, rich=False)
        text_body = (
            await self.translator.translate(lesson.text_body, language=language, rich=True)
            if lesson.text_body
            else lesson.text_body
        )
        await self.repo.upsert_lesson_translation(
            lesson_id=lesson.id,
            language=language,
            title=title,
            text_body=text_body,
            source_hash=src,
        )

    async def _translate_question(self, question: Question, language: str, src: str) -> None:
        prompt = await self.translator.translate(question.prompt, language=language, rich=False)
        explanation = await self.translator.translate(
            question.explanation, language=language, rich=False
        )
        await self.repo.upsert_question_translation(
            question_id=question.id,
            language=language,
            prompt=prompt,
            explanation=explanation,
            source_hash=src,
        )

    async def _translate_option(self, option: QuestionOption, language: str, src: str) -> None:
        text = await self.translator.translate(option.text, language=language, rich=False)
        await self.repo.upsert_option_translation(
            option_id=option.id,
            language=language,
            text=text,
            source_hash=src,
        )


__all__ = [
    "MarkdownAwareTranslator",
    "TranslateAcademy",
    "TranslationError",
    "TranslationFailure",
    "TranslationRepository",
    "TranslationStats",
    "content_hash",
]

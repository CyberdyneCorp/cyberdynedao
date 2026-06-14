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
from dataclasses import dataclass
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
    re.compile(r"```.*?```", re.DOTALL),  # fenced code / plot / mermaid
    re.compile(r"\$\$.*?\$\$", re.DOTALL),  # block LaTeX
    re.compile(r"`[^`\n]+`"),  # inline code
    re.compile(r"\$[^$\n]+\$"),  # inline LaTeX
)


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
        message = ChatMessage(
            id=uuid.uuid4(),
            session_id=uuid.uuid4(),
            role=ChatRole.USER,
            content=masked,
        )
        language_name = LANGUAGE_NAMES.get(language, language)
        system_prompt = (_SYSTEM_PROMPT_RICH if rich else _SYSTEM_PROMPT_PLAIN).format(
            language=language_name
        )
        response = await self.llm.complete(
            messages=[message],
            tools=[],
            system_prompt=system_prompt,
        )
        out = response.content
        # Guard against placeholder corruption — better to retry than to
        # silently lose a code/math block.
        missing = [tok for tok in tokens if tok not in out]
        if missing:
            raise TranslationError(
                f"translation dropped {len(missing)} protected span(s) for {language}"
            )
        return _restore(out, tokens)


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
class TranslationStats:
    translated: int = 0
    skipped: int = 0
    failed: int = 0

    def merge(self, other: TranslationStats) -> None:
        self.translated += other.translated
        self.skipped += other.skipped
        self.failed += other.failed


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
                    self._translate_course(course, language, src),
                )
            else:
                stats.skipped += 1
            for lesson in course.lessons:
                lsrc = content_hash(lesson.title, lesson.text_body)
                if lesson_hashes.get(lesson.id) != lsrc:
                    await self._guard(
                        stats,
                        self._translate_lesson(lesson, language, lsrc),
                    )
                else:
                    stats.skipped += 1

        for quiz in quizzes:
            for question in quiz.questions:
                qsrc = content_hash(question.prompt, question.explanation)
                if question_hashes.get(question.id) != qsrc:
                    await self._guard(
                        stats,
                        self._translate_question(question, language, qsrc),
                    )
                else:
                    stats.skipped += 1
                for option in question.options:
                    osrc = content_hash(option.text)
                    if option_hashes.get(option.id) != osrc:
                        await self._guard(
                            stats,
                            self._translate_option(option, language, osrc),
                        )
                    else:
                        stats.skipped += 1
        return stats

    async def _guard(self, stats: TranslationStats, coro: Awaitable[None]) -> None:
        try:
            await coro
            stats.translated += 1
        except TranslationError:
            stats.failed += 1

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
    "TranslationRepository",
    "TranslationStats",
    "content_hash",
]

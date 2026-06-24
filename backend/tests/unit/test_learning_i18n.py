"""Unit tests for the learning i18n merge helper + language validation."""

from __future__ import annotations

import pytest

from cyberdyne_backend.application.learning import UpsertModuleTranslation
from cyberdyne_backend.domain.learning import (
    LearningContentValidationError,
    LearningModule,
    LearningTranslation,
    with_translation,
)

_M = LearningModule(
    slug="m1",
    title="Digital Logic",
    category="Engineering",
    description="Gates.",
    level="Beginner",
    duration="3 courses",
    icon="🔢",
    topics=(),
    course_slugs=(),
)


def test_with_translation_replaces_per_field() -> None:
    out = with_translation(_M, title="Lógica Digital", description="Puertas.")
    assert (out.title, out.description) == ("Lógica Digital", "Puertas.")
    assert out.slug == "m1" and out.level == "Beginner"  # other fields intact


def test_with_translation_per_field_fallback() -> None:
    # Empty translated value keeps the English base value (per field).
    title_only = with_translation(_M, title="Lógica Digital", description="")
    assert title_only.title == "Lógica Digital"
    assert title_only.description == "Gates."  # fallback
    assert with_translation(_M, title=None, description=None) is _M  # no-op


class _FakeRepo:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def upsert_module_translation(self, slug, *, language, title, description):
        self.calls.append((slug, language))
        return LearningTranslation(language, title, description)


@pytest.mark.asyncio
async def test_upsert_translation_rejects_english_and_unsupported() -> None:
    uc = UpsertModuleTranslation(repo=_FakeRepo())
    for bad in ("en", "de", "zh"):
        with pytest.raises(LearningContentValidationError):
            await uc.execute(slug="m1", language=bad, title="x", description="y")


@pytest.mark.asyncio
async def test_upsert_translation_accepts_supported() -> None:
    repo = _FakeRepo()
    tr = await UpsertModuleTranslation(repo=repo).execute(
        slug="m1", language="es", title="Lógica", description="Puertas"
    )
    assert tr.language == "es" and repo.calls == [("m1", "es")]

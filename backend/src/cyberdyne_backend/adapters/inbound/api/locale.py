"""Request locale resolution for the public Academy endpoints.

Course/lesson/quiz content is stored per-language with English fallback
(see the ``*_translations`` tables). Endpoints that serve learner-facing
content use :func:`resolve_locale` to pick the language: an explicit
``?lang=`` query wins, then the ``Accept-Language`` header, otherwise
English. Unknown tags fall back to English.
"""

from __future__ import annotations

from fastapi import Query, Request

#: Languages the Academy content is translated into. ``en`` is the source
#: of truth (base rows); the rest live in the translation tables.
SUPPORTED_LANGUAGES: tuple[str, ...] = ("en", "pt-BR", "es", "fr")
DEFAULT_LANGUAGE = "en"

# Lower-cased lookup so matching is case-insensitive (browsers send
# ``pt-BR`` / ``pt-br`` / ``PT`` interchangeably).
_BY_LOWER = {lang.lower(): lang for lang in SUPPORTED_LANGUAGES}
_BY_PRIMARY = {lang.lower().split("-")[0]: lang for lang in SUPPORTED_LANGUAGES}


def match_language(tag: str | None) -> str | None:
    """Best-effort match of a single BCP-47 tag to a supported language.

    Exact (case-insensitive) match wins; otherwise the primary subtag is
    compared so ``pt-PT`` still resolves to ``pt-BR``. Returns ``None`` when
    nothing matches.
    """
    if not tag:
        return None
    cleaned = tag.strip().lower()
    if cleaned in _BY_LOWER:
        return _BY_LOWER[cleaned]
    primary = cleaned.split("-")[0]
    return _BY_PRIMARY.get(primary)


def _from_accept_language(header: str | None) -> str | None:
    """Pick the first supported language from an ``Accept-Language`` header,
    honouring its ``q=`` priority order."""
    if not header:
        return None
    # e.g. "pt-BR,pt;q=0.9,en;q=0.8" — sort by q descending, default q=1.
    parsed: list[tuple[float, str]] = []
    for part in header.split(","):
        token = part.strip()
        if not token:
            continue
        tag, _, params = token.partition(";")
        q = 1.0
        if params.startswith("q="):
            try:
                q = float(params[2:])
            except ValueError:
                q = 0.0
        parsed.append((q, tag.strip()))
    for _q, tag in sorted(parsed, key=lambda p: p[0], reverse=True):
        matched = match_language(tag)
        if matched is not None:
            return matched
    return None


def resolve_locale(
    request: Request,
    lang: str | None = Query(default=None, description="Override content language (BCP-47)."),
) -> str:
    """FastAPI dependency: resolve the content language for this request."""
    return (
        match_language(lang)
        or _from_accept_language(request.headers.get("accept-language"))
        or DEFAULT_LANGUAGE
    )

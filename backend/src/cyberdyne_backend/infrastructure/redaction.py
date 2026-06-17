"""PII redaction helpers for log lines.

Lead-capture and license-delivery flow learner emails through stdlib
logging; mask them so server logs don't accumulate raw PII (issue #7).
"""

from __future__ import annotations


def redact_email(value: str | None) -> str:
    """Mask the local part of an email for logging, preserving the domain
    so logs stay useful for debugging without storing the full address.

    ``alice@example.com`` -> ``a***@example.com``;
    a single-char local part is fully masked (``a@x`` -> ``*@x``);
    a value with no ``@`` is treated as a bare token and middle-masked.
    """
    if not value:
        return ""
    if "@" not in value:
        return _mask_token(value)
    local, _, domain = value.partition("@")
    if not local:
        return f"@{domain}"
    if len(local) == 1:
        return f"*@{domain}"
    return f"{local[0]}***@{domain}"


def _mask_token(value: str) -> str:
    """Keep the first character, mask the rest — for non-email tokens."""
    if len(value) <= 1:
        return "*"
    return f"{value[0]}***"

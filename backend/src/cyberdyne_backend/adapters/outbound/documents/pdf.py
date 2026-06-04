"""ReportLab markdown/plain-text → PDF renderer for the agent's
``create_document`` tool.

Deliberately small: it understands the common markdown the agent emits
(ATX headings, ``-``/``*`` bullets, ``1.`` ordered items, blank-line
paragraphs, and inline ``**bold**`` / ``*italic*`` / ``` `code` ```). It is
NOT a full markdown engine — anything it doesn't recognise renders as a
plain paragraph, which is fine for a downloadable summary.
"""

from __future__ import annotations

import re
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_BULLET = re.compile(r"^\s*[-*]\s+(.*)$")
_ORDERED = re.compile(r"^\s*\d+[.)]\s+(.*)$")


def _inline(text: str) -> str:
    """Escape for ReportLab's mini-HTML, then re-apply bold/italic/code."""
    out = escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", out)
    out = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', out)
    return out


class ReportlabDocumentRenderer:
    """Implements ``DocumentRendererPort.render_pdf``."""

    def render_pdf(self, *, content: str, title: str | None = None) -> bytes:
        styles = getSampleStyleSheet()
        body = ParagraphStyle(
            "CdBody", parent=styles["BodyText"], fontSize=11, leading=15, alignment=TA_LEFT
        )
        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            title=title or "Document",
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )
        flowables: list[object] = []
        if title:
            flowables.append(Paragraph(_inline(title), styles["Title"]))
            flowables.append(Spacer(1, 0.4 * cm))

        # Group consecutive bullet/ordered lines into a single list flowable.
        pending_items: list[ListItem] = []
        pending_ordered = False

        def flush_list() -> None:
            nonlocal pending_items, pending_ordered
            if pending_items:
                flowables.append(
                    ListFlowable(
                        pending_items,
                        bulletType="1" if pending_ordered else "bullet",
                        leftIndent=18,
                    )
                )
                pending_items = []

        for raw in content.splitlines():
            line = raw.rstrip()
            heading = _HEADING.match(line)
            bullet = _BULLET.match(line)
            ordered = _ORDERED.match(line)
            if heading:
                flush_list()
                level = min(len(heading.group(1)), 4)
                flowables.append(Paragraph(_inline(heading.group(2)), styles[f"Heading{level}"]))
            elif bullet or ordered:
                is_ordered = ordered is not None
                if pending_items and pending_ordered != is_ordered:
                    flush_list()
                pending_ordered = is_ordered
                text = (ordered or bullet).group(1)  # type: ignore[union-attr]
                pending_items.append(ListItem(Paragraph(_inline(text), body)))
            elif line.strip() == "":
                flush_list()
                flowables.append(Spacer(1, 0.2 * cm))
            else:
                flush_list()
                flowables.append(Paragraph(_inline(line), body))
        flush_list()

        if not flowables:
            flowables.append(Paragraph(" ", body))
        doc.build(flowables)
        return buf.getvalue()

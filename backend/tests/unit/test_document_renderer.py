"""Smoke tests for the ReportLab markdown→PDF renderer."""

from __future__ import annotations

from cyberdyne_backend.adapters.outbound.documents.pdf import ReportlabDocumentRenderer


class TestReportlabDocumentRenderer:
    def test_renders_a_real_pdf(self) -> None:
        pdf = ReportlabDocumentRenderer().render_pdf(
            content="# Heading\n\nSome **bold** text.\n\n- one\n- two\n\n1. first\n2. second",
            title="Meeting Summary",
        )
        assert pdf.startswith(b"%PDF")
        assert len(pdf) > 500  # a non-trivial document

    def test_empty_content_still_produces_a_pdf(self) -> None:
        pdf = ReportlabDocumentRenderer().render_pdf(content="")
        assert pdf.startswith(b"%PDF")

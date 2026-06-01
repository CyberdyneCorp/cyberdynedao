"""ReportLab implementation of ``CertificatePdfRenderer``.

Renders a single-page A4 landscape certificate of completion. Pure
in-memory render → bytes; no temp files. Kept deliberately plain (title,
recipient, path, date, verification id + URL) so it reads well without a
design system.
"""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from cyberdyne_backend.domain.learning import Certificate

_ACCENT = HexColor("#3B82F6")
_INK = HexColor("#0F172A")
_MUTED = HexColor("#64748B")


class ReportlabCertificateRenderer:
    def render(self, *, certificate: Certificate, path_title: str, verify_url: str) -> bytes:
        buffer = BytesIO()
        width, height = landscape(A4)
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))

        # Border.
        pdf.setStrokeColor(_ACCENT)
        pdf.setLineWidth(3)
        pdf.rect(12 * mm, 12 * mm, width - 24 * mm, height - 24 * mm)

        center = width / 2

        pdf.setFillColor(_MUTED)
        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(center, height - 45 * mm, "CYBERDYNE ACADEMY")

        pdf.setFillColor(_INK)
        pdf.setFont("Helvetica-Bold", 34)
        pdf.drawCentredString(center, height - 70 * mm, "Certificate of Completion")

        pdf.setFillColor(_MUTED)
        pdf.setFont("Helvetica", 16)
        pdf.drawCentredString(center, height - 92 * mm, "This certifies that learner")

        pdf.setFillColor(_INK)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawCentredString(center, height - 106 * mm, str(certificate.user_id))

        pdf.setFillColor(_MUTED)
        pdf.setFont("Helvetica", 16)
        pdf.drawCentredString(center, height - 124 * mm, "has successfully completed")

        pdf.setFillColor(_ACCENT)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(center, height - 140 * mm, path_title)

        pdf.setFillColor(_MUTED)
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(
            center,
            height - 158 * mm,
            f"Issued {certificate.issued_at.date().isoformat()}",
        )

        # Footer: verification reference.
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(center, 22 * mm, f"Certificate ID: {certificate.id}")
        pdf.drawCentredString(center, 17 * mm, f"Verify at: {verify_url}")

        pdf.showPage()
        pdf.save()
        return buffer.getvalue()

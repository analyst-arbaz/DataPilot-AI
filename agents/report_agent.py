import os
import re
import tempfile
import logging

logger = logging.getLogger(__name__)


def _sanitize(text):
    replacements = {
        "\u2014": "-",  "\u2013": "-",  "\u2012": "-",  "\u2015": "-",
        "\u2019": "'",  "\u2018": "'",  "\u201c": '"',  "\u201d": '"',
        "\u2026": "...","\u2022": "-",  "\u25cf": "-",
        "\u2605": "*",  "\u2713": "v",  "\u2714": "v",
        "\u00b0": " deg", "\u20b9": "Rs", "\u20ac": "EUR",
        "\u00a3": "GBP",  "\u00a9": "(c)", "\u00e9": "e",
        "\u00e0": "a",    "\u00fc": "u",
    }
    for ch, repl in replacements.items():
        text = text.replace(ch, repl)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def _strip_markdown(text):
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*",     r"\1", text)
    text = re.sub(r"`(.*?)`",       r"\1", text)
    return text


def create_pdf(content, filename):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

    path = os.path.join(tempfile.gettempdir(), filename)

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm,  bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=18,
        textColor=colors.HexColor("#0f3460"),
        spaceAfter=6,
    )
    heading_style = ParagraphStyle(
        "heading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#00A4EF"),
        spaceBefore=10,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=4,
    )

    body = _sanitize(_strip_markdown(content))
    story = []

    story.append(Paragraph("DataPilot AI - Business Analysis Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Spacer(1, 8*mm))

    for line in body.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 3*mm))
        elif line.endswith(":") or line.isupper():
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    logger.info(f"PDF saved: {path}")
    return path
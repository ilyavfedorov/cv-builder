#!/usr/bin/env python3
"""Build Tanya's career research PDF from the canonical Markdown report."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tanya" / "report-source.md"
OUTPUT = ROOT / "output" / "pdf" / "tanya-calm-high-value-career-strategy.pdf"

NAVY = colors.HexColor("#173F5F")
TEAL = colors.HexColor("#147D7E")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#52606D")
PALE = colors.HexColor("#EAF3F3")
LINE = colors.HexColor("#C9D6DE")


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<link href="\2" color="#147D7E"><u>\1</u></link>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)
    return escaped


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=NAVY, alignment=TA_LEFT, spaceAfter=8),
        "subtitle": ParagraphStyle("Subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=10, leading=15, textColor=MUTED, spaceAfter=5),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=13, spaceAfter=7, keepWithNext=True),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=TEAL, spaceBefore=10, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.6, textColor=INK, spaceAfter=6),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.1, leading=13.1, textColor=INK, leftIndent=2, spaceAfter=2),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=MUTED),
        "table_head": ParagraphStyle("TableHead", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=colors.white, alignment=TA_CENTER),
        "table": ParagraphStyle("Table", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=INK),
    }


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 9 * mm, "Tanya Poletaeva | Calm, high-value career strategy | 30 Aug 2026")
    canvas.drawRightString(width - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def parse_markdown(text: str):
    s = styles()
    story = []
    lines = text.splitlines()
    i = 0
    first_heading = True
    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            if first_heading:
                story.extend([Spacer(1, 18 * mm), Paragraph(inline(line[2:]), s["title"]), HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10)])
                first_heading = False
            else:
                story.extend([CondPageBreak(35 * mm), Paragraph(inline(line[2:]), s["h1"])])
            i += 1
            continue
        if line.startswith("## "):
            story.extend([CondPageBreak(28 * mm), Paragraph(inline(line[3:]), s["h1"])])
            i += 1
            continue
        if line.startswith("### "):
            story.extend([CondPageBreak(21 * mm), Paragraph(inline(line[4:]), s["h2"])])
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            rendered = []
            for r, row in enumerate(rows):
                rendered.append([Paragraph(inline(c), s["table_head"] if r == 0 else s["table"]) for c in row])
            table = Table(rendered, colWidths=[48 * mm, 58 * mm, 58 * mm], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 7)])
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(ListItem(Paragraph(inline(lines[i].strip()[2:]), s["bullet"]), leftIndent=10))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet", start="circle", leftIndent=15, bulletFontName="Helvetica", bulletFontSize=6, bulletColor=TEAL, spaceAfter=5))
            continue
        if re.match(r"\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i].strip()):
                content = re.sub(r"^\d+\. ", "", lines[i].strip())
                items.append(ListItem(Paragraph(inline(content), s["bullet"]), leftIndent=12))
                i += 1
            story.append(ListFlowable(items, bulletType="1", leftIndent=18, bulletFontName="Helvetica-Bold", bulletFontSize=8, bulletColor=NAVY, spaceAfter=5))
            continue
        if line.startswith("**") and line.endswith("  "):
            story.append(Paragraph(inline(line[:-2]), s["subtitle"]))
            i += 1
            continue
        paragraph = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith(("#", "- ", "|")) or re.match(r"\d+\. ", nxt):
                break
            paragraph.append(nxt)
            i += 1
        story.append(Paragraph(inline(" ".join(paragraph)), s["body"]))
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=19 * mm, title="Calm, High-Value Career Strategy for Tanya Poletaeva",
        author="OpenAI Codex", subject="Career research, job-market evidence and development plan",
    )
    doc.build(parse_markdown(SOURCE.read_text(encoding="utf-8")), onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()

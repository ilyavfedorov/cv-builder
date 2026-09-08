#!/usr/bin/env python3
"""Render a tailored Tanya CV from Markdown to a polished A4 PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


INK = colors.HexColor("#17212B")
NAVY = colors.HexColor("#173F5F")
TEAL = colors.HexColor("#147D7E")
MUTED = colors.HexColor("#52606D")
LINE = colors.HexColor("#C9D6DE")


def inline(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(
        r"\[([^]]+)]\((https?://[^)]+)\)",
        r'<link href="\2" color="#147D7E"><u>\1</u></link>',
        value,
    )
    return value


def cv_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=25, textColor=NAVY, alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "target": ParagraphStyle(
            "Target", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=14, textColor=TEAL, alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.5, leading=11, textColor=MUTED, alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=7,
            spaceAfter=4, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10, leading=12.5, textColor=INK, spaceBefore=5,
            spaceAfter=2, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8.7, leading=12, textColor=INK, spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=base["BodyText"], fontName="Helvetica-Oblique",
            fontSize=8.2, leading=10.5, textColor=MUTED, spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8.5, leading=11.5, textColor=INK, spaceAfter=1.5,
        ),
    }


def parse_markdown(source: str):
    styles = cv_styles()
    story = []
    lines = source.splitlines()
    heading_count = 0
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("# "):
            heading_count += 1
            style = styles["name"] if heading_count == 1 else styles["h2"]
            story.append(Paragraph(inline(line[2:]), style))
            if heading_count == 1:
                story.append(HRFlowable(width="100%", thickness=1.4, color=TEAL, spaceAfter=5))
            i += 1
            continue
        if line.startswith("## "):
            story.extend([
                CondPageBreak(24 * mm),
                Paragraph(inline(line[3:]), styles["h2"]),
            ])
            i += 1
            continue
        if line.startswith("### "):
            story.extend([
                CondPageBreak(18 * mm),
                Paragraph(inline(line[4:]), styles["h3"]),
            ])
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                text = inline(lines[i].strip()[2:])
                items.append(ListItem(Paragraph(text, styles["bullet"]), leftIndent=9))
                i += 1
            story.append(ListFlowable(
                items, bulletType="bullet", start="circle", leftIndent=13,
                bulletFontName="Helvetica", bulletFontSize=5.5,
                bulletColor=TEAL, spaceAfter=3,
            ))
            continue
        if line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), styles["meta"]))
            i += 1
            continue

        paragraph = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line or next_line == "---" or next_line.startswith(("#", "- ", "> ")):
                break
            paragraph.append(next_line)
            i += 1
        joined = " ".join(paragraph)
        if heading_count == 1 and len(story) <= 3:
            style = styles["target"] if "**" in joined else styles["contact"]
        elif joined.startswith("**") and ("present" in joined.lower() or "20" in joined):
            style = styles["meta"]
        else:
            style = styles["body"]
        story.append(Paragraph(inline(joined), style))

    return story


def footer(canvas, doc) -> None:
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(17 * mm, 13 * mm, width - 17 * mm, 13 * mm)
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(17 * mm, 8.5 * mm, "Tanya Poletaeva | Tailored CV")
    canvas.drawRightString(width - 17 * mm, 8.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Tailored CV Markdown file")
    parser.add_argument("output", type=Path, help="Output PDF file")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    source = args.input.read_text(encoding="utf-8")
    if "Tanya Poletaeva" not in source:
        raise SystemExit("Input does not appear to be Tanya's CV")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(args.output), pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm,
        topMargin=13 * mm, bottomMargin=17 * mm, title="Tanya Poletaeva - Tailored CV",
        author="Tanya Poletaeva",
    )
    doc.build(parse_markdown(source), onFirstPage=footer, onLaterPages=footer)
    print(args.output)


if __name__ == "__main__":
    main()


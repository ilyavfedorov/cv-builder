#!/usr/bin/env python3
"""
export.py — CV markdown to PDF converter.

Usage:
    python3 export.py <input.md> <output.pdf>

Dependencies (install once):
    pip3 install --user markdown2

Uses the system Google Chrome for headless PDF rendering — no extra downloads.
"""

import os
import subprocess
import sys
import tempfile

SYMBOL_REPLACEMENTS = [
    ("\u2014", " - "),   # em-dash
    ("\u2013", "-"),     # en-dash
    ("\u201c", '"'),     # left double quotation mark
    ("\u201d", '"'),     # right double quotation mark
    ("\u2018", "'"),     # left single quotation mark
    ("\u2019", "'"),     # right single quotation mark
    ("\u2026", "..."),   # horizontal ellipsis
]

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]


def clean_text(text: str) -> str:
    for symbol, replacement in SYMBOL_REPLACEMENTS:
        text = text.replace(symbol, replacement)
    return text


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    return ""


def ensure_markdown2():
    try:
        import markdown2  # noqa: F401
    except ImportError:
        print("Error: markdown2 not installed. Run: pip3 install --user markdown2")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 export.py <input.md> <output.pdf>")
        sys.exit(1)

    ensure_markdown2()
    import markdown2

    input_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2])

    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    chrome = find_chrome()
    if not chrome:
        print("Error: Google Chrome not found. Install Chrome or add its path to CHROME_CANDIDATES in export.py")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.normpath(os.path.join(script_dir, "..", "cv-style.css"))

    if not os.path.isfile(css_path):
        print(f"Error: stylesheet not found: {css_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    cleaned = clean_text(content)

    body_html = markdown2.markdown(
        cleaned,
        extras=["tables", "fenced-code-blocks", "strike"],
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    # Write temporary HTML file — Chrome needs a file:// URL
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(html)
        tmp_html_path = tmp.name

    try:
        result = subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                f"--print-to-pdf={output_path}",
                "--print-to-pdf-no-header",
                f"file://{tmp_html_path}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            print("Chrome failed:")
            print(result.stderr)
            sys.exit(result.returncode)

        print(f"PDF created: {output_path}")

    finally:
        if os.path.isfile(tmp_html_path):
            os.remove(tmp_html_path)


if __name__ == "__main__":
    main()

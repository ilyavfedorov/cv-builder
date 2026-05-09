#!/usr/bin/env python3
"""
export.py — CV markdown to PDF converter.

Usage:
    python3 export.py <input.md> <output.pdf>

Dependencies (install once):
    pip3 install --user markdown2 websocket-client

Uses the system Google Chrome via the DevTools Protocol for headless PDF
rendering — no extra downloads needed beyond Chrome itself.
"""

import base64
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

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

# A4 in inches; margins match the @page rule in cv-style.css (20mm top/bottom, 22mm left/right)
PDF_PARAMS = {
    "displayHeaderFooter": False,
    "printBackground": True,
    "paperWidth": 8.2677,    # 210 mm
    "paperHeight": 11.6929,  # 297 mm
    "marginTop": 0.7874,     # 20 mm
    "marginBottom": 0.7874,
    "marginLeft": 0.8661,    # 22 mm
    "marginRight": 0.8661,
}


def clean_text(text: str) -> str:
    for symbol, replacement in SYMBOL_REPLACEMENTS:
        text = text.replace(symbol, replacement)
    return text


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    return ""


def find_free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def ensure_deps():
    missing = []
    try:
        import markdown2  # noqa: F401
    except ImportError:
        missing.append("markdown2")
    try:
        import websocket  # noqa: F401
    except ImportError:
        missing.append("websocket-client")
    if missing:
        print(f"Error: missing packages: {', '.join(missing)}")
        print(f"Run: pip3 install --user {' '.join(missing)}")
        sys.exit(1)


def wait_for_cdp(port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
            return True
        except Exception:
            time.sleep(0.15)
    return False


def render_pdf_via_cdp(chrome: str, html_file_url: str, output_path: str) -> None:
    import websocket

    port = find_free_port()
    proc = subprocess.Popen(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            f"--remote-debugging-port={port}",
            "--remote-allow-origins=*",
            html_file_url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_cdp(port):
            raise RuntimeError("Chrome CDP did not become ready in time")

        # Give the page a moment to fully load
        time.sleep(1.0)

        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list") as resp:
            targets = json.loads(resp.read())

        page_target = next((t for t in targets if t.get("type") == "page"), None)
        if not page_target:
            raise RuntimeError("No page target found in Chrome CDP")

        ws = websocket.WebSocket()
        ws.connect(page_target["webSocketDebuggerUrl"])
        ws.settimeout(30)

        try:
            ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            ws.recv()

            ws.send(json.dumps({
                "id": 2,
                "method": "Page.printToPDF",
                "params": PDF_PARAMS,
            }))

            for _ in range(200):
                raw = ws.recv()
                msg = json.loads(raw)
                if msg.get("id") == 2:
                    if "error" in msg:
                        raise RuntimeError(f"CDP printToPDF error: {msg['error']}")
                    pdf_bytes = base64.b64decode(msg["result"]["data"])
                    with open(output_path, "wb") as f:
                        f.write(pdf_bytes)
                    return

            raise RuntimeError("No printToPDF response received from Chrome")
        finally:
            ws.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 export.py <input.md> <output.pdf>")
        sys.exit(1)

    ensure_deps()
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

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(html)
        tmp_html_path = tmp.name

    try:
        render_pdf_via_cdp(chrome, f"file://{tmp_html_path}", output_path)
        print(f"PDF created: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if os.path.isfile(tmp_html_path):
            os.remove(tmp_html_path)


if __name__ == "__main__":
    main()

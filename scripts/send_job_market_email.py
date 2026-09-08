#!/usr/bin/env python3
"""Send the prepared Tanya job-market report using Gmail SMTP."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


REPORT = Path("tanya/job-feed/latest-refresh.md")


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    sender = required("GMAIL_ADDRESS")
    password = required("GMAIL_APP_PASSWORD")
    recipient = required("REPORT_TO")
    if not REPORT.is_file():
        raise SystemExit(f"Report not found: {REPORT}")

    body = REPORT.read_text(encoding="utf-8")
    search_date = next(
        (line.removeprefix("Search date: ").strip() for line in body.splitlines() if line.startswith("Search date: ")),
        "latest",
    )
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = f"Tanya job-market refresh — {search_date}"
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Sent report to {recipient}")


if __name__ == "__main__":
    main()


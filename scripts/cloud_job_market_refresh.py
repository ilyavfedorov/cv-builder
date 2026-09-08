#!/usr/bin/env python3
"""Cloud runner for Tanya's scheduled job-market search and CV preparation."""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "tanya/search-profile.json"
CV_DATA_PATH = ROOT / "tanya/cv-data.json"
CURRENT_PATH = ROOT / "tanya/job-feed/current-jobs.csv"
SCORED_PATH = ROOT / "tanya/job-feed/scored-jobs.csv"
REPORT_PATH = ROOT / "tanya/job-feed/latest-refresh.md"
OPPORTUNITIES = ROOT / "tanya/job-opportunities"
GENERATION_LOG = OPPORTUNITIES / "generation-log.csv"

CURRENT_FIELDS = [
    "captured_date", "source", "company", "title", "location", "work_mode",
    "employment_type", "salary_min_nzd", "salary_max_nzd", "url",
    "skills_fit_0_5", "calm_fit_0_5", "energy_fit_0_5", "calm_evidence",
    "calm_risks", "status",
]

SEARCH_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["candidates"],
    "properties": {
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": CURRENT_FIELDS + ["job_description", "salary_evidence", "recruiter_questions"],
                "properties": {
                    **{key: {"type": "string"} for key in CURRENT_FIELDS},
                    "job_description": {"type": "string"},
                    "salary_evidence": {"type": "string"},
                    "recruiter_questions": {"type": "array", "items": {"type": "string"}},
                },
            },
        }
    },
}

TAILOR_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["decision", "positioning_brief", "analysis_markdown", "cv_markdown"],
    "properties": {
        "decision": {"type": "string", "enum": ["Apply", "Research first", "Exceptional-case apply", "Decline"]},
        "positioning_brief": {"type": "string"},
        "analysis_markdown": {"type": "string"},
        "cv_markdown": {"type": "string"},
    },
}


def api_response(prompt: str, schema_name: str, schema: dict) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
        "tools": [{"type": "web_search"}],
        "include": ["web_search_call.action.sources"],
        "input": prompt,
        "text": {"format": {"type": "json_schema", "name": schema_name, "strict": True, "schema": schema}},
        "store": False,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {error.code}: {details}") from error

    texts = [
        part.get("text", "")
        for item in result.get("output", []) if item.get("type") == "message"
        for part in item.get("content", []) if part.get("type") == "output_text"
    ]
    if not texts:
        raise RuntimeError("OpenAI response did not contain output_text")
    return json.loads("".join(texts))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def write_current(rows: list[dict[str, str]]) -> None:
    with CURRENT_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CURRENT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def canonical(value: str) -> str:
    return re.sub(r"[?#].*$", "", value.strip().lower()).rstrip("/")


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:60]


def render_and_verify(markdown_path: Path, pdf_path: Path) -> str:
    subprocess.run(
        ["python", str(ROOT / "scripts/render_tanya_cv.py"), str(markdown_path), str(pdf_path)],
        check=True,
    )
    reader = PdfReader(pdf_path)
    if not 2 <= len(reader.pages) <= 3:
        raise RuntimeError(f"Unexpected CV page count: {len(reader.pages)}")
    page_text = [(page.extract_text() or "").strip() for page in reader.pages]
    if any(not text for text in page_text) or "Tanya Poletaeva" not in "\n".join(page_text):
        raise RuntimeError("CV PDF text verification failed")
    return f"PASS: {len(reader.pages)} pages; text verified"


def append_generation_log(values: list[str]) -> None:
    with GENERATION_LOG.open("a", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerow(values)


def main() -> None:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    cv_data = json.loads(CV_DATA_PATH.read_text(encoding="utf-8"))
    current = read_csv(CURRENT_PATH)
    known_urls = {canonical(row["url"]) for row in current}
    generated_urls = {canonical(row["url"]) for row in read_csv(GENERATION_LOG)}
    last_date = max((row["captured_date"] for row in current), default=profile.get("marketDate", ""))
    today = date.today().isoformat()

    search_prompt = f"""Search current public job vacancies posted after {last_date}.
Candidate profile and rules:
{json.dumps(profile, ensure_ascii=False)}

Verified CV evidence:
{json.dumps(cv_data, ensure_ascii=False)}

Search only these families: mature-platform .NET/SQL Tech Lead, Principal or Staff Engineer,
ERP Technical Architect, Principal ERP/SQL Consultant, internal Solution Architect, and
small-team Engineering Manager. Prioritise employer career pages, SEEK, LinkedIn and reputable
New Zealand recruiters. Location must support Auckland/North Shore with no more than 3 office
days, remote New Zealand, or NZ-based work for an Australian organisation. Compensation must
plausibly reach NZD 160,000 base. Calm work is a first-class requirement. Exclude routine on-call,
escalation support, presales-heavy consulting, broad programme management and ambiguous startup
generalist work. Do not invent salary, work mode or calm evidence; use empty strings for unknowns.
Return only genuinely current roles with canonical source URLs. Use {today} for captured_date.
Set fit ratings from 0 to 5 conservatively and preserve source wording in evidence and risks.
Known URLs to exclude: {json.dumps(sorted(known_urls))}
"""
    discovery = api_response(search_prompt, "job_market_candidates", SEARCH_SCHEMA)
    new_details: dict[str, dict] = {}
    for candidate in discovery["candidates"]:
        url_key = canonical(candidate["url"])
        if not url_key or url_key in known_urls:
            continue
        row = {field: str(candidate.get(field, "")).strip() for field in CURRENT_FIELDS}
        row["captured_date"] = today
        current.append(row)
        known_urls.add(url_key)
        new_details[url_key] = candidate
    write_current(current)

    subprocess.run([
        "python", str(ROOT / "scripts/job_feed.py"), "--profile", str(PROFILE_PATH),
        "--input", str(CURRENT_PATH), "--output", str(SCORED_PATH),
    ], check=True)
    scored = read_csv(SCORED_PATH)
    new_scored = [row for row in scored if canonical(row["url"]) in new_details]

    generated: dict[str, tuple[str, str]] = {}
    for row in new_scored:
        url_key = canonical(row["url"])
        if (
            float(row["total_score_100"]) < 80
            or row["compensation_gate"].startswith("FAIL")
            or row["location_gate"].startswith("FAIL")
            or url_key in generated_urls
        ):
            continue
        detail = new_details[url_key]
        policy = (ROOT / "tanya/career-framework/tailored-cv-policy.md").read_text(encoding="utf-8")
        briefs = (ROOT / "tanya/career-framework/positioning-briefs.md").read_text(encoding="utf-8")
        tailor_prompt = f"""Create a truthful tailored CV package for Tanya Poletaeva.
Vacancy: {json.dumps(detail, ensure_ascii=False)}
Scored result: {json.dumps(row, ensure_ascii=False)}
Canonical CV data (the only permitted source of candidate claims):
{json.dumps(cv_data, ensure_ascii=False)}
Policy:
{policy}
Positioning briefs:
{briefs}
The CV must be 2-3 A4 pages after rendering, preserve exact employers/titles/dates, and contain
no salary, internal scoring, uncertainty or recruiter questions. Put those only in analysis.
"""
        package = api_response(tailor_prompt, "tailored_cv_package", TAILOR_SCHEMA)
        folder_name = f"{today} {safe_slug(row['company'])} {safe_slug(row['title'])} - {package['decision'].upper()}"
        folder = OPPORTUNITIES / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "job-description.md").write_text(
            f"# {row['company']} - {row['title']}\n\nSource: {row['url']}\n\n{detail['job_description']}\n",
            encoding="utf-8",
        )
        (folder / "analysis.md").write_text(package["analysis_markdown"].strip() + "\n", encoding="utf-8")
        base = f"tanya-poletaeva-{safe_slug(row['company'])}-{safe_slug(row['title'])}-cv-tailored"
        markdown_path = folder / f"{base}.md"
        pdf_path = folder / f"{base}.pdf"
        markdown_path.write_text(package["cv_markdown"].strip() + "\n", encoding="utf-8")
        verification = render_and_verify(markdown_path, pdf_path)
        rel_folder = folder.relative_to(ROOT).as_posix()
        rel_md = markdown_path.relative_to(ROOT).as_posix()
        rel_pdf = pdf_path.relative_to(ROOT).as_posix()
        append_generation_log([
            today, row["company"], row["title"], row["url"], row["total_score_100"],
            package["decision"], package["positioning_brief"], rel_folder, rel_md, rel_pdf, verification,
        ])
        generated[url_key] = (rel_md, rel_pdf)

    repo_url = os.environ.get("GITHUB_REPOSITORY_URL", "").rstrip("/")
    lines = [f"Tanya job-market refresh", "", f"Search date: {today}", ""]
    qualifying = [row for row in new_scored if float(row["total_score_100"]) >= 62]
    if not qualifying:
        lines.append("No new role cleared the bar. The criteria were not weakened.")
    else:
        lines.append("Best new matches:")
        for index, row in enumerate(qualifying[:5], 1):
            detail = new_details[canonical(row["url"])]
            decision = "Decline" if row["compensation_gate"].startswith("FAIL") or row["location_gate"].startswith("FAIL") else "Research first"
            lines.extend([
                "", f"{index}. {row['company']} - {row['title']} - {row['total_score_100']}/100 - {decision}",
                f"Salary: {detail['salary_evidence'] or 'Not advertised; verification required.'}",
                f"Location/work mode: {row['location']} / {row['work_mode'] or 'Unknown'}",
                f"Why it fits: {row['calm_evidence']}",
                f"Calm-work risks: {row['calm_risks']}",
                f"Source: {row['url']}",
                "Recruiter questions: " + "; ".join(detail["recruiter_questions"]),
            ])
            if canonical(row["url"]) in generated:
                md, pdf = generated[canonical(row["url"])]
                lines.append(f"Tailored CV: {repo_url}/blob/main/{md} | {repo_url}/blob/main/{pdf}")
    REPORT_PATH.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Added {len(new_details)} new roles; generated {len(generated)} tailored CVs")


if __name__ == "__main__":
    main()

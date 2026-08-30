#!/usr/bin/env python3
"""Normalize and score job-alert exports for a candidate search profile.

This intentionally does not scrape LinkedIn or SEEK. Their pages and access rules
change frequently. Export saved-alert results to CSV or add bookmarked jobs to the
inbox, then use this script to apply the same screening rules every time.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


REQUIRED_COLUMNS = {"company", "title", "location", "url"}


def number(value: str) -> float | None:
    cleaned = re.sub(r"[^0-9.]", "", value or "")
    return float(cleaned) if cleaned else None


def bounded_score(value: str) -> float:
    parsed = number(value)
    return max(0.0, min(5.0, parsed if parsed is not None else 0.0))


def compensation_score(row: dict[str, str], preferred: float, minimum: float) -> tuple[float, str]:
    low = number(row.get("salary_min_nzd", ""))
    high = number(row.get("salary_max_nzd", ""))
    if high is not None and high < minimum:
        return 0.0, "FAIL: advertised maximum is below the hard floor"
    if low is None and high is None:
        return 8.0, "VERIFY: compensation not advertised"
    if low is not None and low >= preferred:
        return 20.0, "PASS: advertised minimum meets preferred floor"
    if high is not None and high >= preferred:
        return 16.0, "VERIFY: preferred floor is within advertised range"
    return 12.0, "VERIFY: meets hard floor but may miss monthly-net target"


def location_score(row: dict[str, str], profile: dict) -> tuple[float, str]:
    text = " ".join([row.get("location", ""), row.get("work_mode", "")]).lower()
    if "remote" in text:
        return 10.0, "PASS: remote-compatible"
    allowed = [item.lower() for item in profile["hardFilters"]["allowedOfficeAreas"]]
    if any(place in text for place in allowed):
        return 8.0, "VERIFY: location allowed; confirm office days"
    return 0.0, "FAIL: location does not match profile"


def score_row(row: dict[str, str], profile: dict) -> dict[str, str]:
    hard = profile["hardFilters"]
    compensation, compensation_gate = compensation_score(
        row, float(hard["preferredSalaryNzd"]), float(hard["minimumSalaryNzd"])
    )
    location, location_gate = location_score(row, profile)
    skills = bounded_score(row.get("skills_fit_0_5", "")) * 6
    calm = bounded_score(row.get("calm_fit_0_5", "")) * 6
    energy = bounded_score(row.get("energy_fit_0_5", "")) * 2
    total = round(skills + calm + energy + compensation + location, 1)
    hard_fail = compensation_gate.startswith("FAIL") or location_gate.startswith("FAIL")
    recommendation = "NO GO" if hard_fail else ("PRIORITY" if total >= 78 else "RESEARCH" if total >= 62 else "HOLD")
    result = dict(row)
    result.update(
        {
            "skills_score_30": f"{skills:.1f}",
            "calm_score_30": f"{calm:.1f}",
            "compensation_score_20": f"{compensation:.1f}",
            "location_score_10": f"{location:.1f}",
            "energy_score_10": f"{energy:.1f}",
            "total_score_100": f"{total:.1f}",
            "compensation_gate": compensation_gate,
            "location_gate": location_gate,
            "recommendation": recommendation,
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    with args.input.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")
        rows = [score_row(row, profile) for row in reader]

    rows.sort(key=lambda row: float(row["total_score_100"]), reverse=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else list(reader.fieldnames or []))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Scored {len(rows)} jobs -> {args.output}")


if __name__ == "__main__":
    main()

# Scheduled task: Tanya job-market refresh

**Schedule:** `RRULE:FREQ=WEEKLY;BYDAY=MO,TH;BYHOUR=9;BYMINUTE=0`
**Timezone:** `Pacific/Auckland`
**Destination:** This existing career-search chat
**Project mode:** Local project `C:\Source\cv-builder`

## Prompt

Run Tanya Poletaeva's job-market refresh using the local project at `C:\Source\cv-builder`.

1. Read `tanya/search-profile.json`, `tanya/cv-data.json`, `tanya/job-feed/current-jobs.csv`, `tanya/job-feed/scored-jobs.csv`, `tanya/career-framework/application-decision-gate.md`, `tanya/career-framework/calm-work-screen.md`, `tanya/career-framework/positioning-briefs.md`, `tanya/career-framework/tailored-cv-policy.md`, and `tanya/job-opportunities/generation-log.csv` before searching.
2. Search current public vacancies posted since the previous scheduled run. Prioritise employer career pages, SEEK, LinkedIn, reputable NZ recruiters, and roles that explicitly support Auckland hybrid, North Shore, remote New Zealand, or NZ-based work for Australian organisations.
3. Search only Tanya's target families: mature-platform .NET/SQL Tech Lead, Principal or Staff Engineer, ERP Technical Architect, Principal ERP/SQL Consultant, internal Solution Architect, and small-team Engineering Manager roles.
4. Apply hard gates: compensation must plausibly reach NZD 160,000 base and should preferably reach NZD 170,000-180,000; Auckland office attendance must be no more than three days; exclude routine on-call, escalation-led support, presales-heavy consulting, broad programme management, and high-ambiguity startup generalist roles unless evidence strongly contradicts the risk.
5. Treat calm work as a first-class requirement: clear ownership, feasible workload, limited interruptions and meetings, protected focus, low concurrent work in progress, and no routine after-hours responsibility.
6. Deduplicate by company, title, location, and canonical URL. Do not re-add expired, rejected, or already-screened roles unless the description or compensation materially changed.
7. Add genuinely new candidates to `tanya/job-feed/current-jobs.csv`, preserving source wording for calm evidence and risks. Do not invent salary, work mode, or stress evidence; leave unknown fields blank and make them verification gates.
8. Run `python scripts/job_feed.py --profile tanya/search-profile.json --input tanya/job-feed/current-jobs.csv --output tanya/job-feed/scored-jobs.csv`.
9. For every newly discovered role scoring at least 80.0/100 without a failed compensation or location gate, follow `tanya/career-framework/tailored-cv-policy.md`. Create a dated opportunity folder under `tanya/job-opportunities`, preserve the job description and URL, write `analysis.md`, select one primary positioning brief, create a truthful tailored Markdown CV, render its PDF with `scripts/render_tanya_cv.py`, verify the output, and append the result to `tanya/job-opportunities/generation-log.csv`. Do not regenerate a URL already in the log unless the vacancy materially changed.
10. Report only the best new matches. Apply the framework's hard gates and positive-fit test. For each, give score, salary evidence, location/work mode, why it fits, calm-work risks, decision (`Apply`, `Research first`, `Exceptional-case apply`, or `Decline`), recruiter questions, and links to any generated Markdown and PDF CV. If nothing clears the bar, say so plainly rather than weakening the criteria.
11. Include source links and the search date. Creating a CV draft is authorised for qualifying roles; applying, uploading the CV, or contacting an employer or recruiter is never authorised without Tanya's explicit instruction.

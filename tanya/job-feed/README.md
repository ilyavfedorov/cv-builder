# Tanya's job-feed workflow

## What this does

The feed stores current vacancies in a portable CSV, then applies Tanya's hard filters and a weighted fit model. The score gives equal importance to skills and calm-work fit, rather than treating salary or title as sufficient evidence.

## Refresh cycle

1. Open the saved searches listed in `../search-profile.json` or enable alerts on SEEK and LinkedIn.
2. Add promising results to `current-jobs.csv`. Keep the source URL and exact wording that supports any calm-work score.
3. Run:

```powershell
python scripts/job_feed.py --profile tanya/search-profile.json --input tanya/job-feed/current-jobs.csv --output tanya/job-feed/scored-jobs.csv
```

4. Research every `PRIORITY` result before applying. Unknown salary, office pattern, workload, on-call, and meeting load remain verification questions.

## Calm-work interview gate

Ask the hiring manager for concrete examples, not cultural adjectives:

- What proportion of a normal week is scheduled meetings?
- How many concurrent initiatives would I own?
- Who handles production incidents and customer escalations?
- How often does urgent work interrupt planned work?
- What was the team's overtime pattern during the last six months?
- How are priorities changed, and who has authority to say no?
- What are the first 90-day outcomes, and what is explicitly outside the role?

Reject a role when the answers reveal persistent overload, unclear ownership, routine escalation duty, or several equally urgent workstreams, even if the title and salary look attractive.

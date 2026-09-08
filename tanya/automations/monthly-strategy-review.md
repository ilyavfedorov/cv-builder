# Scheduled task: Tanya monthly career-strategy review

**Schedule:** First Friday of each month at 5:00 PM
**Recurrence:** `RRULE:FREQ=MONTHLY;BYDAY=FR;BYSETPOS=1;BYHOUR=17;BYMINUTE=0`
**Timezone:** `Pacific/Auckland`
**Destination:** Email to Tanya, sent by GitHub Actions
**Project mode:** Cloud workflow `.github/workflows/tanya-monthly-strategy-review.yml`

## Prompt

Run Tanya Poletaeva's monthly career-strategy review using the local project at `C:\Source\cv-builder`.

Read `tanya/career-framework/README.md`, `tanya/career-framework/monthly-review.md`, `tanya/search-profile.json`, both job-feed CSVs, `tanya/career-framework/recruiter-intelligence.csv`, `tanya/career-framework/skills-gap-tracker.csv`, and `tanya/cv-data.json`.

Create or update `tanya/career-framework/reviews/YYYY-MM.md`. Analyse the funnel, strongest role families, salary evidence, calm-work risks, rejection reasons, recruiter intelligence, positioning feedback and recurring skill gaps. Recommend what to keep, change and stop. Choose no more than one skill-development priority, and only when it appears in at least three otherwise suitable roles and Tanya wants the work it enables. Propose any changes to `tanya/search-profile.json`, but wait for Tanya's confirmation before changing hard filters or role families.

Do not describe a low vacancy count as failure and do not weaken salary, location or calm-work requirements merely to produce more matches.

Email the concise review summary with a tagged subject. When Tanya replies with corrections, outcomes or decisions, the hourly reply-import workflow sanitises and appends the response to that month's review under `Tanya's email follow-up`.

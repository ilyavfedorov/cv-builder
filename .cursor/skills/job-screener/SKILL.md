---
name: job-screener
description: Screens job opportunities against a candidate's cv-data.json. Writes an analysis.md and renames each job-opportunities subfolder with " - GO" or " - NO GO". Use when asked to screen, evaluate, or triage job opportunities.
disable-model-invocation: true
---

# Job Screener

## Step 0 — Identify the person folder

List the workspace root. The person folder is any subdirectory that is not `.cursor` or another system folder (e.g. `ilya`).

- If exactly one person folder exists, use it automatically.
- If multiple exist, ask the user which person to process.

All subsequent paths use `<person>` to refer to that directory.

---

## Step 1 — Load candidate data

Read `<person>/cv-data.json` in full. The fields used for matching are:

- `summary` — overall profile and seniority signals
- `workExperience[].role`, `.from`, `.to`, `.type`, `.inferredSkills`, `.techStack` — concrete skills and career trajectory
- `education` — formal qualifications

---

## Step 2 — Find unprocessed job folders

List `<person>/job-opportunities/`. Collect every subfolder whose name does **not** already end with ` - GO` or ` - NO GO`. These are the folders to process.

If there are no unprocessed folders, report that all jobs have already been screened and stop.

---

## Step 3 — Analyze each job

For each unprocessed folder, read `job-description.md` inside it (if there is no file by that exact name, read the first `.md` file found).

Evaluate fit across these dimensions:

- **Seniority match** — do the required years of experience and leadership scope align with the candidate's career history?
- **Skills match** — map each stated required skill or technology to entries in `inferredSkills` and `techStack` across all roles
- **Role type match** — is this a leadership, IC, or hybrid role? Does it match the candidate's recent trajectory?
- **Industry relevance** — is there directly transferable domain experience, or meaningful adjacent experience?
- **Gaps** — list any requirements the candidate clearly does not meet and cannot plausibly bridge with existing experience

**Verdict logic:**

- `GO` — strong match on seniority and core required skills; any gaps are minor, learnable, or secondary to the role
- `NO GO` — significant mismatch on seniority, role type, or one or more non-negotiable requirements the candidate lacks

---

## Step 4 — Write `analysis.md`

Write the file to `<person>/job-opportunities/<folder>/analysis.md` using this structure:

```markdown
# Job Screening: <Company> — <Role>

**Verdict: GO** _(or NO GO)_

## Summary
One paragraph explaining the overall verdict — what makes this a strong or poor fit.

## Strengths
- One bullet per matched requirement or relevant strength

## Gaps / Concerns
- One bullet per gap, risk, or concern
- Write "None identified" if there are no meaningful gaps

## Requirements Match
| Requirement | Evidence from CV | Match |
|---|---|---|
| <requirement from job description> | <matching role, skill, or achievement> | Yes / Partial / No |
```

---

## Step 5 — Rename the folder

After writing `analysis.md`, rename the folder by appending the verdict to its name. Use the Shell tool with a two-step approach to avoid duplicate folders in sandboxed environments:

```bash
cp -r "<person>/job-opportunities/<original-name>" "<person>/job-opportunities/<original-name> - GO" && rm -rf "<person>/job-opportunities/<original-name>"
```

Replace ` - GO` with ` - NO GO` for a no-go verdict. Quote all paths to handle spaces. After running, verify only the renamed folder exists.

---

## Step 6 — Report

After all folders have been processed, report:

- Total number of folders processed
- GO count and NO GO count
- One-line rationale for each folder (company name, role, verdict, one sentence why)

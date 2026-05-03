---
name: generate-tailored-cv
description: Generates a tailored CV and cover letter for a specific job opportunity by matching the job description's tone, style, and keywords to the candidate's factual cv-data.json. Use when asked to create a tailored CV, write a cover letter, generate application materials, or customise a CV for a job.
disable-model-invocation: true
---

# Generate Tailored CV & Cover Letter

Produces two files for a specific job opportunity:
- `cv-tailored.md` — a CV with job-matched language, keyword-injected and emphasis-tiered
- `cover-letter.md` — written per [cover-letter-composer](../cover-letter-composer/SKILL.md) (conversational, short sentences, JD keywords, evidence-mapped)

Facts come exclusively from `cv-data.json`. Nothing is invented.

---

## Step 0 — Identify folders

**Person folder:** list the workspace root. Use any subdirectory that is not `.cursor` or a system folder (e.g. `ilya`). If more than one exists, ask the user.

**Job folder:** use the folder containing the file the user currently has open (or most recently mentioned). If unclear, list `<person>/job-opportunities/` and ask.

**Job folder layout (canonical files):** each opportunity is a subfolder of `<person>/job-opportunities/`. Before Step 1, **list `<jobFolder>`** and confirm these exist:
- `job-description.md` — raw job posting (this exact filename)
- `analysis.md` — fit analysis from job-screener (if not run yet, create or obtain before tailoring)

If `job-description.md` is missing after listing, stop and ask the user to add it or give the correct path. Do not guess from other `.md` files in the folder (e.g. `analysis.md` is not a substitute for the JD).

All subsequent paths use `<person>` and `<jobFolder>`.

---

## Step 1 — Load inputs

Read all three in parallel:

- `<jobFolder>/job-description.md` — raw job description
- `<jobFolder>/analysis.md` — pre-computed fit analysis (strengths, gaps, requirements match)
- `<person>/cv-data.json` — ground truth for every fact

---

## Step 2 — Analyse the job description

### 2a — Tone and style fingerprint

Extract these signals — they govern Step 3; supply Step 2b keywords for the cover letter (see [cover-letter-composer](../cover-letter-composer/SKILL.md)):

| Signal | What to detect |
|---|---|
| Register | Formal-corporate / direct-operational / startup-casual |
| Sentence shape | Short and punchy (≤12 words) vs longer narrative |
| Voice | Active commands ("you will own") vs third-person ("the successful candidate") |
| Vocabulary preferences | ~10 specific word choices the JD makes — note them explicitly |

Example vocabulary capture:
> JD says "delivery predictability" → use that, not "on-time delivery"
> JD says "operating rhythm" → use that, not "process" or "cadence"
> JD says "ownership" → use that, not "responsibility" or "accountability"

### 2b — Keyword list

Extract ~20–30 terms in two tiers:

**Must-use** — role-critical terms, methodology names, domain terms that appear multiple times or in requirements headers. These must appear in the tailored CV if they can be placed naturally.

**Should-use** — supporting terms that appear once but are distinctive to this role.

For each keyword, note whether `cv-data.json` has direct evidence in `inferredSkills` or `techStack` across any role.

---

## Step 3 — Write `cv-tailored.md`

Output to `<jobFolder>/cv-tailored.md`.

### Document structure

```
# <contact.fullName> — <Role Title from JD>

## Contact

Render from `<person>/cv-data.json` → `contact`: **Full name**, **Phone**, **Email**, **LinkedIn**, and **Location** / **Immigration status** when those fields exist. Omit a line if the field is missing.

## Summary

## Work Experience

## Education

## Professional Development & Community
```

### Summary (5–7 bullets)

- Source every bullet from `cv-data.json summary[]` — no invented claims
- Reorder so bullets addressing the JD's top requirements come first
- Swap in vocabulary from the Step 2a fingerprint and Step 2b must-use keywords where they fit naturally
- Drop any summary item with no relevance to the role

### Work experience

Apply three emphasis tiers based on recency and relevance to the role:

**Tier 1** — the 3 most recent or most relevant roles:
- Show full `highlights` (combined scope and outcomes for the role)
- Reframe bullet wording to use JD vocabulary where it fits — the factual content must remain directly traceable to `cv-data.json`; only the phrasing changes
- Front-load JD-relevant technologies in the `Tech:` line

**Tier 2** — older roles with meaningful relevance:
- Show full `highlights`
- Consider trimming duplicate or low-value bullets — keep at least outcomes and headline scope visible
- No vocabulary reframing required

**Tier 3** — roles pre-2010 or with low relevance:
- Company, role, dates, and one-line `companyDescription` only
- No highlights or tech stack

Format each role identically to `cv.md`:

```markdown
### Company — Role
**Mon YYYY – Mon YYYY** · type · industry

> Company description

**Highlights**

- ...

**Tech:** comma-separated tech stack
```

Omit `Highlights` or `Tech:` sections entirely if empty or suppressed by tier.

After `**Highlights**`, include **one blank line** before the first bullet so Markdown (and Chrome PDF export) treats the bullets as a list, consistent with spacing under section headings such as Summary.

### Education and Professional Development & Community

Copy items verbatim from `cv-data.json` (`education`, `professionalDevelopment`) — no changes. Use heading `## Professional Development & Community`.

---

## Step 4 — Write `cover-letter.md`

Read and follow [cover-letter-composer](../cover-letter-composer/SKILL.md). Use the same `<person>`, `<jobFolder>`, and inputs as Steps 1–2. Output to `<jobFolder>/cover-letter.md`.

---

## Step 5 — Report

After both files are written, report:

- Paths of both files created
- Top 5 JD keywords used and where each appears (CV summary / work experience / cover letter per cover-letter-composer)
- Any must-use keyword from Step 2b that could not be placed naturally in the CV or cover letter (and why)

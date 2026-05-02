---
name: generate-tailored-cv
description: Generates a tailored CV and cover letter for a specific job opportunity by matching the job description's tone, style, and keywords to the candidate's factual cv-data.json. Use when asked to create a tailored CV, write a cover letter, generate application materials, or customise a CV for a job.
disable-model-invocation: true
---

# Generate Tailored CV & Cover Letter

Produces two files for a specific job opportunity:
- `cv-tailored.md` — a CV with job-matched language, keyword-injected and emphasis-tiered
- `cover-letter.md` — a cover letter mirroring the JD's tone and vocabulary

Facts come exclusively from `cv-data.json`. Nothing is invented.

---

## Step 0 — Identify folders

**Person folder:** list the workspace root. Use any subdirectory that is not `.cursor` or a system folder (e.g. `ilya`). If more than one exists, ask the user.

**Job folder:** use the folder containing the file the user currently has open (or most recently mentioned). If unclear, list `<person>/job-opportunities/` and ask.

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

Extract these signals — they govern every sentence you write in Steps 3 and 4:

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
# <Full Name> — <Role Title from JD>

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

Output to `<jobFolder>/cover-letter.md`.

Apply the tone/vocabulary fingerprint from Step 2a to every sentence.

### Structure (4 paragraphs)

**Paragraph 1 — Opening**
Reference the company's stated mission, product, or challenge using their own language from the JD. State clearly why this specific role is compelling. One short paragraph.

**Paragraph 2 — Core fit**
Pick the 2–3 strongest alignment points from `analysis.md` Strengths. State each as a concrete claim backed by a specific achievement or role from `cv-data.json`. Use JD must-use keywords. Do not list everything — be selective and confident.

**Paragraph 3 — Gap acknowledgement** *(include only if `analysis.md` lists a meaningful gap)*
One sentence naming the gap plainly. Two sentences explaining why it does not block success in this role or how it is actively being bridged. Keep it brief and forward-looking. Omit this paragraph entirely if there are no meaningful gaps in `analysis.md`.

**Paragraph 4 — Close**
A direct, confident sentence expressing intent to discuss further. No filler phrases ("I look forward to", "please find attached", "thank you for your consideration"). Match the register of the JD's close section if it has one.

---

## Step 5 — Report

After both files are written, report:

- Paths of both files created
- Top 5 JD keywords used and where each appears (CV summary / work experience / cover letter)
- Any must-use keyword from Step 2b that could not be placed naturally (and why)

---
name: generate-tailored-cv
description: Generates a tailored CV and cover letter for a specific job opportunity by matching the job description's tone, style, and keywords to the candidate's factual cv-data.json while keeping a human, professional voice. Use when asked to create a tailored CV, write a cover letter, generate application materials, or customise a CV for a job.
disable-model-invocation: true
---

# Generate Tailored CV & Cover Letter

Produces two files for a specific job opportunity:
- `{personSlug}-{jobKey}-cv-tailored.md` — a CV with job-matched language, human-readable phrasing, and emphasis-tiered experience
- `{personSlug}-{jobKey}-cover-letter.md` — written per [cover-letter-composer](../cover-letter-composer/SKILL.md) (conversational, short sentences, JD keywords, evidence-mapped)

Facts come exclusively from `cv-data.json`. Nothing is invented.

---

## Step 0 — Identify folders

**Person folder:** list the workspace root. Use any subdirectory that is not `.cursor` or a system folder (e.g. `ilya`). If more than one exists, ask the user.

**Job folder:** use the folder containing the file the user currently has open (or most recently mentioned). If unclear, list `<person>/job-opportunities/` and ask.

**Job folder layout (canonical files):** each opportunity is a subfolder of `<person>/job-opportunities/`. Before Step 1, **list `<jobFolder>`** and confirm these exist:
- `job-description.md` — raw job posting (this exact filename)
- screening analysis file — prefer exactly one `*-analysis.md`; if none exists, use legacy `analysis.md`

If `job-description.md` is missing after listing, stop and ask the user to add it or give the correct path. Do not guess from other `.md` files as a substitute.

Resolve `analysisPath` with this priority:
1. If exactly one file matches `*-analysis.md`, use it.
2. If no `*-analysis.md` exists but `analysis.md` exists, use `analysis.md` (legacy compatibility).
3. If more than one `*-analysis.md` exists, ask the user which one to use.
4. If none exist, stop and ask the user to run screening first.

From `job-description.md`, extract `company` and advertised `role`, then compute:
- `companySlug` and `roleSlug` — lowercase, replace runs of non-alphanumeric characters with `-`, trim leading/trailing `-`, collapse duplicate `-`
- `jobKey` — `{companySlug}-{roleSlug}`

If either slug is empty after normalization, stop and ask the user instead of guessing. If `jobKey` exceeds ~80 characters, truncate `roleSlug` from the right until `jobKey` is within ~80 characters.

All subsequent paths use `<person>` and `<jobFolder>`.

---

## Step 1 — Load inputs

Read all three in parallel:

- `<jobFolder>/job-description.md` — raw job description
- `<jobFolder>/<analysisPath>` — pre-computed fit analysis (strengths, gaps, requirements match)
- `<person>/cv-data.json` — ground truth for every fact

From `cv-data.json` → `contact.fullName`, compute `personSlug` using the same normalization as `companySlug`. If `fullName` is missing or `personSlug` is empty after normalization, stop and ask the user instead of guessing.

Define `applicationFileStem` as `{personSlug}-{jobKey}`. If `applicationFileStem` is longer than ~100 characters, truncate `roleSlug` further (from the right) until it is within ~100 characters, keeping `personSlug` and `companySlug` intact.

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

**High-priority** — role-critical terms, methodology names, domain terms that appear multiple times or in requirements headers. Prioritize these in the tailored CV when they can be placed naturally.

**Should-use** — supporting terms that appear once but are distinctive to this role.

For each keyword, note whether `cv-data.json` has direct evidence in `inferredSkills` or `techStack` across any role.

Do not force exact terms into awkward wording. Natural, readable language is more important than maximizing exact keyword count.

---

## Step 3 — Write `{personSlug}-{jobKey}-cv-tailored.md`

Output to `<jobFolder>/{applicationFileStem}-cv-tailored.md`.

### Document structure

```
# <contact.fullName> — <Role Title from JD>

## Contact

Render from `<person>/cv-data.json` → `contact` as follows — bold full name on its own line, then each remaining field as a markdown list item. Omit a field if missing.

```markdown
**<fullName>**

- <phone>
- <email>
- <linkedinUrl as a markdown link>
- <location>
- <immigrationStatus>
```

## Summary

## Work Experience

## Education

## Professional Development & Community (include only if relevant entries qualify)
```

### Voice guardrails (apply across Summary and Work Experience)

- Write in a professional, human tone: clear, grounded, and personable
- Preserve factual traceability to `cv-data.json`; do not invent
- Avoid robotic mirroring of JD wording; prefer natural phrasing that a person would say
- Where evidence supports it, favor impact language that shows outcomes for people, teams, customers, or stakeholders
- Final pass: rewrite any sentence that feels keyword-stuffed or templated

### Summary (5–7 bullets)

- Source every bullet from `cv-data.json summary[]` — no invented claims
- Reorder so bullets addressing the JD's top requirements come first
- Swap in vocabulary from the Step 2a fingerprint and Step 2b high-priority keywords where they fit naturally
- Drop any summary item with no relevance to the role
- Ensure at least 1 bullet (where evidence exists) reflects collaboration style or human impact, not just tools/process terms

### Work experience

Apply three emphasis tiers based on recency and relevance to the role:

**Tier 1** — the 3 most recent or most relevant roles:
- Show full `highlights` (combined scope and outcomes for the role)
- Reframe bullet wording to use JD vocabulary where it fits — keep phrasing natural and human; the factual content must remain directly traceable to `cv-data.json`; only the phrasing changes
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

For `education`, copy items from `cv-data.json education` without inventing facts.

For `professionalDevelopment`, apply a relevance gate before inclusion:
- Include only entries that clearly strengthen candidacy for this JD (domain knowledge, tools/platforms, methodology, compliance, language requirement, leadership/community leadership relevant to the role)
- Prefer recent entries, unless an older one is directly role-critical
- Keep only top 2-4 entries by relevance then recency
- Exclude low-signal or unrelated entries
- Keep included entries factually faithful to `cv-data.json`; light wording cleanup is allowed for readability, but no new claims

Only add heading `## Professional Development & Community` if at least one entry passes the relevance gate. If none qualify, omit the section entirely.

---

## Step 4 — Write `{personSlug}-{jobKey}-cover-letter.md`

Read and follow [cover-letter-composer](../cover-letter-composer/SKILL.md). Use the same `<person>`, `<jobFolder>`, `analysisPath`, `jobKey`, `personSlug`, and `applicationFileStem` from Steps 0–1. Output to `<jobFolder>/{applicationFileStem}-cover-letter.md`.

---

## Step 5 — Report

After both files are written, report:

- Paths of both files created
- Top 5 JD keywords used and where each appears (CV summary / work experience / cover letter per cover-letter-composer)
- Any high-priority keyword from Step 2b that could not be placed naturally in the CV or cover letter (and why)
- Professional Development & Community decision:
  - included entries and one-line relevance reason for each, or
  - confirmation the section was omitted because no entry added clear value
- Quality checks:
  - CV reads like a human professional voice, not templated AI text
  - no forced keyword insertions that hurt readability

---

## Step 6 — Quick validation runs

When validating skill changes, run these two checks:

1. A role where `professionalDevelopment` is clearly relevant:
   - confirm `## Professional Development & Community` appears
   - confirm entries are concise, role-matched, and high-signal
2. A role where `professionalDevelopment` is weakly relevant:
   - confirm the section is omitted entirely
   - confirm tone remains warm, specific, and factual in Summary + Tier 1 roles

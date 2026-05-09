---
name: cover-letter-composer
description: Composes a {personSlug}-{jobKey}-cover-letter.md file for a job application from job-description.md, a screening analysis file, and cv-data.json. Weaves JD keywords naturally, maps requirements to evidence from the CV, uses short conversational plain English with a warm, human professional voice, and includes a brief genuine-interest close. Use when writing or revising a cover letter, producing a job-specific cover letter file, or applying to a job folder.
disable-model-invocation: true
---

# Cover letter composer

Writes `<jobFolder>/{applicationFileStem}-cover-letter.md` where `applicationFileStem` is `{personSlug}-{jobKey}`. Facts come only from `<person>/cv-data.json`. Nothing invented.

---

## Step 0 — Identify folders

Same as [generate-tailored-cv Step 0](../generate-tailored-cv/SKILL.md): resolve `<person>` (workspace person folder) and `<jobFolder>` (open or named job under `<person>/job-opportunities/`).

**Confirm inputs:** list `<jobFolder>` and ensure `job-description.md` (exact name) and a screening analysis file are present before reading. Example resolved path: `<person>/job-opportunities/<subfolder>/job-description.md`. If `job-description.md` is missing, ask the user; do not treat the screening analysis file as the job description.

Resolve `analysisPath` with this priority:
1. If exactly one file matches `*-analysis.md`, use it.
2. If no `*-analysis.md` exists but `analysis.md` exists, use `analysis.md` (legacy compatibility).
3. If more than one `*-analysis.md` exists, ask the user which one to use.
4. If none exist, stop and ask the user to run screening first.

From `job-description.md`, extract `company` and advertised `role`, then compute:
- `companySlug` and `roleSlug` — lowercase, replace runs of non-alphanumeric characters with `-`, trim leading/trailing `-`, collapse duplicate `-`
- `jobKey` — `{companySlug}-{roleSlug}`

If either slug is empty after normalization, stop and ask the user instead of guessing. If `jobKey` exceeds ~80 characters, truncate `roleSlug` from the right until `jobKey` is within ~80 characters.

From `cv-data.json` → `contact.fullName`, compute `personSlug` using the same normalization as `companySlug`. If `fullName` is missing or `personSlug` is empty after normalization, stop and ask the user instead of guessing.

Define `applicationFileStem` as `{personSlug}-{jobKey}`. If `applicationFileStem` is longer than ~100 characters, truncate `roleSlug` further (from the right) until it is within ~100 characters, keeping `personSlug` and `companySlug` intact.

Paths to read: `<person>/cv-data.json`, `<jobFolder>/job-description.md`, `<jobFolder>/<analysisPath>`.

---

## Step 1 — Load inputs

Read all three in parallel (same files as tailored CV workflow).

---

## Step 2 — Pre-write pass

1. **Must-use JD phrases** — role title exactly as advertised, stack, domain terms, methodology names, terms repeated or in requirement headers.
2. **Proof map** — for each major JD requirement, one concrete proof from `cv-data.json`: company, role, and a specific outcome or highlight (verbatim traceable).
3. **Motivation notes** — 2–3 lines: what about this JD aligns with what the candidate already does or values, using only JD + CV facts. No invented hobbies or claims.

---

## Step 3 — Voice and reading load

Write as if talking **to the hiring manager** (you / I ok).

- **Short sentences**: aim ~10–15 words on average; occasional longer sentence only if it stays simple.
- **One idea per sentence.** Small paragraphs (1–3 sentences). Breathing room between ideas.
- Plain everyday words. **No fancy or literary English.**
- Avoid stacked transitions: "Furthermore", "Moreover", "Additionally".
- Avoid long chains of dependent clauses.
- Keep tone warm, sincere, and grounded. Sound like a thoughtful professional person, not a script.
- Use specific motivation tied to JD facts and CV evidence, not generic enthusiasm.

**Audience:** assume a very busy reader and low spare attention. They should get the point in a skim.

---

## Step 4 — Surface rules (no polish that reads like a bot)

- No emojis.
- No bullet lists in the letter body.
- Do not stack parallel triples or perfectly symmetric sentences every sentence.
- Avoid résumé-speak: e.g. "leverage", "synergy", "delve", "robust", "passionate about", "thrilled to", "I am writing to express".
- Use normal commas and periods. **Do not lean on em dashes** to tie clauses together.
- Do not read like a press release or a template.
- If a sentence sounds like stock AI phrasing, rewrite it in plain natural language.

---

## Step 5 — Relevance

- Tie each major JD ask you keep to **one specific past win** (where, what moved).
- Use **their** keywords where it still sounds like speech.
- If the screening analysis file lists a meaningful gap: **one short block** — name it in plain language, then one or two short sentences on why it is not a blocker or how adjacent experience covers it. No essay.

---

## Step 6 — Excitement

End with a **short** beat (a few sentences max): what about this role, product, or problem space is a strong match for what they already do. Factual and specific to the JD. No hype words.

Close with sincere, specific contribution intent ("how I can help here"), not generic flattery.

---

## Step 7 — Output

Write `<jobFolder>/{applicationFileStem}-cover-letter.md`:

- Title line optional: e.g. `# Cover Letter — <Role>, <Company>` if that matches other materials in the folder.
- Greeting (e.g. Dear Hiring Manager, or a named contact if present in the JD).
- Body in small paragraphs.
- Sign-off and full name from `contact` in `cv-data.json`.
- Optional date line if sibling files in the job folder use one; stay consistent.

---

## Step 8 — Quality gate

Before finishing:

- [ ] Every big JD theme is **addressed or consciously deferred** (gap paragraph).
- [ ] Must-use phrases appear **naturally**, not stuffed.
- [ ] No fact that is not supported by `cv-data.json`.
- [ ] Tone reads as human and professional, not AI-templated.
- [ ] Closing is specific and sincere (interest + contribution intent), without hype.

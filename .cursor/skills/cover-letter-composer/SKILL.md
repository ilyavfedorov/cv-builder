---
name: cover-letter-composer
description: Composes cover-letter.md for a job application from job-description.md, analysis.md, and cv-data.json. Weaves JD keywords naturally, maps requirements to evidence from the CV, uses short conversational plain English for a busy reader, and includes a brief genuine-interest close. Use when writing or revising a cover letter, producing cover-letter.md, or applying to a job folder.
disable-model-invocation: true
---

# Cover letter composer

Writes `<jobFolder>/cover-letter.md`. Facts come only from `<person>/cv-data.json`. Nothing invented.

---

## Step 0 — Identify folders

Same as [generate-tailored-cv Step 0](../generate-tailored-cv/SKILL.md): resolve `<person>` (workspace person folder) and `<jobFolder>` (open or named job under `<person>/job-opportunities/`).

**Confirm inputs:** list `<jobFolder>` and ensure `job-description.md` (exact name) and `analysis.md` are present before reading. Example resolved path: `<person>/job-opportunities/<subfolder>/job-description.md`. If `job-description.md` is missing, ask the user; do not treat `analysis.md` as the job description.

Paths to read: `<person>/cv-data.json`, `<jobFolder>/job-description.md`, `<jobFolder>/analysis.md`.

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

**Audience:** assume a very busy reader and low spare attention. They should get the point in a skim.

---

## Step 4 — Surface rules (no polish that reads like a bot)

- No emojis.
- No bullet lists in the letter body.
- Do not stack parallel triples or perfectly symmetric sentences every sentence.
- Avoid résumé-speak: e.g. "leverage", "synergy", "delve", "robust", "passionate about", "thrilled to", "I am writing to express".
- Use normal commas and periods. **Do not lean on em dashes** to tie clauses together.
- Do not read like a press release or a template.

---

## Step 5 — Relevance

- Tie each major JD ask you keep to **one specific past win** (where, what moved).
- Use **their** keywords where it still sounds like speech.
- If `analysis.md` lists a meaningful gap: **one short block** — name it in plain language, then one or two short sentences on why it is not a blocker or how adjacent experience covers it. No essay.

---

## Step 6 — Excitement

End with a **short** beat (a few sentences max): what about this role, product, or problem space is a strong match for what they already do. Factual and specific to the JD. No hype words.

---

## Step 7 — Output

Write `<jobFolder>/cover-letter.md`:

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

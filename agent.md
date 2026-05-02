# CV Data Extraction Agent

## Goal

Read all CV PDFs for a given person, extract and consolidate all career data, and write a single `cv-data.json` into that person's folder.

---

## Step 0 — Identify the person folder

List the contents of the workspace root. The person folder is any subdirectory that is not `.cursor` or another config/system folder (e.g. `ilya`).

- If exactly one person folder exists, use it automatically.
- If multiple person folders exist, ask the user which person to process before continuing.

All subsequent paths use `<personFolder>` to refer to that directory (e.g. `ilya`).

---

## Step 1 — Read all CVs

Use the Read tool on every PDF file found inside `<personFolder>/cv-history/`. The PDFs are automatically converted to plain text.

List the contents of `<personFolder>/cv-history/` first, then read each PDF found there. Read all files before writing anything.

---

## Step 2 — Extract the Summary

Collect every bullet point from the **Summary** section of all three CVs.

Rules:
- Deduplicate semantically: if the same idea appears in multiple CVs with different wording, keep the **most detailed / most recent version** only.
- Do **not** paraphrase — preserve the original wording exactly.
- Order items starting from the most recent CV (2026), then 2024, then 2020.
- The result is a flat array of strings in the top-level `"summary"` key.

---

## Step 3 — Extract Work Experience

Build the `"workExperience"` array ordered **newest-first**.

### Roles to extract

| Company | Role | From | To | Type |
|---|---|---|---|---|
| Mindhive | Head of Engineering | 2025-02 | present | full-time |
| Tradify | Senior Software Engineering Manager | 2023-12 | 2025-02 | full-time |
| Te Kete Hono | Head of Technology | 2020-05 | 2024-10 | contract |
| Serko | Software Engineering Manager | 2019-08 | 2020-04 | contract |
| Propellerhead | Product Owner / Development Manager | 2017-10 | 2019-11 | contract |
| Schooltalk | Co-founder / Software Engineering Manager | 2015-01 | 2017-09 | co-founder |
| Fraedom.com | Senior Full-Stack Software Developer | 2013-04 | 2015-01 | full-time |
| Freightways | Senior Analyst-Programmer | 2007-11 | 2013-03 | full-time |
| Thor United | Senior Analyst-Programmer | 2006-02 | 2007-11 | full-time |
| Nicotech International | Analyst-Programmer | 2005-04 | 2005-10 | full-time |
| Sportmaster | Analyst-Programmer | 2001-09 | 2005-04 | full-time |

> **Note on Te Kete Hono:** Create a single entry with role "Head of Technology" spanning May 2020 – Oct 2024. Merge all role bullets (`highlights`) and inferred skills from across the full tenure into this one entry.

### Source priority

Each CV was written at a point in time. Use the source that was **closest to the role's end date** as the primary source (it will have the most detail for that role). Supplement from other CVs if they add highlight bullets not present in the primary source.

- **2026 CV** → primary for Mindhive and Tradify
- **2024 CV** → primary for Te Kete Hono and Serko
- **2020 CV** → primary for Propellerhead, Schooltalk, Fraedom.com, Freightways, Thor United, Nicotech International, Sportmaster

### Schema for each entry

```json
{
  "company": "string — company name",
  "role": "string — exact job title",
  "type": "full-time | contract | advisory | co-founder",
  "from": "YYYY-MM",
  "to": "YYYY-MM | present",
  "industry": "string — one short phrase describing the industry",
  "companyDescription": "string — one or two sentences describing the company from the CV",
  "highlights": [
    "string — merged list: outcomes and delivered work first, then ongoing scope/duties; verbatim from the CV"
  ],
  "techStack": [
    "string — each distinct technology, language, framework, or tool listed for this role"
  ],
  "inferredSkills": [
    "string — see skill inference rules below"
  ]
}
```

**Ordering within `highlights`:**
- When the CV splits **Achievements** and **Responsibilities**, concatenate into one array: all achievement bullets first, then all responsibility bullets, preserving verbatim wording.
- If the CV combines them already, preserve source order.

**techStack:**
- List each individual technology separately — do not bundle them into a comma-separated string.
- Include languages, frameworks, libraries, databases, cloud services, tools, and platforms.
- Example: `["React", "Redux", "TypeScript", "Node.js", "C# .NET", "Azure", "SQL Server", "Azure DevOps", "CI/CD pipelines"]`

---

## Step 4 — Infer Skills

For each work experience entry, populate `"inferredSkills"` by reading every item in `highlights` for that role and extracting the concrete, specific skill demonstrated.

### Rules

1. **Stay granular and literal** — use the exact capability named or strongly implied by the text. Do not roll up into category labels.
   - ✅ `"pair programming"` — not `"Engineering Practices"`
   - ✅ `"mob programming"` — not `"Engineering Practices"`
   - ✅ `"TDD"` — not `"Testing"`
   - ✅ `"CI/CD pipeline management"` — not `"DevOps"`
   - ✅ `"infrastructure as code"` — not `"Cloud"`
   - ✅ `"flow metrics"` — not `"Delivery Management"`
   - ✅ `"microservices architecture"` — not `"Architecture"`
   - ✅ `"grant writing"` — not `"Funding"`
   - ✅ `"technical debt management"` — not `"Code Quality"`
   - ✅ `"security audit preparation"` — not `"Security"`
   - ✅ `"vendor coordination"` — not `"Stakeholder Management"`

2. **Infer, do not invent** — only extract skills that are evidenced by the text. If it is not written or directly implied, leave it out.

3. **Use short noun phrases** — each skill should be 1–5 words. No sentences.

4. **Include soft skills when explicitly evidenced** — e.g. "fostered psychological safety" → `"psychological safety building"`. Do not add generic soft skills that are not mentioned.

5. **Deduplicate within a role** — if the same skill appears in multiple bullets, list it once.

6. **Do not copy techStack items into inferredSkills** — technologies belong in `techStack` only.

---

## Step 5 — Extract Education

Find the **Education** section (present in all three CVs). The qualifications are the same across all CVs. Extract each qualification once.

```json
{
  "qualification": "string — full qualification name",
  "institution": "string — institution name"
}
```

Known entries:
- Postgraduate Diploma in Information Technology and Computer Science — Auckland University of Technology
- Postgraduate Diploma in Business Analysis — Russian Academy of National Economy
- Master of Applied Physics and Mathematics — Moscow Institute of Physics and Technology

---

## Step 6 — Extract Professional Development & Community

Find the **Professional Development**, **Professional Development & Community**, **Leadership & Community**, and any equivalent sections in the CVs. These appear only in the 2026 CV. Extract each distinct activity.

```json
{
  "description": "string — what it is, verbatim or very close to the source",
  "period": "string — year or date range if given, otherwise omit the field"
}
```

Known entries from the 2026 CV:
- Executive Coaching with Noah Cantor (2024–present)
- Executive Coaching with Paul Birch (2025–present)
- Founded and facilitate a peer forum of engineering leaders (Canva, Gentrack, Fintfox)
- Mentor at University of Auckland Chiasma programme
- Chair, local VEX V5 robotics club supporting homeschooled students in competitive robotics (2026)

---

## Step 7 — Write the output file

Write the complete JSON to `<personFolder>/cv-data.json` (e.g. `ilya/cv-data.json`).

The top-level structure must be:

```json
{
  "contact": {
    "fullName": "string",
    "phone": "string",
    "email": "string",
    "linkedinUrl": "string",
    "location": "string — optional, e.g. city and country from CV header",
    "immigrationStatus": "string — optional; include if stated on the CV or provided by the candidate"
  },
  "summary": [],
  "workExperience": [],
  "education": [],
  "professionalDevelopment": []
}
```

Extract **`contact`** from the CV header / footer of the most recent PDF (typically name, phone, email, LinkedIn; location if shown). Omit any field that does not appear in the source; use `"immigrationStatus"` only when the CV or candidate states it explicitly.

Validate that:
- Every work experience entry has all required fields
- `from` and `to` use `YYYY-MM` format (or the string `"present"` for current roles)
- `techStack` and `inferredSkills` are arrays of individual strings, not comma-separated strings
- There are no trailing commas or syntax errors in the JSON

---

## Step 8 — Generate the Markdown CV

After writing `cv-data.json`, read it back and write a human-readable `<personFolder>/cv.md`.

### Document structure

```
# <Full name from contact.fullName> — CV

## Contact
 Render from `contact`: full name (if not only in the title), phone, email, LinkedIn URL, location and immigration status when present.

## Summary
(one bullet per summary item)

## Work Experience
(one section per role, newest first)

## Education
(bullet list)

## Professional Development & Community
(bullet list)
```

### Work experience format (per role)

```markdown
### Company — Role
**Mon YYYY – Mon YYYY** · type · industry

> Company description

**Highlights**

- ...

**Tech:** comma-separated tech stack
```

Rules:
- Omit `inferredSkills` — it is downstream-processing metadata, not human-facing content.
- Skip the **Highlights** section entirely if the `highlights` array is empty.
- After `**Highlights**`, output one blank line before the first `-` bullet so bullets render as a list in PDF export.
- Skip the **Tech:** line entirely if `techStack` is empty.
- Format dates as `Mon YYYY` (e.g. `Feb 2025`). Use `present` as-is for the current role.

### Education format

Render as a bullet list. Bold the qualification name and separate the institution with an em-dash:

```markdown
- **Qualification name** — Institution name
```

### Professional Development & Community format

Render as a bullet list. Bold the description and append the period in parentheses where a `period` field exists.

---

## Completion

Once both files have been written, confirm the full file paths (including the person folder) and report:
- Total number of work experience entries
- Total number of unique inferred skills across all entries
- Total number of summary points

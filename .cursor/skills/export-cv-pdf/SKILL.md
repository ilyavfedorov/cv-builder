---
name: export-cv-pdf
description: Exports a CV markdown file (cv.md, {personSlug}-{jobKey}-cv-tailored.md, or legacy cv-tailored.md) to a clean PDF with 1.5 line spacing, consistent typography, and AI-signature symbols removed. Use when the user asks to export, save, or convert a CV to PDF.
disable-model-invocation: true
---

# Export CV to PDF

Converts a CV markdown file to a clean PDF. Symbol cleanup runs automatically before conversion.

---

## One-time setup

If `markdown2` is not installed, run this once:

```bash
pip3 install --user markdown2
```

PDF rendering uses the system Google Chrome in headless mode — no extra downloads needed.

---

## Step 1 - Identify the input file

- If the user has an open tailored CV file in the current job folder, use it:
  - prefer `{personSlug}-{jobKey}-cv-tailored.md` (name derived from `cv-data.json` and the job description, same as the generate-tailored-cv skill)
  - otherwise allow legacy `cv-tailored.md`
- If no file is open, list the current job folder:
  - if exactly one file matches `*-cv-tailored.md`, use it
  - if multiple files match `*-cv-tailored.md`, ask the user which one to export
  - if none match, fall back to legacy `cv-tailored.md` when present
- Otherwise use `<person>/cv.md`.

The output PDF is placed in the same folder as the input file, with the same basename and a `.pdf` extension (e.g. `jane-doe-acme-senior-product-manager-cv-tailored.pdf`).

---

## Step 2 - Run the export script

The script lives inside this skill's directory. Locate it relative to this SKILL.md file:

```
.cursor/skills/export-cv-pdf/scripts/export.py
```

Run:

```bash
python3 ".cursor/skills/export-cv-pdf/scripts/export.py" "<path/to/input.md>" "<path/to/output.pdf>"
```

The script:
1. Replaces AI-signature symbols (em-dashes, en-dashes, curly quotes, ellipsis)
2. Converts markdown to HTML via markdown2 with the CSS embedded inline
3. Renders to PDF using system Chrome in headless mode (`--print-to-pdf`)

---

## Step 3 - Report

Tell the user the full path of the PDF that was created.
If the script fails, show the error output so the user can troubleshoot.

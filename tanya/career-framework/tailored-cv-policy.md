# Automatic tailored-CV policy

## Generation trigger

Generate a CV when all conditions hold:

- The vacancy was newly discovered in the current Monday or Thursday pull.
- Its final score is at least 80.0/100.
- Neither `compensation_gate` nor `location_gate` begins with `FAIL`.
- The canonical URL is not already present in `../job-opportunities/generation-log.csv`.
- Enough job-description evidence is available to tailor truthfully.

An unknown salary, office pattern or calm-work condition does not prevent draft creation, but the opportunity must remain `Research first` until verified.

## Tailoring rules

1. Use only facts supported by `../cv-data.json`.
2. Select one primary brief from `positioning-briefs.md` based on the role's principal outcome.
3. Target two or three A4 pages. Preserve career chronology and do not hide dates.
4. Rewrite the summary and choose the most relevant achievements and skills; do not keyword-stuff.
5. Never change job titles, employers, dates, qualifications or measured results.
6. Do not claim expertise from evidence levels 1 or 2.
7. Use exact technology names only when they exist in the CV data.
8. Do not include salary, mortgage, calm-work preferences, internal scoring, recruiter questions or the target employer's confidential information in the CV.
9. Include contact details, concise summary, relevant capabilities, work experience, education and certifications.
10. Label uncertainty in `analysis.md`, never inside the CV.

## Quality gate

Before logging success:

- Compare every substantive claim with `../cv-data.json`.
- Render the Markdown with `python scripts/render_tanya_cv.py <input.md> <output.pdf>`.
- Confirm the PDF opens, contains Tanya's name and has no blank pages.
- Render pages to images when Poppler is available and inspect for clipping, overlap or unreadable text.
- Record failures in the generation log and report them; do not silently claim a CV was created.


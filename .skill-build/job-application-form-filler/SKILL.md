---
name: job-application-form-filler
description: Prepare and fill Tanya Poletaeva's online job application forms using verified CV evidence, tailored documents, and vacancy-specific answers. Use when Tanya asks to apply for a role, complete an employer application, populate a recruitment form, or reuse her application details. Do not submit an application without her explicit final approval.
---

# Job Application Form Filler

Help Tanya complete online employment applications accurately and efficiently while preserving her control over sensitive disclosures and final submission.

## Reusable candidate details

- **Name:** Tanya Poletaeva
- **Email:** tt.korenev@gmail.com
- **Phone:** 021 049 0083
- **Street address:** 66 Shakespear Road
- **Suburb:** Army Bay
- **City:** Whangaparaoa
- **Region:** Auckland
- **Postcode:** 0930
- **Country:** New Zealand
- **Work eligibility:** New Zealand citizen

Use the canonical career evidence in `C:\Source\cv-builder\tanya\cv-data.json` when available. Treat that file as authoritative for experience, qualifications, technologies and measured results. Never invent or silently strengthen a claim.

## Workflow

1. Read the vacancy and any linked full job description. Identify required documents, mandatory questions, character limits and possible screening gates.
2. Check for an existing opportunity folder under `C:\Source\cv-builder\tanya\job-opportunities`. Reuse a verified tailored CV and cover letter when they match the exact role. Otherwise prepare truthful role-specific documents according to the project's tailored-CV policy.
3. Inspect the entire application form before entering data. Separate fields into:
   - known reusable details;
   - role-specific answers that can be derived safely;
   - optional diversity questions;
   - sensitive declarations or material choices that Tanya must answer.
4. Ask one concise grouped question for genuinely missing information. Common examples are desired pay, relocation or office attendance, notice period, pronouns, and legal or health declarations. Do not infer sensitive answers from silence.
5. Before typing personal or sensitive data or uploading files to an employer or recruitment platform, obtain action-time confirmation that identifies the destination and the data/documents to be transmitted.
6. Fill only confirmed information. Leave honeypot fields blank. Preserve nuance in a cover letter when a required Yes/No screening question cannot express Tanya's actual position, but answer the screening question truthfully.
7. Upload the correct tailored CV and cover letter, then verify visible filenames and all populated required fields. If an upload fails, inspect the actual local path and retry safely; do not substitute an unrelated document.
8. Leave optional gender, ancestry and similar diversity questions unanswered unless Tanya explicitly supplies her choices.
9. Stop before acknowledgement checkboxes, CAPTCHA and final submission unless Tanya explicitly asks for those actions at the time they are ready. Always request action-time confirmation before representational submission. Never bypass CAPTCHA or safety interstitials.
10. Keep the populated application page open for Tanya's review and report exactly what remains.

## Application defaults

- Prefer `SEEK` as the discovery source only when the vacancy or Tanya confirms it came from SEEK.
- Use the salary preference in `cv-data.json` as context, not as permission to enter a number. Confirm the desired salary for each application.
- Use `Whangaparaoa` in city fields and `Auckland` in region/province fields. Split the street, suburb and postcode according to the form's field structure.
- Do not add a complete street address when it is optional unless Tanya requests it for that application; it remains available above for required address fields.

## Quality checks

- Every substantive career claim is supported by the canonical CV data or a fact Tanya supplied directly.
- Employer name, role title and document filenames match the current vacancy.
- Salary, location, work eligibility and declarations reflect Tanya's explicit answers for the current application.
- Required uploads show as attached; no stale or failed upload warning remains.
- No optional demographic response has been selected without instruction.
- The final application has not been submitted without explicit approval.

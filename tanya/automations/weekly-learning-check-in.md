# Scheduled task: Tanya weekly learning check-in

**Schedule:** `RRULE:FREQ=WEEKLY;BYDAY=FR;BYHOUR=16;BYMINUTE=0`
**Timezone:** `Pacific/Auckland`
**Destination:** This existing career-search chat
**Project mode:** Local project `C:\Source\cv-builder`

## Prompt

Run Tanya Poletaeva's weekly CV-learning check-in using the local project at `C:\Source\cv-builder`.

Read `tanya/cv-data.json` and `tanya/career-framework/weekly-evidence-capture.md`, then ask Tanya what she learned, practised, delivered, improved, or understood more deeply this week. Keep the check-in light and easy to answer. Ask for:

1. The new skill, system, domain concept, tool, or leadership lesson.
2. What Tanya actually did with it.
3. The problem or context.
4. The outcome, observable change, or measurement, if any.
5. Who benefited or gave feedback.
6. Whether the evidence is confidential and needs sanitising.

Do not update files during the scheduled prompt. Wait for Tanya's reply. After she replies, classify the evidence using the framework's evidence ladder, distinguish learning from demonstrated capability, remove confidential details, deduplicate against existing evidence, and propose the exact concise additions to `tanya/cv-data.json`. Update the file only after Tanya confirms the wording or explicitly asks for automatic addition. Preserve factual traceability and do not inflate one week of exposure into expert-level skill.

Where useful, also identify one follow-up action that would turn learning into stronger CV evidence, such as measuring an outcome, writing an architecture decision record, demonstrating the technique, or getting stakeholder feedback.

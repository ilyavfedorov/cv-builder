# Scheduled task: Tanya weekly learning check-in

**Schedule:** `RRULE:FREQ=WEEKLY;BYDAY=FR;BYHOUR=16;BYMINUTE=0`
**Timezone:** `Pacific/Auckland`
**Destination:** Email to Tanya, sent by GitHub Actions
**Project mode:** Cloud workflow `.github/workflows/tanya-weekly-learning-check-in.yml`

## Prompt

Run Tanya Poletaeva's weekly CV-learning check-in using the local project at `C:\Source\cv-builder`.

Read `tanya/cv-data.json` and `tanya/career-framework/weekly-evidence-capture.md`, then ask Tanya what she learned, practised, delivered, improved, or understood more deeply this week. Keep the check-in light and easy to answer. Ask for:

1. The new skill, system, domain concept, tool, or leadership lesson.
2. What Tanya actually did with it.
3. The problem or context.
4. The outcome, observable change, or measurement, if any.
5. Who benefited or gave feedback.
6. Whether the evidence is confidential and needs sanitising.

Do not update evidence files when sending the scheduled prompt. When Tanya replies by email, the hourly reply-import workflow classifies the evidence using the framework's evidence ladder, distinguishes learning from demonstrated capability, removes confidential details, and deduplicates it. Add the sanitised entry to `tanya/career-framework/learning-log.md`. Add concise evidence to `tanya/cv-data.json` automatically only for level 3-5 evidence directly supported by Tanya's reply. Preserve factual traceability and do not inflate one week of exposure into expert-level skill.

Where useful, also identify one follow-up action that would turn learning into stronger CV evidence, such as measuring an outcome, writing an architecture decision record, demonstrating the technique, or getting stakeholder feedback.

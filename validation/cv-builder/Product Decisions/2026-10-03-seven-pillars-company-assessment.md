# Use the seven pillars as the company-assessment model

- **Date**: 2026-10-03
- **Status**: Accepted

## Context

Interview preparation must help a candidate both demonstrate their suitability and investigate whether a company provides the conditions for meaningful, sustainable work. A generic culture-fit score would be too vague, and a fully candidate-defined framework would make comparisons inconsistent.

The source philosophy, *Seven pillars of a thriving software company*, defines seven observable dimensions: meaningful purpose and customer impact; clear direction and priorities; autonomy with support; trust and psychological safety; growth and competence; sustainable working conditions; and fairness, recognition and belonging.

## Decision

Use the seven pillars as the stable company-assessment model for software roles. Keep candidate-specific hard gates and preferences as a separate overlay.

For each pillar, preserve four things independently:

1. What the company or interviewer claimed.
2. What concrete example or operating evidence supports the claim.
3. The candidate's interpretation and confidence.
4. Unknowns or contradictions requiring follow-up.

Do not reduce the seven pillars to a single company score. Present a pillar-by-pillar evidence profile and apply personal hard gates before recommending whether to proceed.

Interview questions should be selected for the interview stage and the largest unresolved risks. The candidate should ask a small number of high-value questions, not recite the full framework in every conversation.

## Alternatives considered

| Option | Why rejected |
|--------|--------------|
| Let every candidate invent their own company pillars | Makes the product harder to use and prevents consistent learning across opportunities. |
| Use only universal red flags and hard gates | Detects obvious harm but misses positive conditions such as purpose, autonomy, growth and recognition. |
| Produce one weighted company-fit score | Conceals uncertainty and permits strength in one dimension to compensate for a serious weakness in another. |
| Ask every pillar question in every interview | Creates an unnatural interrogation and ignores what different interviewers can credibly answer. |

## Consequences

The product can prepare candidate answers and company questions from one coherent model. Opportunities remain comparable without pretending that incomplete interview evidence is objective measurement.

The implementation needs an interview-stage question selector, evidence and confidence fields for every pillar, a contradiction log, personal hard gates, and a post-interview debrief. The framework is designed for software companies; application to other sectors will require validation rather than silent generalisation.

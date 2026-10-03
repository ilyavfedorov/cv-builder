# Make interviews a bidirectional diligence process

- **Date**: 2026-10-03
- **Status**: Superseded by `2026-10-03-seven-pillars-company-assessment.md`

## Context

The current product helps a candidate identify suitable opportunities, screen basic working-condition risks, and prepare truthful application material. That leaves a critical gap between applying and deciding whether to accept a role. Interviews are both an assessment of the candidate and the candidate's best opportunity to test how a company actually operates.

The product must help a candidate perform well in interviews while also collecting concrete evidence about leadership, workload, decision-making, team health, and working practices. Company claims should not be treated as evidence without recent examples.

## Decision

Make interview preparation and post-interview company evaluation a core product loop rather than an optional extension.

For every active opportunity, the product will support:

1. Candidate preparation grounded in verified career evidence and the requirements of the role.
2. A small set of high-value candidate questions mapped to configurable company-success pillars.
3. Structured capture of the interviewer's answers, examples, unknowns, and contradictions.
4. A post-interview assessment separating observed evidence from interpretation.
5. A decision recommendation that applies personal hard gates before overall attractiveness.
6. Learning that improves future interview preparation, career positioning, and company assessment.

The candidate's company-success pillars will be stored separately from universal safeguards. Universal safeguards cover issues such as chronic overload, routine after-hours expectations, unclear accountability, and unsafe or disrespectful conduct. Personal pillars express the type of company and operating system in which the candidate expects to thrive.

## Alternatives considered

| Option | Why rejected |
|--------|--------------|
| Limit the product to CV tailoring and application generation | Stops before the highest-risk decision and provides little differentiation from commodity CV tools. |
| Provide generic interview questions only | Does not use the candidate's evidence, role context, personal constraints, or company philosophy. |
| Produce a single opaque company-fit score | Hides uncertainty and can create false confidence from incomplete or rehearsed interview answers. |
| Treat interview preparation and company evaluation as separate products | Splits one user journey and loses the connection between what the candidate is asked, what they ask, and what both sides reveal. |

## Consequences

The product becomes a career and company decision system, with CV generation as one supporting capability. It can help candidates avoid unsuitable roles as well as win suitable ones.

The system must preserve provenance, confidence, and unknown states rather than presenting subjective impressions as facts. It also requires an explicit post-interview debrief and a configurable representation of the candidate's company-success pillars. Automated recording or transcription is deferred; interview notes can be captured manually unless all participants have consented to another method.

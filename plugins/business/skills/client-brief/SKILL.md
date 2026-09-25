---
name: client-brief
description: "Turns a client's vague ask or problem statement into a structured, client-facing requirements brief (goals, non-goals, user stories, acceptance criteria) — the document to align on before detailed product/engineering planning. Triggers EN: write a brief, scope this feature, requirements document, client requirements, what does the client actually want. Triggers FR: cadrage client, note de cadrage, cahier des charges leger, definir le perimetre."
---

<!-- Provenance: condensed from anthropics/knowledge-work-plugins (Apache-2.0), product-management/skills/write-spec.
Reframed from an internal PRD to a client-facing requirements brief; connector-search boilerplate removed. -->

# Client Brief

Turn a client's request (a feature name, a problem statement, a vague idea, or a forwarded email) into a
structured requirements brief the client can read and sign off on, before detailed product or engineering
planning starts. This is a **cadrage** document, not a PRD or a technical spec — it is written for the client
to understand and approve, not for an engineering team to implement from directly. All prose goes through
`writing-voice` and `language-strategy`.

**Handoff:** once the client agrees to this brief, it becomes the input to a full PRD workflow (BMAD's
`bmad-product-brief` step, or your own PRD skill/process) — this skill stops here, at client alignment, and
does not produce a PRD, a roadmap, or a technical breakdown itself.

## Step 1 — Understand the ask
Take it in whatever form it arrives: a feature name, a problem statement, a user request, or a vague idea.
Ask (conversationally, most important first — don't dump every question at once): the user problem and who
experiences it, target users/segment, how success will be measured, constraints (technical, timeline,
regulatory, budget), and whether this has been attempted before.

## Step 2 — Pull available context
Use whatever is connected (project tracker, knowledge base, prior specs) or provided (pasted notes, an RFP);
without connectors, work entirely from what the client and user supply — never block on a missing tool.

## Step 3 — Produce the brief

- **Problem statement** (2-3 sentences) — the problem, who's affected, cost of not solving it. Ground it in
  evidence when available (client-supplied data, support history, stated pain) rather than assumption.
- **Goals** (3-5) — specific, measurable outcomes. Outcomes, not outputs ("reduce time-to-first-value by 50%",
  not "build an onboarding wizard").
- **Non-goals** (3-5) — explicitly out of scope, each with a one-line reason (not enough impact, separate
  initiative, premature). Non-goals prevent scope creep as much as goals define direction.
- **User stories**, grouped by persona: "As a [specific user type], I want [capability] so that [benefit]."
  Include edge cases and error states. Avoid vague ("as a user, I want it to be faster") or
  solution-prescriptive ("I want a dropdown") stories — describe the need, not the UI.
- **Requirements**, tagged Must-have / Nice-to-have / Future consideration, each with acceptance criteria in
  Given/When/Then or checklist form. Be ruthless about Must-have: "would we really not ship without this?"
- **Success metrics** — leading indicators (adoption, activation, task completion — visible within weeks) and
  lagging indicators (retention, satisfaction, revenue impact — visible over months). Specific targets, not
  "high adoption".
- **Open questions** — genuinely unresolved, tagged with who needs to answer them. Never include a question
  answerable from context already given.
- **Timeline considerations** — hard deadlines, dependencies, suggested phasing if too large for one release.

## Step 4 — Review with the client
Ask if any section needs adjustment before treating this as agreed. Offer to expand any section, or to hand
off to the next step (PRD, design brief, engineering breakdown) once approved.

## Rules
- Be opinionated about scope — a tight, well-defined brief beats an expansive vague one. If the ask is too big
  for one brief, propose phasing and brief the first phase only.
- Non-goals are as important as goals; write them explicitly, don't leave scope boundaries implicit.
- Any scope addition after sign-off should come with either a scope removal elsewhere or an explicit
  timeline/budget adjustment — say so if the client tries to add scope silently.
- Success metrics must be specific and measurable — "improve the experience" is not a metric.
- Keep it scannable: headers and bold text should carry the gist for a reader skimming on their phone.

## Output
Markdown with clear headers, one document. After delivery, ask whether to proceed to the PRD/BMAD handoff, or
to adjust the brief further.

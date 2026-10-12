---
name: critique
description: "Review a concrete interface's information hierarchy, cognitive load, visual coherence and discoverability; return prioritized issues with evidence and proposed fixes. Use for design review, an AI-looking UI or assessing clarity before revision. FR : « critique le design », « évalue cette interface », « pourquoi ce front est chargé ». Own design assessment; use frontend-qa for functional/accessibility testing and distill, clarify or layout for edits."
---

<!-- Adapted and modified from pbakaus/impeccable, .agents/skills/impeccable/reference/critique.md, commit 919dbeba520df760a157fe635be62faae88d58da. Apache-2.0; Copyright 2025 Paul Bakaus. Portable adaptation: scoped evidence-based review; omit upstream detector, persistence, grading and orchestration requirements. License: ../../../../licenses/APACHE-2.0.txt. -->

# Critique

Resolve the requested screen/flow, audience and main task from the brief and source. Read [frontend-content](../frontend-content/SKILL.md) and the current spec. Inspect the rendered target when available; otherwise state that the review uses source or supplied screenshots.

Assess:

- Whether the visible hierarchy makes the main task/result understandable.
- Whether headings, paragraphs, cards or charts repeat the same information.
- Whether exploration/detail are discoverable and preserve decision-critical context.
- Whether layout, density, visual identity and vocabulary fit the real audience.
- Whether empty/error states, mobile reading, keyboard paths and chart labels expose usability problems.

Return at most five priority findings: **location/evidence → user impact → concrete fix → appropriate skill** (`distill`, `clarify`, `layout` or `frontend-qa`). Separate observed problems from untested concerns. Record material decisions in the existing spec.

For a review-only request, deliver findings. When revision is already authorized, apply the relevant fixes and verify them; do not add a mandatory approval round, arbitrary score or a full upstream runtime.

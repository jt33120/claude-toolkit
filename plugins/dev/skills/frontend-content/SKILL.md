---
name: frontend-content
description: "Decide what belongs in a product interface versus its companion spec; design three levels of progressive disclosure before building or reshaping UI. Use for a new screen, feature, dashboard, simulator or site, or when a brief contains too much explanatory material. FR : « front trop verbeux », « interface trop chargée », « moins de texte », « quoi afficher », « progressive disclosure », « produit et spec ». Own information priority; leave visual identity to frontend-direction and existing-UI reduction to distill."
---

# Frontend content

**Deliver two complementary artifacts: the usable product and its maintained spec.** Preserve the brief's facts and constraints in the spec; select UI content by the user's task. Make routine information choices autonomously from the brief, users and existing product.

## Before building

1. State the audience, the screen's main question or task, and the next useful action in one sentence each, in the spec.
2. Inventory material facts, requirements, calculations, assumptions and open questions. Classify each as **visible**, **on demand**, **spec only**, or **redundant** with a short reason. Preserve unique context when removing its UI presentation.
3. Choose a representation for each retained item. Use a number, table, chart, diagram or short sentence according to the question; consult [visual selection](../frontend-direction/references/charts-and-disclosure.md) when data or relationships matter.
4. Build the selected hierarchy, then update the spec to match what was actually implemented. Ask only when a missing fact materially changes scope, factual meaning or a consequential action.

## Three levels of progressive disclosure

| Level | Show | Access |
|---|---|---|
| 1 — Synthesis | Main result, status or decision; essential context and primary action | Visible without interaction |
| 2 — Exploration | Breakdown, comparison, category or useful explanation | One clear click/tap on a labeled control or selectable item |
| 3 — Detail | Formula, evidence, assumptions or advanced options needed to inspect or act | Explicit detail view; companion spec for author/maintainer context |

The spec spans all levels; do not make it the only home of detail product users need. Do not add three panels or a three-step wizard merely to enact this hierarchy. Omit unnecessary layers.

## Content rules

- Say each idea once. Remove titles that restate labels, subtitles that restate titles, introductory filler, decorative cards and repeated prose summaries of a chart.
- Start with one dominant idea per panel and one primary action per task. Keep necessary dense comparisons together for expert workflows; record why their density helps.
- Keep enough text to name actions, axes, units, status and consequences. Choose visuals when they reduce reading or reveal relationships, never to replace an already clear value.
- Keep price, consent, destructive consequences, errors, blockers and qualifications that change the decision visible at the point of action. Mark estimates and missing data honestly.
- Make on-demand information discoverable, keyboard/touch accessible, dismissible and readable without hover. Use descriptive triggers, focus management and semantic expanded states.
- Keep documentation language, implementation details and the agent's reasoning out of product copy unless the product user needs them.

## Companion spec and handoff

Use the existing PRD/spec location and format. If none exists, create `docs/ui/<screen-or-feature>.md` using [the template](references/content-spec-template.md). For a small copy/layout edit, update the relevant existing section instead of adding a new document.

Record the source facts, content allocation, final strings/representations, interactions, calculations, unknowns and acceptance checks at the depth the change needs. Keep this context out of the app bundle and public routes unless the product calls for it.

For real UI work, run this skill first, then `frontend-direction`, implementation, targeted `distill` / `clarify` / `layout` when needed, and `frontend-qa`. Use [examples](references/examples.md) only when allocation is unclear. Finish with working UI **and** the updated spec, with both paths identified in the handoff.

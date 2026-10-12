---
name: layout
description: "Restructure an existing interface's reading order, grouping, spacing, density and responsive behavior within its current visual identity. Use for weak hierarchy, repetitive card grids, poor spacing or a layout that breaks on mobile. FR : « revois la mise en page », « organise cet écran », « trop de cartes », « hiérarchie visuelle ». Own spatial structure; use frontend-direction for identity and frontend-content for information priority."
---

<!-- Adapted and modified from pbakaus/impeccable, .agents/skills/impeccable/reference/layout.md, commit 919dbeba520df760a157fe635be62faae88d58da. Apache-2.0; Copyright 2025 Paul Bakaus. Portable adaptation: project tokens and rendered checks without upstream detector/live-mode dependencies. License: ../../../../licenses/APACHE-2.0.txt. -->

# Layout

Read [frontend-content](../frontend-content/SKILL.md) and the screen's spec. Identify the reading/task path, which items belong together, the leading element and the density the audience needs.

1. Group by meaning using proximity and alignment before adding containers. Reserve cards for units with independent content or interaction.
2. Express primary/secondary priority through space and type hierarchy. Avoid equally weighted boxes for unrelated priorities.
3. Use the project's spacing scale, grid and platform conventions. Preserve identity and useful data density.
4. Make responsive behavior structural: reflow, collapse or reveal secondary regions according to priority. Keep DOM, visual and focus order consistent.
5. Keep comparisons needed for one decision together. Avoid disclosure that makes users remember values across separate screens.

Inspect representative widths, long content, empty states, zoom, localization and overlays. Verify readable charts, usable touch targets and keyboard access to revealed content. If only source was inspected, state that limit.

Update the companion spec's grouping and disclosure behavior; run the relevant `frontend-qa` checks after editing.

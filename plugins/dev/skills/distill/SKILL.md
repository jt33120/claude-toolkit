---
name: distill
description: "Simplify an existing UI by removing redundant content, decoration and competing structure while preserving tasks and access to useful detail. Use when asked to simplify, declutter or strip a screen to its essence. FR : « simplifie cet écran », « allège le front », « retire le superflu », « trop de cartes ». For initial content allocation use frontend-content; for wording alone use clarify."
---

<!-- Adapted and modified from pbakaus/impeccable, .agents/skills/impeccable/reference/distill.md, commit 919dbeba520df760a157fe635be62faae88d58da. Apache-2.0; Copyright 2025 Paul Bakaus. Portable adaptation: preserve functionality, project identity and companion spec; omit upstream CLI dependencies. License: ../../../../licenses/APACHE-2.0.txt. -->

# Distill

Read [frontend-content](../frontend-content/SKILL.md) and the current UI/spec. Identify the main task and observed sources of clutter before editing.

1. Map what must remain visible, what belongs on demand and what belongs only in the spec.
2. Remove repeated headings, helper paragraphs, duplicate numbers, decorative containers and competing emphasis. Prefer spacing and alignment to a card around every item.
3. Combine related controls and remove unnecessary steps. Retain secondary functionality through clear access points; do not silently remove capabilities.
4. Preserve the project's tokens, navigation and task-appropriate density. Use `layout` for structural changes and `clarify` for unclear copy.
5. Update the companion spec with relocated context and reasons for the cuts.

Keep essential labels, decision-critical information, errors and accessibility intact. Do not impose a fixed font/color count or erase necessary domain complexity.

Verify the primary task, detail access, responsive layout and absence of broken references after removal. Report the few meaningful cuts and the updated spec path; use `frontend-qa` for the affected flows.

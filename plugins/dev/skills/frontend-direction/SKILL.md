---
name: frontend-direction
description: "Frame the visual and interaction direction of a UI (web or mobile) without imposing a style: follow the project design system if one exists, otherwise propose 3 contrasting directions and record the choice. Use when starting a screen, app or site, when a UI looks generic or AI-made, or when choosing style, palette, typography, density or motion. FR : « direction artistique », « le front fait générique », « propose des styles », « quelle palette », « design de cet écran »."
---

# Frontend direction

<!-- Incorporates adapted guidance from anthropics/skills frontend-design (Apache-2.0) and selected UI UX Pro Max reference data (MIT). See references/frontend-design.md, references/ATTRIBUTION.md and the repository NOTICE for pinned sources and modifications. -->

**Rule 0 — the project wins.** If a design system exists (Claude Design synced with `/design-sync`, a tokens file, a component library in the repo, or `.claude/design-direction.md`), follow it and only propose within its bounds. This skill gives options and checks, never a house style.

Before styling a new or reshaped screen, use [frontend-content](../frontend-content/SKILL.md) to decide visible content, on-demand detail and spec-only context. Keep its three-level hierarchy; do not turn the entire brief into UI copy.

## 1. Context (ask only what is missing)

Platform(s): web / iOS / Android / cross-platform · audience and tone · existing brand assets · density (data-heavy vs content-led) · constraints (accessibility level, dark mode, languages).

When establishing a direction or correcting a generic result, consult [Frontend Design principles](references/frontend-design.md), adapted from Anthropic. Read the UI UX Pro Max catalogs only for the current decision: `references/styles.csv`, `references/colors.csv`, `references/typography.csv` or `references/ux-guidelines.csv`.

## 2. Three contrasting directions (only when there is no design system)

For each direction give: a name, a one-line intent, type pairing (≤ 2 families + scale), palette by role (background, surface, text, accent, semantic) with AA contrast, shape and radius, spacing scale and density, motion level, 2–3 signature components.

- The 3 must differ on at least 3 axes. Do not default to the previous project's direction.
- **Mobile:** start from platform conventions (Apple HIG, Material 3). Differentiate through color, type, iconography and motion, not by breaking native navigation patterns.
- The user picks or mixes. Write `.claude/design-direction.md` (tokens + rationale) and suggest pushing it into Claude Design so design and code share one source.

## 3. Build with real components

- **Names and alternatives:** `ui-vocabulary`. When a pattern repeats, offer 2–3 options (e.g. modal vs sheet vs inline expansion).
- **Web:** shadcn MCP (bundled with this plugin) and shadcn-compatible open registries (Magic UI, Origin UI, Base UI, React Aria). Tokens as CSS variables / Tailwind theme — no hard-coded colors.
- **Mobile:** native components (SwiftUI, Jetpack Compose) or Expo UI; keep platform navigation idioms.
- **Motion:** purposeful (feedback, continuity, hierarchy), roughly 150–300 ms for UI transitions, always respect reduced-motion.

## 3a. Represent information

Use [charts and disclosure](references/charts-and-disclosure.md) for choosing a number, table, chart or diagram. Consult `references/charts.csv` only when a chart shortlist is useful. Keep the question, labels, units and decision-critical context visible; make supporting calculations explorable. Record the selection and interaction contract in the companion spec.

## 4. Pre-show checklist

- [ ] One dominant idea per panel; no repeated title/subtitle/paragraph/chart summary
- [ ] Visible, exploration and detail levels work; meaningful context is preserved in the spec
- [ ] Visuals answer a question; exact values and necessary dense comparisons remain usable
- [ ] Every stylistic choice is intentional and traceable to the direction (no leftover template look)
- [ ] Clear type hierarchy, consistent spacing scale and grid
- [ ] Real content; loading, empty and error states designed
- [ ] AA contrast, visible focus states, touch targets ≥ 44 pt / 48 dp
- [ ] Dark mode handled if in scope

## 5. Audit and QA

Use the bundled Impeccable adaptations as needed: `critique` to assess, `distill` to reduce clutter, `clarify` for copy and `layout` for structure. Then `frontend-qa` for functional and disclosure checks. Vercel `web-design-guidelines` may complement web QA if installed. Assets: `asset-brief`.

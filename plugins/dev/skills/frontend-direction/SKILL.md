---
name: frontend-direction
description: "Frame the visual and interaction direction of a UI (web or mobile) without imposing a style: follow the project design system if one exists, otherwise propose 3 contrasting directions and record the choice. Use when starting a screen, app or site, when a UI looks generic or AI-made, or when choosing style, palette, typography, density or motion. FR : « direction artistique », « le front fait générique », « propose des styles », « quelle palette », « design de cet écran »."
---

# Frontend direction

**Rule 0 — the project wins.** If a design system exists (Claude Design synced with `/design-sync`, a tokens file, a component library in the repo, or `.claude/design-direction.md`), follow it and only propose within its bounds. This skill gives options and checks, never a house style.

## 1. Context (ask only what is missing)

Platform(s): web / iOS / Android / cross-platform · audience and tone · existing brand assets · density (data-heavy vs content-led) · constraints (accessibility level, dark mode, languages).

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

## 4. Pre-show checklist

- [ ] Every stylistic choice is intentional and traceable to the direction (no leftover template look)
- [ ] Clear type hierarchy, consistent spacing scale and grid
- [ ] Real content; loading, empty and error states designed
- [ ] AA contrast, visible focus states, touch targets ≥ 44 pt / 48 dp
- [ ] Dark mode handled if in scope

## 5. Audit and QA

If installed: `impeccable` and Vercel `web-design-guidelines` (web). Then `frontend-qa`. Assets: `asset-brief`.

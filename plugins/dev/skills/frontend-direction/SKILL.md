---
name: frontend-direction
description: >
  Orchestrates UI design decisions for a project without imposing one house
  style: follows the project's own design system when it has one, otherwise
  proposes 3 contrasting directions (style family, palette, type pairing,
  density, motion) drawn from a curated reference library, records the
  chosen direction, then routes component and motion work to shadcn/open
  registries (web) or native toolkits (mobile) and closes with free
  audits. Use before building or restyling any screen, page, or app when no
  direction has been chosen yet. English triggers: "what should this look
  like", "pick a design direction", "propose some UI styles", "we don't
  have a design system yet", "design direction for this app". French
  triggers: "quelle direction design", "propose des styles UI", "on n'a pas
  de design system", "à quoi ça doit ressembler". Distinct from
  `ui-vocabulary` (naming components/patterns once a direction exists),
  `asset-brief` (sourcing icons/images once the direction is set), and
  `frontend-qa` (testing after the UI is built) — this is the upstream
  decision, made once per project and revisited only on request.
model: claude-opus-5-5
effort: medium
---

<!-- claude-toolkit: jt33120/claude-toolkit — dev plugin -->

# Frontend Direction

Decides *how a project should look* — once — so every later screen is
consistent with it, and hands off cleanly to component sourcing, motion,
and audits. This skill never pushes one aesthetic: it offers frameworks and
options, and the project's own design system, the client's brief, and
platform conventions always win over anything in `references/`.

## a) A design system already exists — follow it, stop here

Check, in order:

1. `.claude/design-direction.md` at the repo root (this skill's own record
   of a previous decision for *this* project).
2. A Claude Design system synced via `/design-sync` (tokens, components).
3. A tokens file (`tailwind.config.*` theme block, `design-tokens.json`,
   CSS custom properties file, a `theme/` folder) or an existing component
   library already in use in the codebase.

If any of these exist, **use it and stop proposing styles** — read the
existing direction/tokens, apply them to the task at hand, and skip
straight to step (d). Do not re-run step (b) "just to check" once a
direction is recorded; a project's direction changes only when the user
explicitly asks to revisit it.

## b) No design system yet — propose 3 contrasting directions

Ask (if not already clear from the request): what is this, who is it for,
web or mobile (and if mobile: native iOS/Android or cross-platform —
Expo/React Native/Flutter)? Then read `references/styles.csv`,
`references/colors.csv`, and `references/typography.csv` and build **three
genuinely contrasting** directions — not three variations on the same
theme. For each direction, name:

- **Style family** — from `styles.csv` (`Style Category`/`Type` columns),
  pick a real, named style (e.g. neo-brutalist, editorial-serif, soft
  neumorphic, glassmorphism, minimal-swiss) with 2-3 keywords each, not a
  vague adjective.
- **Palette** — one full row from `colors.csv` (primary/secondary/accent +
  surface/text/border/destructive), picked for tonal contrast against the
  other two directions.
- **Type pairing** — one row from `typography.csv` (heading + body font,
  mood keywords), one that reads as visually distinct from the other two.
- **Density** — compact / comfortable / spacious.
- **Motion level** — minimal (state changes only) / purposeful (a few
  signature transitions) / expressive (motion as a brand element).

Adapt every direction to the target platform before presenting it: on web,
name it in terms of layout and CSS; on mobile, translate it into the
platform's own vocabulary (iOS: SF Symbols/Dynamic Type/materials; Android:
Material 3 dynamic color/elevation; cross-platform: what's achievable in
Expo/RN without ejecting). Web and mobile conventions are genuinely
different — don't present an iOS direction with web-only affordances
(hover states, cursor changes) or vice versa (bottom tab bars on desktop
web).

Present the three side by side (short paragraph or table, not full mockups)
and let the user pick one, or mix elements across them if they ask to.

## c) Record the choice

Once a direction is chosen — from (b), or confirmed when following an
existing system in (a) — write or update `.claude/design-direction.md`
with: the chosen style family, palette (actual values, not just the name),
type pairing, density, motion level, platform, and the date decided. This
file is **per project**: never carry a previous project's direction into a
new one, even silently, even if the two look similar — a project with no
`.claude/design-direction.md` yet has no direction until this skill (or the
user) sets one.

## d) Components

**Web:** use the shadcn MCP server (bundled with this plugin's
`.mcp.json`) to browse, search, and install components from the shadcn
registry and any shadcn-compatible open registry configured in the
project (Magic UI, Origin UI, Base UI, React Aria — add a registry's URL
to the project's `components.json` `registries` if it isn't there yet).
Pick components that match the chosen style family and density, not
whatever's fastest to wire up. For exact component/pattern naming across
libraries (what shadcn calls a thing vs. what Base UI or Origin UI calls
the same thing), defer to the `ui-vocabulary` skill.

**Mobile:** use platform-native components — SwiftUI for native iOS,
Jetpack Compose for native Android, Expo UI / React Native primitives for
cross-platform — rather than reimplementing web-style components in a
WebView. Again, `ui-vocabulary` has the exact component names and
platform-appropriate alternatives when a web-first request ("give me a
modal") needs translating to the platform's own idiom (an iOS sheet, an
Android bottom sheet dialog).

## e) Motion

Motion should be purposeful, not decorative: it should confirm an action,
show a spatial relationship (where did this element come from/go to), or
carry brand personality at the level chosen in (b) — never all three at
once on every element. Concretely:

- Match the motion level recorded in `.claude/design-direction.md`:
  minimal = only opacity/color transitions on state change; purposeful =
  add entrance/exit and a couple of signature transitions (e.g. a shared-
  element transition for a card-to-detail flow); expressive = motion is
  part of the brand, but still every individual animation still needs a
  reason.
- Always respect `prefers-reduced-motion` on web (swap to instant/opacity-
  only transitions), and the platform's reduce-motion setting on mobile
  (`UIAccessibility.isReduceMotionEnabled` on iOS,
  `Settings.Global.ANIMATOR_DURATION_SCALE` / the system "Remove
  animations" setting on Android).
- For web CSS/JS motion detail (springs, easing, durations,
  `linear()` curves), the free tier of Motion's docs
  (motion.dev/docs — documentation search and best-practice guidance are
  free with no account; the premium Motion+ tier only gates advanced
  extras like MotionScore audits and 450+ example source) is a good
  reference; don't reach for a paid tool for something CSS can already do.

## f) Close with audits

Before calling the UI done, run whatever of these is available/relevant —
skip silently what isn't installed rather than blocking on it:

- **impeccable** (`pbakaus/impeccable`, Apache-2.0) — if installed in this
  project (project-level `npx impeccable install`, or the
  `pbakaus/impeccable` plugin marketplace), run its design review against
  the direction recorded in step (c). Not bundled or auto-installed by
  this skill; if it isn't present, say so and move on rather than gating
  completion on it. (Not a `skills add` skill — it ships its own CLI.)
- **Vercel web-design-guidelines** (web only) — installed per-project by
  `stack-check` for Vercel/React stacks; if present in the session, run
  its checks against the built UI.
- Both are free/open-source and non-blocking: report what they flag, but
  the call on whether to fix something stays with the human, especially
  for anything that's a deliberate part of the chosen direction rather
  than a genuine defect.

## references/

- `styles.csv`, `colors.csv`, `typography.csv`, `ux-guidelines.csv` —
  ported from `nextlevelbuilder/ui-ux-pro-max-skill` (MIT). These four
  files (the style/palette/type-pairing/UX-guideline data the task
  needs) total ~265 KB; the rest of that project's data (full Google
  Fonts catalog, Phosphor icon manifest, chart/product/reasoning
  catalogs) was left out as out of scope for this skill — icons in
  particular are sourced live by `asset-brief`, not from a static list
  here. See `references/ATTRIBUTION.md` for the full provenance note and
  `references/LICENSE-ui-ux-pro-max-skill` for the upstream license text.
- Treat these as a **starting point for options**, never as a fixed
  catalog to pick from mechanically — the three directions in (b) should
  be genuinely tailored to the request, using this data as raw material
  (real palettes, real type pairings, real UX pitfalls) rather than sole
  source of the wording.

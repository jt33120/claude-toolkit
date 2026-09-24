---
name: asset-brief
description: >
  Decides where each visual asset should come from and executes or hands
  off accordingly: UI icons are sourced live from open icon sets, never
  generated; illustrations, hero images, app icons, marketing visuals, and
  textures are handed off to OpenAI Codex (gpt-image-2) as a manual step —
  a ready-to-paste prompt, never an API call — followed by an integration
  checklist (optimization, responsive sizes, favicon/PWA set, iOS/Android
  app icons). Use when a screen or app needs an icon, illustration, hero
  image, app icon, or marketing visual and it isn't clear where it should
  come from. English triggers: "I need an icon for this", "generate an
  illustration", "we need a hero image", "make an app icon", "what icon
  set should I use". French triggers: "il me faut une icône", "génère une
  illustration", "on a besoin d'une image hero", "fais une icône d'app",
  "quel set d'icônes utiliser". Distinct from `frontend-direction` (sets
  the palette/style this skill's Codex prompts draw from) and `ui-vocabulary`
  (component naming, not visual assets) — this is sourcing and handoff for
  actual image/icon files.
model: claude-opus-5-5
effort: low
---

<!-- claude-toolkit: jt33120/claude-toolkit — dev plugin -->

# Asset Brief

Decides, per asset, whether it should be **sourced** (icons, from an open
set — instant, free, consistent) or **generated** (illustrations, hero
images, app icons, marketing visuals, textures — via a manual OpenAI Codex
handoff, since there's no free/open-source image generator worth using
here and the user's own Codex access is the approved path). Never
generates an icon; never hand-draws or fakes an illustration/photo with
CSS/SVG when the brief actually calls for one.

## Step 1 — Classify the asset

| Asset type | Source |
|---|---|
| UI icon (nav, button, status, action) | Open icon set — see below. Never generated. |
| Illustration, hero image, marketing visual, texture, app icon artwork | Codex handoff — see below. |
| Logo | Ask — usually supplied by the user/brand, not generated here. |

## Step 2 — UI icons: source, never generate

Use an open icon set, matched to the density/style chosen in
`.claude/design-direction.md` (if `frontend-direction` has already run) —
outline sets (Lucide, Tabler) read lighter/more modern; filled/duotone
sets (Phosphor's filled weight) read bolder:

- **Lucide** (ISC license) — the default for shadcn-based web projects;
  most shadcn/Magic UI/Origin UI components already assume it.
- **Phosphor** (MIT) — six weights (thin → fill), broadest range for
  matching a chosen density/motion level.
- **Tabler Icons** (MIT) — large, consistent 24px grid set, good for
  dashboards.
- **Iconify MCP**, if connected in this session (`stack-check` adds it
  per-project on request, it isn't bundled with this plugin) — search and
  fetch across all of the above plus 150+ other open sets from one tool
  instead of browsing each site by hand. If it isn't connected, fall back
  to the set's own site/package (`lucide-react`, `@phosphor-icons/react`,
  `@tabler/icons-react`, or the plain SVG/webfont for non-React stacks).

Pick one set per project and stay consistent — don't mix Lucide and
Phosphor icons in the same UI.

## Step 3 — Everything else: manual Codex handoff

Illustrations, hero images, app-icon artwork, marketing visuals, and
textures go through **OpenAI Codex's `gpt-image-2`**, by hand — this
session cannot call it. Prepare a production-ready prompt following
OpenAI's own prompting guidance (developers.openai.com/cookbook, "GPT
Image Generation Models Prompting Guide"), then output it in a block the
user copies into Codex:

```
👉 Passe sur Codex et colle ce prompt :

[prompt]

Fichiers attendus : <file names + target paths in the repo, e.g.
public/images/hero-desktop@2x.png, public/images/hero-mobile@2x.png>

Dépose les fichiers dans le repo aux emplacements ci-dessus, puis
dis-moi "c'est fait" pour que je fasse l'intégration.
```

Build the prompt with every relevant element, in OpenAI's recommended
order — omit what genuinely doesn't apply, but don't skip a section out of
laziness:

- **Use case / subject** — what this image is for and what's in it,
  concretely (materials, shapes, textures, medium: photo / watercolor / 3D
  render / flat vector).
- **Composition & layout** — viewpoint, framing, where the subject sits in
  frame, safe area for any text/UI that will overlay it.
- **Style anchor** — for a *set* of images (e.g. 3 feature illustrations,
  an icon family), describe the style once precisely and repeat it
  verbatim across every prompt in the set, so Codex/gpt-image-2 renders a
  consistent family rather than three unrelated images. When editing/
  extending an existing generated asset, say explicitly what must stay
  identical (character, palette, proportions) and what may change.
- **Palette** — pull the actual hex values from `.claude/design-direction.md`
  if it exists; don't invent a palette that drifts from the chosen
  direction.
- **Explicit negatives** — state what to exclude: no watermark, no logos/
  trademarks, no embedded text unless the brief calls for text.
- **Size / aspect ratio** — match the target placement (hero, card,
  square app-icon canvas, etc.).
- **Transparent background** — call it out explicitly when the asset needs
  one (icons/illustrations meant to sit over varying backgrounds); Codex
  needs this stated, it isn't the default.

## Step 4 — Integration checklist

Once the user drops the generated (or sourced) files in the repo:

- **Optimize** — raster photos/illustrations to WebP/AVIF (with a
  same-name fallback only if the target browser support requires it);
  vector marks stay SVG (and run through SVGO or equivalent to strip
  editor cruft).
- **Responsive sizes** — generate the srcset sizes the layout actually
  needs (don't ship one 4000px master to a 400px slot); name files
  predictably (`hero-mobile.webp`, `hero-desktop@2x.webp`).
- **Favicon / PWA minimal set** — `favicon.ico` (multi-size, for legacy
  UA support), `favicon-32x32.png`, `favicon-16x16.png`,
  `apple-touch-icon.png` (180×180), `icon-192.png` and `icon-512.png`
  (referenced from `manifest.json`'s `icons` array) — that's the minimal
  set; don't generate every historical size nobody requests anymore.
- **iOS app icon** — a single 1024×1024 master (no transparency, no
  rounded corners — the system applies masking), then build the actual
  app icon with **Icon Composer** (bundled with Xcode 26, or downloadable
  standalone from developer.apple.com/icon-composer — free) as a single
  layered `.icon` file for Liquid Glass: import the master's layers (SVG
  preferred, PNG where SVG isn't practical, text converted to outlines),
  organize into at most 4 groups, and let Icon Composer render the
  default/dark/clear/tinted variants across iOS, iPadOS, macOS, and
  watchOS from that one file instead of hand-exporting every legacy size.
- **Android adaptive icon** — a foreground layer (the mark, in the safe
  zone) and a background layer (solid color or pattern), each their own
  108×108dp asset (with the 72×72dp safe zone respected), wired through
  `mipmap-anydpi-v26/ic_launcher.xml`.

Keep this checklist platform-neutral in the brief itself — which of these
apply depends on whether the project targets web, iOS, Android, or more
than one; skip what the project doesn't ship.

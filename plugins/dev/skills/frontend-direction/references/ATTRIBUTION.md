# Attribution

`styles.csv`, `colors.csv`, `typography.csv`, and `ux-guidelines.csv` in
this directory are ported, unmodified, from:

- **Project:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- **License:** MIT (Copyright (c) 2024 Next Level Builder) — see
  `LICENSE-ui-ux-pro-max-skill` in this directory for the full text.
- **Source paths** (commit `dcc40ff5133ef78276117db0cc34e7b83cc8aeba`):
  - `src/ui-ux-pro-max/data/styles.csv`
  - `src/ui-ux-pro-max/data/colors.csv`
  - `src/ui-ux-pro-max/data/typography.csv`
  - `src/ui-ux-pro-max/data/ux-guidelines.csv`

## What was left out, and why

The upstream `data/` directory holds ~1.3 MB across 14 files. This skill
ports only the four files above (~265 KB total) — the ones the
`frontend-direction` skill actually needs (UI style catalog, color
palettes, font pairings, UX guideline checklist). Left out:

- `google-fonts.csv` (747 KB) and `google-font-licenses.json` (433 KB) —
  a full Google Fonts catalog; `typography.csv`'s font *pairings* already
  cover what this skill uses fonts for, and the full catalog would blow
  past a reasonable reference-data budget for one skill.
- `phosphor-icons-upstream.json` (824 KB) and `icons.csv` (58 KB) — icon
  data. Out of scope here by design: `asset-brief` sources icons live
  from open icon sets (Lucide, Phosphor, Tabler, Iconify) rather than a
  static bundled list.
- `charts.csv`, `landing.csv`, `motion.csv`, `products.csv`,
  `app-interface.csv`, `react-performance.csv`, `ui-reasoning.csv`,
  `data-provenance.json`, `catalog-summary.json` — adjacent catalogs
  (chart types, landing-page patterns, motion presets, industry
  reasoning rules, React perf tips) that overlap with guidance this
  plugin already gives elsewhere (`backend-standards`, `frontend-qa`) or
  that this skill's own step (e) (motion) and vendor audits (step f)
  already cover more directly for this toolkit's purposes.

If a future need justifies porting more of this catalog, re-check the
upstream commit for changes first — this snapshot is pinned to
`dcc40ff5133ef78276117db0cc34e7b83cc8aeba`.

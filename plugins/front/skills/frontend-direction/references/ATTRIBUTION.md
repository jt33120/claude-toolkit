# Attribution

`styles.csv`, `colors.csv`, `typography.csv`, and `ux-guidelines.csv` in
this directory are ported from the following source. The styles catalog was
consolidated in the toolkit; the other three files retain the source data.

- **Project:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- **License:** MIT (Copyright (c) 2024 Next Level Builder) — see
  `LICENSE-ui-ux-pro-max-skill` in this directory for the full text.
- **Source paths** (commit `dcc40ff5133ef78276117db0cc34e7b83cc8aeba`):
  - `src/ui-ux-pro-max/data/styles.csv`
  - `src/ui-ux-pro-max/data/colors.csv`
  - `src/ui-ux-pro-max/data/typography.csv`
  - `src/ui-ux-pro-max/data/ux-guidelines.csv`

## Charts catalog

`charts.csv` is ported unmodified from the same project's
`src/ui-ux-pro-max/data/charts.csv`, commit
`7246805992a42b7bba37d4cac83b01416f0c6c44` (MIT, same license and copyright).
It adds an on-demand chart shortlist, accessibility guidance and alternatives.
The toolkit's original `charts-and-disclosure.md` supplies the selection and
three-level disclosure workflow; it does not require the upstream CLI or libraries.

## Anthropic Frontend Design

`frontend-design.md` adapts `skills/frontend-design/SKILL.md` from `anthropics/skills`,
commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44`, under Apache License 2.0
(see the repository's `licenses/APACHE-2.0.txt` and `NOTICE`).
It is shortened for this toolkit and keeps existing brand rules and the
content/spec contract authoritative. Upstream ASCII planning and mandatory
confirmation are omitted.

## What was left out, and why

The original upstream snapshot's `data/` directory held ~1.3 MB across 14 files. This skill
ports the four original catalogs and the charts catalog — the data used for
UI styles, palettes, font pairings, UX checks and visual selection. Left out:

- `google-fonts.csv` (747 KB) and `google-font-licenses.json` (433 KB) —
  a full Google Fonts catalog; `typography.csv`'s font *pairings* already
  cover what this skill uses fonts for, and the full catalog would blow
  past a reasonable reference-data budget for one skill.
- `phosphor-icons-upstream.json` (824 KB) and `icons.csv` (58 KB) — icon
  data. Out of scope here by design: `asset-brief` sources icons live
  from open icon sets (Lucide, Phosphor, Tabler, Iconify) rather than a
  static bundled list.
- `landing.csv`, `motion.csv`, `products.csv`,
  `app-interface.csv`, `react-performance.csv`, `ui-reasoning.csv`,
  `data-provenance.json`, `catalog-summary.json` — adjacent catalogs
  (landing-page patterns, motion presets, industry
  reasoning rules, React perf tips) that overlap with guidance this
  plugin already gives elsewhere (`backend-standards`, `frontend-qa`) or
  that this skill's motion guidance and vendor audits
  already cover more directly for this toolkit's purposes.

If a future need justifies porting more data, re-check the upstream source
first. The original four catalogs and charts have separate pinned commits
listed above.

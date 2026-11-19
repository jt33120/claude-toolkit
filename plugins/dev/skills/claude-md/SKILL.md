---
name: claude-md
description: "Keep the project's CLAUDE.md short and true: add what a newcomer would get wrong, drop what became false or obvious, 80 lines max. Runs after each compaction (dev hook) or on request. FR : « mets à jour le CLAUDE.md », « retiens ça pour ce repo »."
---

# CLAUDE.md maintenance

`CLAUDE.md` is loaded in full at every session. Every line costs tokens and attention, so it only holds what Claude cannot work out by reading the code.

## When

- After a compaction: the `dev` plugin hook asks for it. Use the compaction summary — it still holds the user's corrections and decisions.
- When the user says « retiens ça », « mets-le dans le CLAUDE.md », or corrects the same thing twice.

## What earns a line

Ask: **would a competent developer, new to this repo, get this wrong?** Keep only yes answers:

- Commands: run the app, the full test suite, **one single test**, lint, build, migrations.
- Traps: wrong venv, generated files not to edit, a cache marker to bump, a proxy, an OS quirk.
- Invariants enforced by tests or CI (layering rules, « X never writes to Y »).
- Conventions that differ from the ecosystem default; deploy and release rules.
- The user's corrections from this session that will recur.

Never add: file trees, lists of components, generic advice (« write tests », « handle errors »), anything already in the README that Claude can read when needed, or one-off task details.

## How

1. Read `CLAUDE.md` (create it with the header below if missing) and `git diff -- CLAUDE.md` to see pending edits by the user — never undo them.
2. Edit in place: add, rewrite or delete lines. Prefer replacing a stale line over adding a new one.
3. Keep it **80 lines or fewer**, the `<!-- stack-check:begin/end -->` block included. Over budget: move path-specific detail to `.claude/rules/<topic>.md` with a `paths:` frontmatter (loaded only when matching files are touched), and leave one pointer line.
4. Do not touch the `@AGENTS.md` import, the stack-check block, or `CLAUDE.local.md` (personal, not versioned).
5. Write without asking, then report **one line**: `CLAUDE.md : +2 / −1 (venv .venv, marqueur ?v=)` — or `CLAUDE.md : rien à changer`.

New file header:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

Writing style for agent instructions: see the `writing-for-agents.md` reference of `core:toolkit-maintainer`.

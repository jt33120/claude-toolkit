---
name: dev-playbook
description: 'Concise map of this toolkit''s dev workflow — which phase uses which tool, and who decides. Use when unsure which skill/command applies ("what should I use for this", "quel outil pour ça", "comment on procède", "workflow dev", "process pour une nouvelle feature"). Not a workflow itself — read this, then invoke the tool it points at.'
model: claude-opus-5-5
effort: low
---

# Dev Playbook

One page, no ceremony. Find your phase, use its tool, respect who decides.

| Phase | Tool | Who decides |
|---|---|---|
| Design (new UI, redesign) | Claude Design, then `/design-sync` | User approves the design before it's wired to code |
| Framing a new project or a major feature | BMAD analyst → PM → architect → UX, in that order, producing PRD → architecture → epics & ultra-detailed stories | User validates each artifact (PRD, architecture, each epic) before the next stage starts |
| Build — a real story | `story-execution` | Orchestrator dispatches; user is the only one who can approve a merge/push |
| Build — a tiny, obvious change | Just do it — no BMAD ceremony, no story-execution. BMAD's own quick flow (a bare `bmad-build` run with route `oneshot`) is fine for something small enough not to warrant a story | You, using judgment — see "when it's small enough" below |
| Bug | `systematic-debugging` | — |
| Before merge | Built-in `/code-review` and `/security-review`, plus this plugin's `security` skill for stack-specific audit (Supabase RLS, Next.js headers, FastAPI auth, etc.) | User merges; nothing here merges on its own |
| Deploy | `infra-deploy` | User approves any production deploy |
| Code navigation | If `graft/` exists at the repo root, query it with the `graft_*` MCP tools before grep/read | — |

## When it's small enough to skip ceremony

A change is "small" when it's a single, obvious edit with no ambiguity about
what "done" means — a typo, a config value, a one-line bug fix, adding a
field to an existing form. If you'd need more than a sentence to describe the
acceptance criteria, it's not small — write a story and run
`story-execution`.

## Framing, in order

1. **Analyst** — problem framing, market/user context.
2. **PM** — PRD: what's being built and why, in requirements the user signs
   off on.
3. **Architect** — architecture: how it's built, the decisions that would be
   expensive to reverse later.
4. **UX** (when there's a UI) — screens/flows before implementation detail.
5. **Epics & stories** — `bmad-create-epics-and-stories`, then
   `bmad-sprint-planning` to generate `sprint-status.yaml`. Stories must be
   ultra-detailed (explicit ACs, explicit files, explicit Dev Notes with
   source citations) — `story-execution`'s implementer subagents get no
   context beyond what the story gives them.

The user validates the PRD, the architecture, and each epic before work
starts on it. Skipping validation to move faster is the single most common
way a large feature drifts from what was actually wanted.

## Build: story-execution vs bmad-build

Use `story-execution` for every real story — it's this plugin's replacement
for running `bmad-build`/`bmad-dev-story` by hand: same story bookkeeping
(Status, Tasks/Subtasks, Dev Agent Record, File List, Change Log,
sprint-status.yaml), but with real implementer/reviewer subagent dispatch and
a bounded fix loop instead of one continuous session doing everything itself.
Reach for BMAD's own quick flow (`bmad-build`, oneshot route) only for a
change too small to be worth a story in the first place — not as a shortcut
around story-execution for something that already has one.

## Models

Every agent in this plugin runs on Claude Opus 5.5, with effort tuned to the
role: `low` for planning/lookup work (this playbook, `setup-repo`,
`backend-standards`' lookup role), `medium` for implementation
(`implementer`, code-review passes), `high` for judgment-heavy review
(`spec-reviewer`, `story-execution`'s own orchestration). Effort is not a
knob to raise "to be safe" — a low-effort agent given a look-up-and-report
job that gets it right is strictly better than the same job run at high
effort for no benefit.

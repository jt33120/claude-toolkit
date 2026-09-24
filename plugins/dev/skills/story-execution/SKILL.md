---
name: story-execution
description: 'Execute ONE BMAD story end to end — locate it, verify it is ready-for-dev, dispatch implementer/reviewer subagents per task with a fix loop, run full verification, then update the story file and sprint-status.yaml exactly like BMAD dev-story does. Use for "execute story 2.3", "implement story 4.1", "dev story <id>", "work the next ready-for-dev story", "implémente la story 2.3", "exécute la story", "développe la story suivante", "avance la story <id>". Not for tiny one-off edits (see dev-playbook) and not for the review or debugging passes themselves (see systematic-debugging, code-review).'
model: claude-opus-5-5
effort: high
---

<!--
Provenance: the dispatch → task-review → fix-loop → final-review shape below is
adapted from obra/superpowers, skills/subagent-driven-development (MIT License,
Copyright (c) 2025 Jesse Vincent). https://github.com/obra/superpowers
The story bookkeeping (Status, Tasks/Subtasks, Dev Agent Record, File List,
Change Log) and sprint-status.yaml semantics replicate what bmad-code-org/
BMAD-METHOD's `bmad-build` skill and its `sync-sprint-status.md` task do
(skills/bmad-build/step-03-implement.md, step-05-present.md,
sync-sprint-status.md; skills/bmad-sprint-planning/scripts/sprint_plan.py for
the exact status vocabulary and story-key grammar), and what the classic
per-story file format still produced by BMAD-METHOD's `v6-shims/bmad-create-story`
and by BMAD module forks (e.g. bmad-code-org/bmad-module-game-dev-studio's
gds-create-story/gds-dev-story) documents as the only story sections a build
may touch. Neither upstream project is vendored; this skill is an original
adaptation for this plugin.
-->

# Story Execution

Runs one BMAD story from `ready-for-dev` to `review`: real subagents write and
review the code, this skill orchestrates and keeps the paper trail. **The
orchestrator never writes production code itself** — only a trivial one-line
fix (a typo, an import) is acceptable inline; everything else goes through
`implementer`.

## 0. Resolve the BMAD project

Look for `_bmad/` at the repo root.

- If present, read `_bmad/core/config.yaml` and `_bmad/bmm/config.yaml` (team/user
  overrides in `_bmad/custom/*.toml` may adjust these — merge scalars-override,
  best-effort) for `modules.bmm.planning_artifacts` and
  `modules.bmm.implementation_artifacts`. These are the two directories
  everything below reads from and writes to.
- If `_bmad/` is missing, stop and say so: this skill assumes a BMAD-initialized
  repo (`npx bmad-method install`). Offer to hand off to `setup-repo` or to
  proceed read-only against whatever `docs/stories` / `docs/prd` layout exists,
  but do not invent BMAD paths.

## 1. Locate the story

The invocation names a story by id (`2.3`, `4.1a`) or by path.

- **By id `E.S`:** the canonical key is `E-S-<slug>` (BMAD story-key grammar —
  epic number, story number, optional split-letter, kebab slug). Search
  `{implementation_artifacts}/sprint-status.yaml`'s `development_status` map
  for a key matching `^E-S[a-z]?-`. If `sprint-status.yaml` doesn't exist yet,
  glob `{implementation_artifacts}/E-S-*.md` directly, or fall back to finding
  a `### Story E.S:` heading inside the epics file under
  `{planning_artifacts}`.
- **By path:** use it directly; still derive the story key from the filename
  (`{key}.md`) so sprint-status.yaml can be kept in sync.
- If nothing matches, stop and say so — do not guess a different story.

## 2. Check status — hard gate

Read the story file's `Status:` field (or, if the story lives only as a
section in the epics file, its `development_status` entry). Normalize legacy
values the same way BMAD does: `drafted` → `ready-for-dev`, `contexted` →
`in-progress`.

| Status found | Action |
|---|---|
| `backlog` | STOP. The story hasn't been written yet — tell the user to run `bmad-create-epics-and-stories` / `bmad-sprint-planning` first. |
| `ready-for-dev` | Proceed. |
| `in-progress` | This is a resume. Read the existing Dev Agent Record / File List / ledger before touching anything, and ask the user to confirm resuming rather than silently restarting. |
| `review` or `done` | STOP. Already implemented — point at `bmad-code-review` (or nothing to do) instead of re-running this skill. |

Never start work against any other status without the user's explicit say-so.

## 3. Load context

Read, in this order:

1. The story file in full (Story, Acceptance Criteria, Tasks/Subtasks, Dev
   Notes — Dev Notes usually cites `[Source: path#section]`; follow those
   citations rather than re-reading whole documents).
2. Only the referenced architecture/PRD sections the Dev Notes point at — not
   the entire architecture or PRD file, unless nothing is cited.
3. `_bmad/bmm/project-context.md` if it exists (house rules the story author
   assumed you already know).

**Code navigation:** if a `graft/` folder exists at the repo root, use the
`graft_*` MCP tools to find the relevant symbols/call sites before falling
back to grep/read (see `dev-playbook`). Without `graft/`, use targeted
Grep/Glob/Read — never a broad unscoped read of the whole codebase.

## 4. Baseline and claim the story

Before any edit:

- Capture `baseline_commit` = `git rev-parse HEAD` (or `NO_VCS`) into the
  story file's frontmatter — **unless it's already set from a prior resumed
  run**, in which case preserve it untouched.
- Set the story's `Status:` to `in-progress`.
- If `sprint-status.yaml` exists, update `development_status[{story_key}]` to
  `in-progress` (merge — never downgrade a status that's already ahead), and
  flip the parent epic (`epic-{E}`) from `backlog` to `in-progress` if this is
  its first story starting. Preserve the file's comments/structure — read it,
  patch only the changed keys, write it back; do not regenerate it from
  scratch.
- Content inside any human-authored/frozen section of the story (however the
  project marks it — e.g. a `<frozen-after-approval>` block, or a Dev Notes
  section) is **read-only**. Never edit it; if it's wrong, stop and say so.

## 5. Build the task list

Parse the story's Tasks/Subtasks checklist into discrete units of work. For
each task, note the files it touches (the story usually names them; if not,
a quick Grep/graft lookup before dispatch is worth it — the implementer
brief should name files, not make the subagent go hunting).

**Parallelism:** two or more tasks may be dispatched together only when their
file sets are provably disjoint (no shared file, no producer/consumer
relationship between them). Default to sequential — a wrong parallel dispatch
produces a merge conflict a fresh subagent cannot resolve. Never dispatch more
than one implementer against the same file at the same time.

## 6. Per-task loop

For each task (or disjoint parallel batch):

1. **Dispatch `implementer`** using `implementer-brief-template.md` filled
   in with: the task text, the ACs it must satisfy, the files involved,
   project constraints (this repo's lint/format/test commands), and which
   standards skills to load (`tdd` always; `backend-standards` for
   backend/API/DB code; any vendor skill already installed under
   `.claude/skills/` that's relevant — e.g. a Supabase or Next.js skill).
   One implementer dispatch per task; never split one task's work across
   two parallel implementers.
2. **On DONE/DONE_WITH_CONCERNS:** capture the diff since this task's base
   commit (`git diff <task-base>..HEAD`), then:
   - Dispatch `spec-reviewer` with `spec-review-brief-template.md` — does
     the diff satisfy exactly this task's ACs, nothing missing, nothing
     extra.
   - Dispatch a **code-review** pass with `code-review-brief-template.md`
     (this plugin's/toolkit's `code-reviewer` agent, if installed — if not,
     perform the same checklist as a normal review step yourself, without
     writing fixes inline).
   - Conditionally dispatch, only when the diff touches the matching
     surface: `silent-failure-hunter` (error handling changed —
     try/catch, error returns, retries), `type-design-analyzer` (new
     types/interfaces/models introduced), `pr-test-analyzer` (tests were
     added or changed).
3. **On BLOCKED/NEEDS_CONTEXT:** resolve what's missing (more context, a
   decision only you can make from the story/architecture) and re-dispatch;
   never force a retry with nothing changed.
4. **Fix loop:** any Critical/Important finding from spec-reviewer,
   code-reviewer, or a conditional reviewer sends the findings back to the
   same implementer subagent (or a fresh one if the platform can't resume
   it) to fix. **Maximum 3 iterations per task.** If findings are still open
   after iteration 3, stop this story and escalate to the user with: the
   task, the open findings, and what was tried — do not silently ship
   unresolved Critical/Important findings, and do not keep looping past the
   cap.
5. Once clean (or the user has explicitly accepted a residual minor
   finding), record the task's commits and move to the next task.

## 7. Full verification

Once every task is done, dispatch (or run directly if no such skill/agent is
installed) `verification-before-completion`: the project's full test suite,
lint, and typecheck — not just the tests touched by this story. A story does
not reach `review` on green individual-task tests alone.

## 8. Update the story exactly like BMAD dev-story

The **only** parts of the story file this skill (or the implementer) may
touch are: frontmatter `baseline_commit`, the Tasks/Subtasks checkboxes,
**Dev Agent Record** (Agent Model Used, Debug Log references, Completion
Notes), **File List**, **Change Log**, and **Status**. Everything else —
Story, Acceptance Criteria, Dev Notes, any frozen section — is read-only.

- Check off every completed Tasks/Subtasks item.
- Dev Agent Record: note the agent model used for implementation, a pointer
  to debug/test output if the project keeps one, and a short Completion
  Notes paragraph (what was built, any deviation from the plan and why).
- File List: every file created, modified, or deleted across all tasks.
- Change Log: one dated entry summarizing the story's implementation.
- Status → `review` (not `done` — a human or `bmad-code-review` decides
  `done`).
- If `sprint-status.yaml` exists, sync `development_status[{story_key}]` to
  `review` the same way step 4 synced it to `in-progress` (merge, never
  downgrade, preserve structure/comments).

## 9. Commit — never push

If the tree is dirty, create **one local commit** per completed story with a
conventional message derived from the story title (e.g.
`feat(2-3): add guest checkout`). Never push, never open a PR, never touch a
shared branch — that decision belongs to the user (see the four-stop
conditions in `dev-playbook`).

## 10. Report

A short completion summary: what changed, the verification result, whether
anything was deferred or escalated, and the commit hash. Do not restate the
diff or narrate the process. Offer next steps in one line: run
`bmad-code-review`, open a PR, or start the next ready-for-dev story.

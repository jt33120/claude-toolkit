---
name: stack-check
description: >
  Confirms every component of this project's declared stack (database, backend,
  frontend, repo, and anything else declared) is actually connected via MCP with
  read and write access, and reports a matrix. On first run (no `.claude/stack.yaml`
  yet) it also asks for the stack, wires `.claude/settings.json`, installs matching
  vendor skills, and inits Graft/BMAD. Run this at the start of a dev session, or
  explicitly. English triggers: "check my stack", "is everything connected", "stack
  check", "verify my connections", "start of a dev session". French triggers:
  "vérifie la stack", "vérifie ma stack", "est-ce que tout est branché",
  "stack-check", "vérifie mes connexions". Distinct from `infra-deploy` (deploy
  checklist / incident response) and `security` (security audit) — this is
  connectivity and read/write permission verification only.
---

<!-- claude-toolkit: jt33120/claude-toolkit — dev plugin -->

# Stack Check

Two modes depending on whether `.claude/stack.yaml` exists yet:

- **INIT** (first run, file missing): the user declares the stack, this skill
  writes it down, then bootstraps the repo once (settings, vendor skills,
  Graft, BMAD, `CLAUDE.md` rules).
- **CHECK** (every other run): re-read the declared stack and verify, live,
  that each component is reachable through MCP with read and write access.

Keep every run fast and cheap — this is a connectivity check, not an audit.
Prefer one lightweight, real call per component over parsing everything a
connector offers.

## a) INIT — first run only

Triggered when `.claude/stack.yaml` doesn't exist. If the user typed the
stack inline, use that; otherwise ask, in plain language, for: database
(Supabase or Neon, project ref/id, and which environment is production),
backend (Railway project/service/environments), frontend (Vercel project),
repo (GitHub owner/repo), and any other MCP-connected tool worth tracking.
Write the answer to `.claude/stack.yaml` using `templates/stack.yaml` as the
shape — keep the comments, drop unused sections.

Then, in order:

1. **Merge `.claude/settings.json` — never clobber.** Read the existing file
   (empty object if none). Merge in `templates/settings.json`'s
   `extraKnownMarketplaces` and `enabledPlugins` entries — add missing keys,
   keep everything already there, never overwrite a value the user set. The
   `trailofbits` marketplace + `modern-python@trailofbits` entries are
   conditional: merge them only when the declared backend is Python
   (FastAPI or otherwise); skip them for every other stack.

2. **Install vendor skills matching the declared stack**, via the `skills`
   CLI (project scope, targeting Claude Code — `-a claude-code -y`), only
   for stacks actually declared:
   - Supabase: `npx skills add supabase/agent-skills --skill supabase --skill supabase-postgres-best-practices -a claude-code -y`
   - Neon: `npx skills add neondatabase/agent-skills --skill neon-postgres -a claude-code -y`
   - React / Next.js / Vercel frontend: `npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines --skill vercel-optimize -a claude-code -y`
   - FastAPI backend: `npx skills add fastapi/fastapi --skill fastapi -a claude-code -y`
     (the skill lives at `fastapi/.agents/skills/fastapi/SKILL.md` inside the
     `fastapi/fastapi` repo — confirmed to exist, frontmatter `name: fastapi`)
   - Frontend / mobile (web, iOS, Android, Expo/React Native): follow `references/frontend-mobile.md` — free/open-source tools only.
   Skip any line whose stack wasn't declared.

3. **Init Graft:**
   ```bash
   npx @nanonets/graft init --agents claude --no-global
   ```
   Gives every skill in this plugin a code graph to query instead of blind
   grep, once `graft/` exists at the repo root.

4. **Init BMAD — check before acting, don't double-install.** BMAD's
   Claude Code *plugin* (`bmad-method`/`bmad-toolbox` from the
   `bmad-code-org/bmad-plugins` marketplace) only gives the tool access to
   BMAD's agents and skills — it does not by itself configure a project.
   Current upstream guidance (bmad-code-org/BMAD-METHOD README) is to open
   the coding tool in the project and **ask the bundled `bmad` skill to run
   `bmad setup`** — not to shell out to `npx bmad-method install` directly.
   So: look for a sign the project is already initialized (a `bmad/` or
   `_bmad/` folder, or a BMAD config file such as `core-config.yaml`, at the
   repo root). If none exists, invoke BMAD's own setup (`bmad setup`, via the
   `bmad-method` plugin) rather than running an install command by hand, and
   do it once — never re-run it just because this skill runs again later.

5. **Append the `CLAUDE.md` snippet — idempotent.** Read `CLAUDE.md` at the
   repo root (create it if missing). If the markers
   `<!-- stack-check:begin -->` / `<!-- stack-check:end -->` are already
   present, leave it alone. Otherwise append the block from
   `templates/CLAUDE.md.snippet` verbatim, markers included.

6. **Show the full diff, then ask.** Not a summary — the actual diff of
   `.claude/settings.json`, `.claude/stack.yaml`, any new
   `.claude/skills/*`, `graft/`, BMAD's own files, and `CLAUDE.md`. Ask
   explicitly whether to commit. On yes, one commit,
   `chore: bootstrap Claude/BMAD/Graft tooling for this repo`. On no or no
   answer, leave everything staged/unstaged — never commit without an
   explicit yes.

After INIT finishes, run CHECK once so the first session ends with a matrix,
not just a setup log.

## b) CHECK — every run

For each component declared in `.claude/stack.yaml`:

### 1. Find the tool

Tool names for the same connector vary across accounts and connector
versions (`mcp__Supabase__*`, `mcp__claude_ai_Supabase__*`, and similar). Use
`ToolSearch` with the provider's name as a keyword to find what this session
actually has, rather than assuming a fixed prefix. If nothing matches for a
declared component, that component is **❌ non connecté** — report which
connector to add and move on; don't fail the whole check over one missing
connector.

### 2. Read probe — one cheap, real call

- **Supabase:** `list_projects`, or `get_project`/`list_tables` scoped to
  the declared project ref.
- **Neon:** `list_projects`, or `describe_project` scoped to the declared
  project id.
- **Railway:** `whoami`, then `list-services`/`list-variables` scoped to the
  declared project/service.
- **Vercel:** `list_projects`, or `get_project`/`list_deployments` scoped to
  the declared project.
- **GitHub:** `get_me`, then `get_file_contents` on the declared repo (e.g.
  its root or README).

A call that returns data is **✅**. An auth/permission error is **❌ lecture
refusée**. A missing tool is **❌ non connecté** (see above).

### 3. Write level 1 — default, non-destructive, no calls that change data

Check that write-capable tools are actually *exposed* in this session (not
just read tools — e.g. a connector in read-only mode won't list them), and
that the account's role is adequate wherever that's checkable without a
write call:

- **Supabase:** `apply_migration`/`execute_sql` present.
- **Neon:** the server's own instructions/notice says write mode is active
  (Neon's MCP server states this explicitly when destructive tools are
  exposed — treat its absence as read-only).
- **Railway:** `set-variables` present.
- **Vercel:** `create_project_env` present.
- **GitHub:** `push_files`/`create_branch` present, and (when checkable)
  `get_me` or a collaborator listing shows write/push access on the repo.

Present + adequate role → **✅**. Tools present but role looks read-only, or
role isn't checkable → **⚠️ écriture présumée, non prouvée**. Tools absent →
**❌**.

### 4. Write level 2 — opt-in only, `--write-probe`

Only when the user explicitly asks for it (e.g. runs `/stack-check
--write-probe`), and **never** against an environment `stack.yaml` marks
`production: true`. Only probe a component if a matching delete/undo tool
actually exists in this session for it — otherwise leave it at whatever
level 1 found and report **⚠️ écriture présumée, non prouvée** for that row
instead of guessing:

- **Neon:** `create_branch` on a non-prod parent, then `delete_branch` it.
- **GitHub:** `create_branch` off a non-prod default; delete it afterwards
  only if a branch-deletion tool is available in this session — if not,
  leave the branch and say so explicitly rather than silently skipping.
- **Railway:** `set-variables` a `CLAUDE_PROBE` key on a non-prod
  environment, confirm it, then remove it the same way.
- **Vercel:** create an env var scoped to the `preview` target via
  `create_project_env`, confirm it, then remove it — only if a removal tool
  is present in this session; if there isn't one, don't create it in the
  first place and report **⚠️ écriture présumée, non prouvée**.
- **Supabase:** level 1 only, always — Neon-style throwaway branches are
  billed on Supabase, so this skill never creates one just to prove a point.

**Always clean up.** Before reporting, re-check that anything level 2
created was actually removed, and call out in the report anything that
couldn't be cleaned up (so the user can remove it by hand).

## c) Output — the matrix

Report in French, one row per declared component:

| Brique | Outil MCP | Lecture | Écriture | Action si ❌/⚠️ |
|---|---|---|---|---|
| DB (ex. Supabase) | `mcp__Supabase__*` | ✅ | ✅ | — |
| Backend (ex. Railway) | `mcp__Railway__*` | ✅ | ⚠️ | Vérifier le rôle du compte sur le projet |
| Front (ex. Vercel) | `mcp__Vercel__*` | ❌ | ❌ | Connecter le MCP Vercel |
| Repo (GitHub) | `mcp__Github_MCP__*` | ✅ | ✅ | — |

Below the table, add:

- **Claude Design** — if a Claude Design/`import-claude-design-from-url`-style
  tool is reachable in this session, say so; otherwise say authorization
  status can't be checked from here (it's a VS Code "/" menu, machine-level
  grant) and point the user at it.
- **Git** — current branch and whether the working tree is clean, from
  `git status`/`git branch --show-current`.

Keep the write-up to the table plus these two lines — no extra narrative.
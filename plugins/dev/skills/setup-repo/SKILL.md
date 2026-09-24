---
name: setup-repo
description: 'Manual, one-time repo bootstrap: detect the stack, wire up .claude/settings.json (claude-toolkit + BMAD + Anthropic security-guidance marketplaces and plugins), install relevant vendor skills, init Graft and BMAD, then show the full diff and ask before committing. Invoke explicitly ("set up this repo", "configure ce repo", "initialise ce projet pour Claude") — never triggered automatically.'
disable-model-invocation: true
model: claude-opus-5-5
effort: low
---

# Setup Repo

One-time, explicit-invocation-only bootstrap for a repo that will use this
toolkit and BMAD. Never runs unprompted, and never commits without the user
looking at the diff first.

## 1. Detect the stack

Look for, in the repo root and one level down:

| Signal | Stack |
|---|---|
| `package.json` with `next`, `react`, or `react-dom` | Next.js / React |
| `@supabase/supabase-js`, `@supabase/ssr` in `package.json`, or a `supabase/` folder | Supabase |
| `@neondatabase/serverless`, or a `DATABASE_URL`/`.env*` referencing `neon.tech` | Neon |
| `pyproject.toml` / `requirements.txt` naming `fastapi` | FastAPI / Python |
| `package.json` with `express`, `fastify`, `koa`, or `@nestjs/core` (no `next`) | Node backend |
| `vercel.json`, or `package.json` with a `vercel` script/dep | Vercel |
| `railway.json` / `railway.toml` | Railway |

Report what was detected before changing anything. If nothing matches a row,
say so rather than guessing.

## 2. Merge `.claude/settings.json` — never clobber

Read the existing `.claude/settings.json` if one exists (empty object if not).
**Merge** the following into it — add missing keys, keep everything already
there, never overwrite a value the user already set:

- `extraKnownMarketplaces`:
  - `claude-toolkit` → `{"source": {"source": "github", "repo": "jt33120/claude-toolkit"}}`
  - `bmad` → `{"source": {"source": "github", "repo": "bmad-code-org/bmad-plugins"}}` (the BMAD marketplace's own `name` field in its `marketplace.json` is `"bmad"` — use that as the key, not `"bmad-plugins"`)
  - `claude-code-plugins` → `{"source": {"source": "github", "repo": "anthropics/claude-code"}}` (Anthropic's official bundled-plugins marketplace; its `marketplace.json` name is `"claude-code-plugins"`, not `"anthropics/claude-code"`)
- `enabledPlugins`:
  - `"core@claude-toolkit": true`
  - `"dev@claude-toolkit": true`
  - `"bmad-method@bmad": true` (BMAD Method core — agents/workflows for analysis, planning, architecture, implementation)
  - `"bmad-toolbox@bmad": true` (BMAD's standalone utility skills)
  - `"security-guidance@claude-code-plugins": true` (Anthropic's security-reminder hook plugin)

`templates/settings.json` in this skill has the exact shape to merge in. Use
it as the source of truth for key names and nesting, not as a file to copy
over the user's — merge field by field.

## 3. Install relevant vendor skills

Only for stacks actually detected in step 1, using the `skills` CLI
(`npx skills add`, project scope, targeting Claude Code):

- **Supabase:** `npx skills add supabase/agent-skills --skill '*' -a claude-code -y`
- **Neon:** `npx skills add neondatabase/agent-skills --skill neon --skill neon-postgres -a claude-code -y`
- **React / Next.js:** `npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines -a claude-code -y`
- **Vercel deploy target:** `npx skills add vercel-labs/agent-skills --skill vercel-optimize -a claude-code -y`

Repeat `--skill` for multiple skills in one call (as above); `-a claude-code`
targets Claude Code, `-y` skips prompts, and the default install scope is the
project (`.claude/skills/`). Skip any of the above whose stack wasn't
detected — do not install skills for a stack the repo doesn't have.

## 4. Init Graft

```bash
npx @nanonets/graft init --agents claude --no-global
```

Gives `story-execution` (and everything else in this plugin) a code graph to
query instead of blind grep, once `graft/` exists at the repo root.

## 5. Init BMAD, if not already

Check for `_bmad/` at the repo root. If it's missing:

```bash
npx bmad-method install
```

Follow its own interactive prompts (module selection etc.) rather than
pre-answering them — this is the one step in this skill that isn't silent,
because BMAD's installer asks its own questions.

## 6. Show the diff, then ask

Before committing anything:

- Show the user the full diff (`.claude/settings.json`, any new
  `.claude/skills/*`, `graft/`, `_bmad/`) — not a summary, the actual diff.
- Ask explicitly whether to commit. On yes, one commit,
  `chore: bootstrap Claude/BMAD/Graft tooling for this repo`. On no, or no
  answer, leave the changes staged/unstaged for the user to handle — never
  commit on their behalf without an explicit yes.

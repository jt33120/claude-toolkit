---
name: agent-bridge
description: "Share project context, skills and MCP servers between Claude Code and OpenAI Codex so switching tools loses nothing: AGENTS.md as the single shared instructions file imported by CLAUDE.md, repo skills in .agents/skills linked into .claude/skills, toolkit skills exposed to Codex, MCP config translated for Codex. Use when a repo is used with both tools, when switching to Codex, or when context files diverge. FR : « partage avec codex », « AGENTS.md », « je passe sur codex », « synchronise claude et codex », « mêmes skills dans codex »."
model: claude-opus-5-5
effort: low
---

# Agent bridge (Claude Code ↔ Codex)

## How each tool reads things (checked Sept. 2026)

| | Claude Code | Codex |
|---|---|---|
| Instructions | `CLAUDE.md`; reads `AGENTS.md` only when no `CLAUDE.md`/`CLAUDE.local.md` exists (v2.1.277+), or always via `@AGENTS.md` import | `AGENTS.md` |
| Repo skills | `.claude/skills/` (does **not** read `.agents/`) | `.agents/skills/` from cwd up to repo root |
| User skills | plugins (claude-toolkit), `~/.claude/skills` | `~/.agents/skills` |
| MCP | `.mcp.json`, plugin `.mcp.json` | `~/.codex/config.toml` `[mcp_servers.*]` |

## Setup (run `scripts/bridge.py`, dry-run first, then `--apply`)

1. **Context — one source:** `python3 scripts/bridge.py context`. Shared rules go to `AGENTS.md`; `CLAUDE.md` becomes `@AGENTS.md` + a short "Claude Code only" section (plugins, Claude-specific tools). The explicit import works in every Claude session, including ones where native AGENTS.md reading is unavailable, and survives a `CLAUDE.local.md`.
2. **Repo skills:** `python3 scripts/bridge.py skills` — moves skills into `.agents/skills/` and links each into `.claude/skills/` (copies on Windows without symlink rights). Commit both.
3. **Toolkit skills for Codex:** clone `jt33120/claude-toolkit` once, then `python3 scripts/bridge.py toolkit ~/path/to/claude-toolkit --apply`. A `git pull` in the clone updates Codex. Claude keeps using the plugins.
4. **Vendor skills:** install for both with `npx skills add <repo> --skill <name> -a claude-code -a codex -y`.
5. **MCP:** `python3 scripts/bridge.py mcp` prints the Codex TOML for the repo's `.mcp.json`; the user pastes it into `~/.codex/config.toml` after review (never write secrets into it; use env vars).

## Rules

- Tool-neutral content only in `AGENTS.md` (stack, commands, conventions, BMAD rhythm). Nothing that names a Claude-only tool.
- When the user switches tool mid-task, write the current state (goal, done, next step, open questions) in `.agents/HANDOFF.md` so the other agent resumes without re-explaining. Delete it once resumed.
- Re-run `context` and `skills` after adding skills or when the two files drift.
---
name: agent-bridge
description: >
  Share project instructions and skills between Claude Code and Codex using AGENTS.md,
  a CLAUDE.md import and compatible skill directories. Assist with reversible local
  migration, MCP configuration and handoffs. Use when switching between Claude Code
  and Codex or when project instructions drift. FR : « partage avec codex »,
  « AGENTS.md », « synchronise claude et codex », « mêmes skills dans codex ».
---

# Agent bridge (Claude Code ↔ Codex)

| Content | Claude Code | Codex |
|---|---|---|
| Project instructions | `CLAUDE.md` with `@AGENTS.md` import | `AGENTS.md` |
| Project skills | `.claude/skills/` | `.agents/skills/` |
| User skills | Claude plugins or `~/.claude/skills/` | Installed plugins or `~/.agents/skills/` |
| MCP | `.mcp.json` or plugin config | `~/.codex/config.toml` locally; configure other hosts separately |

## Local setup

Locate `bridge.py` inside this installed skill's `scripts/` folder. **Run it from the target project's root with its absolute path**, for example:

```bash
python3 /absolute/path/to/claude-toolkit/plugins/core/skills/agent-bridge/scripts/bridge.py context
python3 /absolute/path/to/claude-toolkit/plugins/core/skills/agent-bridge/scripts/bridge.py context --apply
```

The first invocation is a dry run. Use the same absolute script path for `skills`, `toolkit /absolute/path/to/claude-toolkit`, and `mcp`; add `--apply` to make file changes where applicable.

- **Context:** When `AGENTS.md` exists, add `@AGENTS.md` to `CLAUDE.md` while retaining its existing content. When only `CLAUDE.md` exists, the script leaves it alone: manually copy the shared rules to `AGENTS.md` and review any overlap before rerunning. Keep Claude-specific instructions in `CLAUDE.md`. The import also avoids relying on version-specific behavior for automatically reading `AGENTS.md`.
- **Repo skills:** Copy Claude skill folders into `.agents/skills/` for review; retain originals. Link the shared skill back into `.claude/skills/` only if no original exists. Resolve duplicates manually before deleting any original. Where symlinks are unavailable (including Windows without permission), managed copies are refreshed on rerun only if they have no local edits.
- **Toolkit locally:** With a local clone of this repo, `toolkit PATH --apply` exposes all plugin skills to local Codex. Re-run after updating the clone to refresh managed copies on Windows. Alternatively install the portable plugins through the Codex plugin catalog where supported. Each cloud host or conversation needs its own installation; local filesystem links do not install a plugin in ChatGPT Work.
- **MCP:** `mcp` prints a TOML starting point from a project's `.mcp.json`. Inspect it before adding to local Codex config. It forwards environment variable *names* with `env_vars`, never credential values. Configure authentication for each environment separately; the bridge does not transfer remote credentials or make MCP servers automatically available in Work/cloud.

When switching agents mid-task, leave a concise `.agents/HANDOFF.md` with goal, completed work, next step and open questions; remove it after the handoff. Keep tool-neutral project instructions in `AGENTS.md`.

Codex `/import` in a local terminal session can bring selected Claude Code setup into Codex. It is an import operation; it does not run Claude. A deliberate local call to Claude Code (for example `claude -p` with the user's own installation and authorization) is a separate workflow. In the desktop app the import is in Settings; remote tasks do not provide the terminal `/import` command.

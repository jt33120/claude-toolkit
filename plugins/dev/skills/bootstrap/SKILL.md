---
name: bootstrap
description: "Prepare a repository for Claude Code in one pass: a short CLAUDE.md, plugins enabled in .claude/settings.json, stack-check, AGENTS.md if Codex is used, then a baseline audit. Use at the start of a project or on a repo without CLAUDE.md. FR : « prépare ce repo », « initialise le projet pour claude »."
disable-model-invocation: true
---

# Bootstrap

Run once per repository. Each step keeps the confirmation its own skill asks for; stop and report if one fails.

1. **CLAUDE.md** — read the README, the manifests (`package.json`, `pyproject.toml`, `Makefile`, CI files) and any `.cursorrules` / `.github/copilot-instructions.md`. Write `CLAUDE.md` with the `claude-md` rules: real commands (including one single test), traps, invariants, non-default conventions — 80 lines max, the stack-check block included, so aim for about 60 here. Existing file: improve it, never discard the user's lines.
2. **Stack and plugins** — run `stack-check`. It writes `.claude/stack.yaml`, merges `.claude/settings.json` (toolkit marketplace, `core` and `dev`, `front` only with a UI, `media` only for video) and adds its block to `CLAUDE.md`. Committed, that file makes every machine offer the same plugins when the repo is opened.
3. **Codex** — if the user also works with Codex, run `core:agent-bridge`.
4. **Git hygiene** — make sure `.gitignore` lists `.claude/settings.local.json` and `CLAUDE.local.md`; never stage secrets or `.env`.
5. **Baseline** — run `audit` on the whole repo in **report-only** mode: change no source, config or `.env` file. Give the user the five most important items, not the full list; fixes come later, on request, in their own commits.

End with what was created or changed and the next step: commit `CLAUDE.md`, `.claude/settings.json` and `.claude/stack.yaml`. In cloud sessions, plugins come from the environment's setup script (see the toolkit README), not from local installs.

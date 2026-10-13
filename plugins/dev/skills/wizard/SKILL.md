---
name: wizard
description: "Generate an interactive bash wizard that walks the user through steps only a human can do: creating API keys in a third-party dashboard, setting .env values and GitHub secrets, a one-off migration or cutover. Use when setup needs clicks in a web console or values only the user can copy. Not for steps the agent can run itself. FR : « crée-moi un assistant de configuration », « guide-moi pour récupérer les clés », « configure les secrets », « procédure manuelle pas à pas »."
---

<!-- Adapted from mattpocock/skills (MIT) — https://github.com/mattpocock/skills — modified for jt33120/claude-toolkit -->

# Wizard

A wizard is a bash script that walks the user through a manual procedure: it opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at each stage and shows progress. The UX lives in `scripts/template.sh`; never edit the library above its `STAGES` marker. Your job is to scope the procedure and write its stages.

Ephemeral by default (scratch path, deleted after use). Commit it under `scripts/` only when the user wants a repeatable setup path, and link it from the README.

## 1. Scope

Read the repo before asking: `.env*`, `README`, `docker-compose*`, framework config, `.github/workflows/*` (every `secrets.*` / `vars.*` is a value to produce), `.claude/stack.yaml`. For a migration: current state, target state, irreversible actions between them.

Show the ordered stages and the values each produces; the user may add, drop or reorder.

Done when, for every captured value, you know where the human gets it, where it is written (`.env`, GitHub secret, both, nowhere) and whether it is secret.

## 2. Map each stage

Write the exact path a stranger could follow: URL, then "Dashboard → Developers → API keys → Reveal → copy". When the current UI or command is uncertain, check the vendor docs or ask; never invent a menu.

## 3. Write the wizard

Copy `scripts/template.sh` to the target path, replace the example stage with one `stage` per step in dependency order, set `TOTAL_STAGES`. Helpers: `stage`, `say`, `step`, `note`, `warn`, `open_url`, `ask`, `ask_secret`, `write_env`, `set_secret`, `set_var`, `pause`, `confirm`.

- Open the URL before asking for its value; `ask_secret` for anything secret.
- `write_env` every persisted value; `set_secret` only what CI actually reads.
- `confirm` before any irreversible action.
- One focused task per stage (each stage clears the screen).
- Check `.env` is in `.gitignore`; add it if missing.

## 4. Verify and hand off

- `bash -n <script>`, `shellcheck` if available, `chmod +x`.
- Do not run it yourself (it opens browsers and waits for input). Trace it statically: every value from step 1 is captured and lands where planned; every `set_secret` name matches a `secrets.*` reference in CI.
- Give the user the exact command to run, on their machine.

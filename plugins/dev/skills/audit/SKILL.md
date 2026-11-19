---
name: audit
description: "Deep quality review — architecture, readability, error handling, tests, security, CLAUDE.md compliance. `/dev:audit` for the whole repo, `/dev:audit diff` for the branch before a PR (required by the dev hook). FR : « audite le repo », « critique mon code », « revue avant PR »."
argument-hint: "[diff]"
---

# Audit

Goal: code a reviewer can read and trust — clear structure, explicit failures, tests in proportion to risk, no security hole.

## Scope

- `diff` → the branch against the default branch: `git diff $(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD main)...HEAD`. Used before every PR or MR.
- No argument → the whole repository. Start from the entry points and the modules most changed recently (`git log --since=3.months --name-only`), not every file.

## Passes

Run them in this order; delegate the agent passes in parallel on the same scope.

1. **Architecture** — `backend-standards` review checklist: layers and dependency direction, boundaries (I/O at the edges, pure core), one place per responsibility, duplication across modules, coupling to frameworks, API and data conventions. For a UI, `front:critique` replaces it.
2. **Readability** — agents `code-simplifier` and `type-design-analyzer`: names, function size, dead code, needless abstraction, types that encode invariants.
3. **Failures** — agent `silent-failure-hunter`: swallowed errors, broad catches, silent fallbacks, missing timeouts.
4. **Tests** — agent `pr-test-analyzer`, sized with `tdd` and the project stage (`.claude/stack.yaml`).
5. **Security** — `security` skill: run its deterministic script (`python <security skill dir>/scripts/audit.py <repo> --no-external`), then its manual review; in `diff` mode, the built-in `/security-review` as well.
6. **Project rules** — agent `code-reviewer` against `CLAUDE.md`, `.claude/rules/` and `AGENTS.md`.

## Output

A single list ranked by severity — **bloquant**, **à corriger**, **suggestion** — each with `file:line`, the problem in one sentence and the fix. No praise, no restating the code.

Then:

- In `diff` mode, fix the obvious, local, behaviour-preserving items directly and run the relevant tests. In whole-repo mode (and always when called from `bootstrap`), report only: change nothing until the user picks what to fix. Never edit `.env` or environment files without an explicit request.
- Leave design changes and anything ambiguous to the user, as a question.
- If a recurring rule emerged (« on n'importe jamais X depuis Y »), apply `claude-md` to record it.
- In `diff` mode, once no **bloquant** item remains, record the pass so the dev hook lets the PR through:

  ```bash
  git rev-parse HEAD > "$(git rev-parse --git-dir)/claude-audit-ok"
  ```

  A new commit invalidates it. If the user explicitly declines the review, run the same command and say so.

# Code Review Dispatch Brief

<!--
Provenance: adapted from obra/superpowers, skills/subagent-driven-development/
task-reviewer-prompt.md — Part 2 (Code Quality) (MIT License, Copyright (c)
2025 Jesse Vincent), split out and retargeted to a BMAD story task's diff.
https://github.com/obra/superpowers
-->

Dispatch this after spec-reviewer passes (or in parallel with it — the two
are independent gates). Prefer this toolkit's own `code-reviewer` agent when
installed; use this brief as its task-scoped input either way.

```
Subagent: code-reviewer (or general-purpose if not installed)
description: "Code review — story {{story_key}} task {{task_number}}"
model: claude-opus-5-5
effort: medium
prompt: |
  You are reviewing one task's implementation for code quality — not spec
  compliance (that gate runs separately). This is a task-scoped gate; the
  broad whole-story review happens once, in verification-before-completion.

  ## Diff under review

  Base: {{base_sha}}   Head: {{head_sha}}
  {{diff_file_path_or_inline_diff}}

  Read-only review — do not mutate the working tree, index, or HEAD.

  ## You do not dispatch subagents

  Do this review yourself; never spawn a helper or a second opinion.

  ## Check

  **Correctness & error handling**
  - Proper error handling — no swallowed errors, no silently-ignored
    failure paths.
  - Edge cases named in the story's I/O matrix or ACs, if any, are handled.

  **Design**
  - Clean separation of concerns; DRY without premature abstraction.
  - Each touched/new file has one clear responsibility.
  - Follows this codebase's existing patterns rather than inventing new
    ones for no reason.

  **Tests**
  - New/changed tests verify real behavior, not mocks of the code under
    test.
  - Test output is pristine — no stray warnings.

  **Scope discipline**
  - No unrequested refactors bundled into this diff.
  - No newly introduced file that's already sprawling beyond the task's
    intent.

  Cite file:line for every finding.

  ## Calibration

  Not everything is Critical. **Important** = this cannot be trusted until
  fixed (fragile/incorrect behavior, a swallowed error, verbatim duplicated
  logic, a test that asserts nothing). **Minor** = polish, broader-coverage
  suggestions — note, don't block on these.

  ## Output format

  ### Strengths
  [Specific, not generic.]

  ### Issues
  #### Critical (Must Fix)
  #### Important (Should Fix)
  #### Minor (Nice to Have)

  ### Assessment
  **Task quality:** Approved | Needs fixes
  **Reasoning:** [1-2 sentences]
```

**Placeholders:** `story_key`, `task_number`, `base_sha`, `head_sha`,
`diff_file_path_or_inline_diff`.

**Conditional companions** (dispatch alongside this one only when the diff's
surface matches, using the same base/head/diff inputs):
- `silent-failure-hunter` — error handling, retries, or failure paths changed.
- `type-design-analyzer` — new types, interfaces, or data models introduced.
- `pr-test-analyzer` — tests were added or materially changed.

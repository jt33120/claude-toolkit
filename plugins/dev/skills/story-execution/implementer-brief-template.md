# Implementer Dispatch Brief

<!--
Provenance: adapted from obra/superpowers, skills/subagent-driven-development/
implementer-prompt.md (MIT License, Copyright (c) 2025 Jesse Vincent),
retargeted from a generic implementation-plan task to one BMAD story task.
https://github.com/obra/superpowers
-->

Fill in every `{{placeholder}}` before dispatching. Dispatch the `implementer`
agent (see `plugins/dev/agents/implementer.md`) with this brief as its prompt.

```
Subagent: implementer
description: "Story {{story_key}} — Task {{task_number}}: {{task_title}}"
model: claude-opus-5-5
effort: medium
prompt: |
  You are implementing one task of BMAD story {{story_key}} ({{story_title}}).

  ## Task

  {{task_text_verbatim_from_story}}

  ## Acceptance criteria this task must satisfy

  {{relevant_acceptance_criteria_verbatim}}

  ## Files

  {{file_list_with_role_one_per_line}}

  ## Project constraints

  - Test command: {{test_command}}
  - Lint command: {{lint_command}}
  - Typecheck command: {{typecheck_command}}
  - Load these standards skills before writing code: tdd{{, backend-standards if backend/API/DB}}{{, any relevant vendor skill under .claude/skills/}}
  - Follow existing patterns in this codebase; do not restructure code outside this task.

  ## Context from the story's Dev Notes relevant to this task

  {{relevant_dev_notes_excerpt_with_source_citations}}

  ## Before you begin

  If anything about the requirements, the approach, or an assumption in the
  task text is unclear, ask now. Do not guess.

  ## Your job

  1. Implement exactly what the task specifies — nothing more (no
     unrequested refactors, no speculative abstraction).
  2. Write tests per the `tdd` skill.
  3. Run the focused tests for what you changed; run the full suite once
     before committing.
  4. Commit your work with a clear message.
  5. Self-review your diff (completeness against the ACs, quality, no
     overbuilding, tests verify real behavior).
  6. Report back.

  ## You do not dispatch subagents

  Do all of this task's work yourself. Never spawn a subagent to implement
  part of it, and never spawn your own reviewer — the orchestrator dispatches
  spec-reviewer and code review after you report; a reviewer you spawn
  duplicates that at full cost and counts for nothing.

  ## When you're stuck

  Stop and report BLOCKED or NEEDS_CONTEXT rather than guess. Bad work is
  worse than no work: an architectural decision with several valid answers,
  a scope question the task text doesn't settle, or code you can't
  understand well enough to touch safely are all reasons to escalate, not
  push through.

  ## After review findings

  If you're resumed with findings from spec-reviewer or code review, fix
  them, re-run the tests covering the amended code, and append a fix note
  to your report: what changed, the covering tests, the command, the
  output. Then reply with the same status contract below.

  ## Report format

  Report back with (under 15 lines):
  - Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  - Files changed
  - Commits (short SHA + subject)
  - One-line test summary
  - Concerns, if any
```

**Placeholders:** `story_key`, `story_title`, `task_number`, `task_title`,
`task_text_verbatim_from_story`, `relevant_acceptance_criteria_verbatim`,
`file_list_with_role_one_per_line`, `test_command`, `lint_command`,
`typecheck_command`, `relevant_dev_notes_excerpt_with_source_citations`.
Never paste the whole story or the whole architecture doc — only what this
task needs; the story file itself is the source of truth the implementer can
re-read if needed.

---
name: tdd
description: >
  Choose tests in proportion to the behavior and risk of a change. Use a failing test
  first for a reproducible bug or consequential new behavior; run focused checks while
  implementing, and broaden verification at the review or release gate. Mechanical,
  reversible edits may need only direct inspection. Use for features, bug fixes and
  refactors, or when asked for TDD. FR : « écris le test d'abord », « corrige ce bug »,
  « implémente », « développe cette fonctionnalité », « quels tests lancer ».
---

<!-- Adapted from obra/superpowers (MIT) — https://github.com/obra/superpowers — modified for jt33120/claude-toolkit -->

# Test-driven development

## Decide what evidence matters

| Change | Evidence during implementation | Wider gate |
|---|---|---|
| Bug with a reproducible symptom, business rule, permissions, migration, API contract | Write the smallest regression test that fails for the right reason, then implement and pass it | Relevant integration tests; full suite at the project's PR/release gate |
| New behavior with meaningful failure cost | Write a focused failing behavior test first when feasible; check a risky edge | Broaden to impacted components, then normal CI at the review gate |
| UI exploration, prototype, content, reversible mechanical change | Inspect the actual result; test only when a behavior or regression risk warrants it | Build/visual review or existing gate if the work is shipped |

Choose the narrowest check that would catch a plausible regression. A test that only mirrors implementation or mocks away the behavior adds no evidence. When a test is required, read [writing-good-tests.md](writing-good-tests.md): name the behavior, assert an observable outcome, and mock only necessary boundaries.

## Red → green → refactor, when a test is useful

1. Write one focused test for the missing behavior or original bug. Run it; confirm the expected failure. If the environment prevents a meaningful red run, record that limitation.
2. Implement the smallest fix. Run that test, then relevant nearby tests. Report any failures you find, including pre-existing ones.
3. Refactor while keeping the focused tests green. Expand to integration or end-to-end checks when the change crosses boundaries or has significant risk.

For an existing defect, `systematic-debugging` establishes the cause first. A regression test is especially useful when the bug could return unnoticed. If direct reproduction is more reliable than an automated test, record how the symptom was reproduced and verified.

## Avoid redundant work

- Do not delete already written code merely because a test was written later; add useful coverage for the real risk.
- Do not require a test for every helper or a full project suite after every small code change.
- Avoid rerunning the same unmodified full suite without a new risk or an explicit project gate.
- A throwaway spike need not carry production-level tests; if it becomes production code, verify the behavior according to its risk before release.

Before claiming success, use `verification-before-completion` to describe the actual checks run and any gaps. `ci-budget` sets the economical CI cadence; a security-sensitive or migration change merits immediate targeted checks.

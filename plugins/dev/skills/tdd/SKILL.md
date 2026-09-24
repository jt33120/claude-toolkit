---
name: tdd
description: >
  Runs test-driven development in two modes: STRICT (business logic, API endpoints, bug
  fixes, anything that ships to production — write one failing test first, watch it fail
  for the right reason, then minimal code to pass) and LIGHT (a POC, spike, UI/visual, or
  exploratory task — tests after, covering the main path plus the one known risky edge,
  with the spike marked throwaway or given STRICT tests before it merges to main). Default
  is STRICT for anything ship-bound. Use before implementing any feature, bugfix, or
  refactor, or whenever behavior is about to change without a test that already fails for
  it. English triggers: "implement this feature", "write the code for", "add a function
  that", "fix this bug" (before the fix), "TDD", "test-driven development",
  "red-green-refactor", "write the test first", "quick prototype", "spike this". French
  triggers: "implémente cette fonctionnalité", "écris le code pour", "ajoute une fonction
  qui", "corrige ce bug" (avant le correctif), "TDD", "développement piloté par les
  tests", "écris le test d'abord", "fais un prototype rapide", "explore vite fait". Not
  for choosing a debugging strategy once something is already broken (use
  systematic-debugging) or for the final evidence pass before claiming work complete (use
  verification-before-completion).
model: claude-opus-5-5
effort: medium
---

<!-- Adapted from obra/superpowers (MIT) — https://github.com/obra/superpowers — modified for jt33120/claude-toolkit -->

# Test-Driven Development (TDD)

## Overview

Two modes. Both end with tests that actually prove the code works — they
differ in *when* the test is written and how much rigor is mandatory.

| | STRICT | LIGHT |
|---|---|---|
| When | Business logic, API endpoints, bug fixes — anything that ships to production | POC, spike, UI/visual work, exploratory code |
| Test written | Before the code, one behavior at a time | After, covering the main path + the one known risky edge |
| Core discipline | Watch the test fail for the right reason before making it pass | Main path + the risky edge are covered before the spike is trusted |
| Default | **This is the default.** Unsure or ship-bound → STRICT. | Only when explicitly chosen |

**Core principle (STRICT):** if you didn't watch the test fail, you don't know if it tests the right thing.

## Choosing the Mode

Ask: **will this code, or code derived from it, run in production?**

- Yes, or unsure → **STRICT**. This is the default; don't reach for LIGHT
  because a STRICT task merely feels slow.
- No — a genuine throwaway spike to answer a question ("does this API
  return what we need", "does this UI pattern feel right") → **LIGHT** is
  allowed, on one condition: **mark the spike as throwaway** (a comment, a
  branch name, a task note) **or** give it the STRICT tests-first treatment
  before it merges to `main`. A spike that quietly becomes the production
  implementation without ever getting that treatment is exactly the failure
  mode this split exists to prevent.

## STRICT Mode

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. Don't keep it "as
reference" — you'll adapt it while writing tests, which is testing after
with extra steps. Delete means delete.

### Red-Green-Refactor

```
RED (write failing test) → verify it fails for the right reason
  → GREEN (minimal code) → verify the whole suite passes
  → REFACTOR (clean up, stay green) → next behavior, back to RED
```
A test that fails for the wrong reason sends you back to RED, not forward.

**RED.** One minimal test, one behavior, clear name, real code (mock only if
unavoidable):

<Good>
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  const result = await retryOperation(operation);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
</Good>
<Bad>
```typescript
test('retry works', async () => {
  const mock = jest.fn().mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error()).mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3); // tests the mock, not the code
});
```
</Bad>

**Verify RED — mandatory, never skip.** It must fail (not error), with the
expected message, because the feature is missing — not a typo. Passes
immediately? You're testing existing behavior; fix the test. Errors
instead of failing cleanly? Fix the error, re-run until it fails correctly.

**GREEN.** Simplest code that passes — no added options, no "while I'm here"
features:

<Good>
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try { return await fn(); } catch (e) { if (i === 2) throw e; }
  }
  throw new Error('unreachable');
}
```
</Good>
<Bad>
An `options?: { maxRetries?, backoff?, onRetry? }` param nobody asked for — YAGNI.
</Bad>

**Verify GREEN — mandatory.** Pristine output, and — critically — **the
project's suite**, not just the file you touched, is green (run
`pytest`/`npm test`/`cargo test` even when the task named one file). Any
failure that run shows, including one you didn't cause, goes in your report
by name — a red test you scrolled past and didn't mention is a report
falsified by omission.

**REFACTOR.** After green only: remove duplication, improve names, extract
helpers. Keep tests green. Don't add behavior. Then repeat for the next
behavior.

### Good Tests

Read [writing-good-tests.md](writing-good-tests.md) whenever writing or
changing a test: name the production change that would make it fail before
writing it, assert on real behavior never mock behavior, keep test-only
code in test utilities, understand a dependency's side effects before
mocking it.

### Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests written after pass immediately — proves nothing. You never watched it fail, so you never proved it can catch the bug. |
| "Already manually tested" | Ad hoc: no record, doesn't survive the next change, easy to forget cases under pressure. |
| "This is basically a spike" | Then say so and use LIGHT mode explicitly — don't quietly skip tests under STRICT. |
| "3+ fixes failed, one more try" | That's `systematic-debugging`'s architecture-question signal, not a license to skip tests. |
| "TDD will slow me down" | Debugging in production is slower. Test-first catches it before commit. |

### Red Flags — Stop and Start Over

Code before test · test written after implementation · test passes
immediately · can't explain why it failed · "keep as reference" · "just this
once" · "spirit not ritual" · any variant of the rationalizations above.

**All of these mean: delete the code, start over with TDD.**

### Verification Checklist (STRICT)

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing, for the right reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass, project suite is green, output pristine
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check every box? You skipped TDD. Start over.

## LIGHT Mode

For a genuine POC, spike, UI/visual change, or exploratory task — not yet
shipping. "Tests after" here still means all three:

1. **Main path** — what the spike is meant to prove — has one test
   exercising it for real (not a mock of the thing you're validating).
2. **The one known risky edge** — the case you'd feel bad about if it
   silently broke (empty input, a UI boundary, the API's documented error
   response) — is covered too.
3. **Explicit exit**: marked throwaway (comment/branch/task note), **or**,
   before merging to `main`, given STRICT treatment retroactively — the
   tests you'd have written first, now written and green.

LIGHT is deferred-and-minimal, not "no tests":

```typescript
// SPIKE — throwaway, do not merge without STRICT tests
test('vendor API returns the fields we need for the main case', async () => {
  const result = await fetchVendorQuote(KNOWN_TEST_SKU);
  expect(result.price).toBeGreaterThan(0);
});

test('vendor API — the risky edge: SKU not found', async () => {
  const result = await fetchVendorQuote('does-not-exist');
  expect(result).toBeNull(); // confirms it doesn't throw
});
```
Written after the exploratory call worked, covering the case that matters
and the one that could silently break the feature. If this becomes the real
implementation, it gets STRICT tests-first treatment before merge — not a
grandfather pass.

## Debugging Integration

Bug found? Write the failing test reproducing it — a bug fix is STRICT by
definition (it ships to production). Follow the `systematic-debugging`
skill's process to find the root cause, then apply the STRICT cycle here to
fix it. Never fix a bug without a regression test.

## Before Calling It Done

Run the `verification-before-completion` skill's gate before claiming the
feature works or the bug is fixed — passing tests are evidence only once
you've actually run them fresh.

## Final Rule

```
Ships to production, or unsure  → STRICT: test exists and failed first
Throwaway spike, marked as such → LIGHT: main path + risky edge, tested before merge
```

No silent third option, and no exceptions to STRICT's default without your
human partner's permission.

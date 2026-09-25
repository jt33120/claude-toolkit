---
name: verification-before-completion
description: >
  Check evidence before claiming a change works, tests pass, or a release is ready.
  Choose checks that match the claim and change risk, read their output, and report
  what was and was not verified. Use before a completion claim, PR, release, or deploy.
  FR : « c'est terminé », « les tests passent », « prêt à committer », « on peut merger ».
---

<!-- Adapted from obra/superpowers (MIT) — https://github.com/obra/superpowers — modified for jt33120/claude-toolkit -->

# Verification before completion

**Evidence before claims.** Name the claim, run an appropriate check on the current change, read the result and exit code, then state exactly what it proves. A focused check proves only that focused scope; describe uncovered areas without calling the entire project green.

| Claim | Useful evidence |
|---|---|
| A bug is fixed | Reproduce the original symptom or run its regression test and inspect the result |
| Impacted behavior works | Focused unit/integration tests or a direct behavioral check covering the changed path |
| The full suite passes | A completed full-suite run on the relevant revision |
| A build passes | A completed build, not a passing linter |
| A release is ready | Required project gates, including appropriate security, build and deployment checks |

For a low-risk reversible edit, checking the diff and the actual rendered or written result may be sufficient. Changes to auth, data, migrations, external actions or shared contracts need stronger checks. When no test environment is available, state the limitation and the checks you could perform.

Run the full suite at the review or release gate if the project requires it, or sooner when the scope warrants it. Do not rerun the same suite before each small commit or task transition if the tested revision and relevant inputs have not changed. A new change after a passing run may require a targeted rerun or the next CI gate; do not attribute an old result to an untested revision.

Report the command or manual check, its outcome, and material gaps. A failure or incomplete run must be reported as such. For regression tests, observing a meaningful failure before the fix is useful; reverting a working fix just to repeat the failure is unnecessary.

---
name: ci-budget
description: "Audit and reduce GitHub Actions minutes on private repos without dropping real tests: measure minutes per workflow, align CI triggers with the BMAD rhythm (story / epic / review / merge), tune triggers, concurrency and caching. Use when Actions minutes run high, before adding a workflow, or when setting up CI on a new repo. FR : « optimise mes github actions », « trop de minutes CI », « quota actions », « revoir ci.yml », « stratégie CI »."
model: claude-opus-5-5
effort: medium
---

# CI budget (GitHub Actions)

Goal: run expensive checks **less often, at the right moment** — never remove tests that cover real risks (migrations, E2E, build, security).

## 1. Measure first

- Minutes and run count per workflow over the last 30 days (GitHub billing usage, or `gh run list --limit 500 --json workflowName,createdAt,conclusion` + run timings).
- For each workflow: triggers (`on:`), jobs, average duration, runs per week.
- Scheduled workflows (`schedule:`): check they still exist on the default branch and are still needed — a cron can keep consuming minutes unnoticed.
- Quota: included minutes are **shared across all private repos** of the account (check the current plan on docs.github.com). Aim for ~75% of the quota planned, keep the rest as margin.

Rank workflows by minutes and start with the biggest one.

## 2. Target rhythm (BMAD)

| Moment | Work | GitHub Actions |
|---|---|---|
| Each story | Claude codes, runs the relevant tests locally, commits locally | Nothing |
| During the epic | Push to a branch to back up or collaborate; draft PR if useful | No full suite |
| End of epic | PR marked « Ready for review » | Full CI: build, tests, E2E, relevant security checks |
| Fixes after review | New push on the PR | Full CI again on the fixed version |
| Merge to the default branch | Deploy + production checks | Don't re-run what already passed on the PR |

Do not limit pushes: push whenever backup or sharing is needed. What changes is which pushes trigger costly jobs. Exception: a migration or a security change gets its targeted checks right away, even mid-epic.

## 3. Trigger patterns

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  workflow_dispatch: {}

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    if: github.event.pull_request.draft == false || github.event_name == 'workflow_dispatch'
    timeout-minutes: 20
```

- Remove `push:` on the default branch from the full CI **only if** merges go through a PR with required status checks (branch protection). Otherwise keep it.
- `paths` / `paths-ignore`: filter precisely per workflow. Never ignore a folder the app reads at runtime (e.g. some `docs/` or content folders).
- Split cheap checks (lint, typecheck, unit) from expensive ones (E2E, Docker build); the cheap job can run on every push.
- Cache dependencies (`actions/setup-node` / `setup-python` cache, Docker layer cache), set `timeout-minutes` on every job, avoid wide matrices on PRs.
- Scheduled jobs: lowest useful frequency, and skip when nothing changed.

## 4. Deliver

A table per workflow (current minutes → expected minutes, change, risk), then the YAML diff. Apply only after the user validates, and re-measure after two weeks.

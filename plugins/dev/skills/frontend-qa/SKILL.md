---
name: frontend-qa
description: "Deep QA of a web or mobile frontend with free open-source tools: smoke flows, exploratory testing, performance, accessibility, visual regression, responsive checks, durable end-to-end tests, and a standard bug report. Use before a merge or release, after a UI change, or when asked to test the front. FR : « teste le front », « QA de l app », « vérifie l interface », « tests e2e », « fais une passe QA »."
---

# Frontend QA

Pick the levels the change needs (a small UI fix: 1 + 4; a release: all). Start the app locally or target a preview URL — never test against production data with write actions.

| # | Level | Tool (free / OSS) | What to check |
|---|---|---|---|
| 1 | Smoke | Playwright MCP (bundled) — accessibility-tree snapshots | Key user flows end to end, no console errors |
| 2 | Exploratory | Claude in Chrome (real, logged-in session) | Edge cases, odd inputs, back/refresh, slow network |
| 3 | Performance | Chrome DevTools MCP (bundled) | Performance trace, LCP / CLS / INP, network waterfall, console and failed requests |
| 4 | Accessibility | `@axe-core/playwright` + keyboard-only pass | WCAG violations, focus order, labels, contrast |
| 5 | Visual regression | Playwright `toHaveScreenshot()` | Unintended visual diffs vs baseline |
| 6 | Responsive | Playwright device emulation | Phone / tablet / desktop breakpoints, touch targets |
| 7 | Durable tests | Playwright Test Agents (`npx playwright init-agents --loop=claude`): planner → generator → healer | TS specs in `tests/e2e/`, run with `npx playwright test` |
| 8 | Mobile | XcodeBuildMCP (iOS simulator build/run/screenshots), Maestro MCP (iOS/Android flows in YAML) | Same flows on device sizes, safe areas, gestures, dark mode |

Missing tool → `stack-check` installs it (see [`frontend-mobile.md`](../stack-check/references/frontend-mobile.md)).

## Bug report (output)

| # | Severity (blocker/major/minor/cosmetic) | Screen / flow | Repro steps | Expected | Actual | Evidence (screenshot/trace path) | Suspected cause |
|---|---|---|---|---|---|---|---|

Then: fix blockers and majors (use `systematic-debugging`), add a regression spec for each fixed bug, re-run the affected levels, and finish with `verification-before-completion`.

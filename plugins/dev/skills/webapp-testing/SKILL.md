---
name: webapp-testing
description: >
  Playwright toolkit for testing local web applications end-to-end: manage dev-server
  lifecycle, drive a real headless browser, capture screenshots and console logs, and
  discover selectors on rendered pages. Use when verifying frontend behavior in an
  actual browser rather than at the unit level — debugging UI behavior, checking a
  page renders and behaves correctly, or reproducing a frontend bug. English triggers:
  "test this in the browser", "click through the UI", "take a screenshot of the app",
  "check the browser console for errors", "e2e test", "Playwright". French triggers:
  "teste ça dans le navigateur", "clique sur l'interface", "prends une capture d'écran
  de l'app", "vérifie la console du navigateur", "test end-to-end". Not for unit-level
  TDD (tdd) or for verifying a deploy went well in production (infra-deploy).
license: Complete terms in LICENSE.txt
model: claude-opus-5-5
effort: medium
---

<!-- Adapted from anthropics/skills (Apache-2.0) — https://github.com/anthropics/skills — modified for jt33120/claude-toolkit -->

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation

## Durable Tests: Playwright Test (TS) vs. Ad-Hoc Scripts Here

The Python scripts in this skill (`scripts/with_server.py`, the
`examples/`) are for **ad-hoc, throwaway checks** — reproducing a bug,
confirming a page renders, one-off reconnaissance. They aren't meant to
become the project's regression suite.

**If the project uses TypeScript, or already has `@playwright/test`
installed**, write any test meant to survive past this session as a
**Playwright Test spec** instead of a Python script:
- Location: `tests/e2e/*.spec.ts`
- Run with: `npx playwright test`
- Use Playwright Test's own fixtures (`test`, `expect`, `page`) and its
  config (`playwright.config.ts`) rather than hand-rolling
  `sync_playwright()` — parallelization, retries, trace/video capture, and
  CI reporting come for free, and the suite lives next to the app's other
  tests instead of as a one-off script nobody re-runs.
- An e2e spec proving a bug fix or a shipped feature follows the `tdd`
  skill's STRICT discipline like any other test — written to fail first
  where practical.

**Keep using the Python scripts here when:** the project has no Playwright
Test setup, the check is genuinely one-off (a screenshot to eyeball, a
console-log capture while debugging), or you're doing reconnaissance before
writing the durable spec.

**For a quick visual/manual check** — "does this look right," a one-time
click-through, eyeballing a rendered page — Claude in Chrome can drive the
user's actual browser session instead of spinning up a headless Playwright
run; reach for it when the goal is a human-style look, not a repeatable
check.

## Where This Fits

Once a feature passes here (renders correctly, behaves correctly in the browser), that's
UI-level evidence — it doesn't replace the `tdd` skill's unit tests, and it doesn't replace
running the `verification-before-completion` gate before claiming the feature is done. Before
shipping a change verified this way, run `infra-deploy`'s pre-deploy checklist.

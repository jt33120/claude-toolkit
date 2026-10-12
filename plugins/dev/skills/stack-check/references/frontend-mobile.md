# Frontend and mobile tooling (free / open source only)

Install only what the declared stack needs (`front:` in `.claude/stack.yaml`: `web`, `ios`, `android`, `expo`, `react-native`, `flutter`). Commands marked *(verify)* were not tested end to end — check the tool's README on first use.

## Always available (bundled in the `dev` plugin)

Playwright MCP, Chrome DevTools MCP, shadcn MCP — CHECK: each responds to one read call.

Shared frontend skills for Claude Code and Codex: `frontend-content` (product + spec, three disclosure levels), `frontend-direction` (Anthropic Frontend Design principles and UI UX Pro Max catalogs), plus the focused Impeccable adaptations `distill`, `clarify`, `critique` and `layout`. Use them before/after implementation as needed; do not install duplicate copies of these skills.

## Web

- Vendor skills: `npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines -a claude-code -y`
- The complete upstream Impeccable runtime is optional for features beyond the bundled adaptations. Install it only for a concrete need after checking skill-name conflicts; it is not a prerequisite for this toolkit's frontend flow.
- E2E + accessibility: `npm i -D @playwright/test @axe-core/playwright && npx playwright install && npx playwright init-agents --loop=claude`

## iOS native (SwiftUI)

- SwiftUI skill: `npx skills add AvdLee/SwiftUI-Agent-Skill -a claude-code -y` *(verify)*
- Build/run/screenshots on simulator: `claude mcp add XcodeBuildMCP -s project -- npx -y xcodebuildmcp@latest` *(verify — the package may have been renamed mobilebuildmcp)*

## Expo / React Native

- `npx skills add expo/skills -a claude-code -y` *(verify)*

## Mobile E2E (iOS + Android)

- Maestro CLI: `curl -fsSL "https://get.maestro.mobile.dev" | bash`, then `claude mcp add maestro -s project -- maestro mcp` *(verify)*

## Optional

- Iconify MCP (community) for open icon sets *(verify repo and license before adding)*

Never add paid services (pattern libraries, hosted visual-diff SaaS). Report anything that could not be installed.

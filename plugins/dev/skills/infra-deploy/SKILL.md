---
name: infra-deploy
description: >
  Two-mode operations skill for a Vercel (Next.js frontends) + Railway (backends/workers)
  + Supabase/Neon (Postgres) + GitHub Actions stack: a pre-deploy checklist before shipping,
  and an incident-response workflow when production is down. Uses the Vercel, Railway,
  Supabase, and Neon MCP connectors when available for deploy status, logs, env vars, and
  DB branches — falls back to their CLIs otherwise. English triggers: "ready to deploy",
  "deploy checklist", "ship this release", "we have an incident", "production is down",
  "rollback", "write a postmortem", "post-mortem". French triggers: "prêt à déployer",
  "checklist de déploiement", "on livre cette release", "on a un incident", "la prod est
  down", "rollback", "écris un post-mortem". Not for the root-cause investigation itself
  once things are stable (systematic-debugging), for unit/e2e test verification before
  shipping (tdd, frontend-qa, verification-before-completion), or for infrastructure
  security hardening and audits (security).
---

<!-- Adapted from anthropics/knowledge-work-plugins engineering/skills/deploy-checklist and
     engineering/skills/incident-response (Apache-2.0) — https://github.com/anthropics/knowledge-work-plugins
     — merged into one skill and adapted for the Vercel/Railway/Supabase/Neon/GitHub Actions
     stack, for jt33120/claude-toolkit -->

# Infra: Deploy & Incident Response

Two modes, one skill, because they share the same stack context and the same tools. Pick
the mode that matches what's happening:

- **Mode 1 — Pre-Deploy Checklist**: about to ship a change. See
  [references/pre-deploy-checklist.md](references/pre-deploy-checklist.md).
- **Mode 2 — Incident Response**: something is broken in production right now. See
  [references/incident-response.md](references/incident-response.md).

In case of doubt, ask: "Are we about to ship something, or is something already broken in
production?" Don't run both at once — a checklist run mid-incident just delays mitigation,
and incident triage before a routine deploy is wasted ceremony.

## The Stack This Skill Assumes

| Layer | Service | Primary interface |
|---|---|---|
| Frontend | Vercel (Next.js) | Vercel MCP connector, else `vercel` CLI |
| Backend / workers | Railway | Railway MCP connector, else `railway` CLI |
| Postgres (app data) | Supabase | Supabase MCP connector, else `supabase` CLI |
| Postgres (branching / preview DBs) | Neon | Neon MCP connector, else `neonctl` CLI |
| CI | GitHub Actions | `gh` CLI / GitHub MCP connector for run status |

**Connector-first, CLI as fallback.** Before shelling out to a CLI, check whether the
matching MCP connector is available in this session — it returns structured data (deploy
status, logs, env vars, DB branch state) without you having to parse text output or hold
credentials. Use it for:
- **Vercel connector** — latest deployment status, build logs, runtime logs, environment
  variables per environment (production/preview), triggering or inspecting a rollback.
- **Railway connector** — service deploy status, build/runtime logs, environment variables,
  restarting a service, metrics (error rate, latency).
- **Supabase connector** — project status, migration history, advisors (security/performance
  lint), logs, table/schema inspection.
- **Neon connector** — branch list and status, creating a throwaway branch to reproduce an
  incident against production-like data without touching production, connection strings.

When a connector isn't available or doesn't cover what you need, fall back to the CLI
(`vercel`, `railway`, `supabase`, `neonctl`, `gh`) run via a shell tool. Say explicitly which
one you used, since the person may not have every connector configured.

## Containers & Builds (Railway)

Short, concrete rules for the build side of a Railway service — separate
from the deploy sequence in Mode 1 below:

- **Dockerfile vs. Railpack/Nixpacks:** let Railway's builder (Railpack, or
  Nixpacks on older services) auto-detect and build when the app is a
  standard framework with no unusual system dependencies — less to
  maintain. Reach for an explicit `Dockerfile` once the build needs
  something the auto-builder can't express: a specific base image, native
  system packages, a multi-stage build to keep the shipped image small, or
  a non-Node/Python runtime combination. Don't maintain both — a
  `Dockerfile` at the service root always wins and the auto-builder is
  skipped, which silently changes build behavior if left there by
  accident.
- **Healthchecks:** set a Railway healthcheck path (`/health` or
  equivalent) that actually exercises a dependency (DB ping), not just
  `return 200` — a healthcheck that always passes lets Railway route
  traffic to an instance that can't reach its database.
- **Graceful shutdown:** the process must handle `SIGTERM` — stop accepting
  new connections, finish in-flight requests, exit — within Railway's kill
  timeout, or deploys and restarts drop requests. See the `backend-standards`
  skill's [Node backend reference](../backend-standards/references/node.md) Docker section for the Node-specific
  mechanics (PID 1, no `npm start` wrapper).
- **Image size:** a multi-stage build that ships only the production
  dependencies and build output (not the build toolchain or dev
  dependencies) deploys faster and shrinks the attack surface — check this
  before assuming a slow deploy is a Railway problem.
- **Env parity:** the same variables that exist in production should exist
  (with safe/throwaway values) in preview/staging — a preview deploy that
  silently no-ops a feature because a var is missing masks a bug until
  production.

## Mode 1: Pre-Deploy Checklist

Read [references/pre-deploy-checklist.md](references/pre-deploy-checklist.md) and run it in
full before shipping anything beyond a trivial change. It covers: CI status, migrations,
environment variables, feature flags, rollback plan, and the actual deploy + verify sequence
across Vercel and Railway.

**Before running this mode**, the `verification-before-completion` gate should already be
green — this checklist assumes the code is proven to work, and adds the deploy-specific
checks (migrations, env vars, rollback plan) on top of that, not instead of it.

## Mode 2: Incident Response

Read [references/incident-response.md](references/incident-response.md) and follow it from
whichever phase the incident is in: triage → communicate → mitigate → postmortem. It covers
severity classification, where to pull signal from on this stack (Vercel/Railway
logs and metrics, Supabase/Neon advisors and logs), and the postmortem template.

**Stabilize first, root-cause after.** Incident response is about stopping the bleeding —
rollback, feature-flag kill switch, scaling up — not about finding the root cause. Once the
incident is mitigated and users are unaffected, switch to the `systematic-debugging` skill
to actually find and fix the root cause; a mitigation you stop at is a recurring incident.

## Customization

Tell me about your deploy or incident and this skill adapts the checklist/template:
- "We use feature flags" → adds flag verification and kill-switch steps
- "This includes a database migration" → adds Supabase/Neon migration-specific checks
- "This is a breaking API change" → adds consumer notification steps
- "This is a SEV1" → skips straight to all-hands communication cadence

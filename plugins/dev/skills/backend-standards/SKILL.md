---
name: backend-standards
description: 'Senior-level, opinionated backend standards for FastAPI, Node/TypeScript, Postgres, and API design — principles and a review checklist, pointing to vendor skills for stack-specific depth. Use when writing or reviewing backend/API/database code ("backend standards", "API design review", "is this endpoint well-designed", "revue backend", "bonnes pratiques API", "standards base de données"). Distinct from `security` (stack-specific security audit) and `tdd` (test discipline) — this is architecture and API/data conventions.'
---

<!--
Original synthesis for this plugin — no upstream text copied. Claims are
attributed to their sources inline and in each reference file; read the
sources for full detail rather than treating this skill as a substitute for
them.
-->

# Backend Standards

Opinionated, senior-level conventions for backend code. This file is a
**thin layer**: the index, the cross-stack principles, and the review
checklist. Stack-specific depth belongs to the vendor skills below, not
duplicated here — load a reference only when the task touches ground those
vendor skills don't cover.

## Vendor skills — defer to these first

`stack-check` installs these per project when it detects the matching
stack. **If one is present in the session, follow it — it wins over this
skill on its own topic.** This skill is the cross-cutting layer above them
(API contracts, error shape, transactions/idempotency as a whole), not a
competing source of truth for FastAPI, Postgres, or Python-tooling detail.

- **FastAPI** — the official FastAPI skill (`fastapi/fastapi` repo,
  `.agents/skills/fastapi`). Endpoint/dependency patterns, Pydantic v2,
  project layout, async correctness — the FastAPI-specific how-to.
- **Postgres on Supabase** — `supabase-postgres-best-practices`
  (`supabase/agent-skills`). Query performance, schema design, connection
  management, and RLS policy detail.
- **Postgres on Neon** — `neon-postgres` (`neondatabase/agent-skills`).
  Neon's branching model, pooled connections, egress.
- **Python tooling** — Trail of Bits' `modern-python` (`trailofbits/skills`,
  `plugins/modern-python`): `uv` for dependency/env management, `ruff` for
  lint+format, `ty` for type checking. Not backend architecture, but the
  toolchain every Python backend here should run.

## Principles

1. **Explicit over implicit.** Validate at the boundary (request body, query
   params, env vars) with a schema (Pydantic v2 / zod), not ad-hoc `if`
   checks scattered through the handler.
2. **Errors are part of the contract.** A caller should be able to
   distinguish "your request was wrong" from "we broke" from "try again
   later" without parsing prose. Use a consistent error shape and real HTTP
   status codes — never `200` with an `{"error": ...}` body.
3. **Async correctness beats async everywhere.** Async is for I/O-bound
   work; a blocking call inside an async handler (sync DB driver, CPU-heavy
   loop) stalls the whole event loop, not just that request.
4. **Migrations are the schema's source of truth**, applied forward-only in
   CI/CD — never hand-edit a production schema, never rely on
   auto-migrate-on-boot in a multi-instance deployment.
5. **Every write path either fits in a transaction or is idempotent.** A
   retried request (client timeout, proxy retry, queue redelivery) must not
   double-charge, double-insert, or double-send.
6. **Pooled connections on serverless.** A serverless/edge function opening
   its own Postgres connection exhausts the database's connection limit
   under concurrency — always go through the platform's pooler (Supabase's
   pgbouncer endpoint, Neon's pooled connection string).
7. **Secrets never enter source control or logs.** Env vars for secrets,
   never a literal in code, a fixture, or a log line — including inside a
   stack trace.
8. **Observability is structured, not printf.** A log line without a
   request id, without a level, and without machine-parseable fields is a
   log line nobody can query when it matters.

## Review checklist

- [ ] Boundary validated by schema (request/response/env), not scattered
      `if`s.
- [ ] Errors use the project's standard shape and precise HTTP status codes
      (`references/api-design.md` — RFC 9457 problem details).
- [ ] No blocking call inside an async handler — sync driver, `time.sleep`,
      unbounded CPU work (vendor FastAPI skill / `references/node.md`).
- [ ] DB access goes through the pooled/serverless-safe connection path.
- [ ] Every filtered/joined/sorted column is indexed, or the gap is
      documented.
- [ ] No N+1 (a loop issuing one query per iteration).
- [ ] Multi-step writes are transactional, or the endpoint is idempotent
      under retry (idempotency key, upsert, safe check-then-write).
- [ ] Unbounded list endpoints paginate (`references/api-design.md`).
- [ ] No secret in code, fixtures, test output, or a log line.
- [ ] Logs are structured (level + fields), not string-concatenated prose.
- [ ] Public-writable endpoints are rate-limited, or the deferral is
      documented.

## When to load which reference

- **`references/node.md`** — writing or reviewing TypeScript/Node backend
  code: project structure, validation, layering, async pitfalls, error
  handling, production readiness, Docker.
- **`references/api-design.md`** — designing or reviewing a new endpoint's
  shape: REST conventions, pagination, idempotency keys, versioning, the
  error format, rate limits, long-running operations, and what to log.
- **Postgres section below** — the cross-cutting rules vendor skills don't
  own; for anything Supabase- or Neon-specific (RLS, schema, connection
  internals), load the matching vendor skill instead.
- **FastAPI vendor skill** — any FastAPI endpoint/dependency/Pydantic work.

## Postgres — what the vendor skills don't cover

The vendor skills above own RLS, schema design, and platform-specific
connection internals. These four rules are cross-cutting and apply
regardless of which Postgres provider is in play:

- **Serverless pooling.** A serverless/edge function opening a direct
  connection per invocation exhausts `max_connections` under concurrency —
  use the pooled/transaction-mode endpoint for application code, and reserve
  the direct connection for migrations and session-level features
  (`LISTEN/NOTIFY`, prepared statements, advisory locks). Transaction-mode
  pooling drops session state between statements — code written for a
  direct connection can silently misbehave once pointed at a pooler.
- **Forward-only migrations.** The migration history is the schema's source
  of truth, applied through CI/CD (or Alembic/Prisma Migrate/Drizzle Kit) —
  never hand-edited against production. Never auto-run migrations on
  multi-instance boot: two instances racing the same migration is a real
  failure mode; run it as a separate, single-instance step.
- **N+1 queries.** A loop issuing one query per iteration is the single
  most common backend performance bug. Fix with `JOIN` / `WHERE id = ANY($1)`
  or the ORM's explicit eager-loading — never rely on default lazy loading
  inside a loop.
- **Transactions and idempotency.** Wrap a multi-statement write in a single
  short transaction — held open across an external HTTP call or a long
  computation, it becomes production lock contention. A "check then insert"
  race is not safe under concurrent requests even inside a transaction at
  the default `READ COMMITTED` isolation level — use
  `INSERT ... ON CONFLICT` instead.

## Not this skill

- Auth, RLS, secrets scanning, dependency vulnerabilities → `security`.
- Whether tests exist and are structured well → `tdd`.
- Deploy pipeline and infra config → `infra-deploy`.

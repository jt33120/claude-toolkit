---
name: backend-standards
description: 'Senior-level, opinionated backend standards for FastAPI, Node/TypeScript, Postgres, and API design — principles and a review checklist, with references loaded on demand. Use when writing or reviewing backend/API/database code ("backend standards", "API design review", "is this endpoint well-designed", "revue backend", "bonnes pratiques API", "standards base de données"). Distinct from `security` (stack-specific security audit) and `tdd` (test discipline) — this is architecture and API/data conventions.'
model: claude-opus-5-5
effort: medium
---

<!--
Original synthesis for this plugin — no upstream text copied. Claims are
attributed to their sources inline and in each reference file; read the
sources for full detail rather than treating this skill as a substitute for
them.
-->

# Backend Standards

Opinionated, senior-level conventions for backend code. This file is the
index and the checklist; load a reference only when the task touches its
area — do not load all four for a one-line endpoint fix.

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

- [ ] Request/response validated by schema at the boundary, not scattered
      `if`s.
- [ ] Errors use the project's standard shape and correct HTTP status codes
      (see `references/api-design.md` for the RFC 9457 problem-details
      format).
- [ ] No blocking call inside an `async def` handler (sync driver, `time.sleep`,
      unbounded CPU work) — see `references/fastapi.md` / `references/node.md`.
- [ ] DB access goes through the pooled/serverless-safe connection path — see
      `references/postgres.md`.
- [ ] A new query that filters/joins/sorts on a column has an index backing
      it, or a documented reason it doesn't.
- [ ] No N+1 query pattern (a loop issuing one query per iteration) — see
      `references/postgres.md`.
- [ ] A multi-step write is in a transaction, or the endpoint is idempotent
      (idempotency key, upsert, or a check-then-write pattern safe under
      retry).
- [ ] Pagination on any list endpoint that can grow unbounded — see
      `references/api-design.md`.
- [ ] No secret (API key, connection string, token) in code, fixtures, test
      output, or a log line.
- [ ] Logs are structured (level + fields), not string-concatenated prose.
- [ ] Rate limiting exists on any public-writable endpoint, or there's a
      documented reason it's deferred.

## When to load which reference

- **`references/fastapi.md`** — writing or reviewing a FastAPI endpoint,
  dependency, or Pydantic v2 model; project layout and settings for a Python
  backend.
- **`references/node.md`** — writing or reviewing TypeScript/Node backend
  code: validation, layering, async pitfalls, error handling.
- **`references/postgres.md`** — anything touching a migration, an index, a
  transaction boundary, or a serverless connection to Supabase/Neon. Row
  Level Security itself is out of scope here — defer to the vendor's own
  Supabase skill (`supabase/agent-skills`) for RLS policy design.
- **`references/api-design.md`** — designing or reviewing a new endpoint's
  shape: REST conventions, pagination, idempotency keys, versioning, the
  error format, rate limits, and what to log.

## Not this skill

- Auth, RLS, secrets scanning, dependency vulnerabilities → `security`.
- Whether tests exist and are structured well → `tdd`.
- Deploy pipeline and infra config → `infra-deploy`.

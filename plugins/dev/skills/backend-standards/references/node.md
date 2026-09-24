# Node / TypeScript Backend

Original synthesis; sources cited inline. Primary source:
[goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)
(one of the most-starred, actively curated Node.js best-practices
collections) and the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html).

## TypeScript strict mode

- `"strict": true` in `tsconfig.json` (bundles `strictNullChecks`,
  `noImplicitAny`, etc.) — non-negotiable for a backend that will run
  unattended. A backend without `strictNullChecks` will eventually null-deref
  in production on a code path no test happened to exercise.
- No `any` at a module boundary (a function's public parameters/return type).
  `unknown` plus a narrowing check is the honest alternative when the input
  really is untyped (e.g. `JSON.parse`, a webhook body).
- Prefer `type` aliases and discriminated unions for domain modeling over
  class hierarchies for pure data — a union like
  `{status: "ok", data: T} | {status: "error", error: E}` makes illegal
  states unrepresentable in a way a boolean flag plus optional fields
  doesn't.

## Validation with zod (or an equivalent schema library)

- Validate every external input — HTTP body, query params, path params, env
  vars, a message-queue payload — at the boundary with a schema, and infer
  the TypeScript type from the schema (`z.infer<typeof Schema>`) rather than
  writing the type by hand and hoping it matches.
- A schema's `.parse()` failing is an expected, client-facing error (400),
  not an unhandled exception that becomes a 500 — catch `ZodError`
  specifically and map it to the project's standard error shape (see
  `api-design.md`).
- Validate env vars once at startup with the same tool, so a missing
  required variable fails the process at boot, not at the first request that
  touches it.

## Layering

- Route/controller layer: parse the request, call a service function, shape
  the response. No business logic, no direct DB queries here.
- Service layer: business logic, orchestration across repositories/external
  calls. Framework-agnostic — should not import `express`/`fastify` types.
- Data-access layer: the only place that talks to the database or an ORM.
  Swapping the ORM should touch this layer only.
  ([nodebestpractices: project structure practices](https://github.com/goldbergyoni/nodebestpractices#1-project-structure-practices))

## Error handling

- Distinguish **operational errors** (expected: bad input, not found, a
  downstream service down — recoverable, should produce a clean client
  response) from **programmer errors** (a bug — a `TypeError` from
  undefined-is-not-a-function). Operational errors are caught and mapped to
  a response; programmer errors are logged with full context and the
  process should be allowed to crash and restart under a supervisor
  (PM2/systemd/container orchestrator) rather than limp on in an unknown
  state.
  ([nodebestpractices: error handling](https://github.com/goldbergyoni/nodebestpractices#2-error-handling-practices))
- Always use `Error` subclasses (or a typed error union) — never `throw`
  a plain string or object; you lose the stack trace and `instanceof`
  narrowing.
- One centralized error-handling middleware (Express `(err, req, res, next)`,
  or the framework's equivalent) that maps known error types to the
  project's error shape and logs unknown ones — not a `try/catch` with
  bespoke handling copy-pasted into every route.

## Async pitfalls

- Never leave a `Promise` unhandled — an unawaited async call whose
  rejection nobody catches becomes an `unhandledRejection`, which in modern
  Node **crashes the process** by default. Await it, `.catch()` it, or
  explicitly fire-and-forget with a documented reason and its own error
  handler.
- `Promise.all` fails fast on the first rejection and abandons the other
  promises' results — use `Promise.allSettled` when partial failure is
  acceptable and you need every result regardless.
- Don't `await` sequentially in a loop when the operations are independent —
  that serializes I/O that could run concurrently; build an array of
  promises and `Promise.all` them (see `postgres.md` on N+1 for the same
  mistake with database queries specifically).
- A synchronous, CPU-heavy loop (large JSON transform, crypto, image
  processing) still blocks Node's single thread even inside an `async`
  function — offload it to a worker thread or a queue for anything
  non-trivial.

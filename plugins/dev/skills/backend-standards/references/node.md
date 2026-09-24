# Node / TypeScript Backend

Original synthesis; sources cited inline — this is a checklist-with-rationale
built by reading and condensing the sources below, not a copy of their text
(nodebestpractices is CC BY-SA 4.0, which permits synthesis-with-attribution
but not verbatim reproduction). Primary sources:
[goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)
(one of the most-starred, actively curated Node.js best-practices
collections) and the
[TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html).

## Project structure

- Structure by **business component** (bounded context: `orders/`,
  `users/`, `payments/`), not by technical layer sprawled across the whole
  app (`controllers/`, `models/` each spanning every feature) — a change to
  one feature should touch one directory, not scatter across the codebase.
  Within a component, layer by responsibility (entry-points/routes, domain
  logic, data-access).
  ([nodebestpractices: project structure](https://github.com/goldbergyoni/nodebestpractices))
- Environment-aware, hierarchical config, validated at startup with the same
  schema tool used for request validation (see below) — not `process.env.X`
  read ad hoc through the codebase.
- Choose the framework deliberately (Express/Fastify/Nest), not by default —
  Fastify's schema-based validation and Nest's DI matter once the backend
  passes trivial size.

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
  ([nodebestpractices: project structure practices](https://github.com/goldbergyoni/nodebestpractices))

## Error handling

- Distinguish **operational errors** (expected: bad input, not found, a
  downstream service down — recoverable, should produce a clean client
  response) from **programmer errors** (a bug — a `TypeError` from
  undefined-is-not-a-function). Operational errors are caught and mapped to
  a response; programmer errors are logged with full context and the
  process should be allowed to crash and restart under a supervisor rather
  than limp on in an unknown state.
  ([nodebestpractices: error handling practices](https://github.com/goldbergyoni/nodebestpractices))
- Always use `Error` subclasses (or a typed error union) — never `throw` a
  plain string or object; you lose the stack trace and `instanceof`
  narrowing.
- One centralized error-handling middleware (Express `(err, req, res, next)`,
  or the framework's equivalent) that maps known error types to the
  project's error shape and logs unknown ones — not bespoke `try/catch`
  handling copy-pasted into every route.

## Async pitfalls

- Never leave a `Promise` unhandled — an unawaited async call whose
  rejection nobody catches becomes an `unhandledRejection`, which in modern
  Node **crashes the process** by default. Await it, `.catch()` it, or
  explicitly fire-and-forget with a documented reason and its own error
  handler. Catching it at the `process`-level listener is a last-resort net
  for what slips through, not the primary handling path.
- `Promise.all` fails fast on the first rejection and abandons the other
  promises' results — use `Promise.allSettled` when partial failure is
  acceptable and every result is still needed.
- Don't `await` sequentially in a loop when the operations are independent —
  that serializes I/O that could run concurrently; build an array of
  promises and `Promise.all` them (see `../SKILL.md`'s Postgres section on
  N+1 for the same mistake with database queries specifically).
- A synchronous, CPU-heavy loop (large JSON transform, crypto, image
  processing) still blocks Node's single thread even inside an `async`
  function — offload it to a worker thread or a queue for anything
  non-trivial.

## Production readiness

- Monitor uptime, resource metrics (CPU/memory/event-loop lag), and errors
  as three distinct concerns — a check that only pings `/health` misses
  event-loop starvation, the most Node-specific failure mode.
- Structured, centrally-aggregated logs, correlated by request id (see
  `api-design.md`) — a `console.log` on a container the platform recycles is
  a log line that never existed.
- Delegate CPU-heavy edge work (gzip, TLS termination) to a reverse proxy or
  load balancer, not the Node process — freeing the event loop for actual
  request handling.
- Commit the lockfile (`package-lock.json`/`pnpm-lock.yaml`) so `npm ci`
  reproduces the exact dependency tree in every environment.
- Run under the deployment platform's own supervisor (a container
  orchestrator's restart policy) rather than stacking a second one like PM2
  on top when already containerized.
  ([nodebestpractices: production practices](https://github.com/goldbergyoni/nodebestpractices))

## Security basics

- Validate every external input against a schema (above) before it reaches
  business logic — most injection and malformed-payload DoS bugs start
  here.
- Never hardcode a secret; read from env/secret manager. Hash passwords with
  bcrypt/scrypt/argon2 — never a fast general-purpose hash.
- Run the process as a non-root user (especially in a container — see
  below) and cap request body size (`express.json({ limit: '1mb' })` or the
  framework's equivalent) to blunt trivial memory-exhaustion attacks.
- Use the ORM/query builder's parameterized queries — never string-concat a
  query with request input.
- Run `npm audit`/`pnpm audit` (or the project's Trail of Bits `modern-python`
  equivalent, on the Python side) in CI, not just locally on a good day.
  ([nodebestpractices: security practices](https://github.com/goldbergyoni/nodebestpractices)
  — full auth/session/secrets depth belongs to the `security` skill, not
  duplicated here)

## Docker

- Multi-stage build: install and build in one stage, copy only the
  production `node_modules` plus the build output into a slim final image
  (`node:XX-slim` or distroless) — keeps the shipped image small and the
  build toolchain out of the attack surface.
- Invoke `node dist/index.js` directly as the container's entrypoint, not
  `npm start` — an extra shell/npm process between PID 1 and the app
  swallows signals and breaks graceful shutdown.
- Handle `SIGTERM` explicitly: stop accepting new connections, let in-flight
  requests finish, then exit — the orchestrator's kill timeout (Railway,
  Kubernetes) is short, and an app that ignores `SIGTERM` gets hard-killed
  mid-request.
- Set a memory limit at both the container level and `--max-old-space-size`
  for V8 — a container OOM-killed by the platform loses the stack trace; a
  V8 heap limit under the container's own limit fails more gracefully.
  ([nodebestpractices: Docker practices](https://github.com/goldbergyoni/nodebestpractices)
  — see `infra-deploy` for the Railway-specific build/deploy side of this)

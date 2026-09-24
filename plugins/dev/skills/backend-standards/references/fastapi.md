# FastAPI

Original synthesis; sources cited inline. Read them for depth — this is a
checklist-with-rationale, not a replacement.

Primary sources: [FastAPI official docs](https://fastapi.tiangolo.com/) and
[zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
(a widely-cited, actively maintained community best-practices collection).

## Pydantic v2

- Use `model_config = ConfigDict(...)` (v2 style), not the v1 `class Config`.
- Separate request models from response models from ORM/DB models. A
  request model should never accidentally expose a field the client
  shouldn't set (e.g. `is_admin`); a response model should never leak a
  field the client shouldn't see (a password hash, an internal id).
  ([FastAPI: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/))
- Prefer `Annotated[Type, Field(...)]` over bare `Field()` defaults for
  clarity with static type checkers.
- Validate cross-field invariants with a `@model_validator(mode="after")`,
  not in the route handler.

## Dependency injection

- Push cross-cutting concerns (current user, DB session, feature flags) into
  `Depends(...)`, not into decorators or manual calls at the top of every
  handler. ([FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/))
- A DB-session dependency should `yield` the session and close/rollback it
  in a `finally`, so a handler that raises still releases the connection.
- Keep dependencies composable and testable — a dependency that itself takes
  `Depends(...)` is normal and preferred over one giant "get everything"
  dependency.

## Async correctness

- `async def` is for I/O-bound work (DB, HTTP, disk). A synchronous DB
  driver call, `time.sleep`, or CPU-heavy work inside an `async def` handler
  blocks the single event loop for **every concurrent request**, not just
  this one — use an async driver (`asyncpg`, `httpx.AsyncClient`) or push the
  blocking call into `run_in_threadpool` / a background worker.
- A plain `def` handler in FastAPI is automatically run in a thread pool —
  correct for genuinely sync, blocking code, wrong for something that's
  actually async-capable (you lose concurrency for no reason).
- Never mix a sync ORM session with an async route without explicitly
  offloading it to a thread.

## Project layout

- Layer by responsibility, not by Django-style app-per-feature-with-
  everything-in-one-file: `routers/` (route declarations only),
  `schemas/` (Pydantic models), `services/` or `crud/` (business logic and
  DB access), `models/` (ORM models), `core/` (settings, security,
  dependencies shared across routers).
  ([zhanymkanov: project structure](https://github.com/zhanymkanov/fastapi-best-practices#project-structure))
- Route handlers should be thin: parse/validate (Pydantic already did this),
  call a service function, return. Business logic belongs in the service
  layer so it's testable without spinning up HTTP.

## Settings

- One `Settings(BaseSettings)` class (`pydantic-settings`), instantiated
  once, injected via `Depends` or imported as a singleton — never
  `os.environ[...]` scattered through the codebase.
- Fail fast: settings should validate at import/startup time (missing
  required env var = the app doesn't start), not at the first request that
  happens to touch that field.

## Error model

- Raise `HTTPException(status_code=..., detail=...)` for expected,
  client-facing errors; let a custom `exception_handler` translate
  domain/service-layer exceptions into the project's standard error shape
  (see `api-design.md` for the shape itself — RFC 9457).
  ([FastAPI: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/))
- Never let a raw unhandled exception reach the client as a 500 with a stack
  trace in production — register a catch-all handler that logs the full
  trace server-side and returns the standard error shape to the caller.
- Don't use exceptions for expected control flow inside a service function
  (e.g. "not found" during a lookup used elsewhere) — return an `Optional`
  and let the route layer decide the HTTP status.

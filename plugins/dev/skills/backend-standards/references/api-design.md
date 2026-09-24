# API Design

Original synthesis; sources cited inline. Primary sources:
[RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457),
[Stripe API docs — idempotent requests](https://docs.stripe.com/api/idempotent_requests),
and general REST convention as documented across
[Microsoft's REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md).

## REST conventions

- Resources are nouns, plural (`/users`, `/orders/{id}/items`), not verbs
  (`/getUser`). The HTTP method carries the verb.
- Use status codes precisely: `200` (OK, has a body), `201` (created, return
  the created resource + `Location` header), `202` (accepted, async
  processing), `204` (no content, e.g. a successful `DELETE`), `400`
  (malformed/invalid request), `401` (not authenticated), `403`
  (authenticated but not authorized), `404` (resource doesn't exist — or,
  deliberately, to avoid leaking existence, when that's a real requirement),
  `409` (conflict — e.g. a uniqueness violation), `422` (well-formed but
  semantically invalid), `429` (rate limited), `500`/`502`/`503` (server-side
  failure — never returned deliberately as "business logic").
- Be consistent about casing and naming across the whole API (`camelCase` or
  `snake_case`, pick one) — a mixed API is a constant source of client bugs.

## Pagination

- Any endpoint returning a list that can grow unbounded must paginate.
  Cursor-based pagination (`?cursor=...&limit=...`, opaque cursor encoding
  the last-seen sort key) is more robust under concurrent writes than
  offset-based (`?page=2&limit=20`), which skips or repeats rows when items
  are inserted/deleted between pages — but offset pagination is acceptable
  for small, rarely-mutated collections where simplicity wins.
- Always include a way for the client to know there's more (a `next_cursor`
  / `has_more` field, or a `Link` header per
  [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288)) — never make the
  client guess from an empty page whether it reached the end or hit an
  error.

## Idempotency keys

- Any endpoint that creates a resource with a real-world side effect
  (charging a card, sending an email, placing an order) should accept an
  `Idempotency-Key` header: the same key retried returns the original
  result instead of repeating the side effect. This is what makes a client
  timeout-and-retry safe.
  ([Stripe docs: Idempotent requests](https://docs.stripe.com/api/idempotent_requests))
- Store the key with the request's outcome (status + response body) keyed
  by `(endpoint, key)`, with a reasonable TTL (Stripe uses 24 hours) — not
  forever, and not so short a legitimate retry after a slow response
  double-fires.
- A `PUT` with a natural idempotent shape (full-resource replace by a known
  id) doesn't need a separate key; `POST` almost always does when it has a
  side effect.

## Versioning

- Version in the URL path (`/v1/...`) or a header
  (`Accept: application/vnd.api+json;version=1`) — pick one convention and
  apply it everywhere; don't mix.
- A breaking change (removing/renaming a field, changing a field's type,
  changing status-code semantics) requires a new version. Adding an
  optional field is not breaking and does not require one.
- Deprecate with a `Sunset` header ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594))
  and a documented timeline before removing an old version — don't just
  delete it.

## Error format — RFC 9457

- Use the `application/problem+json` shape for error responses:
  `type` (a URI identifying the error kind), `title` (short, human-readable
  summary), `status` (matches the HTTP status), `detail` (specific to this
  occurrence), and an `instance` (URI/id of the specific request), plus any
  problem-specific extension members (e.g. `errors: [...]` for
  field-level validation failures).
  ([RFC 9457](https://www.rfc-editor.org/rfc/rfc9457))
- One shape for the whole API — a client should never need a different
  parser for a validation error versus a not-found error versus a rate-limit
  error.
- Never put a stack trace, an internal exception message, or a SQL error in
  `detail` in production — log those server-side with a correlation id and
  put the id in `instance` so support/on-call can find the full context.

## Rate limits

- Any public-writable or expensive endpoint needs a rate limit — per-API-key
  or per-IP as appropriate. Return `429` with a `Retry-After` header, not a
  silent drop or a generic `500`.
- Surface the limit proactively via `RateLimit-Limit`/`RateLimit-Remaining`
  headers (or the equivalent `X-RateLimit-*` convention already used
  elsewhere in the API) so well-behaved clients back off before hitting
  `429`.

## Observability / structured logs

- Every request gets a correlation/request id, generated at the edge if the
  client didn't send one, propagated through every downstream log line and
  returned to the client (e.g. in the error response's `instance`).
- Logs are structured (JSON, or the platform's structured-log convention) —
  `level`, `message`, `request_id`, and relevant fields as separate keys,
  not interpolated into a prose string. A log line that can't be queried by
  field is a log line that won't be found during an incident.
- Log the *decision*, not just the event: "rate limit exceeded, key=X,
  limit=100/min" is useful; "error" is not.

## Secrets

- No secret (API key, DB connection string, signing key) in a URL query
  string (it ends up in access logs), in a client-visible response, or in
  a log line — including inside a caught exception's message that gets
  logged. Redact known secret-shaped fields before logging request/response
  bodies.

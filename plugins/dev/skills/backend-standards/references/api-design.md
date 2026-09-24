# API Design

Original synthesis; sources cited inline. Primary sources:
[RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457),
the IETF draft
[The Idempotency-Key HTTP Header Field](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
(expired as an Internet-Draft, but already the de facto convention — see
[Stripe's implementation](https://docs.stripe.com/api/idempotent_requests) for
a production example),
[Google AIP](https://google.aip.dev/) (Google's resource-oriented API design
standard), and the
[Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md).

## REST conventions

- Resources are nouns, plural (`/users`, `/orders/{id}/items`), not verbs
  (`/getUser`). The HTTP method carries the verb. For an API large enough to
  need a rigorous take, [AIP-121](https://google.aip.dev/121) (resource-
  oriented design) and [AIP-122](https://google.aip.dev/122) (resource
  names) formalize this into a resource hierarchy
  (`/publishers/{p}/books/{b}`) — better than a flat sprawl of unrelated
  collections once nesting reflects real ownership.
- Use status codes precisely: `200` (OK, has a body), `201` (created, return
  the created resource + `Location` header), `202` (accepted, async
  processing), `204` (no content, e.g. a successful `DELETE`), `400`
  (malformed/invalid request), `401` (not authenticated), `403`
  (authenticated but not authorized), `404` (resource doesn't exist — or,
  deliberately, to avoid leaking existence, when that's a real requirement),
  `409` (conflict — e.g. a uniqueness violation), `422` (well-formed but
  semantically invalid), `429` (rate limited), `500`/`502`/`503` (server-side
  failure — never returned deliberately as "business logic").
- Be consistent about casing and naming across the whole API — a mixed API
  is a constant source of client bugs. The Microsoft guidelines default to
  camelCase for JSON fields and kebab-case for URL path segments; a
  reasonable choice if the project has no existing convention, but the
  choice matters less than applying it everywhere.

## Pagination

- Any endpoint returning a list that can grow unbounded must paginate.
  Cursor-based pagination (`?cursor=...&limit=...`, opaque cursor encoding
  the last-seen sort key) is more robust under concurrent writes than
  offset-based (`?page=2&limit=20`), which skips or repeats rows when items
  are inserted/deleted between pages — but offset pagination is acceptable
  for small, rarely-mutated collections where simplicity wins.
- [AIP-158](https://google.aip.dev/158) formalizes the same idea as an
  opaque `page_token` / `next_page_token` pair — semantically identical to
  `cursor`/`next_cursor`. Microsoft's convention instead wraps the page as
  `{ value: [...], nextLink: <absolute URL> }`, worth adopting wholesale if
  the client already expects Microsoft-shaped APIs (Graph, Azure SDKs). The
  field names matter less than the one hard rule below.
- Always include a way for the client to know there's more (a `next_cursor`
  / `has_more` field, a `nextLink`, or a `Link` header per
  [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288)) — never make the
  client guess from an empty page whether it reached the end or hit an
  error.

## Idempotency keys

- Any endpoint that creates a resource with a real-world side effect
  (charging a card, sending an email, placing an order) should accept an
  `Idempotency-Key` request header: the same key retried returns the
  original result instead of repeating the side effect. This is what makes
  a client timeout-and-retry safe. Use the IETF header name rather than
  inventing a bespoke one — it's what Stripe, PayPal, and most payment/
  webhook APIs already ship, so clients and libraries expect it even though
  the I-D itself expired without becoming an RFC.
  ([IETF draft-ietf-httpapi-idempotency-key-header](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/);
  [Stripe docs: idempotent requests](https://docs.stripe.com/api/idempotent_requests))
- Fingerprint the request body alongside the key: the same key arriving with
  a *different* body is a client bug (a reused key for a different logical
  request), not a legitimate retry — reject it (`409`/`422`) rather than
  silently replaying the first response for a different request.
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
  apply it everywhere; don't mix. [AIP-185](https://google.aip.dev/185)
  argues for path versioning specifically for a public API: a header is
  easy for a client to omit by accident and doesn't show up in
  browser/curl exploration. Microsoft instead mandates an explicit
  `api-version` **query parameter** on every request (`YYYY-MM-DD` format,
  rejecting with `400` if missing) — also defensible, but pick one up
  front; mixing path and query versioning across endpoints of the same API
  is its own bug class.
- A breaking change (removing/renaming a field, changing a field's type,
  changing status-code semantics) requires a new version. Adding an
  optional field is not breaking and does not require one.
- Deprecate with a `Sunset` header ([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594))
  and a documented timeline before removing an old version — don't just
  delete it.

## Long-running operations

- An operation that can't complete synchronously (a bulk import, a report
  generation) returns `202 Accepted` with an `operation-location`/`Location`
  header pointing at a status resource — never make the client poll the
  original endpoint or hold a connection open.
- The status resource reports a status (`pending`/`running`/`succeeded`/
  `failed`) plus a `result`/`error` once terminal, and stays fetchable for
  at least 24h after completion so a slow client isn't left with nothing.
  ([Microsoft REST API Guidelines: long-running operations](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md))

## Error format — RFC 9457

- Use the `application/problem+json` shape for error responses:
  `type` (a URI identifying the error kind), `title` (short, human-readable
  summary), `status` (matches the HTTP status), `detail` (specific to this
  occurrence), and an `instance` (URI/id of the specific request), plus any
  problem-specific extension members (e.g. `errors: [...]` for
  field-level validation failures).
  ([RFC 9457](https://www.rfc-editor.org/rfc/rfc9457))
- Google's own APIs converge on the same idea from a different shape
  (`google.rpc.Status`: `code` + `message` + typed `details[]`, per
  [AIP-193](https://google.aip.dev/193)) — worth matching if the client
  ecosystem is already gRPC/Google-shaped. For a plain HTTP/JSON API, RFC
  9457 is the more interoperable default: it's an actual IETF standard with
  an IANA-registered media type, not a convention tied to one vendor.
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

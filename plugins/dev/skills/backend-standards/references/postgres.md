# Postgres

Original synthesis; sources cited inline. Primary sources:
[PostgreSQL official documentation](https://www.postgresql.org/docs/current/),
[Supabase docs — connecting to your database](https://supabase.com/docs/guides/database/connecting-to-postgres),
and [Neon docs — connection pooling](https://neon.tech/docs/connect/connection-pooling).

## Migrations

- The migration history is the schema's source of truth, applied
  forward-only through CI/CD (or the ORM's migration tool — Alembic,
  Prisma Migrate, Drizzle Kit). Never hand-edit a production schema through
  a one-off `psql` session; the drift is invisible until the next migration
  conflicts with it.
- Every migration that changes an existing column's type or constraint on a
  non-trivial table should be checked for lock behavior: an
  `ALTER TABLE ... ADD COLUMN ... NOT NULL` without a default takes an
  `ACCESS EXCLUSIVE` lock and rewrites the table on older Postgres versions
  — for a live table, add the column nullable, backfill, then add the
  constraint (`ADD CONSTRAINT ... NOT VALID` + `VALIDATE CONSTRAINT`
  separately avoids a long-held lock on validation).
  ([Postgres docs: ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html))
- Never let application startup auto-run migrations against a shared
  database in a multi-instance deployment — two instances racing the same
  migration is a real failure mode. Run migrations as a separate,
  single-instance deploy step.

## Indexes

- Every column used in a `WHERE`, a `JOIN ON`, or an `ORDER BY` on a table
  that will grow needs an index, or a documented reason it doesn't (e.g. the
  table is small and bounded).
- A composite index's column order matters: put the equality-filtered column
  first, the range-filtered/sorted column last — Postgres can use a prefix
  of a composite index but not a suffix.
- `EXPLAIN (ANALYZE, BUFFERS)` before assuming an index fixed something —
  a sequential scan on a small table is often faster than an index scan; the
  planner's choice is usually right.
  ([Postgres docs: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html))
- An index has a write cost (every insert/update maintains it) — don't add
  one speculatively on a write-heavy table without a query that needs it.

## Transactions

- Wrap a multi-statement write (e.g. debit one row, credit another) in a
  single transaction — partial application on failure is a real bug, not an
  edge case.
- Keep transactions short. A transaction held open across an external HTTP
  call, an email send, or a long computation holds row/table locks the
  whole time and is a common source of production lock contention — do the
  external work before or after the transaction, not inside it.
- Understand the isolation level in use (`READ COMMITTED` is Postgres's
  default). A "check then insert" pattern relying on uniqueness should use
  `INSERT ... ON CONFLICT DO NOTHING/UPDATE` (upsert) rather than a
  check-then-write race, which is not safe under concurrent requests even
  inside a transaction at the default isolation level.
  ([Postgres docs: INSERT ... ON CONFLICT](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT))

## N+1 queries

- A loop that issues one query per iteration (fetch a list, then fetch each
  item's related row one at a time) is the single most common backend
  performance bug. Fix with a single query using `JOIN` or `WHERE id = ANY($1)`
  /`IN (...)`, or with the ORM's explicit eager-loading (`selectinload` in
  SQLAlchemy, `include` in Prisma) — never rely on an ORM's default lazy
  loading inside a loop.
- The fix is a code-review checklist item, not just a monitoring concern:
  any handler that loops over a list and calls a DB or DAO function inside
  the loop body should be flagged.

## Serverless / edge connection pooling

- A serverless or edge function that opens its own direct Postgres
  connection per invocation exhausts the database's connection limit under
  concurrency — Postgres's default `max_connections` is in the low hundreds,
  and a burst of serverless invocations can each hold one.
- **Supabase:** use the pooled connection string (the `pgbouncer`/Supavisor
  endpoint, port 6543 in transaction mode) for application code, not the
  direct connection (port 5432) — reserve the direct connection for
  migrations and long-lived connections that need session-level features
  (prepared statements, `LISTEN/NOTIFY`).
  ([Supabase docs: Connecting to your database](https://supabase.com/docs/guides/database/connecting-to-postgres))
- **Neon:** use the pooled connection string (`-pooler` in the hostname) for
  application/serverless code; Neon's pooler is also PgBouncer-based in
  transaction mode.
  ([Neon docs: Connection pooling](https://neon.tech/docs/connect/connection-pooling))
- Transaction-mode pooling means no session state across statements
  (prepared statements, advisory locks, `SET` outside a transaction won't
  persist) — code written assuming a direct session-mode connection can
  silently misbehave when pointed at a pooled endpoint.

## Row Level Security

Out of scope here by design — RLS policy design, testing, and pitfalls are
covered in depth by the vendor's own skill
(`supabase/agent-skills`, installed by `setup-repo` when Supabase is
detected). Defer to it rather than duplicating RLS guidance here.

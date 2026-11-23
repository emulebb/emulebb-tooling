# emulebb-rust Persistence Policy

This task-routed annex applies only to persisted settings, metadata, database
schemas, or profile compatibility.

- Keep TOML limited to basic process/profile/service bootstrap configuration.
  Beta3 uses snake_case keys such as `bind_addr`, `api_key` and
  `web_root_dir`, with REST `20017`, P2P TCP `20019` and UDP `20020`.
  Preserve these keys and semantics across updates by default. Future changes
  need explicit contract review. The [Public Foundation](../design/PUBLIC-FOUNDATION.md)
  defines the coordinated DB, settings, CLI and REST contract.
- SQLite owns mutable settings and durable product state. Runtime-only sockets,
  timers, queues, and pending work remain in memory. Downloaded payloads, logs,
  and retained diagnostics remain files, not alternative settings authorities.
- `server.met` and `nodes.dat` are read-only compatibility import inputs.
  The Rust client must never write them. [RUST-CI-055](../active/items/RUST-CI-055.md)
  tracks end-to-end qualification of the import and checkpoint lifecycle.
  Stock MFC and upstream fixtures have their own contracts.
- Review schema changes against the [Public Foundation](../design/PUBLIC-FOUNDATION.md).
  Preserving profiles across incompatible schemas requires separate review.
  [RUST-FEAT-063](../active/items/RUST-FEAT-063.md) owns explicit
  source-version semantic export and fresh-target import.
- Round one implements a coordinated fresh-profile schema. Review every
  persisted-data change against the accepted foundation and exact current
  model. Future automatic upgrades are an objective, not implemented machinery
  or enforcement in this round.
- Product code requires the current schema exactly. It must not contain legacy
  branches, fallback reads, migrations, repair, profile-reset logic, or silent
  compatibility behavior.
- The bounded-monolith product uses one SQLite database for client, future
  autonomous-index, and future adapter-owned durable state. Domain ownership is
  an internal code boundary, not a separate compatibility or migration domain.
- A schema-version change makes existing end-user profiles incompatible.
  Startup fails visibly and instructs the user to create an entirely fresh
  profile; it must not delete, move, replace, migrate, or partially reset the
  incompatible profile.
- An index-only incompatibility invalidates the whole profile. Do not add an
  automatic partial index rebuild, domain-specific migration, or preservation
  path during the beta phases.
- The future autonomous index persists observations until explicit operator
  deletion. It has no product TTL or configured capacity limit. On low disk or
  index-write failure, pause index writes and active discovery, keep normal
  client networking/transfers available, and expose a persistent fault.
- Python migrations in `repos\emulebb-build-tests` are backup-first internal
  support for known test and soak schemas only. They are not an end-user
  migration or recovery path and do not belong in product-facing guidance.

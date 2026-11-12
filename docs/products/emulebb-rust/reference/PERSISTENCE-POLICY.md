# emulebb-rust Persistence Policy

This task-routed annex applies only to persisted settings, metadata, database
schemas, or profile compatibility.

- Keep TOML limited to basic process/profile/service bootstrap configuration.
  The accepted clean Beta3 target uses snake_case `bind_addr`, `api_key` and
  `web_root_dir`, with REST `20017`, P2P TCP `20019` and UDP `20020`. Adopt that
  contract directly, then preserve its keys and semantics across updates by
  default; future changes need explicit contract review. Never add aliases,
  compatibility shims, fallback reads, remapping or silently ignored obsolete
  fields. Retired shapes are hard errors. This stability goal is separate from
  database readability and the post-Arr REST freeze.
  [RUST-CI-043](../active/items/RUST-CI-043.md) owns the concrete configuration
  and API consistency review; it does not itself freeze every existing shape.
- SQLite owns mutable settings and durable product state. Runtime-only sockets,
  timers, queues, and pending work remain in memory. Downloaded payloads, logs,
  and retained diagnostics remain files, not alternative settings authorities.
- `server.met` and `nodes.dat` are read-only compatibility import inputs. The
  Rust client must not create, refresh, replace, or write them back. Existing
  `nodes.dat` persistence paths must be removed under
  [RUST-FEAT-062](../active/items/RUST-FEAT-062.md); the target contract is not
  a claim that those paths are already fixed. This rule does not rewrite stock
  MFC or upstream server fixture-generation behavior.
- Review schema efficiency, naming, and future domain boundaries under
  [RUST-CI-044](../active/items/RUST-CI-044.md). Configuration stability does not
  authorize product migrations, aliases, or silent profile repair. A proposal
  to preserve profiles across incompatible schemas is a separate parent review
  of the current beta rules below. Existing
  [RUST-FEAT-063](../active/items/RUST-FEAT-063.md) owns explicit source-version
  semantic export and fresh-target import; that workflow does not migrate an
  old database during normal startup and remains unimplemented.
- During the compatibility-unstable beta phases, every persisted-data change reviews whether
  the checked-in schema remains the clean current model. Evolve it when
  warranted; do not preserve inferior shapes for development profiles.
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

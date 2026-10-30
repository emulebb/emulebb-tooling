# emulebb-rust Persistence Policy

This task-routed annex applies only to persisted settings, metadata, database
schemas, or profile compatibility.

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

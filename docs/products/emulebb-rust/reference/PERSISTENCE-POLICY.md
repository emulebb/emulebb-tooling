# emulebb-rust Persistence Policy

This task-routed annex applies only to persisted settings, metadata, database
schemas, or profile compatibility.

- During the experimental phase, every persisted-data change reviews whether
  the checked-in schema remains the clean current model. Evolve it when
  warranted; do not preserve inferior shapes for development profiles.
- Product code requires the current schema exactly. It must not contain legacy
  branches, fallback reads, migrations, repair, profile-reset logic, or silent
  compatibility behavior.
- A schema-version change makes existing end-user profiles incompatible.
  Startup fails visibly and instructs the user to create an entirely fresh
  profile; it must not delete, move, replace, migrate, or partially reset the
  incompatible profile.
- Python migrations in `repos\emulebb-build-tests` are backup-first internal
  support for known test and soak schemas only. They are not an end-user
  migration or recovery path and do not belong in product-facing guidance.

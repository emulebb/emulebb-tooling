---
id: RUST-BUG-184
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/299
title: Make settings PATCH persistence atomic
status: DONE
priority: Major
category: bug
labels: [rust, audit, settings, sqlite, api]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-directed config/API and database review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/299. This local document owns the durable engineering specification and evidence.

# RUST-BUG-184 - Make settings PATCH persistence atomic

## Closure And Evidence

[PR #316](https://github.com/emulebb/emulebb-rust/pull/316) merged as
`32305dabe90b59abad642c6c3ae1687dc53b27ae` and closed
[#299](https://github.com/emulebb/emulebb-rust/issues/299). Mixed requests
validate the whole candidate and commit affected sections in one serialized
transaction before publication. Concurrent partial updates retain omitted
fields; admitted updates finish publication despite caller cancellation.

The accepted PR records real-router later-write rollback, direct-core
validation, independent-connection, cancellation, concurrency and restart
regressions. A committed update's later runtime-refresh error is classified
separately; artificial injection of that post-commit refresh failure remains an
accepted follow-up, not completed runtime evidence. No TOML keys, DTOs or
migration path were introduced.

The fix is included in qualified main and published
[Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
at `080a5dea70186da31dab958757b5b8c0fd883f82`. The earlier findings and
checklist below preserve the original contract; configuration/schema reviews
must reuse this implementation rather than commission another atomicity fix.

## Problem

A multi-section settings update spans separate database transactions. At Rust
`edc59a003fff873e26d2c720bf9ca06f4b640871`,
`EmulebbCore::update_app_settings` persists non-core sections before calling
`update_core_settings`, which validates the core candidate. Each non-core
section is also committed separately.

Direct-core-API source example:
`{"nat":{"enabled":true},"core":{"uploadLimitKiBps":0}}`. If passed directly
to `update_app_settings`, NAT can commit before core validation fails. This is
not an HTTP reproduction: REST middleware validates core ranges before the
handler and rejects this payload before the update path. Choose a different
initial NAT value when writing the direct-core regression.

The separate per-section transactions also leave a partial-commit risk if a
later storage operation fails after an earlier section commits. Reproduce that
through the actual HTTP router with a valid request and injected later-write
failure before claiming a REST partial-update witness. No runtime reproduction
or fault injection was performed by this review.

## Source evidence

- `crates/emulebb-core/src/app_api.rs`, `update_app_settings` and `update_core_settings`.
- `crates/emulebb-core/src/profile_state.rs`, `persist_app_settings_update` and `persist_settings_section`.
- `crates/emulebb-settings/src/lib.rs`, core upload-limit validation.
- `crates/emulebb-rest/src/handlers/app.rs`, PATCH error response.
- `crates/emulebb-rest/src/route_metadata.rs` and `route_body_metadata.rs`,
  pre-handler request validation.
- `crates/emulebb-rest/src/route_body_metadata/validators/core_settings.rs`,
  core numeric range checks before the handler.
- Metadata settings replacement currently provides a transaction per section rather than per request.

## Acceptance criteria

- [ ] With a synthetic disposable profile, test direct-core invalid input and
      the same request through the real HTTP router separately. Both rejected
      paths must leave requested persisted sections and live settings unchanged.
- [ ] Use a valid multi-section HTTP PATCH with an injected later DB-write
      failure to establish the storage-failure path. Prove all requested
      persisted sections remain unchanged when the operation fails.
- [ ] Decode and validate the entire effective candidate before writing any section. Keep current setting names, units, defaults, and retired-field errors.
- [ ] Commit all durable sections from one PATCH in one SQLite transaction through the owning metadata API. An injected failure in a later write must roll back earlier writes.
- [ ] Publish live settings only after successful durable commit; define and test ordering/concurrency so simultaneous PATCHes do not publish stale snapshots or introduce lost updates.
- [ ] Successful partial PATCHes preserve unspecified settings, return the committed canonical state, and retain documented restart-only semantics.
- [ ] Keep REST, OpenAPI, and first-party consumer tests coherent. Do not change the API namespace, introduce aliases, migrate schemas/profiles, or refactor unrelated settings behavior.

## Ownership and validation

One implementation owner coordinates core, settings, metadata, and REST files through the parent. Both RUST-CI-043 / #297 and RUST-CI-044 / #298 reference this issue; they must not commission competing fixes. Coordinate nearby settings-authority work with RUST-BUG-156 / #223.

Use meaningful core/metadata/REST regressions for invalid input, transactional rollback, a successful multi-section update, unchanged omitted values, and concurrent updates. Run scoped required checks on Windows/Linux; source inspection alone is insufficient completion evidence. Do not use operator databases or launch live/soak tests.

Major, Phase 0, Beta 3 backlog. Queued behind the current workspace/platform foundation. Beta 3 release and candidate certification remain on hold.

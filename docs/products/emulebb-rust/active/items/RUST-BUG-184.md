---
id: RUST-BUG-184
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/299
title: Make settings PATCH persistence atomic
status: OPEN
priority: Major
category: bug
labels: [rust, audit, settings, sqlite, api]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-directed config/API and database review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/299. This local document owns the durable engineering specification and evidence.

# RUST-BUG-184 - Make settings PATCH persistence atomic

## Problem

A rejected multi-section settings PATCH can already have changed persisted settings. At Rust `edc59a003fff873e26d2c720bf9ca06f4b640871`, `EmulebbCore::update_app_settings` persists non-core sections before calling `update_core_settings`, which validates the core candidate. Each non-core section is also committed separately.

Source-traced example: `{"nat":{"enabled":true},"core":{"uploadLimitKiBps":0}}`. The NAT section can commit before the invalid core upload limit is rejected and REST returns BAD_REQUEST. Choose an initial NAT value different from the request when writing the regression. This is source evidence, not a runtime reproduction or a claim that every failure path was tested.

## Source evidence

- `crates/emulebb-core/src/app_api.rs`, `update_app_settings` and `update_core_settings`.
- `crates/emulebb-core/src/profile_state.rs`, `persist_app_settings_update` and `persist_settings_section`.
- `crates/emulebb-settings/src/lib.rs`, core upload-limit validation.
- `crates/emulebb-rest/src/handlers/app.rs`, PATCH error response.
- Metadata settings replacement currently provides a transaction per section rather than per request.

## Acceptance criteria

- [ ] Reproduce the rejected-request partial mutation with a synthetic disposable profile; add a regression proving every requested persisted section and live core setting remains unchanged when validation fails.
- [ ] Decode and validate the entire effective candidate before writing any section. Keep current setting names, units, defaults, and retired-field errors.
- [ ] Commit all durable sections from one PATCH in one SQLite transaction through the owning metadata API. An injected failure in a later write must roll back earlier writes.
- [ ] Publish live settings only after successful durable commit; define and test ordering/concurrency so simultaneous PATCHes do not publish stale snapshots or introduce lost updates.
- [ ] Successful partial PATCHes preserve unspecified settings, return the committed canonical state, and retain documented restart-only semantics.
- [ ] Keep REST, OpenAPI, and first-party consumer tests coherent. Do not change the API namespace, introduce aliases, migrate schemas/profiles, or refactor unrelated settings behavior.

## Ownership and validation

One implementation owner coordinates core, settings, metadata, and REST files through the parent. Both RUST-CI-043 / #297 and RUST-CI-044 / #298 reference this issue; they must not commission competing fixes. Coordinate nearby settings-authority work with RUST-BUG-156 / #223.

Use meaningful core/metadata/REST regressions for invalid input, transactional rollback, a successful multi-section update, unchanged omitted values, and concurrent updates. Run scoped required checks on Windows/Linux; source inspection alone is insufficient completion evidence. Do not use operator databases or launch live/soak tests.

Major, Phase 0, Beta 3 backlog. Queued behind the current workspace/platform foundation. Beta 3 release and candidate certification remain on hold.

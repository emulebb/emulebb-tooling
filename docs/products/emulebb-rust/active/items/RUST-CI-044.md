---
id: RUST-CI-044
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/298
title: Review SQLite schema efficiency and evolution boundaries
status: IN_PROGRESS
priority: Major
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-directed configuration and persistence architecture review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/298. This local document owns the durable engineering specification and evidence.

# RUST-CI-044 - Review SQLite schema efficiency and evolution boundaries

## Outcome

Review the Rust SQLite schema for efficiency, clear ownership and naming, safe evolution, and the bounded-monolith Client/Indexer/Arr direction before Beta 3. Produce evidence-backed decisions and independent implementation slices; no speculative schema rewrite.

## Operator direction

- SQLite is the authority for mutable settings and durable product state. Keep only basic, stable bootstrap configuration in TOML.
- `server.met` and `nodes.dat` are read-only compatibility inputs; the Rust client never writes them back. RUST-FEAT-062 / #233 owns the remaining implementation.
- Runtime-only work stays in memory. Downloaded payloads, logs, diagnostic artifacts, and the database file itself are not additional mutable settings authorities.
- Avoid breaking configuration on each update. Current exact-schema/fresh-profile beta rules must be reviewed explicitly; do not introduce migrations, repair paths, or aliases without a concrete compatibility decision.
- Beta 3 release/certification remains held. Source-only review may run alongside workspace/platform work.

## Acceptance criteria

- [ ] Map current tables, columns, indexes, constraints, foreign keys, identifiers, units, nullability, domain ownership, and settings authorities against actual repositories and queries.
- [ ] Review read/write hot paths, indexes and query plans, batching/transactions, WAL/durability settings, locking/concurrency, prepared statements, and large-library/index growth. Separate measured evidence from source-based hypotheses.
- [ ] Review schema/table/column naming and typed representation against Rust domain models and REST/OpenAPI. Prioritize confusing or incorrect semantics over cosmetic churn.
- [ ] Check atomicity and restart behavior for settings, transfer/library state, and Kad snapshots; enumerate mutable side files and their existing owners.
- [ ] Test the design against Windows/Linux, x64/ARM64, path/filename semantics, bounded memory, and the future single-daemon/single-SQLite Client/Indexer/Arr boundaries without implementing later phases.
- [ ] Produce an explicit config/schema evolution proposal with update examples and rollback/failure behavior. Flag the existing whole-profile incompatibility policy as an important parent decision; do not silently change it.
- [ ] Route findings to existing backlog owners; create bounded new work only where gaps remain. Include performance verification plans using synthetic/disposable data, never operator DBs.
- [ ] Reconcile durable architecture/persistence references with approved conclusions; do not report the review as a completed implementation.

## Coordination

The sibling config/API review owns bootstrap key semantics and REST/consumer coherence. RUST-BUG-156 / #223 owns ED2K setting duplication; RUST-FEAT-062 / #233 owns Kad SQLite/import-only persistence. Respect other active transfer, library, profile-ownership, and index backlog owners. Schema/manifests/shared contracts require parent coordination before edits.

RUST-FEAT-063 / #234 already owns explicit source-version semantic export and
fresh-target import, without opening or migrating an old database in the new
binary. Evaluate that continuity design before proposing another mechanism.

Priority: Major. Client/Phase 0 review for Beta 3; release remains held.

## Initial Source Review

Reviewed Rust `edc59a003fff873e26d2c720bf9ca06f4b640871`, current schema 67.
The existing model already uses strict tables, checked numeric mappings,
foreign-key index regression checks, and synthetic large-catalog query-plan
tests. Preserve those strengths; source inspection does not justify a broad
schema rewrite or prove production performance.

Settings sections currently commit separately, and non-core sections can
commit before core validation rejects a PATCH. The one coordinated fix owner
is [RUST-BUG-184](RUST-BUG-184.md),
[issue #299](https://github.com/emulebb/emulebb-rust/issues/299), shared with
RUST-CI-043. Runtime reproduction and failure-injection regressions remain
pending. No profile data was inspected and no migration was performed.

Other findings retain their existing owners: RUST-REF-016 / #155 for bounded
persistence execution, RUST-BUG-163 / #247 for profile process ownership,
RUST-REF-008 / #96 for I/O/query work, and RUST-FEAT-062 / #233 for normalized
Kad snapshots. WAL does not by itself make synchronous mutex-held DB work
safe to run on async workers; coordinate that implementation through #155.

Minor assurance question: current schema descriptors validate structure and
object names without proving all CHECK, trigger, partial-index predicate, or
FTS-option SQL semantics. Define the promised validation boundary before
hardening it. This source observation is not a reproduced corruption or
security failure and does not justify a schema rewrite.

Detailed source evidence and eight bounded work slices are retained below
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/db-schema-review/` in
`db-schema-review.json` and `findings.txt`. Performance remains unmeasured by
this review. Serialize schema/version integration and overlapping settings
edits; other source-review slices can proceed independently.

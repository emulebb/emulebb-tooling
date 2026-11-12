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

## Distribution Intake Acceptance

- [ ] Reconcile actual current schema/owner facts before making update claims;
      intake main `a2414638` uses schema 68. Packaging cannot convert a database.
- [ ] Keep one SQLite authority, minimal stable TOML, readonly met imports and
      existing fresh-profile refusal. Retain matching binary/profile rollback
      without aliases, repair, automatic reset or partial index reconstruction.
- [ ] Package/channel/service consumers use this contract. Scheduling stays with
      [#155](RUST-REF-016.md), Kad persistence with [#233](RUST-FEAT-062.md),
      and semantic continuity with [#234](RUST-FEAT-063.md); add no rival owner.

## Outcome

Review the Rust SQLite schema for efficiency, clear ownership and naming, safe evolution, and the bounded-monolith Client/Indexer/Arr direction before Beta 3. Produce evidence-backed decisions and independent implementation slices; no speculative schema rewrite.

## Parent Review Refresh (2026-11-12)

The parent [refreshed the review](https://github.com/emulebb/emulebb-rust/issues/298#issuecomment-6830060765)
against Rust `080a5dea70186da31dab958757b5b8c0fd883f82`, schema 68. Accepted
shared boundaries retain one SQLite authority, stable minimal TOML, WAL/FULL
durability and the exact-schema/fresh-profile rule. The review remains In
Progress; current-source inspection is not measured query/latency evidence.

[#299's atomic settings fix](https://github.com/emulebb/emulebb-rust/pull/316)
is merged and closed. Preserve its coordinated transaction and ordered
post-commit publication. The proposed target settings representation, revision
and ETag model is additional unaccepted design, not missing atomicity work.
The operator accepted clean snake_case bootstrap keys `bind_addr`, `api_key`,
`web_root_dir` and target REST `20017` / P2P TCP `20019` / UDP `20020`.
No aliases, compatibility shims, fallback keys, remapping or silent ignoring
are permitted. The remaining leaf/storage/REST redesign still requires bounded
review; naming/default acceptance does not claim runtime implementation.

The accepted [155-A friend-persistence slice](https://github.com/emulebb/emulebb-rust/issues/155#issuecomment-6830001541)
preserves schema 68 and guarantees ordering through commit/cache publication,
including cancellation, without holding the SQLite mutex across a finalizer.
Legacy synchronous paths remain. #233 must later reuse that owner for typed,
generation-safe Kad snapshots; the parent reserves schema/version/Core/shutdown
integration. [Scoop's accepted boundary](https://github.com/emulebb/emulebb-rust/issues/324#issuecomment-6830047076)
uses the current deployment and fresh-profile contract without converting a
database or translating configuration. No schema or runtime implementation
is claimed by this refresh; unproven checklist items stay open.

## Operator direction

- SQLite is the authority for mutable settings and durable product state. Keep only basic, stable bootstrap configuration in TOML.
- `server.met` and `nodes.dat` are read-only compatibility inputs; the Rust client never writes them back. RUST-FEAT-062 / #233 owns the remaining implementation.
- Runtime-only work stays in memory. Downloaded payloads, logs, diagnostic artifacts, and the database file itself are not additional mutable settings authorities.
- Preserve the exact-schema/fresh-profile beta rules. Do not introduce migrations, repair paths, automatic resets, aliases, compatibility shims, fallback keys, remapping or silent ignoring of obsolete configuration.
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

## Initial Source Review (Historical)

Reviewed Rust `edc59a003fff873e26d2c720bf9ca06f4b640871`, current schema 67.
The existing model already uses strict tables, checked numeric mappings,
foreign-key index regression checks, and synthetic large-catalog query-plan
tests. Preserve those strengths; source inspection does not justify a broad
schema rewrite or prove production performance.

At that historical source, sections committed separately and direct core API
calls could persist non-core sections before core validation failed. Earlier
HTTP middleware validation meant the invalid-core example was not an HTTP
partial-write reproduction. The coordinated
[RUST-BUG-184](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-BUG-184.md)
fix subsequently supplied real-router later-write failure/rollback regressions
and atomic commit/publication; it is merged and
[#299 is closed](https://github.com/emulebb/emulebb-rust/issues/299).
Artificial post-commit runtime-refresh failure injection remains a distinct
accepted follow-up, not completed runtime evidence. The old finding must not
commission a duplicate fix. No operator profile was inspected or migrated.

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

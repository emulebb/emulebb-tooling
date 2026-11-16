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

## Registered runtime and local-suite evidence (2026-11-16)

The [#233 registered runtime checkpoint](RUST-FEAT-062.md#registered-kad-runtime-checkpoint-2026-11-16)
records the passing supported build and REST CI campaign for the exact Rust
`d5c2cfbe` / tests `0531be83` / tooling `eac34a72` / Builder `e93fca5` bundle.
It qualifies current conformance/SSE, six delegated friend fault/retry frontdoors
and real Kad SQLite fault/retry, graceful reopen and same-profile restart.
The report records graceful termination of all owned daemons; friend-only
`quick_check` evidence is distinct from Kad reopen/restart assertions.

The [#233 local-suite checkpoint](RUST-FEAT-062.md#runtime-coupling-local-suite-checkpoint-2026-11-16)
records green final uncommitted working material: full supported Rust-unit suite,
eight existing Python owners and WebUI unit/browser/typecheck/build checks,
after retained fixture/lifetime and shutdown-failure repairs. Those local suites
preceded the exact committed-stage campaign above. The prepared 100k library
fixture remains preparation, not runtime or combined 100k-job qualification. The canonical settings/CLI and
other public-foundation pieces remain their existing implementation scope.

## Schema and fixture preparation checkpoint (2026-11-15)

The [#233 schema 72 checkpoint](RUST-FEAT-062.md#schema-72-and-typed-owner-checkpoint-2026-11-15)
records current fresh schema 72 at Rust `ca5e6993`, typed owner byte leases,
durable generated Kad identity and focused storage/Core/Python proof. At that
checkpoint runtime DHT binding and persistence were in progress; the registered
runtime proof above is subsequent. Dated schema 71 evidence is retained
without claiming it qualifies schema 72.

The existing shared-library harness fixture is **prepared, not runtime-qualified**:
100,000 files, 10,485,760,000 bytes, 1,000 long paths and 16 Unicode entries, with
zero missing/unexpected entries. Its case-alias cohort was skipped on native
NTFS. Source admission evidence is retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/workstreams/public-foundation-round-1/shared-library-io-admission/348c9e65554443fa84856cf30d097645/sources.json`.
That receipt records prepare provenance, not daemon query/ingest performance.
No combined 100,000-job profile, full platform matrix or 365-day claim follows.

## Registered current-contract checkpoint (2026-11-15)

The [#155 registered conformance/peer checkpoint](RUST-REF-016.md#registered-conformance-and-local-peer-checkpoint-2026-11-15)
retains the first failed campaign, its runtime drain repair and passing rerun at
Rust `b509524f` / tests `a96b5859` / tooling `26492515` / Builder `e93fca5`.
The rerun covered 83/105 current main operations, 43 expected errors and 22 explicit
unsafe skips, plus SSE and 6/6 delegated friend mutations with failure/retry and
clean-process/database proof. These are current-contract results, not
qualification of the unimplemented 59-field settings/CLI or full library/job
foundation. Upload progress under database contention and broad scale/platform
proof remain pending.

## Shared friend-owner dependency checkpoint (2026-11-15)

The [#155 scoped friend-owner checkpoint](RUST-REF-016.md#scoped-friend-owner-checkpoint-2026-11-15)
records implementation at Rust `ea0f9653`, focused Core/REST/integration proof
and selected-artifact OpenAPI validation. Historical discovery notes below
predate that worker implementation. This does not claim runtime Kad persistence,
the canonical settings/CLI redesign, all-SQL async conversion, actual upload
contention behavior or combined-scale qualification. Continue through the same
owner rather than add another persistence lane.

## Typed metadata checkpoint (2026-11-15)

The [#233 typed metadata checkpoint](RUST-FEAT-062.md#typed-metadata-checkpoint-2026-11-15)
records Rust `c14433d5` / `82181294`, fresh schema 71, 108 metadata unit plus 3
integration passes and the existing Python 80-pass/one-skip receipt. Explicit
column ownership is reviewed; this does not prove runtime Kad wiring, the
settings/public-contract redesign, bounded async ownership or combined scale.
Historical schema 68/69 review evidence below is not a downgrade instruction.

## Historical foundation discovery checkpoint (2026-11-15)

Round-one branch evidence: Rust `70e595a2`, build-tests `d14d5871` and
specification/policy baseline tooling `77b30a82`. These are pushed checkpoints,
not merged delivery; no PR is authorized before the operator returns.

The first scoped implementation adds independent durable discovery-initialization
state and atomic server-list initialization. Automatic server import accepts the
first validated nonempty fallback, preserves explicit empty/disabled operator
state, and does not overwrite a list changed while a fetch was in flight. The
existing Python harness uses selected-workstream fixtures and transactional
explicit server inputs, preserving deterministic public-bootstrap isolation.

Focused evidence recorded by the parent: metadata 104 unit plus 3 integration
checks; daemon 108 unit plus 15 integration checks with one ignored helper;
Python 80 passed with one POSIX-only skip. Two review rounds resulted in
operator-race and explicit-fixture repairs. Normal push checks passed with
output-root-relative receipts:

- `reports/local-check/emulebb-rust/20261115T185408Z-f63dbe33`
- `reports/local-check/emulebb-build-tests/20261115T185216Z-90fd5f42`

This does not qualify the full public foundation. Kad file persistence removal,
the coordinated settings/REST redesign, library/download/search changes and
combined-scale proof remain pending. The accepted #155-A bounded persistence
worker is still unimplemented and is a prerequisite for runtime Kad checkpoint
wiring; reuse that owner rather than introduce a competing actor. Bootstrap
state alone is not a claim that runtime Kad persistence is complete.

## Accepted Foundation Round One (2026-11-15)

The operator authorized implementation of the consolidated
[Public Foundation](../../design/PUBLIC-FOUNDATION.md). That specification
supersedes conflicting proposal-only common contracts and acceptance rules in
older review notes below. Existing delivered evidence remains historical proof,
not qualification of this new target. Coordinate with the current persistence
owner; use the existing Python harness. One persistent branch per involved
repo, granular commits and tested pushes; no PR, merge or publication until
the operator returns and reviews. Leaf inventory cleanup and actual validation
remain work, not claims of completion.

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

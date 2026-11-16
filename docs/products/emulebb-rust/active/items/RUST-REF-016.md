---
id: RUST-REF-016
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/155
title: Move blocking SQLite work behind bounded async persistence
status: OPEN
priority: Major
category: refactor
labels: [rust, tokio, sqlite, async, persistence, performance]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/155. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-016 - Move blocking SQLite work behind bounded async persistence

## Registered shared-owner runtime checkpoint (2026-11-16)

The [#233 registered runtime checkpoint](RUST-FEAT-062.md#registered-kad-runtime-checkpoint-2026-11-16)
records the exact staged Rust `d5c2cfbe` / tests `0531be83` / tooling `eac34a72` /
Builder `e93fca5` bundle, supported build receipt and passing REST CI report.
It covers main conformance/SSE, all six delegated friend fault/retry frontdoors,
and real Kad import SQLite fault/retry followed by graceful reopen and same-profile
restart with stable identity and contacts. All owned daemons ended gracefully.
The three friend databases passed `quick_check`; the Kad phase records distinct
reopen/restart assertions and does not record that integrity check.
This is scoped shared-owner runtime proof, not global all-SQL conversion,
measured RSS, sustained upload progress or full-foundation qualification.

## Typed Kad owner extension checkpoint (2026-11-15)

The [#233 schema 72 checkpoint](RUST-FEAT-062.md#schema-72-and-typed-owner-checkpoint-2026-11-15)
records `b08709a1` typed load/initialize byte leases and `ca5e6993` durable generated
Kad identity, with focused metadata/Core/Python proof. These extend the existing
owner rather than introduce a new lane. At this storage checkpoint production
DHT binding and the runtime lifecycle were still in progress. The registered
local peer proof below remains attributed to its exact older staged source
`b509524f`; no later
schema/runtime qualification or global all-SQL conversion is implied.

The [Kad local-suite checkpoint](RUST-FEAT-062.md#runtime-coupling-local-suite-checkpoint-2026-11-16)
records final green uncommitted-material Rust/Python/WebUI suites and the
resource, startup-handoff and daemon SQL-failure cleanup/drain repairs. Earlier
failed/interrupted rounds remain retained. Those suites were local working-material
evidence; the registered checkpoint above now supplies exact staged acceptance
for the new Kad fault/restart phase. Do not claim global async conversion,
measured RSS, sustained upload progress or full-scope delivery from these counts.

## Registered conformance and local peer checkpoint (2026-11-15)

The first registered campaign at Rust `45ca468b` **failed**. Its retained report
is `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261115T205632Z/report.json`.
The main conformance phase exercised 83 of 105 operations with 43 expected errors,
22 unsafe skips and no failed routes; the separate SSE check passed. The local
peer phase proved all 6 required friend-mutation frontdoors and retry behavior,
but two peers exited nonzero during teardown. The campaign correctly remained
failed instead of treating successful HTTP assertions as complete acceptance.

The defect was ordinary handled SQLite request failures being retained as a
sticky owner-drain failure. Rust `b509524f` separates completed request errors
from worker/uncertain-commit faults without weakening the harness. The focused
Core selection passed 510 checks and all selected integrations. The registered
regular runtime was rebuilt in 187 seconds with zero warnings; its build log is
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261115T210559Z-build-clients`.

The rerun **passed**, with exact frozen companions Rust `b509524f`, tests
`a96b5859`, tooling `26492515` and Builder `e93fca5`. Retained report:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261115T210858Z/report.json`.
It exercised 83 of 105 main operations, including 43 expected-error responses;
22 unsafe operations remained explicitly skipped, no route failed, and SSE
passed. The local loopback-only peer phase covered 6/6 active-upload, waiting-
queue and download-source add/remove-friend frontdoors: injected failures
returned HTTP 500 `PERSISTENCE_FAILED`, cache and reopened database stayed
unchanged, and subsequent add/remove retries succeeded. All three databases
reopened with integrity `ok`, fault triggers were removed and every owned
process exited zero. The original failed evidence remains retained.

Logs include bounded forced-download-task-abort warnings during teardown; they
are not claims of leaked processes. This proof does not establish upload-byte
progress under SQLite contention, a full platform matrix, combined 100k scale,
365-day endurance or complete Kad/settings delivery. No PR/merge/publication is
authorized before operator review.

## Scoped friend-owner checkpoint (2026-11-15)

Rust `ea0f9653` implements ordered friend mutations through the allocated owner,
including the direct and delegated REST friend frontdoors. Its scope is converted
friend writes and their commit/cache-publication boundary, not global FIFO or
conversion of every SQLite path. GET reads the cached friend view and reports
an unavailable state after an unresolved owner fault. Kad runtime commands and
canonical settings integration still need to reuse this owner.

The parent recorded 509 Core checks, 155 REST checks and 3 integration checks
passed. Earlier metadata 108 proof belongs to the separate schema 71 repository
checkpoint; it is not new friend-runtime evidence. Selected-artifact OpenAPI
validation passed 130 existing Python checks, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/current-openapi-ea0f9653-9f7040ed/junit.xml`.
The frozen pushed source set was Rust `ea0f9653`, tests `fcf6dbb3`, tooling
`9f7040ed` and Builder `e93fca5`.

The diagnostics runtime build completed in 225 seconds with zero warnings,
with its log under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261115T203327Z-build-clients`.
Compilation is not a runtime contention campaign. Actual upload progress under
SQLite contention, combined-scale proof and full-scope qualification remain
pending. No PR/merge/publication is authorized before operator review.

## Allocated foundation owner: 155-A (2026-11-15)

The parent has explicitly allocated the accepted 155-A owner and friend-CRUD
slice under [public-foundation round one](../../design/PUBLIC-FOUNDATION.md).
The contract was accepted before implementation; the scoped checkpoint above
records current implementation evidence without claiming global completion.
The allocation baseline was Rust `82181294`, fresh schema 71. The slice adds no schema change, new CLI option,
environment input or public tuning knob. Earlier schema 68 acceptance is a
historical review baseline, not a downgrade instruction. Keep WAL/FULL durability,
profile ownership, typed current-model validation and existing busy behavior.

### One owner and composition

Compose one shared profile/runtime persistence owner with one fixed blocking
SQLite worker and one tracked asynchronous coordinator. Cloneable handles share
that owner; they never create workers, queues or coordinators per request or
clone. Commands are a closed typed FIFO. Friend CRUD is the first canonical
integration; later Kad, settings and other converted paths reuse the same owner.
Do not create a rival actor, per-request spawn-blocking lane or unbounded task
fan-out. FIFO and responsiveness claims cover converted paths only; synchronous
unconverted paths still exist and must not be described as globally fixed.

Offline synchronous metadata constructors continue to work without a Tokio
runtime. Runtime composition explicitly starts and owns the coordinator/worker;
there is no hidden runtime requirement during schema/profile construction.
The ownership graph must contain no strong Core-to-Owner-to-Core cycle and no
Store-to-Owner-to-Store cycle. Finalization retains only the necessary independent
cache/state handles or typed completion data, not a strong Core back-reference.

### Admission and resource accounting

Use conservative internal limits of **64 admitted operations** and **8 MiB
(8,388,608 bytes) of admitted owned payload**. These are implementation limits,
not user settings. Eight MiB is chosen to accommodate a full bounded 12,000-
contact routing snapshot plus temporary conversion costs; tests must measure the
actual representation cost rather than assume source-wire size equals owned
memory. Changing this engineering budget requires measured review, not a second
public authority.

Admission is nonblocking: reserve both operation and byte quotas before cloning
or materializing owner-held request data. Account for owned backing storage,
variable-length fields, bounded replies and temporary conversion allocations.
Use checked sizing arithmetic and a conservative documented cost model; do not
admit a zero-cost command that later allocates an unbounded result. Converted
reads need bounded query/results or an explicit pre-allocation size decision.
Do not silently truncate data. The 8 MiB limit bounds retained product-payload
capacity, including the charged owner-held buffers/conversions; it is not a
measured RSS bound. Transport/TLS memory, rejected oversized transport frames,
SQLite internals, allocator bookkeeping and thread stacks are excluded. Keep
those costs explicit and measure them separately; do not report total process
memory as bounded to 8 MiB. Retain quota through the actual worker allocation
peak, not only through request handoff.

Retain the operation and byte permits through required SQL completion, outcome
handling and cache publication, including required finalizers. A queue slot is
not released merely when dequeued or committed. Request cancellation must not
turn a bounded queue into unbounded detached tasks or release retained payload
while a worker/finalizer still owns it. Saturation, closing and oversized work
are explicit typed outcomes; no invisible waiting queue or admission bypass.

### Ordering, cancellation and shutdown

The close/admit boundary is atomic: after close wins no new operation is
accepted; work accepted before close remains owned and drains. Capture normalized
friend intent without holding global CoreState across admission, SQL wait or
publication. Ordering spans durable commit and the matching cache publication;
a later command cannot observe or publish half of its predecessor's result.
Caller cancellation before admission changes nothing. After admission, required
work and finalizers survive caller abort and complete under the tracked owner.
A successful completion is reported after the required publication, not merely
after enqueue or SQL commit.

Release the SQLite connection mutex before any CoreState/cache finalizer. Never
hold that mutex while acquiring CoreState: remaining synchronous callers can
otherwise invert the lock order. Keep commit/publication ownership explicit;
SQL failures do not publish uncommitted cache state. Errors after a successful
commit must retain the fact of commit and cannot pretend the write rolled back.

Shutdown explicitly closes admission, drains accepted required operations and
finalizers, joins the fixed worker and tracked coordinator, then releases the
connection/profile lease. Drain failure is reported honestly. No owner lifetime
may rely on a dropped caller's future, a transient runtime handle or an Arc cycle.
The parent serializes the shared Core, schema and daemon-drain composition seams.

Expose Busy/Closing as retryable native HTTP 503 outcomes when the phase-four REST
mapping is implemented. This owner slice first establishes typed errors and
required completion semantics; it is not permission to change unrelated status
contracts or weaken accepted durability. Oversized work must fail explicitly
before copying and be distinguishable from transient saturation.

### Required acceptance before reuse

Use the existing Rust/Python test owners and supported orchestration. Prove:

- exact slot/byte reservation and checked sizing, refusal before clone, full
  contact-snapshot representation cost and temporary-conversion allowance;
- slow connection acquisition/commit with unrelated runtime progress, FIFO
  ordering through publication and no SQL/CoreState lock inversion;
- saturation and atomic close/admit interleavings;
- caller abort after admission or commit without abandoned finalizers, prematurely released
  permits, lost writes or unbounded tasks;
- failed writes and same-key friend mutations without cache/durable divergence;
- explicit close/drain/join, reopen and profile-lease release ordering;
- one owner across clones, no retention cycle, and offline constructors without
  an async runtime.

Record focused evidence and exact source revisions in this item. Two inspection
rounds and applicable integration gates remain required. Runtime Kad checkpoint
wiring must wait for this owner; no separate temporary worker is authorized.


## Summary

Remove synchronous SQLite waits and durable flushes from Tokio worker threads
and global async state locks. Introduce bounded persistence ownership that keeps
the network runtime responsive while preserving crash consistency and explicit
backpressure.

## Allocated Safety Slice: Peer-Credit Settlement

The parent allocated the bounded `peer-credit-settlement` workstream after
source review at Rust `23e685b87bb76db21489c9b1cc725dd0da4241c1`.
Failed single-peer settlement currently removes parked deltas before fallible
SQL without restoring them. Restore by saturating merge under the existing
flush gate, retain additions parked during SQL, and propagate the original
error. Reuse the batch-flush restoration rule.

Preserve current schema 69, WAL/FULL durability, storage ownership, secure-ident
anti-theft behavior and existing ordering. No persistence actor, queue, shutdown
or Kad snapshot change belongs to this repair. The earlier schema-68 reference
below records the 155-A review baseline, not a schema downgrade instruction.

Required regression proof covers a real SQLite abort with durable rows
unchanged and parked credit retained, additions merged without overwrite or
overflow, exactly-once retry and reopen, plus existing secure-ident wipe tests.
The failed-settlement parked-credit restore and exactly-once SQL retry were
delivered in PR [#335](https://github.com/emulebb/emulebb-rust/pull/335), merged
to Rust `main` at `0840e9005fd2ab28e9cbe262054dd692262e5698`. Its exact
pre-merge source passed all six stages in the full local owner check
(`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/local-check/emulebb-rust/20261115T075009Z-41880a82`),
including Windows, Linux and Android; all 30 hosted checks and four workflows
passed. The broader bounded persistence conversion remains incomplete; the newer
scoped friend-owner checkpoint above records the implemented 155-A slice.

Review confirmed a separate remaining secure-ident boundary: the flush gate
ends before the subsequent `pin_verified_secure_ident`, and additions do not
take that gate. Concurrent pre-bind deltas can therefore flush after the first
bind wipes unsecured credit. The settlement restore does not fix this ordering
gap. A separate coherent bind/add linearization repair needs deterministic
interleaving proof. The analogous absolute-seed path currently has only test
callers; this review establishes no production race for that path.

## Historical accepted 155-A review (2026-11-12)

The parent accepted [one bounded persistence owner plus friend CRUD](https://github.com/emulebb/emulebb-rust/issues/155#issuecomment-6830001541)
after source review at Rust `080a5dea70186da31dab958757b5b8c0fd883f82`.
The allocation above now authorizes implementation under the round-one mandate.
This older review remains evidence; contract acceptance is not implementation
or global completion.

- Compose one fixed worker and typed FIFO for migrated friend operations.
  Bound admitted slots and owned payload bytes through completion; report
  saturation/closing explicitly rather than spawning unbounded work. Cloning
  a handle does not create another owner.
- At this historical review the baseline was schema 68. The current allocation
  preserves actual schema 71, WAL/FULL durability, existing SQLite busy behavior,
  secrets and the OS-backed profile lease. Offline synchronous constructors
  remain usable without a Tokio runtime. No schema change is part of 155-A.
- Capture normalized friend input and release global CoreState before
  admission/wait. Ordering spans durable commit **and** cache publication;
  caller cancellation cannot release that order or strand committed DB/cache
  state. Required success follows publication, not enqueue alone.
- Release the SQLite connection mutex before any cache/CoreState finalizer.
  Legacy synchronous DB-under-CoreState callers still exist; the new lane must
  not introduce a lock-order deadlock with them. Migrated-only FIFO does not
  imply global FIFO or complete removal of blocking persistence.
- Shutdown closes admission, drains accepted required writes and finalizers,
  joins the worker before connection/profile-lease release and reports failed
  drains honestly.
- Use meaningful saturation, slow-commit/connection-contention, failed-write,
  same-key concurrency, cancellation and drain/reopen regressions. Measure
  queue, connection wait and execute/commit behavior; source inspection alone
  establishes no responsiveness or performance result.

Reserve the metadata executor/exports and composition seam, friend APIs and
their ordering boundary, daemon drain seam and existing friends REST error
mapping/tests. The parent serializes shared Core/schema/shutdown edits.
[#233](RUST-FEAT-062.md) must reuse this owner for its later typed,
generation-safe Kad snapshots and met-file removal. No production or schema
implementation is claimed by this accepted slice.

## Current State

The metadata layer shares a synchronous `rusqlite::Connection` behind
`std::sync::Mutex`, uses `synchronous=FULL`, and allows a five-second busy
timeout. Core API methods and search paths call that storage directly from async
contexts, sometimes while holding the global core state or search-index lock.
Upload request handling also performs synchronous counter and metadata writes
before continuing peer work. A busy database or durable flush can therefore
block a Tokio worker and serialize unrelated network, REST, or scheduler work.

`RUST-REF-008` already owns large-library ingestion batching. This item owns the
broader runtime boundary for interactive reads, compound writes, counters, and
hot peer paths.

## Why This Matters

Blocking a cooperative executor on database mutex acquisition, query work, or
filesystem synchronization converts storage latency into protocol latency.
Adding more `spawn_blocking` calls ad hoc would hide ownership, permit
unbounded work, and make ordering harder to reason about.

## Representative Sites

- `crates/emulebb-metadata/src/store.rs` connection ownership and pragmas.
- `crates/emulebb-core/src/category_runtime.rs`, `server_api.rs`,
  `friend_api.rs`, `app_api.rs`, and `search_api.rs` async callers.
- `crates/emulebb-metadata/src/transfer_store.rs` transfer metadata and counter
  updates.
- `crates/emulebb-ed2k/src/ed2k_transfer/upload.rs` upload accounting called
  from the peer payload path.

## Intended Shape

- Own SQLite writes in a dedicated bounded persistence executor or actor with
  typed commands, explicit queue capacity, and measured latency.
- Use set-oriented transactions for compound state changes and bounded
  batching/coalescing for lossy counters where the durability contract permits.
- Run blocking reads through a bounded read lane or dedicated read connections;
  never hold a Tokio mutex guard while waiting for SQLite.
- Define per-command completion semantics so callers know whether they require
  durable commit, ordered enqueue, a snapshot read, or best-effort accounting.
- Surface overload and database unavailability as typed errors or controlled
  backpressure rather than unbounded task creation.

## Accepted Sharing-Path Follow-up (2026-11-06)

This owns approved follow-up 3 from the async-I/O review. It remains in the
post-beta backlog; the update does not promote it into a blocker for the
validated stock-import workflow. Main `e3372aba` and the import/root branch at
`43855fba` were reviewed before recording the following sites.

`shared_file_api.rs` still calls `index.upsert_file` synchronously after
offloaded ingest and calls `index.replace_shared_directory_roots` while holding
the async index guard. Ignore-rule list/add/remove/toggle paths also call the
synchronous metadata layer directly. The async guard does not make the SQLite
query, connection-mutex wait, busy wait, or durable commit asynchronous.

Route these live operations through the same bounded persistence owner as the
other runtime callers. Capture owned arguments, release global state/index
guards before queueing or awaiting storage, and publish the result according to
the command's required durable-commit semantics. Serialize logical root edits
or use configuration revisions so removing a guard does not introduce lost
updates. Do not replace a bounded owner with independent unbounded
`spawn_blocking` calls at each handler.

Keep SQLite synchronous inside that worker. The current `Arc<Mutex<Connection>>`
serializes users of each shared connection even with WAL: a five-second SQLite
busy timeout does not bound time waiting for the Rust connection mutex. Expose
both queue/connection wait and execution/commit latency. A read-lane or
connection-pool expansion needs measured justification and explicit snapshot
consistency; it is not a prerequisite to isolating blocking work.

Whole-file ingest, its local-content/AICH persistence, media extraction, root
membership updates, and paged catalog reads already use blocking boundaries in
important paths. Preserve and consolidate that good behavior. Exclusive offline
imports may keep bounded synchronous transactions because they serve no live
network/API workload.

RUST-REF-018 owns filesystem probes and root state lock scope. RUST-REF-008 owns
the compiled ignore-policy cache and eliminating per-file query/compile work;
its rule edits/invalidation use this persistence boundary. RUST-REF-019 owns
CPU-only bursts. These items must not introduce competing SQLite actors.

Additional representative sites:

- `crates/emulebb-core/src/shared_file_api.rs`: final index upsert, root
  replacement, ignore-rule operations, and current cached progress accessor.
- `crates/emulebb-index/src/lib.rs`: synchronous metadata adapter methods.
- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs`: already-offloaded durable
  local-content/AICH writes to preserve.

Additional acceptance criteria:

- [ ] Live root edits, post-ingest index updates, and ignore-rule operations use
      the bounded storage boundary without global async guards across waits.
- [ ] Injected SQLite mutex contention, busy waits, and slow FULL commits leave
      unrelated REST requests, peer timers, and cached progress responsive.
- [ ] Queue saturation and shutdown preserve required commit guarantees and do
      not silently lose root edits or mark uncommitted content durable.

## Scope Constraints

- Preserve `synchronous=FULL` where the durability contract requires it; improve
  scheduling and transaction shape rather than weakening correctness.
- Keep password/secret handling and profile isolation unchanged; encryption
  feature work is not part of this scheduling change.
- Preserve stock eMule wire timing rules and packet behavior.
- Keep large-library batching performance work in `RUST-REF-008` and category
  deletion atomicity in `RUST-BUG-131`; share one persistence architecture.

## Acceptance Criteria

- [ ] No synchronous SQLite operation runs on a Tokio worker thread while
      holding global core, search, or peer-session async state.
- [ ] Persistence queues and blocking read concurrency are explicitly bounded
      and expose queue depth, wait time, execution time, and failure counters.
- [ ] Compound operations use one transaction and publish in-memory state only
      after the required commit succeeds.
- [ ] Upload accounting cannot delay payload service on a database busy timeout;
      its durability and coalescing policy is explicit and tested.
- [ ] Shutdown drains or rejects persistence commands according to documented
      command guarantees without silently losing required writes.
- [ ] Database contention tests prove REST, search, and peer timers remain
      responsive under the configured busy timeout and durable flush latency.

## Validation

- Tokio paused-time and multi-thread contention tests with injected slow SQLite
  operations and queue saturation.
- Crash/restart tests for commands that promise durable completion.
- Upload/search/API latency regressions under forced database contention.
- Current-schema rejection, metadata durability, REST, eD2K, Kad, and
  large-library validation lanes. Product code gains no migrations or reset path.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_persistence.md` section 2.4 (existing): Do not add speculative pools or independent actors. Existing REF016 owns queue/wait/commit semantics and read-lane justification.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A3-kad-cache-load (existing): Kad cache hydration calls SQLite synchronously during core construction. Existing async SQLite persistence work is the nearest owner; the review did not measure startup blocking or establish a new release defect.

### Scoped Follow-up Acceptance

- [ ] Preserve FULL durability and measure connection/queue latency; keep one storage owner.
- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.
- [ ] Measure representative cache startup and executor responsiveness.
- [ ] Offload substantial work through the bounded persistence owner if required.
- [ ] Preserve startup consistency and the existing cache model.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-REF-016.md

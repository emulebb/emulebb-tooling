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

## Summary

Remove synchronous SQLite waits and durable flushes from Tokio worker threads
and global async state locks. Introduce bounded persistence ownership that keeps
the network runtime responsive while preserving crash consistency and explicit
backpressure.

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

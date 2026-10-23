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

## Scope Constraints

- Preserve `synchronous=FULL` where the durability contract requires it; improve
  scheduling and transaction shape rather than weakening correctness.
- Keep password/secret handling, profile isolation, and SQLCipher behavior
  unchanged unless separately approved.
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
- Existing metadata migrations, SQLCipher, REST, eD2K, Kad, and large-library
  validation lanes.

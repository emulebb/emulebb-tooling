---
id: RUST-BUG-130
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/152
title: Release search drain ownership when persistence fails
status: DONE
priority: Major
category: bug
labels: [rust, search, async, persistence, reliability, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/152. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-130 - Release search drain ownership when persistence fails

## Summary

Keep the search queue runnable when creation of a queued search cannot be
persisted. Queue membership, drain ownership, and durable search visibility
must either become active together or roll back together.

## Current State

`crates/emulebb-core/src/search_api.rs` enqueues a search, claims the queue's
single drain task, persists the search session, and only then spawns the drain.
If persistence fails after the claim, the queued entry remains and the drain
claim is not released. Later searches can enqueue but cannot claim a new drain,
leaving the queue stalled until process restart.

## Why This Matters

A transient SQLite failure must fail one request, not disable all later network
searches. The current ordering converts a recoverable persistence error into a
process-lifetime availability failure without changing any stock eMule wire
behavior.

## Representative Sites

- `crates/emulebb-core/src/search_api.rs` search creation and drain spawning.
- `crates/emulebb-core/src/search_queue.rs` queue insertion, drain claiming,
  and claim release.
- `crates/emulebb-metadata` search-session persistence.

## Intended Shape

- Give queue insertion and drain ownership an explicit commit/rollback boundary.
- Prefer persisting the initial search session before making it runnable, or use
  a guard whose drop path removes the entry and releases the drain claim.
- Make the queue owner responsible for guaranteeing that every non-empty queue
  has one live or immediately schedulable drain.
- Keep remote search dispatch, rate limits, status vocabulary, and eD2K/Kad
  packet behavior unchanged.

## Scope Constraints

- Do not report a search as accepted unless its durable record exists.
- Do not discard already durable searches because a later request fails.
- Do not recover by starting multiple concurrent drain tasks.
- Coordinate the blocking persistence boundary with `RUST-REF-016` without
  making that larger refactor a prerequisite for the focused correctness fix.

## Acceptance Criteria

- [x] Injected initial-search persistence failure leaves no orphan queue entry
      and no claimed drain without a live task.
- [x] A search submitted after the injected failure can be persisted, drained,
      dispatched, and completed without restarting the daemon.
- [x] Queue cancellation and shutdown release ownership on every error path.
- [x] Concurrent submissions preserve exactly one active drain and FIFO policy.
- [x] Search status persistence and REST responses never expose a runnable
      search that lacks its durable session row.

## Validation

- Focused fault-injection tests around enqueue, claim, persistence, spawn, and
  cancellation boundaries.
- Concurrency test that submits searches during and after a persistence failure.
- Existing eD2K/Kad search scheduler and REST conformance tests.

## Resolution

- Separated search prepare, durable persistence, and queue commit so failed persistence cannot orphan drain ownership.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-core search_queue`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`

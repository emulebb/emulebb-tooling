---
id: RUST-BUG-132
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/154
title: Own daemon background tasks through graceful shutdown
status: DONE
priority: Major
category: bug
labels: [rust, tokio, shutdown, lifecycle, concurrency, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/154. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-132 - Own daemon background tasks through graceful shutdown

## Summary

Give every daemon background task explicit runtime ownership, cancellation, and
bounded joining so graceful shutdown cannot race detached work that still
mutates state, accesses persistence, or reinstalls services. Download workers
must quiesce cooperatively and persist their final acknowledged progress before
bounded fallback aborts a non-cooperative task.

## Current State

`crates/emulebb-daemon/src/lib.rs` starts catalog, delivery, VPN, disk, resume,
auto-connect, and diagnostics loops with detached `tokio::spawn` handles.
Graceful teardown begins core shutdown and stops selected services but does not
own or join those loops. The initial shared-directory monitor startup can finish
after teardown has stopped the monitor and install a new monitor while shutdown
is already in progress.

## Why This Matters

Detached process-lifetime tasks make shutdown timing nondeterministic and can
touch network or database state after finalization has begun. This is especially
risky during profile restart, package smoke, and failure recovery, even when an
ordinary fast shutdown appears to pass.

## Representative Sites

- `crates/emulebb-daemon/src/lib.rs` task spawning and `graceful_teardown`.
- `crates/emulebb-core/src/shared_dir_monitor.rs`
  `start_shared_directory_monitor` and monitor installation.
- Long-running delivery, connectivity, disk, diagnostics, and resume loops.

## Intended Shape

- Introduce one daemon task supervisor using a cancellation token and a
  `TaskTracker`, `JoinSet`, or equivalent structured-concurrency owner.
- Pass child cancellation explicitly to every long-running loop and startup
  task; do not rely only on a global flag checked at arbitrary intervals.
- Shutdown in phases: stop accepting new work, cancel producers, join tasks with
  bounded deadlines, then finalize network and durable state.
- Treat timeout or task panic as a surfaced shutdown failure with diagnostics,
  not as permission to silently abandon stateful work.
- Stop download admission, request cooperative worker drain, capture final
  transfer progress, and persist the dirty checkpoint before abort fallback.
- Bound the drain and checkpoint phases independently so one stalled worker or
  persistence failure cannot hang process shutdown.

## Scope Constraints

- Preserve stock eMule disconnect and publication semantics.
- Do not block forever on a task that ignores cancellation; joins need explicit
  deadlines and task names in diagnostics.
- A monitor or network runtime must not be installed after its parent runtime
  has entered shutdown.
- Avoid a second parallel shutdown mechanism inside core; daemon ownership and
  core shutdown phases must compose.

## Acceptance Criteria

- [x] Every daemon-spawned background task is registered with one lifecycle
      owner and observes explicit cancellation.
- [x] Graceful teardown joins all registered tasks before final network and
      persistence resources are released.
- [x] Shared-directory monitor startup cannot install or replace a monitor after
      shutdown begins.
- [x] Task panic and join timeout identify the task and make shutdown failure
      observable.
- [x] Repeated startup/shutdown and profile restart leave no orphan tasks,
      listeners, monitor handles, or post-shutdown database writes.
- [x] A clean shutdown persists every acknowledged transfer byte before worker
      ownership is released, so restart does not unnecessarily redownload it.
- [x] A non-cooperative download is aborted only after the bounded cooperative
      drain expires, with the task and checkpoint outcome reported.

## Validation

- Deterministic paused-time lifecycle tests for cancellation ordering.
- Delayed monitor-start regression that begins shutdown before installation.
- Task panic and timeout tests with named diagnostics.
- In-flight download tests for final progress persistence, checkpoint failure,
  bounded forced abort, and restart recovery.
- Existing package lifecycle smoke on every supported operating system.

## Resolution

- Added cooperative daemon quiescence, bounded task joins, and a final dirty-progress checkpoint before forced abort.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-core`; `cargo test -p emulebb-ed2k`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`

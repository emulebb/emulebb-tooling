---
id: RUST-REF-010
workflow: local
title: Bound watcher reconciliation I/O for large shared libraries
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, watcher, io, concurrency, portability]
milestone: post-beta-polish
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

# RUST-REF-010 - Bound watcher reconciliation I/O for large shared libraries

## Summary

Prevent ordinary watcher bursts from repeatedly walking a 100k-file tree and
route live ingestion through the same storage-domain scheduler as manual/startup
reloads. Keep overflow recovery authoritative without turning every multi-file
copy into an unbounded sequence of full reconciliations.

## Current State

- Watcher events settle for two seconds, queued actions are coalesced by path,
  and paired renames relocate metadata without rehashing unchanged content.
- On Windows, any settled batch with two catalog actions appends a full
  reconciliation because the native watcher buffer can overflow silently.
- The consumer waits for reconciliation to finish. Events accumulated during
  that scan can form another qualifying batch and trigger another full walk.
- Direct watcher shares are consumed serially through one global queue. Linux
  and macOS bursts spanning independent devices do not use the per-domain hash
  workers.
- An unwatchable Linux root degrades to manual scan with a log message, but the
  degraded state is not a first-class API/UI status and no bounded periodic
  reconciliation repairs missed changes automatically.
- The macOS end-to-end delete leg is ignored because FSEvents delivery is not
  deterministic within the test timeout.

## Representative Sites

- `crates/emulebb-core/src/shared_dir_monitor.rs`
  `actions_for_events`, `coalesce_actions`, `run_consumer`, and
  `auto_share_monitored_path`
- `crates/emulebb-core/tests/shared_dir_monitor_e2e.rs`
- `crates/emulebb-core/src/shared_directories.rs` `hash_reload_targets`

## Intended Shape

- Track one dirty/reconcile generation across a burst and schedule at most one
  trailing authoritative reconciliation after quiescence.
- Prefer explicit overflow/`need_rescan` evidence. Where Windows requires a
  defensive heuristic, make it time/burst bounded and observable.
- Route direct watcher hashing into the storage-domain queues from
  `RUST-REF-009`, while preserving final-intent coalescing per path.
- Surface watched, degraded, overflowed, and reconciling states per root through
  diagnostics and REST.
- Add a bounded periodic reconciliation for degraded roots so missed changes are
  repaired without continuous full-tree polling.
- Define and prove macOS delete/rename recovery even when FSEvents delivery is
  delayed or coalesced.

## Scope Constraints

- Never trust watcher delivery as the sole authority after overflow or an
  unwatchable-root condition.
- Preserve metadata-only rename behavior and do not hash files that are still
  being written.
- Keep one active payload reader per mechanical storage domain.
- Do not solve watcher loss by continuously polling the complete tree.

## Acceptance Criteria

- [ ] A synthetic multi-file burst causes a bounded number of full-tree scans,
      with an explicit maximum proved in tests.
- [ ] Events arriving during reconciliation collapse into at most one required
      trailing reconciliation.
- [ ] Live files on independent storage domains can ingest concurrently without
      same-domain overlap.
- [ ] Rename-only bursts preserve hashes and perform no payload reads.
- [ ] Degraded roots are visible through diagnostics/REST and eventually repair
      missed changes through a bounded fallback.
- [ ] Windows, Linux, and macOS watcher create/modify/rename/delete behavior has
      platform-specific integration evidence.

## Validation

- Deterministic action/coalescing state-machine tests.
- Instrumented 1-, 2-, 100-, and 1,000-file watcher bursts recording scan count,
  payload bytes, metadata operations, and convergence time.
- Windows overflow/recovery, Linux inotify-limit degradation, and macOS delayed
  delete/rename tests.
- Cross-device watcher tests through the storage-domain seam.

---
id: RUST-BUG-129
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/151
title: Queue targeted re-hash after upload-time source invalidation
status: DONE
priority: Major
category: bug
labels: [rust, sharing, hashing, upload, integrity, beta]
product: emulebb-rust
phase: Phase 0
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: imported-profile live soak upload-authority withdrawal analysis
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/151. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-129 - Queue targeted re-hash after upload-time source invalidation

## Summary

When an upload-time authority check detects that a verified shared payload has
changed or become unavailable, keep the current fail-closed withdrawal and also
request a bounded targeted reconciliation for that source path. A stable,
readable replacement should be re-hashed and reintroduced without requiring a
restart, a full shared-directory reload, or a second filesystem notification.

## Current State

- The ED2K piece store verifies the persisted native source fingerprint before
  serving a shared payload and withdraws the old hash when the source changed or
  became unavailable.
- Withdrawal clears the manifest fingerprint and removes the stale offer from
  the verified catalog, which correctly prevents unverified bytes from being
  uploaded.
- A later full shared-directory reload notices the missing fingerprint and
  plans a re-hash. The filesystem monitor also re-ingests a file when it
  observes and settles the relevant change event.
- The upload-time invalidation path does not itself request reconciliation. If
  the watcher event was missed, coalesced, or occurred before monitoring became
  authoritative, the file can remain withdrawn until another reload or
  restart.

## Why This Matters

Profile import can preserve trusted ED2K hashes and avoid re-hashing large
libraries, but a source file may legitimately change after import or while the
client is running. The client must preserve its upload-integrity boundary while
recovering automatically and cheaply when the changed file becomes stable.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` owns upload-time source
  verification and `withdraw_untrusted_verified_payload`.
- `crates/emulebb-core/src/shared_directories.rs` owns reload planning,
  missing-fingerprint detection, and `reload_hash_target`.
- `crates/emulebb-core/src/shared_dir_monitor.rs` owns settled path-level
  reconciliation through `auto_share_monitored_path`.

## Intended Shape

- Emit a typed local invalidation signal after the piece store has withdrawn a
  changed or unavailable verified payload.
- Let core translate that signal into one normalized source-path reconciliation
  request rather than coupling the transfer crate to directory scanning.
- Coalesce duplicate requests and run at most one targeted reconciliation per
  source path at a time, with debounce and retry bounds suitable for active
  writers.
- Reuse the existing verified, no-follow share-ingest authority so a stable file
  receives its new ED2K hash and fingerprint before it re-enters the catalog.
- Replace the stale source mapping and let normal eD2K/Kad publication observe
  the new catalog state.

## Scope Constraints

- Keep immediate withdrawal of the stale hash; recovery must never serve bytes
  under an obsolete ED2K hash.
- Do not trigger a full-library scan for a single upload-time mismatch.
- Do not let remote request volume create arbitrary disk work. Only a confirmed
  local source-authority mismatch may enqueue reconciliation, and repeated peer
  requests must collapse into the same bounded work item.
- Missing, excluded, or persistently unreadable files remain unshared without a
  busy retry loop.
- Preserve platform-native path identity and the existing large-library I/O
  constraints.

## Acceptance Criteria

- [x] Upload-time source mismatch withdraws the stale hash before any payload
      bytes are served.
- [x] The mismatch queues one targeted reconciliation for the normalized source
      path without requiring a full reload or watcher event.
- [x] Duplicate invalidations are coalesced and cannot produce concurrent
      re-hashes or peer-amplified unbounded disk work.
- [x] A stable readable replacement is re-hashed, replaces the stale source
      mapping, and becomes eligible for normal eD2K and Kad publication.
- [x] A missing, excluded, or unreadable replacement remains withdrawn and does
      not enter a hot retry loop.
- [x] Restart and explicit shared-directory reload remain correct fallbacks and
      do not create duplicate catalog entries.
- [x] Focused regressions and retained live evidence cover changed-after-import,
      missed-watcher, duplicate-request, and unavailable-file cases.

## Validation

- Focused piece-store tests for fail-closed invalidation signaling.
- Core tests for targeted scheduling, coalescing, retry bounds, and catalog
  replacement.
- Shared-directory monitor regressions proving no duplicate ingest or stale
  mapping survives reconciliation.
- A retained imported-profile live run showing withdrawal followed by bounded
  re-hash and republication without restart or full reload.

## Resolution

- Added bounded, coalesced targeted re-hashing after upload-time source invalidation without falling back to a full scan.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-core shared_dir_monitor`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`

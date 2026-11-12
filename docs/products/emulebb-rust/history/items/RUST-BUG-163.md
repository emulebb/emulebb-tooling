---
id: RUST-BUG-163
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/247
title: Enforce exclusive process ownership of writable profiles
status: DONE
priority: Major
category: bug
labels: [rust, persistence, profiles, robustness]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved stock profile import branch review, finding 7
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/247. This local document owns the durable engineering specification and evidence.

# RUST-BUG-163 - Enforce exclusive process ownership of writable profiles

## Closure And Evidence

[PR #317](https://github.com/emulebb/emulebb-rust/pull/317) merged as
`d2d591d212267f055ea9e35775045bc4900e6462` and closed
[#247](https://github.com/emulebb/emulebb-rust/issues/247). The OS-backed lease
is acquired before mutable loading, retained by cloned metadata handles and
bound to physical profile I/O. The PR records deterministic ownership, alias,
fresh-profile race, process-death and denied-write preservation regressions.

The published [Nightly 43242135692](https://github.com/emulebb/emulebb-rust/actions/runs/43242135692)
at Rust `080a5dea70186da31dab958757b5b8c0fd883f82` independently passed the
Windows/Linux packaged ownership checks: all three offline contenders were
rejected while the daemon owned the profile, bootstrap/settings/roots stayed
unchanged, and reconciliation succeeded after shutdown. Same-binary/profile
partial restart and deterministic transfer also passed. This evidence does not
claim a public-network soak or every filesystem scenario below.

The remaining sections retain the original engineering contract and findings;
their original unchecked criteria are not an active implementation queue.

## Summary

Give the daemon and offline profile commands one shared process ownership
contract. Refuse a second writer before it loads mutable profile state. This
is an approved post-beta follow-up; operators must continue stopping the
destination client before importing, reconciling, or hashing offline.

## Current Findings

`crates/emulebb-daemon/src/lib.rs` loads profiles through `DaemonProfile::load`
and `load_for_import`. Both reach `load_from_dir`, which can bootstrap settings,
open SQLite, seed defaults, and read configuration without acquiring an
exclusive profile lease. The CLI dispatches archive import, directory-list
import, and reconciliation through that loader.

SQLite transaction locks and busy timeouts coordinate individual database
writes. They do not coordinate the daemon's in-memory roots, reload plans,
watchers, or settings with a second process changing those same persisted
values. A documented stopped-profile requirement currently provides the
operational safeguard. PID files alone would not enforce ownership.

## Intended Shape

Acquire one operating-system-backed exclusive lease for a writable profile
before bootstrap and mutable metadata initialization. Centralize it at the
profile/session boundary so every daemon and offline command uses the same
owner. Internal metadata connections and cloned handles share that process's
lease rather than attempting to lock one another.

Keep the lease alive until shutdown and all owned background persistence has
finished. Rely on OS handle lifetime to release it after normal exit or process
death. Use a maintained cross-platform locking facility or platform primitive;
do not implement stale-PID heuristics or unlink-and-recreate lock ownership.

Resolve profile aliases consistently, including Windows casing/junctions and
Unix symlinks, so alternate spellings cannot admit two writers. Handle fresh
profiles through the smallest necessary directory/lock initialization before
settings or database mutation. Document supported locking behavior on network
filesystems and fail explicitly if exclusivity cannot be established.

An ownership failure identifies the busy profile and explains that its client
must be stopped. Pure help/version operations require no profile lease. Keep
the on-disk lease file harmless after crashes; its existence is not ownership.

## Acceptance Criteria

- [ ] The daemon, archive import, directory-list import, and reconciliation
      obtain the same exclusive ownership contract before mutable loading.
- [ ] Two processes cannot operate on the same writable profile concurrently,
      including through supported path aliases.
- [ ] A rejected second process does not alter settings, roots, hashes,
      recovery sets, or the database schema marker.
- [ ] Process termination automatically releases ownership; relaunch needs no
      manual lock-file deletion and preserves committed MD4/AICH work.
- [ ] Internal connections, cached handles, and background jobs do not create
      self-deadlocks or release the lease before shutdown finishes.
- [ ] Unsupported locking and permission failures are actionable and fail
      closed; unrelated profiles can operate concurrently.
- [ ] No schema migration, legacy loader, automatic reset, or import staging
      table is introduced.

## Validation

Extend the existing persisted Python harness with two-process tests using
synthetic profiles. Cover daemon-versus-offline and offline-versus-offline
contention, fresh-profile creation races, clean shutdown, forced termination,
and immediate restart. Snapshot database/settings evidence before a denied
second operation and verify exact preservation afterward.

Run Windows native and Linux/container lanes. Exercise Windows junction and
case aliases, Unix symlinks, and supported shared mount views. Include a native
macOS check in RUST-CI-008. Test permission failures, lock capability failure,
and two distinct profiles; do not use the production library or public P2P
networking for ownership tests.

## Dependencies and Scope

Coordinate the owner lifetime with RUST-REF-018 root operation serialization
and RUST-REF-016 persistence shutdown. This process-level lease complements
SQLite transactions and within-process scheduling; it does not replace them.
Rust database upgradeability and stock-profile locking remain separate work.

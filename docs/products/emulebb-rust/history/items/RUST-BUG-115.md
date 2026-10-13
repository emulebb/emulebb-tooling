---
id: RUST-BUG-115
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/82
title: Ban cross-reconnect userhash changes via a tracked-client identity store
status: DONE
priority: Minor
category: bug
labels: [rust, ed2k, ban, identity, anti-abuse, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/82. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-115 - Ban cross-reconnect userhash changes via a tracked-client identity store

## Summary

Rust bans a peer only when it changes its user hash on an already-bound session.
It does not implement the MFC cross-reconnect check that bans a peer whose user
hash differs from the hash previously tracked for the same (IP, TCP port). A
peer that disconnects and reconnects fresh with a different hash on the same
endpoint is therefore not caught.

## Current State

- `crates/emulebb-ed2k/src/tracked_client_identity.rs` owns a bounded in-memory
  identity store keyed by source IPv4 and advertised ED2K TCP port, with the
  master's two-hour retention window.
- `Ed2kTransferRuntime` shares the store across listener sessions and prunes it
  from the existing 20-minute client-maintenance loop.
- `apply_peer_hello_profile` preserves the live-session hash-change guard and
  also bans a fresh reconnect that changes the tracked endpoint's user hash,
  emitting `identity_userhash_changed_tracked`.
- First-seen endpoints and reconnects with an unchanged hash remain accepted;
  mismatches do not replace the retained identity.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `BaseClient.cpp:662-674`: on first HELLO, `ComparePriorUserhash(ip, port,
  hash)` against the tracked-clients list bans on mismatch
  (`identity_userhash_changed_tracked`); a live credit-slot change to a
  different hash also bans (`identity_userhash_changed`).
- `ClientList.cpp:470` `ComparePriorUserhash` walks the tracked-clients list
  for the matching (IP, port) and compares the stored hash.
- `ClientList.cpp:612` prunes tracked entries after `KEEPTRACK_TIME`.

## Why This Matters

The cross-reconnect check is the layer that stops a peer from rotating its
user hash between connections to farm upload credit or evade hash-scoped bans.
The intra-session guard alone leaves that hole open.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs` - `bound_user_hash`,
  `apply_peer_hello_profile`
- `crates/emulebb-ed2k/src/ed2k_transfer/diag_bad_peer.rs` -
  `identity_userhash_changed`
- `crates/emulebb-ed2k/src/ban_store.rs` - shared ban store (no prior-hash
  tracking)
- `workspaces/workspace/app/emulebb-main/srchybrid/BaseClient.cpp:662-674`
- `workspaces/workspace/app/emulebb-main/srchybrid/ClientList.cpp:470`

## Intended Shape

- Add a bounded tracked-client identity map keyed by (IPv4, TCP port) storing
  the last seen user hash with a `KEEPTRACK_TIME`-equivalent TTL (2 h).
- On the first HELLO binding for a connection, compare the advertised hash
  against the tracked value and ban (hash + IP scope) on mismatch, emitting a
  `identity_userhash_changed_tracked` diagnostic for soak-diff parity.
- Update the tracked entry on every accepted HELLO and prune expired entries on
  the same cadence used by RUST-BUG-116's ban-store pruning.

## Scope Constraints

- Keep the existing intra-session `bound_user_hash` guard unchanged.
- Do not ban a first-ever-seen endpoint with no tracked entry.
- Keep the store in-memory and expiry-driven, like `BanStore`.

## Acceptance Criteria

- [x] A reconnect with a different hash on the same (IP, port) is banned.
- [x] A reconnect with the same hash is not banned.
- [x] Tracked entries expire and are pruned after the TTL.
- [x] A listener test covers changed, unchanged, and never-seen endpoints.

## Validation

- `python tools/rust_quality_gate.py fmt`
- `python tools/rust_quality_gate.py policy` (108 policy tests passed)
- `python tools/rust_quality_gate.py diagnostics`
- `python tools/rust_quality_gate.py clippy`
- Workspace-orchestrated `emulebb-ed2k` tests (1,048 passed) and
  `emulebb-core` unit/integration tests (400 unit tests plus all integration
  suites) passed in Debug configuration.
- PR #107 required CI passed on Windows, macOS, and Ubuntu after rerunning one
  unrelated Ubuntu watcher-timing failure; required CodeQL passed for Rust,
  Python, JavaScript/TypeScript, and Actions.

## Notes

Complements RUST-BUG-116 (shared pruning cadence). The new diagnostic mirrors
the master's `identity_userhash_changed_tracked` event name for diffing.

- Completed on 2026-10-14 by emulebb-rust PR #107 in preserved commits
  `74f08278`, `2c70b8a6`, and `36c0da00`.
- GitHub issue #82 is closed and the eMuleBB Roadmap item is Done.

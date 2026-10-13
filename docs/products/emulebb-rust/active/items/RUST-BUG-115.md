---
id: RUST-BUG-115
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/82
title: Ban cross-reconnect userhash changes via a tracked-client identity store
status: OPEN
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

- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs:1557-1574` compares the
  HELLO hash against the per-session `bound_user_hash` and bans on a live
  session change.
- `crates/emulebb-ed2k/src/ed2k_transfer/diag_bad_peer.rs:78-85` emits
  `identity_userhash_changed` (hash + IP scope, action `ban`).
- There is no tracked-client identity store, so a fresh reconnect with a
  changed hash is invisible to the listener.

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

- [ ] A reconnect with a different hash on the same (IP, port) is banned.
- [ ] A reconnect with the same hash is not banned.
- [ ] Tracked entries expire and are pruned after the TTL.
- [ ] A listener test covers changed, unchanged, and never-seen endpoints.

## Validation

- Listener-session tests for the three identity cases plus a store unit test
  for expiry/pruning. Existing `identity_userhash_changed` coverage stays
  green.

## Notes

Complements RUST-BUG-116 (shared pruning cadence). The new diagnostic mirrors
the master's `identity_userhash_changed_tracked` event name for diffing.

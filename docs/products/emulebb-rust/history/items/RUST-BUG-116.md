---
id: RUST-BUG-116
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/83
title: Wire periodic expiry pruning for the client BanStore
status: DONE
priority: Minor
category: bug
labels: [rust, ed2k, ban, memory, hygiene]
milestone: post-beta-polish
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/83. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-116 - Wire periodic expiry pruning for the client BanStore

## Summary

The periodic production caller now physically removes expired entries from both
internal ban maps. Retained-entry diagnostics and runtime tests distinguish
actual memory reclamation from expiry-aware lookup behavior.

## Current State

- `crates/emulebb-core/src/network_api.rs` wires a periodic prune loop into the
  production runtime with an injected clock seam for deterministic evidence.
- `BanStore::retained_entry_counts` exposes a diagnostic snapshot of physically
  retained IP and user-hash entries.
- Unit and runtime tests prove that each prune removes expired entries from both
  indexes while preserving fresh entries and honoring shutdown.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `ClientList.cpp:568-595` `CClientList::Process()` prunes
  `m_bannedList` / `m_bannedHashList` (and `m_tcpErrorFloodMap`) on the
  `BAN_CLEANUP_TIME` cadence.

## Why This Matters

For a client that stays up for days and bans abusive peers periodically, the
two maps accumulate one entry per ban indefinitely. Lookup still works, but the
memory footprint is a leak proportional to the number of distinct banned
IPs/hashes, with no mechanism to reclaim it.

## Representative Sites

- `crates/emulebb-ed2k/src/ban_store.rs` - `prune_expired`, `ban`, `ban_at`
- `workspaces/workspace/app/emulebb-main/srchybrid/ClientList.cpp` -
  `CClientList::Process`

## Intended Shape

- Keep the existing periodic runtime invocation matching the master's cleanup
  purpose.
- Expose a small retained-entry count snapshot for operational observability and
  deterministic integration assertions.
- Seed expired IP and hash entries into the real shared store, run the periodic
  loop, and prove both retained counts reach zero while fresh entries remain.
- If RUST-BUG-115 lands a tracked-identity store and RUST-FEAT-043 lands a TCP
  error-flood map, prune all three on the same cadence.

## Scope Constraints

- No persistence: bans remain in-memory, expiry-driven state.
- Do not change the 4-hour `CLIENT_BAN_TIME` TTL.

## Acceptance Criteria

- [x] `prune_expired` is called periodically in the running daemon.
- [x] An integration/runtime test proves a ban inserted and then advanced past
      the TTL is physically removed from both maps.
- [x] Every maintenance tick physically removes expired IP and hash entries
      while preserving unexpired entries.

## Validation

- `cargo test -p emulebb-ed2k -p emulebb-core`
- `cargo clippy -p emulebb-ed2k -p emulebb-core --all-targets -- -D warnings -A unfulfilled-lint-expectations`

## Notes

Shares the pruning cadence with RUST-BUG-115 and RUST-FEAT-043.

- PR #101 (commit `7f274dd3`) wired the production loop. The 2026-10-13 closure
  audit reopened the item because existing tests did not prove physical map
  reclamation.
- Completed on 2026-10-13 in emulebb-rust commits `c3707c12` and `dfd4c2f7`.
  All `emulebb-ed2k` and `emulebb-core` tests pass, and the runtime test proves
  physical removal from both retained indexes while preserving fresh bans.

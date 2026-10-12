---
id: RUST-BUG-116
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/83
title: Wire periodic expiry pruning for the client BanStore
status: OPEN
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

`BanStore::prune_expired` exists but has no production caller. Both the IP and
user-hash ban maps therefore grow without bound over a long-running daemon:
expired entries are correctly treated as not-banned on lookup, but they are
never physically removed. The master prunes its ban maps on a timer.

## Current State

- `crates/emulebb-ed2k/src/ban_store.rs:122` defines `prune_expired(&self,
  now)`, which removes entries past `CLIENT_BAN_TIME`.
- The only caller is the unit test (`ban_store.rs:216`); a workspace-wide grep
  finds no daemon/core/runtime call site.

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

- Invoke `BanStore::prune_expired(Instant::now())` from a periodic runtime
  tick (the daemon maintenance loop or the ED2K transfer runtime cadence),
  matching the master's `BAN_CLEANUP_TIME` frequency.
- If RUST-BUG-115 lands a tracked-identity store and RUST-FEAT-043 lands a TCP
  error-flood map, prune all three on the same cadence.

## Scope Constraints

- No persistence: bans remain in-memory, expiry-driven state.
- Do not change the 4-hour `CLIENT_BAN_TIME` TTL.

## Acceptance Criteria

- [ ] `prune_expired` is called periodically in the running daemon.
- [ ] An integration/runtime test proves a ban inserted and then advanced past
      the TTL is physically removed from both maps.
- [ ] Long-running behavior does not grow the ban maps unboundedly.

## Validation

- Extend the `BanStore` tests with a production-cadence call-site test, or add
  a runtime test that exercises the periodic prune.

## Notes

Shares the pruning cadence with RUST-BUG-115 and RUST-FEAT-043.

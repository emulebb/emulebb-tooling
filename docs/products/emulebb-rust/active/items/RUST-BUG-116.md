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

The periodic production caller now exists, but the closure tests do not prove
that the running task physically removes expired entries from both internal ban
maps. Expiry-aware lookups can return "not banned" while an expired key remains
retained, so the current evidence cannot establish memory reclamation.

## Current State

- `crates/emulebb-core/src/network_api.rs` wires a periodic prune loop into the
  production runtime.
- The runtime test starts that loop with an empty store and proves only tick and
  shutdown behavior.
- The `BanStore` unit test checks expiry-aware lookups, not direct map retention;
  those lookups return false for expired entries even if no physical removal
  occurred.

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
- [ ] An integration/runtime test proves a ban inserted and then advanced past
      the TTL is physically removed from both maps.
- [ ] Every maintenance tick physically removes expired IP and hash entries
      while preserving unexpired entries.

## Validation

- Extend the `BanStore` tests with a production-cadence call-site test, or add
  a runtime test that exercises the periodic prune.

## Notes

Shares the pruning cadence with RUST-BUG-115 and RUST-FEAT-043.

- PR #101 (commit `7f274dd3`) wired the production loop. The 2026-10-13 closure
  audit reopened the item because existing tests did not prove physical map
  reclamation.

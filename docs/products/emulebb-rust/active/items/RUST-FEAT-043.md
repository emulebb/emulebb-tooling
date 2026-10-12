---
id: RUST-FEAT-043
workflow: local
title: Port the MFC TCP-error flooder IP ban
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, ban, anti-abuse, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

# RUST-FEAT-043 - Port the MFC TCP-error flooder IP ban

## Summary

Add the MFC TCP-error flooder: count TCP-layer errors per peer IP over a
rolling interval and IP-ban once a threshold is reached. The Rust transport and
listener surface connection errors but do not aggregate them per IP, so a peer
that repeatedly provokes TCP errors (for example connection-reset floods) is
not escalated to an IP ban.

## Current State

- Rust reports transport/listener errors locally (for example
  `crates/emulebb-ed2k/src/ed2k_tcp/transport.rs` and
  `ed2k_tcp/listener/session.rs` read/write error paths) with no per-IP
  counter.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `ClientList.cpp:515-540` `CheckTCPErrorFlooder(dwIP)` maintains an
  interval-window `TCPERRORFLOODERSTATE` per IP, increments per error, and on
  reaching `GetTCPErrorFlooderThreshold()` calls `AddBannedClient(dwIP)`.
- Gated by `thePrefs.IsDetectTCPErrorFlooder()` and bounded by
  `GetTCPErrorFlooderIntervalMinutes()`.
- `ClientList.cpp:595` prunes stale flood-map entries in `CClientList::Process`.

## Why This Matters

This is a defensive anti-abuse behavior in the authority client that Rust
simply lacks. It is a small, bounded addition that closes an escalation path
for peers that abuse the TCP accept path without having to open an upload slot.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/transport.rs` - accept/read error surfaces
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs` - per-session error
  handling
- `crates/emulebb-ed2k/src/ban_store.rs` - `ban` with IP-only scope
- `workspaces/workspace/app/emulebb-main/srchybrid/ClientList.cpp:515-540`

## Intended Shape

- Add a bounded per-IP interval-window counter beside `BanStore` (or as a
  sibling) with configurable interval and threshold matching the MFC prefs.
- Invoke it at the TCP accept/read/write error sites for an established peer
  endpoint.
- On threshold, apply an IP-only ban through `BanStore` and emit a bad-peer
  diagnostic with the event count and interval for soak-diff parity.
- Prune stale counters on the RUST-BUG-116 cadence.

## Scope Constraints

- IP-only ban; do not ban by hash.
- Keep the default detection disabled or matching the master default if one is
  exposed.
- Do not fold this into the queue-rank or file-request flood paths.

## Acceptance Criteria

- [ ] Repeated TCP errors from one IP within the interval produce an IP ban at
      the threshold.
- [ ] Errors outside the interval do not accumulate, and stale counters are
      pruned.
- [ ] A transport/listener test drives N synthetic errors and asserts the ban.

## Validation

- Unit tests for the counter window and threshold, plus a listener fixture
  test that raises the configured number of transport errors.

## Notes

Shares the pruning cadence with RUST-BUG-115 and RUST-BUG-116.

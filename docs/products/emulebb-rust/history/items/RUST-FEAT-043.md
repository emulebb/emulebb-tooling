---
id: RUST-FEAT-043
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/86
title: Port the MFC TCP-error flooder IP ban
status: DONE
priority: Minor
category: feature
labels: [rust, ed2k, ban, anti-abuse, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K upload/ban/slot audit 2026-10-12 vs emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/86. This local document is retained as the durable engineering spec and evidence record.

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

- [x] Repeated TCP errors from one IP within the interval produce an IP ban at
      the threshold.
- [x] Errors outside the interval do not accumulate, and stale counters are
      pruned.
- [x] A transport/listener test drives N synthetic errors and asserts the ban.

## Validation

- Unit tests for the counter window and threshold, plus a listener fixture
  test that raises the configured number of transport errors.

## Evidence

- `tcp_error_flood.rs` implements the bounded rolling per-IP tracker, stale
  pruning, threshold reset, and IP-only `BanStore` escalation.
- Listener seam and tracker tests cover threshold, interval reset, stale
  pruning, disabled policy, and non-transport errors.
- Settings, REST/OpenAPI 2.0, and WebUI surfaces expose the enable, interval,
  and threshold controls with bounded validation.
- Rust PR #130 delivered the feature on 2026-10-18 through rebased commits
  `dc324c08`, `65be4f27`, and `85cefaff`; required CI passed strict policy,
  formatting, Clippy, cargo-deny, CodeQL, live REST/OpenAPI conformance, and
  build/test jobs on Ubuntu, macOS, and Windows.
- Contract and harness support landed through tooling PR #34 (`2a6c2a12`) and
  build-tests PR #4 (`e90a06be`).

## Notes

Shares the pruning cadence with RUST-BUG-115 and RUST-BUG-116.

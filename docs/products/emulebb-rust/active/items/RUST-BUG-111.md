---
id: RUST-BUG-111
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/76
title: Avoid duplicate startup/republish on repeated OP_IDCHANGE
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, server, state-machine, login, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/76. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-111 - Avoid duplicate startup/republish on repeated OP_IDCHANGE

## Summary

The first fix correctly suppresses connected startup for a redundant
`OP_IDCHANGE`, but a genuine client-ID reassignment does not republish a
non-empty offer-file catalog. Reassignment re-enters startup while retaining the
session's published-hash epoch, so every previously published file is skipped.

## Current State

- `packet_handler.rs` now distinguishes first login, same-ID repeats, and a real
  ID change. A same-ID repeat emits no duplicate `ConnectSucceeded` event.
- A real reassignment calls connected startup, but
  `begin_offer_files_publishing` retains the prior published-hash set.
- `send_offer_files_snapshot` skips hashes already in that set, so a non-empty
  catalog produces no second `OP_OFFERFILES` frame for the new assigned ID.
- Existing tests use an empty shared catalog and assert events/public-IP state,
  so they cannot observe either duplicate suppression or required republication
  on the wire.

## Why This Matters

The session state transition and publication epoch must agree. Suppressing a
redundant transition is correct, but a real endpoint/ID reassignment needs a new
publication epoch so the server receives offers carrying the new client ID.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` - `OP_IDCHANGE` branch
- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` - `send_connected_server_startup`
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\ServerSocket.cpp` - IDCHANGE case (~lines 252-356)

## Intended Shape

- Run `ConnectSucceeded` and `send_connected_server_startup` only on the first
  accepted login or when the assigned `client_id` actually changes.
- On a redundant same-ID IDCHANGE, only refresh server flags/public-IP state as
  stock does, without republishing.
- Start a fresh offer-publication epoch before startup on a real LowID-to-HighID
  reassignment, preserving the full republish and public-IP refresh.

## Scope Constraints

- Do not drop valid ID reassignment handling.
- Keep the probe-search gate (`probe_search_sent`) unchanged; it already
  prevents duplicate probe searches.

## Acceptance Criteria

- [ ] A second `OP_IDCHANGE` with the same client ID emits no duplicate
      `ConnectSucceeded` event and triggers no offer-file republish.
- [ ] A genuine client-ID reassignment still emits the connect event, refreshes
      public-IP state, and republishes the catalog.
- [ ] Session-level tests cover both redundant and reassigning IDCHANGE with a
      non-empty catalog and assert emitted `OP_OFFERFILES` frames.

## Validation

- Session/state-machine tests for redundant and reassigning `OP_IDCHANGE`
  sequences.

## Notes

Found by the 2026-10-12 ED2K static audit; complements the RUST-BUG-109 and
RUST-BUG-110 HELLO/callback state-machine closures.

PR #102 (commit `29d5316f`) implemented the transition gate but closed the
GitHub issue before non-empty-catalog wire behavior was proven. The 2026-10-13
closure audit reopened the item.

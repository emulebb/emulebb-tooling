---
id: RUST-BUG-111
workflow: local
title: Avoid duplicate startup/republish on repeated OP_IDCHANGE
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, server, state-machine, login, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K static audit 2026-10-12 vs community-0.72, aMule, ed2k-server, lugdunum 17.15
---

# RUST-BUG-111 - Avoid duplicate startup/republish on repeated OP_IDCHANGE

## Summary

The `OP_IDCHANGE` handler re-runs the full connected-startup path on every
occurrence of the packet, including redundant re-sends of the same assigned
client ID. That re-emits `ConnectSucceeded` and republishes the offer-file
catalog when nothing changed. Stock eMule performs the connected transition
once and does not republish inside the IDCHANGE handler.

## Current State

- In `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs`, the `OP_IDCHANGE`
  branch unconditionally sends `ConnectSucceeded` and calls
  `send_connected_server_startup` after setting `login_accepted = true`.
- A server that echoes IDCHANGE, or sends a second IDCHANGE after the callback
  test, therefore triggers a duplicate connect event and a full offer-file
  republish.

## Why This Matters

This is a server-session state-machine parity divergence: it produces noisy
duplicate connect events and unnecessary full catalog republishes against live
servers, while stock only republishes on a fresh connection or an actual ID
change.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/packet_handler.rs` - `OP_IDCHANGE` branch
- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` - `send_connected_server_startup`
- `EMULEBB_WORKSPACE_ROOT\analysis\community-0.72\srchybrid\ServerSocket.cpp` - IDCHANGE case (~lines 252-356)

## Intended Shape

- Run `ConnectSucceeded` and `send_connected_server_startup` only on the first
  accepted login or when the assigned `client_id` actually changes.
- On a redundant same-ID IDCHANGE, only refresh server flags/public-IP state as
  stock does, without republishing.
- Preserve the full republish and public-IP refresh on a real LowID-to-HighID
  reassignment.

## Scope Constraints

- Do not drop valid ID reassignment handling.
- Keep the probe-search gate (`probe_search_sent`) unchanged; it already
  prevents duplicate probe searches.

## Acceptance Criteria

- [ ] A second `OP_IDCHANGE` with the same client ID emits no duplicate
      `ConnectSucceeded` event and triggers no offer-file republish.
- [ ] A genuine client-ID reassignment still emits the connect event, refreshes
      public-IP state, and republishes the catalog.
- [ ] A session-level test covers both redundant and reassigning IDCHANGE.

## Validation

- Session/state-machine tests for redundant and reassigning `OP_IDCHANGE`
  sequences.

## Notes

Found by the 2026-10-12 ED2K static audit; complements the RUST-BUG-109 and
RUST-BUG-110 HELLO/callback state-machine closures.

---
id: TMBB-FEAT-014
workflow: github
github_issue: TBD - file on emulebb/trackmulebb when scheduled
title: Push-capable transfer adapters - capability-gated SSE subscribe with poll fallback
status: OPEN
priority: Minor
category: feature
labels: [controller, performance, sse, rest, capability]
milestone: phase-2
created: 2026-06-17
source: dashboard design discussion (2026-06-17); depends on emulebb-rust RUST-FEAT-007
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-014 - Push-capable transfer adapters (capability-gated, poll fallback)

## Summary

Teach the transfers sync engine to **consume push** when a backend offers it,
without disturbing the projection/UI. Add an optional `subscribe()` to the
`ClientAdapter` interface that yields transfer snapshots/deltas; the engine uses it
when the backend advertises the relevant capability (`transfers.sse` for
emulebb-rust, see RUST-FEAT-007), and otherwise keeps the current poll loop. The
choice is **capability-driven** via `GET /capabilities` (TMBB-FEAT-004), so it
degrades gracefully to polling everywhere.

## Why This Matters

Push removes poll latency and wasted requests for the dashboard's main data path,
while the adapter abstraction keeps `TransferProjection`, the engine's replace/diff
logic, and the UI completely unchanged — a localized efficiency upgrade.

## Scope Constraints

- The `list_transfers()` poll path remains the universal fallback; push is additive.
- emulebb-rust push = SSE (`/api/v1/events`, RUST-FEAT-007). qBittorrentBB has no
  SSE — its lower-latency path is the `/sync/maindata` delta-pull (TMBB-FEAT-005).
  Both must fit the same `subscribe()`-or-poll abstraction.
- Projection/engine/UI semantics unchanged (same `UnifiedTransfer` snapshots).

## Acceptance Criteria

- [ ] `ClientAdapter` gains an optional `subscribe()` yielding updates applied to
      `TransferProjection` (full snapshot or namespaced delta).
- [ ] Engine selects push when the backend advertises the capability, else polls.
- [ ] SSE client (httpx streaming) with `Last-Event-ID` reconnect and automatic
      fallback to poll on stream failure.
- [ ] Tests: capability gating, push-applies-update, and the fallback path.

## Notes

- Pairs with RUST-FEAT-007 (server side) and TMBB-FEAT-004 (capability negotiation).
- WebSocket intentionally not used: the dashboard need is unidirectional; commands
  stay on normal REST POSTs.

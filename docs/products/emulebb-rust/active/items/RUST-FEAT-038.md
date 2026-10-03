---
id: RUST-FEAT-038
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/27
title: Add current-aMule-style endgame source takeover
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, scheduling, performance]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/27. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-038 - Add current-aMule-style endgame source takeover

## Summary

Allow healthy sources to take over outstanding blocks near download completion
instead of holding an exclusive lease on an entire part until its original
source finishes or fails. Current aMule explicitly redistributes final work
across sources; Rust's whole-part claim can leave the transfer waiting behind a
single slow source even when other useful peers are idle.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` assigns an exclusive
  whole-part claim.
- The exclusive model is simple and avoids duplicates, but it couples every
  remaining block in the part to the first claimant.
- Current aMule's `DownloadClient.cpp` contains endgame redistribution/takeover
  behavior and the 3.1 release notes call out requesting final blocks from
  several sources.

## Why This Matters

Long-tail completion is user-visible and affects whether a nearly complete file
finishes at all when a source stalls. Block-granular ownership also provides a
clean foundation for cancelling stale work without discarding valid blocks
already received from another source.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_transfer\piece_store.rs`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\DownloadClient.cpp`

## Intended Shape

- Represent requested/outstanding ownership at block granularity within a part.
- Enter an explicit bounded endgame mode when only a small amount of work
  remains or a lease becomes stale.
- Permit safe takeover/requeue to another eligible source and cancel obsolete
  requests when the first verified copy arrives.
- Preserve source attribution for invalid, duplicate, late, and accepted data.
- Make deliberate duplicate requests optional and tightly bounded; takeover
  should not imply uncontrolled redundant traffic.

## Scope Constraints

- First verified block wins; a late valid duplicate must not overwrite data or
  corrupt counters.
- Invalid data remains attributable to the sender that supplied it.
- Respect per-peer request limits, bans, disconnect cleanup, and final completion
  integrity checks.
- Do not increase duplicate traffic outside the explicit endgame policy.

## Acceptance Criteria

- [ ] A stalled block lease can be reassigned without releasing unrelated valid
      blocks from the same part.
- [ ] The final blocks can use multiple healthy sources under a documented,
      bounded endgame trigger.
- [ ] Late, duplicate, cancelled, invalid, and out-of-order responses leave
      piece state and peer attribution correct.
- [ ] Disconnect/reconnect and process-recovery paths cannot strand a block in
      an owned-but-unrequestable state.
- [ ] Normal non-endgame transfers do not create duplicate block traffic.
- [ ] Completion latency improves in a deterministic slow-final-source fixture.

## Validation

- Deterministic scheduler tests with fast, slow, stalled, disconnecting, and
  malicious peers.
- Property/state-machine tests for claim, takeover, cancel, receive, verify, and
  restart transitions.
- Local current-aMule interop witness demonstrating bounded final-block
  redistribution and correct completion.

## Notes

This is a current-aMule behavior improvement rather than a strict stock-wire
requirement. It should compose with, not substitute for, RUST-BUG-102's final
whole-file rehash.

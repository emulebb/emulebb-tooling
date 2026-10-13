---
id: RUST-BUG-117
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/103
title: Expire silent Kad buddy links from received activity
status: DONE
priority: Major
category: bug
labels: [rust, kad, buddy, liveness, callback, reliability]
milestone: rust-v0.1.0-beta.2
created: 2026-10-13
source: aMule buddy-liveness fix #1831 and emulebb-rust static audit 2026-10-13
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/103. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-117 - Expire silent Kad buddy links from received activity

## Summary

The outbound Kad buddy link now expires a peer after 25 minutes without a valid
inbound frame. Successful local ping writes do not refresh received liveness,
and link loss returns through the existing buddy manager for immediate cleanup
and re-search.

## Current State

- `crates/emulebb-ed2k/src/ed2k_tcp/buddy_liveness.rs` owns the monotonic
  ten-minute ping and 25-minute received-activity deadlines.
- `buddy_link.rs` refreshes liveness only after recognized, valid inbound frames;
  malformed, partial, and unknown traffic does not refresh it.
- Link completion is identity-safe across the transport registry and core buddy
  state, so a stale task cannot evict a replacement relationship.
- The core buddy manager receives one wake after active-link loss, clears the
  search cooldown, and reuses its existing search/backoff authority.

Current aMule added a dedicated buddy-liveness helper after observing the same
failure mode. Its maintained policy expires a buddy after 25 minutes without
received activity, comfortably above normal ping cadence.

## Why This Matters

A stale buddy can remain advertised while being unable to relay LowID callback
traffic. That is a long-lived correctness failure: the daemon appears connected
and keeps writing pings, but incoming connections routed through the buddy can
never arrive.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_tcp/buddy_link.rs` - buddy transport loop and
  ping cadence
- `crates/emulebb-core/src/kad_buddy.rs` - buddy selection and reconnect owner
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\KadBuddyLiveness.h` - maintained
  received-activity timeout policy

## Intended Shape

- Track the monotonic time of the last successfully decoded inbound buddy
  message.
- Expire the link after 25 minutes without received activity, regardless of
  successful outbound pings.
- Treat every valid inbound buddy frame, including keepalive/control traffic,
  as activity; malformed or partial bytes do not refresh the deadline.
- Return a distinct inactivity outcome through the existing link lifecycle so
  the current manager performs cleanup and bounded reconnect/backoff.
- Keep the timeout as an internal protocol invariant rather than a user-facing
  configuration knob.

## Scope Constraints

- Do not infer liveness from outbound write success.
- Do not create a second buddy-selection or reconnect authority.
- Preserve normal shutdown, cancellation, and explicit peer-disconnect
  behavior.
- Use paused Tokio time in tests; do not add wall-clock sleeps.

## Acceptance Criteria

- [x] A buddy link that receives no valid frames for 25 minutes terminates with
      the inactivity outcome even while ping writes continue to succeed.
- [x] Valid inbound activity refreshes the deadline and prevents premature
      expiry.
- [x] Partial or malformed traffic does not refresh the deadline.
- [x] Inactivity flows through existing cleanup and reconnect/backoff without a
      duplicate live buddy assignment.
- [x] Focused tests cover expiry, refresh, malformed input, shutdown, and
      reconnect handoff with deterministic Tokio time.

## Validation

- `cargo test -p emulebb-ed2k -p emulebb-core`
- `cargo clippy -p emulebb-ed2k -p emulebb-core --all-targets -- -D warnings -A unfulfilled-lint-expectations`

## Notes

This is received-activity liveness, not generic TCP keepalive tuning. The aMule
25-minute bound is reference evidence; Rust should express it through its native
async lifecycle.

- Completed on 2026-10-13 in emulebb-rust commits `92688d17`, `6a822d1e`,
  `5225f8f2`, and `50227302`. All 1,032 ED2K tests and 428 core tests pass;
  adjusted strict all-target Clippy also passes.

---
id: RUST-BUG-117
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/103
title: Expire silent Kad buddy links from received activity
status: OPEN
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

The outbound Kad buddy link sends periodic pings but never expires a peer that
stops sending data while leaving the TCP connection half-open. Read timeouts
currently loop forever, so successful local ping writes can keep a dead buddy
assignment resident and prevent reliable buddy-mediated callbacks.

## Current State

- `crates/emulebb-ed2k/src/ed2k_tcp/buddy_link.rs` sends a buddy ping every ten
  minutes.
- The receive loop wraps reads in a timeout, but timeout expiry continues the
  loop without enforcing any maximum received-activity age.
- Local write success proves only that the local socket accepted bytes; it does
  not prove the buddy is receiving or processing them.
- The surrounding buddy manager already owns reconnect/backoff. The link needs
  to return a liveness failure through that authority rather than create another
  reconnect loop.

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

- [ ] A buddy link that receives no valid frames for 25 minutes terminates with
      the inactivity outcome even while ping writes continue to succeed.
- [ ] Valid inbound activity refreshes the deadline and prevents premature
      expiry.
- [ ] Partial or malformed traffic does not refresh the deadline.
- [ ] Inactivity flows through existing cleanup and reconnect/backoff without a
      duplicate live buddy assignment.
- [ ] Focused tests cover expiry, refresh, malformed input, shutdown, and
      reconnect handoff with deterministic Tokio time.

## Validation

- Buddy-link unit tests with paused Tokio time and a loopback peer.
- Buddy-manager test proving stale-link cleanup reaches the existing reconnect
  path exactly once.

## Notes

This is received-activity liveness, not generic TCP keepalive tuning. The aMule
25-minute bound is reference evidence; Rust should express it through its native
async lifecycle.

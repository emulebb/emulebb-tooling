---
id: RUST-BUG-120
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/121
title: Publish coherent ED2K reachability snapshots
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, ed2k, reachability, concurrency, nat, beta]
product: emulebb-rust
phase: Phase 1
milestone: rust-v0.1.0-beta.3
created: 2026-10-15
source: 2026-10-15 post-RUST-BUG-119 reachability-state audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/121. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-120 - Publish coherent ED2K reachability snapshots

## Summary

Make ED2K public-IP and advertised-port state a coherent snapshot instead of a
collection of independently loaded relaxed atomics. Writers must publish one
complete logical update, and wire encoders that consume multiple reachability
facts must derive them from one immutable read.

This is Beta 3 stabilization work. The internal reachability API may break to
make the ownership and consistency contract explicit.

## Current State

- `ExternalReachability` stores server IP, fallback IP, NAT TCP/UDP mappings,
  and peer-confirmed UDP state in five independent relaxed atomics.
- `clear_all` clears those atomics sequentially, so concurrent readers can
  observe partially retired runtime identity.
- NAT reconciliation publishes its TCP and UDP mappings through two separate
  calls even though both values came from one `NatStatus` snapshot.
- Server-login and peer-hello encoders read advertised TCP and UDP ports in
  separate calls, so one packet can combine values from different NAT mapping
  generations.
- The API exposes only projected scalar reads, which makes coherent multi-field
  consumption impossible to express or review.

## Why This Matters

Reachability identity is protocol state, not independent telemetry. A mixed
packet can advertise a TCP callback port from one mapping generation and a UDP
reask port from another, while partially cleared state can outlive the runtime
that owned it. These races are rare but directly undermine HighID callbacks,
UDP reasks, and deterministic teardown during beta recovery paths.

## Representative Sites

- `crates/emulebb-ed2k/src/reachability.rs`
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session.rs`
- `crates/emulebb-core/src/ed2k_net_drivers.rs`
- `crates/emulebb-core/src/network_api.rs`

## Intended Shape

- Store raw producer evidence in one lock-protected state value and expose a
  cheap copied `ReachabilitySnapshot` for read-side use.
- Keep public-IP precedence and peer-confirmed-UDP precedence as snapshot
  projections, rather than duplicating precedence logic across call sites.
- Publish both ports from a single NAT status with one state transition.
- Read one snapshot when constructing server login and peer hello identities.
- Retain focused scalar convenience methods only where one fact is genuinely
  consumed independently.

## Scope Constraints

- Preserve current stock ED2K wire semantics and evidence precedence.
- Do not add async locks to synchronous packet-encoding paths.
- Do not add lock-free complexity or a new dependency where an infrequently
  written, cheaply copied state value is sufficient.
- Late writes from retired STUN, NAT, or Kad producers require explicit writer
  epochs and are a separate follow-up item.
- NAT lease-expiry policy, UDP-only remap re-login behavior, and active-probe
  evidence expiry remain separate lifecycle decisions.

## Acceptance Criteria

- [ ] Every externally visible reachability read comes from a complete state
      generation rather than independent atomic fields.
- [ ] A NAT status publishes mapped TCP and UDP ports atomically.
- [ ] Server login and peer hello identities consume one reachability snapshot
      for all advertised ports.
- [ ] Runtime-wide invalidation replaces the complete state atomically.
- [ ] Tests prove precedence, clone sharing, batch NAT updates, coherent
      multi-field reads, and complete invalidation.
- [ ] Follow-up ownership gaps found by the audit are recorded without expanding
      this item into a broad runtime rewrite.

## Validation

- Focused `emulebb-ed2k` reachability and wire-identity tests.
- Focused `emulebb-core` NAT synchronization tests.
- Repository formatting and Clippy checks.
- Full repository quality gate before merge.

## Notes

Implement this item in granular commits: establish the snapshot abstraction,
then make NAT publication atomic, then migrate multi-field wire consumers. Keep
the item updated after each validated commit so the remote branch is a durable
recovery point.

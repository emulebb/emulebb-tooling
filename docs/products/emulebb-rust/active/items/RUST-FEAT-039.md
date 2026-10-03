---
id: RUST-FEAT-039
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/28
title: Size ED2K request depth from measured RTT and bandwidth
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, performance, latency]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/28. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-039 - Size ED2K request depth from measured RTT and bandwidth

## Summary

Supplement Rust's rate-tier request window with measured request-to-first-byte
RTT and a bounded bandwidth-delay-product estimate. Current aMule adapts request
depth using RTT/BDP; Rust selects among fixed depths from throughput alone,
which cannot distinguish a high-rate nearby source from an equally fast but
high-latency path.

## Current State

- `crates/emulebb-ed2k/src/ed2k_tcp/download/window.rs` selects fixed request
  depths of 1, 2, 3, 6, 9, 12, or 18 using observed rate.
- It does not retain request-to-first-byte RTT or minimum RTT for the source.
- Current aMule's `DownloadClient.cpp` combines observed bandwidth and latency,
  applies a bounded BDP calculation, and caps the window at 24 while retaining
  protocol request packets of three ranges.

## Why This Matters

Rate alone can underfill a long-fat path or create excess queued work on a fast
low-latency LAN source. An RTT-aware window can sustain throughput while
reducing cancellation waste, head-of-line delay, and unnecessary requests.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_tcp\download\window.rs`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\DownloadClient.cpp`

## Intended Shape

- Measure request-to-first-byte RTT per source with timestamps tied to the
  actual request generation.
- Maintain a smoothed/minimum RTT and throughput estimate, derive a bounded BDP
  target, and translate it into block/request depth.
- Retain conservative startup, explicit minimum/maximum depth, hysteresis, and
  fast reduction after timeout, congestion, cancellation, or source slowdown.
- Keep the ED2K request packet's range-count constraint independent from the
  number of packets allowed in flight.
- Expose enough metrics to explain the chosen depth during evidence runs.

## Scope Constraints

- Never exceed peer/protocol range and payload bounds.
- A high measured RTT must not by itself authorize an unbounded queue.
- Protect against samples from retransmission, stale generations, clock issues,
  or late responses.
- Preserve the existing conservative behavior when there is insufficient
  measurement history.

## Acceptance Criteria

- [ ] Request-to-first-byte RTT and bandwidth estimates are maintained per
      source with invalid/stale samples excluded.
- [ ] Window depth derives from a documented bounded BDP formula with startup,
      hysteresis, and backoff behavior.
- [ ] Packet construction still obeys the three-range request-packet limit.
- [ ] LAN/low-RTT tests remain shallow while WAN/high-RTT tests can grow deeply
      enough to sustain the same bandwidth.
- [ ] A slowdown, timeout, or generation reset promptly reduces or resets the
      window without leaking claims.
- [ ] Runtime diagnostics make the inputs and selected depth observable.

## Validation

- Deterministic virtual-time tests for LAN, WAN, jitter, bandwidth step-up,
  slowdown, timeout, and late-response scenarios.
- Property tests asserting bounds and stable convergence under noisy samples.
- Local shaped-network comparison against current aMule using matched latency
  and bandwidth profiles.

## Notes

The fixed Rust tiers are a useful fallback. This item should evolve the control
signal without changing on-wire block-range semantics.

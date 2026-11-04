---
id: RUST-BUG-157
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/224
title: Eliminate unexplained ED2K offer publication stalls
status: OPEN
priority: Minor
category: bug
labels: [rust, ed2k, protocol, performance, scheduler, tests]
product: emulebb-rust
phase: Phase 1
milestone: post-beta-polish
created: 2026-11-04
source: deterministic 100,000-file OFFERFILES v1 scale evidence
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/224. This local document owns the durable engineering contract.

# RUST-BUG-157 - Eliminate unexplained ED2K offer publication stalls

## Summary

Investigate and eliminate unexplained long idle gaps in the Rust ED2K
OFFERFILES publication pump. Keep publication close to the server-advertised
cadence while candidates are ready, without weakening the negotiated minimum
interval or any packet, connection, or global limit.

## Current State

The deterministic 100,000-file OFFERFILES v1 campaign completed successfully:
the Rust client published every record in 505 batches, the maintained local
ED2K server indexed all 100,000 records, and neither endpoint reported an
oversized packet, blocked record, connection throttle, global throttle, or
disconnect.

Completion nevertheless took 682.422 seconds against a 249.5-second ideal
lower bound for the negotiated 200-record, 500-millisecond envelope. Client and
server logs contain multiple long pauses while publication remained
incomplete. The retained report is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-offerfiles-scale-20261104T130055Z-12836.json`.

## Why This Matters

Large-library publication is correctness-complete but unnecessarily slow when
the pump sleeps without a protocol or server-policy reason. Unexplained stalls
delay server visibility and hide scheduler defects behind a campaign that
eventually succeeds.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_server/session.rs` publication scheduling,
  candidate eligibility, and next-wakeup state.
- `crates/emulebb-ed2k/src/ed2k_server/session_driver.rs` connection-loop timer
  selection and due-publication dispatch.
- `crates/emulebb-ed2k/src/ed2k_server/startup.rs` due-batch construction and
  completion accounting.
- The existing shared-library OFFERFILES campaign in `emulebb-build-tests`.

## Intended Shape

- Attribute every material delay to negotiated pacing, candidate availability,
  connection state, or an explicit bounded retry/backoff.
- Keep a pending eligible batch scheduled without depending on an unrelated
  connection-loop event.
- Expose enough timing/reason state to distinguish intentional pacing from an
  idle pump without adding high-volume logging.
- Test the scheduler with controlled time; retain the existing scale campaign
  as end-to-end evidence rather than making wall-clock timing the unit-test
  oracle.

## Scope Constraints

- Preserve stock-shaped `OP_OFFERFILES` packets and the negotiated
  `offerfiles_v=1` envelope.
- Never publish faster than the server-advertised minimum interval.
- Keep `ed2k-server` upstream-clean; this item owns a Rust client scheduler
  investigation, not a server extension.
- Do not weaken packet, connection, global, memory, cancellation, or reconnect
  bounds to improve elapsed time.

## Acceptance Criteria

- [ ] A controlled-time regression reproduces the idle-pump failure without a
      flaky wall-clock threshold.
- [ ] Pending eligible candidates always retain a bounded next wakeup while the
      server connection remains publishable.
- [ ] Diagnostics distinguish negotiated wait, candidate wait, connection wait,
      retry/backoff, and unintended idle time.
- [ ] The corrected pump respects every negotiated and legacy pacing bound.
- [ ] The deterministic 100,000-file campaign completes with no unexplained
      long idle gaps and preserves all existing correctness and memory checks.
- [ ] The maintained local ED2K server still reports zero oversized packets,
      blocked records, and unexpected throttle events.

## Validation

- Focused controlled-time session and connection-loop scheduler tests.
- Canonical `emulebb-ed2k` tests and Rust quality gates.
- Existing deterministic OFFERFILES v1 cancellation, reconnect, and
  100,000-file completion campaign against the maintained local ED2K server.

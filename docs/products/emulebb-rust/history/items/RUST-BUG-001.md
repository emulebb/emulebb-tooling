---
id: RUST-BUG-001
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/77
title: Eliminate kad_swarm CI isolation debt
status: DONE
priority: Minor
category: bug
labels: [kad, tests, ci, flaky, debt]
milestone: post-beta-polish
created: 2026-06-14
source: PM quality review (2026-06-14) — isolate + document CI timing debt
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/77. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-001 - Eliminate kad_swarm CI isolation debt

## Summary

The `kad_swarm` multi-node networking tests were isolated from the normal
workspace runner because of cross-node transfer timing failures. The product
and CI-environment causes were fixed earlier, and the final CI debt is now
removed: the standard locked workspace test command runs every
`local_kad_swarm` case under normal parallel execution on all supported CI
operating systems.

## Current State

- `tools/rust_quality_gate.py` runs `cargo test --workspace --locked` without a
  `local_kad_swarm` skip.
- Composite `ci` and `ci-test` gates run the workspace suite once and no longer
  duplicate the Kad integration target in a separate serialized step.
- `test-kad-swarm` remains available as a focused serialized diagnostic command
  without weakening or duplicating the required CI path.
- Helper contract tests lock the unfiltered workspace command, prevent a future
  composite-gate duplication, and preserve the focused diagnostic gate.

## Why This Matters

An isolated CI step could hide scheduler or order coupling that would appear in
the normal workspace matrix. The tests cover multi-node Kad transfer, a core
capability of the functional gate, so they now run under the same scheduling
conditions as every other workspace test.

## Representative Sites

- `tools/rust_quality_gate.py` - standard workspace, focused Kad, and composite
  CI gate definitions
- `tools/tests/test_rust_quality_gate.py` - executable gate-contract coverage
- `crates/emulebb-core/tests/kad_swarm.rs` - six multi-node Kad integration
  cases
- `crates/emulebb-core/src/download_source_registry.rs` - per-file endpoint
  retry cooldown fixed during root-cause work

## Intended Shape

- Run Kad swarm integration tests in the normal locked workspace suite with the
  default parallel test runner.
- Keep a separately addressable focused command for local diagnosis, not as a
  second required CI execution path.
- Keep runner LAN address discovery explicit through inherited `X_LOCAL_IP`.

## Acceptance Criteria

- [x] Root causes of the timing failures are identified and documented.
- [x] `kad_swarm` and `local_kad_swarm` pass under normal parallel execution
      across the Windows, macOS, and Ubuntu matrix.
- [x] CI runs them in the standard workspace matrix without `--skip`.
- [x] Composite gates do not rerun the integration target in a serialized step.

## Root Cause

Two independent causes were corrected before the final gate cleanup:

1. **Product defect — per-endpoint retry cooldown starved multi-file peers.**
   `DownloadSourceRegistry.last_attempted_endpoints` keyed the 20-minute
   anti-churn cooldown by bare `(ip, tcp_port)`, so a peer that successfully
   served file A could not be leased for file B during the same window. The
   fix keys the cooldown by `(endpoint, file)`, matching eMule's per-client-file
   `MIN_REQUEST_TIME` relationship.
2. **CI environment — loopback `X_LOCAL_IP`.** The swarm harness intentionally
   rejects loopback LAN binds. CI now resolves each runner's primary IPv4 and
   provides it through `X_LOCAL_IP` before the test gate.

## Validation

- `python tools/tests/test_rust_quality_gate.py` (14 tests passed)
- `python tools/rust_quality_gate.py policy` (111 policy tests passed)
- `python tools/rust_quality_gate.py fmt`
- `python tools/rust_quality_gate.py diagnostics`
- `python tools/rust_quality_gate.py clippy`
- Workspace-orchestrated `emulebb-core` Debug tests passed with normal
  parallelism: 400 unit tests plus all integration suites, including all six
  `kad_swarm` cases in 16.44 seconds.
- The full unfiltered workspace Rust and documentation test suite passed in
  Debug configuration.
- PR #113 required CI passed on Windows, macOS, and Ubuntu with the unfiltered
  workspace gate. Workflow lint, cargo-deny, policy/format/clippy, CodeQL, and
  live REST/OpenAPI conformance also passed.

## Notes

- Product root-cause commit `dab4b290` made retry cooldown per endpoint and
  file; CI root-cause commit `76af38c0` supplied a real runner LAN address.
- Completed on 2026-10-15 by emulebb-rust PR #113 in preserved commit
  `dd05eae7`.
- GitHub issue #77 is closed and the eMuleBB Roadmap item is Done.

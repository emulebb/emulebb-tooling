---
id: RUST-BUG-138
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/187
title: Correlate Kad search responses before flood limiting
status: DONE
priority: Major
category: bug
labels: [rust, kad, protocol, correlation, abuse-resistance]
milestone: rust-v0.1.0-beta.3
created: 2026-10-30
source: 2026-10-30 stock/current-aMule/Rust protocol review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/187. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-138 - Correlate Kad search responses before flood limiting

## Summary

Apply Kad response admission and flood accounting only after a response is
correlated with a pending request. Unsolicited traffic must not consume the
legitimate response allowance of an active lookup.

## Intended Shape

- Validate endpoint, opcode, target, and pending-request identity first.
- Reject stale, duplicate, unsolicited, and mismatched responses without
  charging the valid-response limiter.
- Apply the existing limiter only to correlated response work.

## Acceptance Criteria

- [x] Correlation precedes response-rate accounting.
- [x] Invalid traffic cannot starve a later legitimate response.
- [x] Valid stock-shaped responses retain current traversal behavior.
- [x] Deterministic spoofed-flood and legitimate-response tests pass.

## Validation

- Focused Kad RPC correlation and limiter tests.
- Packet diagnostics proving rejection reason and valid-request continuity.

## Resolution

- Registered expected Kad response targets and endpoints before flood accounting, with RAII cleanup.
- Merged by [emulebb-rust#194](https://github.com/emulebb/emulebb-rust/pull/194) at [431d45a8](https://github.com/emulebb/emulebb-rust/commit/431d45a8283fe5edbc8357be412e933771af3232).

## Evidence

- `cargo test -p emulebb-kad-net`; `cargo test -p emulebb-kad-dht`
- `cargo test --workspace`
- `cargo clippy --workspace --all-targets -- -D warnings`
- `python tools/rust_quality_gate.py build`

---
id: RUST-BUG-138
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/187
title: Correlate Kad search responses before flood limiting
status: OPEN
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

- [ ] Correlation precedes response-rate accounting.
- [ ] Invalid traffic cannot starve a later legitimate response.
- [ ] Valid stock-shaped responses retain current traversal behavior.
- [ ] Deterministic spoofed-flood and legitimate-response tests pass.

## Validation

- Focused Kad RPC correlation and limiter tests.
- Packet diagnostics proving rejection reason and valid-request continuity.

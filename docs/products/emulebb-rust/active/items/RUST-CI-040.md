---
id: RUST-CI-040
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/295
title: Verify download limits charge payload rather than control overhead
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/295. This local document owns the durable engineering specification and evidence.

# RUST-CI-040 - Verify download limits charge payload rather than control overhead

## Summary

A shared payload throttle and multi-transfer tests already exist. The remaining review is the call-site byte accounting for control/header/compressed data; no missing limiter is established.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: transfer-accounting-proof.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/download_throttle.rs:1`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/tests/download_throttle.rs:35`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A12-payload-throttle

## Acceptance Criteria

- [ ] Trace reservations to actual received payload.
- [ ] Prove headers/control traffic do not consume a user payload limit under the selected contract.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

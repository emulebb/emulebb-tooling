---
id: RUST-CI-041
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/296
title: Verify per-address limits when upload slots are immediately available
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/296. This local document owns the durable engineering specification and evidence.

# RUST-CI-041 - Verify per-address limits when upload slots are immediately available

## Summary

A three-client per-IP admission cap and tests already exist. Verify activation/reask/available-slot paths before treating the aMule per-address-slot item as a missing Rust feature.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: upload-admission-proof.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/upload_queue/admission.rs:1`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/upload_queue/admission.rs:190`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A13-address-slot-cap

## Acceptance Criteria

- [ ] Prove admission and promotion cannot bypass the intended address cap.
- [ ] Document intentional differences from aMule and retain stock authority.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

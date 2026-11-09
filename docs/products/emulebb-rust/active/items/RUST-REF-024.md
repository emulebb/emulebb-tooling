---
id: RUST-REF-024
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/292
title: Replace unchecked AICH geometry narrowing with bounded conversions
status: OPEN
priority: Minor
category: refactor
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/292. This local document owns the durable engineering specification and evidence.

# RUST-REF-024 - Replace unchecked AICH geometry narrowing with bounded conversions

## Summary

Plain u64-to-usize casts remain. The audit establishes a hardening opportunity, not a reachable Windows/Linux 64-bit failure. Avoid adding a new supported 32-bit product target merely for this cleanup.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: portable-hardening.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/aich_recovery.rs:136`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/aich_recovery.rs:252`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/aich_cache.rs:158`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section aich-width

## Acceptance Criteria

- [ ] Geometry conversions return an explicit error when not representable.
- [ ] Boundary tests cover the arithmetic without huge allocations.
- [ ] An optional 32-bit compile lane is evaluated separately.

## Dependencies And Coordination

- existing AICH integrity work
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

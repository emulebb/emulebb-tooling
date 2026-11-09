---
id: RUST-BUG-173
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/275
title: Reject file sizes outside representable ED2K hashset geometry
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/275. This local document owns the durable engineering specification and evidence.

# RUST-BUG-173 - Reject file sizes outside representable ED2K hashset geometry

## Summary

Expected MD4 counts still saturate to u16::MAX while the actual encoder rejects overflowing vector length. Make the accepted transfer geometry explicit instead of letting saturation stand in for a supported-size decision.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/hashset.rs:18`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/codec/hashset.rs:78`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_hashset-largefile.md` section 2.2

## Acceptance Criteria

- [ ] Define the largest representable valid part-count boundary from stock geometry.
- [ ] Reject unsupported sizes/counts before expensive work or metadata acceptance.
- [ ] Cover exact-part multiples and both sides of the count boundary.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

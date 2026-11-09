---
id: RUST-BUG-175
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/277
title: Correlate STUN mapping replies with the expected endpoint
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/277. This local document owns the durable engineering specification and evidence.

# RUST-BUG-175 - Correlate STUN mapping replies with the expected endpoint

## Summary

The unconnected mapping probe checks source IP and random transaction ID but not source port. Endpoint matching is reasonable defense in depth; first confirm supported STUN response-source/alternate-port semantics.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/stun.rs:229`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/stun.rs:309`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.3

## Acceptance Criteria

- [ ] Reject a same-IP wrong-port packet for a transaction that expects a fixed endpoint.
- [ ] Preserve supported STUN response endpoint behavior and transaction/cookie validation.
- [ ] Keep receive work and deadlines bounded.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

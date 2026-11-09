---
id: RUST-BUG-180
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/282
title: Bound Kad tracker population under source churn
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/282. This local document owns the durable engineering specification and evidence.

# RUST-BUG-180 - Bound Kad tracker population under source churn

## Summary

Per-source request accounting and minute pruning do not themselves establish aggregate memory bounds. Verify churn exposure, then enforce fail-visible bounded admission while preserving stock ordinary traffic.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

maps lack hard ceiling by static inspection; stress proof pending

- `repos/emulebb-rust/crates/emulebb-kad-net/src/tracker.rs:16`
- `repos/emulebb-rust/crates/emulebb-core/src/kad_routing_maintenance.rs:352`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_dos-resilience.md` section 2.2

## Acceptance Criteria

- [ ] A deterministic distinct-source churn case proves memory/work bounds across prune cadence.
- [ ] Capacity exhaustion cannot erase active bans or cause unbounded eviction work.
- [ ] Record existing same-tick flood-accounting behavior separately from map-population bound.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

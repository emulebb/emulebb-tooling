---
id: RUST-FEAT-066
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/272
title: Weight Kad user estimates by observed firewall and version ratios
status: OPEN
priority: Minor
category: feature
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/272. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-066 - Weight Kad user estimates by observed firewall and version ratios

## Summary

The estimator still uses fixed firewall multipliers. Improving this optional operator statistic has no routing, search or publish correctness impact.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: client-telemetry-followup.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-kad-routing/src/zone.rs:333`
- `repos/emulebb-rust/crates/emulebb-kad-routing/src/zone.rs:348`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_kad-routing-maint.md` section 4.1

## Acceptance Criteria

- [ ] Introduce bounded observed ratio inputs only if their owner and freshness are explicit.
- [ ] Match stock weighted estimates over synthetic populations.
- [ ] Keep telemetry work independent of packet/routing semantics.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

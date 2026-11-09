---
id: RUST-BUG-174
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/276
title: Require authenticated or corroborated public-IP evidence for VPN Guard
status: OPEN
priority: Major
category: bug
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/276. This local document owns the durable engineering specification and evidence.

# RUST-BUG-174 - Require authenticated or corroborated public-IP evidence for VPN Guard

## Summary

Plain HTTP is unauthenticated and current guard logic accepts one allowlisted successful leg when the other fails. This contradicts the report's two-independent-success mitigation. Native VPN remains experimental; keep the fix separate from supported Docker/Gluetun Beta 3 certification unless that experimental mode is promoted.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Major. Delivery lane: vpn-experimental.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/public_ip_probe.rs:120`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/public_ip_probe.rs:153`
- `repos/emulebb-rust/crates/emulebb-core/src/vpn_guard.rs:83`
- `repos/emulebb-rust/crates/emulebb-core/src/vpn_guard.rs:118`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_reachability.md` section 2.1 / 4.1

## Acceptance Criteria

- [ ] A forged HTTP answer alone cannot establish a verified configured egress verdict.
- [ ] Use authenticated pinned-interface HTTP evidence or corroboration with an independent successful leg; preserve explicit failure classification.
- [ ] Exercise STUN failure plus forged HTTP, disagreeing successes and real allowed evidence without weakening interface binding.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

---
id: RUST-BUG-177
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/279
title: Bound remote control-plane admission and authentication abuse
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/279. This local document owns the durable engineering specification and evidence.

# RUST-BUG-177 - Bound remote control-plane admission and authentication abuse

## Summary

32-byte key validation exists under closed issue36. Failure throttling is optional additional hardening, not an established weak-key exposure. Consolidate with dos-resilience 2.4.

Authenticated application middleware cannot limit idle pre-auth TCP sessions. Consolidate with rest-api3.3; do not imply API auth fixes socket exhaustion.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: control-plane.

## Current Findings

static hardening opportunity; short-key premise contradicted

plain axum serve observed; load exposure not reproduced

- `repos/emulebb-rust/crates/emulebb-rest/src/routes.rs:337`
- `repos/emulebb-rust/crates/emulebb-daemon/src/lib.rs:334`
- `repos/emulebb-rust/crates/emulebb-daemon/src/lib.rs:988`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_rest-api.md` section 3.3
- `emulebb-rust-prompt_audit_findings_dos-resilience.md` section 2.4

## Acceptance Criteria

- [ ] Confirm realistic non-loopback admission risk before changing behavior.
- [ ] Bound idle connections and repeated failed authentication without unbounded per-source tracking or leaking API keys.
- [ ] Document reverse-proxy/TLS boundary and retain legitimate API/SSE workflows.
- [ ] Use bounded admission or a documented supported proxy boundary; retain normal authenticated operations.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

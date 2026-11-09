---
id: RUST-REF-023
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/289
title: Move fork-only PCP ownership and route integration into consumers
status: OPEN
priority: Major
category: refactor
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/289. This local document owns the durable engineering specification and evidence.

# RUST-REF-023 - Move fork-only PCP ownership and route integration into consumers

## Summary

Fork-specific init, server-admission and free APIs remain in use. A consumer C adapter can own matched-CRT frees and explicit route filtering while keeping upstream sources unchanged. Context destruction must be tied to the exact upstream revision.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Major. Delivery lane: native-integration.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-pcpnatpmp/src/lib.rs:118`
- `repos/emulebb-rust/crates/emulebb-pcpnatpmp/src/lib.rs:416`
- `repos/emulebb-rust/crates/emulebb-pcpnatpmp/src/lib.rs:472`
- `repos/emulebb-rust/crates/emulebb-pcpnatpmp-sys/src/lib.rs:78`

## Audit Provenance

- `LIBPCPNATPMP-CONSUMER-REFACTOR-AUDIT-2026-11-09.md` section consumer-adapters

## Acceptance Criteria

- [ ] Use a consumer-owned C allocator boundary and safe ownership guards.
- [ ] Validate explicit-server routes before PCP traffic using OS source selection.
- [ ] Preserve automatic gateway operation and existing IPv4 behavior.
- [ ] Remove custom bindings only after replacement evidence passes.

## Dependencies And Coordination

- gateway-inventory-decision
- RUST-REF-006 / issue #9
- RUST-CI-030 / issue #163
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

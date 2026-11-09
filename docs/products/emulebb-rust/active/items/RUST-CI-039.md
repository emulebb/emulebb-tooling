---
id: RUST-CI-039
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/294
title: Measure initial source discovery including hostname-added servers
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/294. This local document owns the durable engineering specification and evidence.

# RUST-CI-039 - Measure initial source discovery including hostname-added servers

## Summary

The audit did not establish a source-discovery timing defect. Create a bounded verification outcome for initial source requests and hostname server UDP behavior before considering a scheduling change.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: source-discovery-proof.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-core/src/ed2k_sources.rs:1`
- `repos/emulebb-rust/crates/emulebb-core/src/server_api.rs:1`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A10-source-latency

## Acceptance Criteria

- [ ] Measure deterministic startup-to-first-request latency under a stated target.
- [ ] Cover hostname resolution and UDP source discovery.
- [ ] Retain reconnect/rate-limit safety.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

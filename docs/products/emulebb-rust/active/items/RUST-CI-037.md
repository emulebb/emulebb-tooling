---
id: RUST-CI-037
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/288
title: Produce a read-only issue and release-readiness digest
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/288. This local document owns the durable engineering specification and evidence.

# RUST-CI-037 - Produce a read-only issue and release-readiness digest

## Summary

A persisted PM command can project GitHub state into a concise digest and readiness view. It must cite owning issues and report uncertainty rather than establish another tracker.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: pm-automation.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-tooling/scripts/gh-actions-status.py:1`
- `repos/emulebb-tooling/docs/reference/RELEASE-BRANCHING-AND-PACKAGING.md:73`

## Audit Provenance

- `PM.md` section pm-digest

## Acceptance Criteria

- [ ] Read GitHub/issues/Actions and canonical specs without mutating workflow state.
- [ ] Report blocking dependencies and evidence freshness with source links.
- [ ] Output contains no operator secrets or private paths.

## Dependencies And Coordination

- board-triage
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

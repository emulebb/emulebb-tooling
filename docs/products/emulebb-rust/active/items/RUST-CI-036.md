---
id: RUST-CI-036
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/287
title: Add issue and PR evidence templates
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/287. This local document owns the durable engineering specification and evidence.

# RUST-CI-036 - Add issue and PR evidence templates

## Summary

No issue or PR templates were found. Standardize scope, evidence, attribution and wire-impact prompts without requiring users to invent an unallocated stable ID.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: pm-process.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/.github/DEFAULT_BRANCH_POLICY.md:1`
- `repos/emulebb-tooling/docs/reference/DEVELOPMENT-GUIDE.md:254`

## Audit Provenance

- `PM.md` section templates

## Acceptance Criteria

- [ ] Bug, feature, audit and PR forms link owning issue/spec and ask for reproducible evidence.
- [ ] Release form references the existing candidate checklist.
- [ ] Templates follow the parent-coordinated PR policy.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

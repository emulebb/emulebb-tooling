---
id: RUST-CI-038
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/291
title: Report bundled SQLite version in build evidence
status: OPEN
priority: Minor
category: ci
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/291. This local document owns the durable engineering specification and evidence.

# RUST-CI-038 - Report bundled SQLite version in build evidence

## Summary

Cargo.lock identifies rusqlite/libsqlite3-sys but not a user-facing SQLite runtime version report. Include the exact bundled SQLite version in safe CI/SBOM evidence and define an update review trigger.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: supply-chain-evidence.

## Current Findings

Static source/spec review; no validation executed.

- `repos/emulebb-rust/Cargo.toml:70`
- `repos/emulebb-rust/tools/ci_environment.py:175`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_dependencies.md` section sqlite-provenance

## Acceptance Criteria

- [ ] Report the SQLite version from the resolved native package/runtime.
- [ ] Link advisory review to the normal dependency-update process.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

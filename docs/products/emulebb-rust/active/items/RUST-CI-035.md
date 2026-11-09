---
id: RUST-CI-035
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/293
title: Separate mandatory Windows/Linux gates from optional platform outcomes
status: OPEN
priority: Major
category: ci
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/293. This local document owns the durable engineering specification and evidence.

# RUST-CI-035 - Separate mandatory Windows/Linux gates from optional platform outcomes

## Summary

Parent-reserved RUST-CI-035 owns the user-authorized split. CI combines Linux ARM/Windows/macOS in build-test and requires Android; release smoke/images depend on the entire native matrix, and the assembler hardcodes macOS assets. Docs alone cannot implement the new gate.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: beta3-platform-gates.

## Current Findings

Exact workflow needs/matrix and assembler contract verified statically; no jobs changed or rerun.

- `repos/emulebb-rust/.github/workflows/ci.yml:222`
- `repos/emulebb-rust/.github/workflows/ci.yml:709`
- `repos/emulebb-rust/.github/workflows/release.yml:133`
- `repos/emulebb-rust/.github/workflows/release.yml:267`
- `repos/emulebb-rust/.github/workflows/release.yml:438`
- `repos/emulebb-rust/.github/workflows/release.yml:630`
- `repos/emulebb-build/emule_workspace/release_candidate.py:124`
- `repos/emulebb-tooling/docs/products/emulebb-rust/active/items/RUST-CI-009.md:210`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_multi-platform.md` section beta3-gate-split

## Acceptance Criteria

- [ ] Define an explicit mandatory Windows/Linux target and artifact contract; separately identify optional macOS, Android and other platform work.
- [ ] Separate required-summary and candidate dependency graphs so an optional OS-only failure cannot skip mandatory smoke/assembly.
- [ ] Keep shared source, workflow lint, quality, supply-chain, CodeQL, REST, integrity and provenance failures mandatory.
- [ ] Publish independent optional results and failures; do not blanket continue-on-error shared checks.
- [ ] Update assembler inventory/manifest validation and failure-injection tests for missing optional versus mandatory assets.
- [ ] Preserve enforced checks until the reviewed workflow change lands; tagging/publication remain separately authorized.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

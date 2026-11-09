---
id: RUST-BUG-170
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/271
title: Restore the compatible-client branch of old-client upload scoring
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/271. This local document owns the durable engineering specification and evidence.

# RUST-BUG-170 - Restore the compatible-client branch of old-client upload scoring

## Summary

Current old_client only checks is_emule_client and old version. The compatible-client soft-id leg is not represented, so legacy non-eMule queue ordering can differ.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-fairness.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/upload_queue/score.rs:74`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/hello.rs:223`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_credits-queue.md` section 3.1

## Acceptance Criteria

- [ ] Parse and retain the required compatible-client identity tag.
- [ ] Reproduce the stock predicate with legacy soft-id boundary fixtures.
- [ ] Preserve queue fairness, bad-guy zeroing and modern-client ordering.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

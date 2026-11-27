---
id: RUST-BUG-181
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/283
title: Bound RIFF media parsing and retain malformed-input regressions
status: DONE
priority: Major
category: bug
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/283. This local document owns the durable engineering specification and evidence.

# RUST-BUG-181 - Bound RIFF media parsing and retain malformed-input regressions

## Closure

PR #319 bounded RIFF LIST traversal to 16 levels within the existing 2 MiB
metadata prefix. It retained deterministic regressions for the nesting
boundary, valid sibling metadata and a truncated AVI list. The fix and its
tests are present on Rust main. GitHub closed the owning issue as completed
and the Roadmap marks it Done. The original audit proposed a continuous
media fuzz target, which remains unverified by this evidence.
[Implementation and validation](https://github.com/emulebb/emulebb-rust/pull/319) · [Closed issue](https://github.com/emulebb/emulebb-rust/issues/283)

## Summary

Consolidate with media-metadata3.1 as one parser-bounds outcome, rather than a second mandatory beta blocker issue.

Adversarial locally shared WAVE/AVI bytes can drive recursion. Scope is local library admission, not demonstrated unauthenticated remote input. Consolidate fuzz-malformed3.1.

The recursive LIST parser has no visible depth budget. The regression belongs with the media-audit defect, not a separate competing implementation.

The fuzz workspace still has no media-metadata target. Share ownership with the fuzz/media audit and ensure recursion/size budgets precede continuous fuzzing.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: parser-safety.

## Current Findings

four fuzz targets confirmed; media target absent

recursive call without depth guard confirmed; no crash executed

Static source/spec review; no validation executed.

- `repos/emulebb-rust/fuzz/Cargo.toml:1`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/media_metadata.rs:563`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/media_metadata.rs:614`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_fuzz-malformed.md` section 3.1
- `emulebb-rust-prompt_audit_findings_media-metadata.md` section 3.1
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section riff-regression
- `emulebb-rust-prompt_audit_findings_testing-harness.md` section media-fuzz

## Acceptance Criteria

- [ ] Bound recursive RIFF LIST processing with explicit depth/work limits or iterative traversal.
- [ ] Deeply nested and truncated synthetic files return safely while normal WAVE/AVI tags remain correct.
- [ ] Exercise media parser through bounded fuzz inputs and retain deterministic regressions; do not claim a remote crash without tracing input admission.
- [ ] Deep nesting terminates within a documented bound without stack overflow.
- [ ] Valid nested metadata remains compatible.
- [ ] Neutral corpus covers supported container metadata and malformed nesting.
- [ ] Target enforces finite resources and runs through the existing fuzz workflow.

## Dependencies And Coordination

- audit media-metadata: RIFF recursion finding
- audit fuzz-malformed: media target
- riff-regression
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

---
id: RUST-BUG-182
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/284
title: Honor ID3 flags before publishing derived text
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/284. This local document owns the durable engineering specification and evidence.

# RUST-BUG-182 - Honor ID3 flags before publishing derived text

## Summary

Display metadata correctness; separate from FEAT040 inbound metadata transport. Skip encrypted/compressed frames; handle supported unsynchronization safely.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: search-metadata.

## Current Findings

parser reads frame size/text but does not process tag/frame flags

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_transfer/media_metadata.rs:375`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_media-metadata.md` section 3.3

## Acceptance Criteria

- [ ] Synthetic ID3v2.3/v2.4 flag combinations yield correct text or no metadata, never garbage tag publication.
- [ ] Truncation and unsupported transformations remain bounded.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

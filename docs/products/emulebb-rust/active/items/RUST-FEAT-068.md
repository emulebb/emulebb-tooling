---
id: RUST-FEAT-068
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/286
title: Make non-Windows legacy encoding policy explicit
status: OPEN
priority: Minor
category: feature
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/286. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-068 - Make non-Windows legacy encoding policy explicit

## Summary

Closed186 establishes negotiated Unicode/legacy behavior, not every locale. Optional explicit operator codepage policy can improve Linux legacy names; silent automatic charset guessing is not a default correctness fix.

Same outcome as4.1. Heuristic repairs must not corrupt already-correct names; also overlaps closed89 intent.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: search-metadata.

## Current Findings

fixed Windows1252 fallback confirmed; no negotiated encoding regression proven

current repair is Windows1252/UTF8 heuristic

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_string.rs:89`
- `repos/emulebb-rust/crates/emulebb-kad-proto/src/tag.rs:115`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/file_name.rs:111`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_search.md` section 4.1
- `emulebb-rust-prompt_audit_findings_search.md` section 5.1

## Acceptance Criteria

- [ ] Keep Windows ACP and negotiated Unicode behavior unchanged.
- [ ] Specify an explicit non-Windows legacy-codepage policy and deterministic malformed/round-trip vectors before accepting configuration.
- [ ] Add ambiguous and already-correct fixtures; never use network-name repair to redefine native filesystem identity.

## Dependencies And Coordination

- search:4.1
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

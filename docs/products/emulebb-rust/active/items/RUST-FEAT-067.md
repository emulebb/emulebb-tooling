---
id: RUST-FEAT-067
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/285
title: Define supported search text syntax and rating criteria
status: OPEN
priority: Minor
category: feature
labels: [rust, audit]
milestone: post-beta-polish
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/285. This local document owns the durable engineering specification and evidence.

# RUST-FEAT-067 - Define supported search text syntax and rating criteria

## Summary

Stock input ergonomics are not wire incompatibility. Preserve structured Rust API; explicitly reject unsupported metatag/link text or define it, and assess rating criteria separately from inbound metadata issue29.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: search-metadata.

## Current Findings

structured criteria present; inline metatags and rating search absent

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_server/search_expr.rs:406`
- `repos/emulebb-rust/crates/emulebb-core/src/search_query.rs:1`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_search.md` section 3.1

## Acceptance Criteria

- [ ] Choose and document supported query syntax without silently treating recognized unsupported syntax as literal keywords.
- [ ] If rating criteria are accepted, update API, validation, encoder and consumers with stock-shaped golden proof.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

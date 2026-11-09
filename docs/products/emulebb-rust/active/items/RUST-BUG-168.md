---
id: RUST-BUG-168
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/269
title: Enforce the stock incoming secure-ident public-key size limit
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/269. This local document owns the durable engineering specification and evidence.

# RUST-BUG-168 - Enforce the stock incoming secure-ident public-key size limit

## Summary

The inbound decoder verifies its byte prefix but does not apply the existing 80-byte stock cap before RSA parsing. The outbound key cap does not cover this path.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:253`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:309`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 4.1

## Acceptance Criteria

- [ ] Reject incoming keys above stock MAXPUBKEYSIZE before parsing.
- [ ] Cover valid boundary and oversized key payloads on inbound/outbound handlers.
- [ ] Preserve normal stock SPKI key exchange.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

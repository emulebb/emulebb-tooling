---
id: RUST-BUG-171
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/273
title: Reject degenerate server Diffie-Hellman public values
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/273. This local document owns the durable engineering specification and evidence.

# RUST-BUG-171 - Reject degenerate server Diffie-Hellman public values

## Summary

The server DH path still computes modpow without rejecting degenerate values. Stock has the same weakness; rejecting invalid inputs preserves valid-peer compatibility and should not imply modern authenticated encryption.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_server/session.rs:995`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_obfuscation.md` section 2.1

## Acceptance Criteria

- [ ] Reject zero, one and out-of-range public values before key derivation.
- [ ] Cover valid fixed-width boundary exchanges and bounded failure behavior.
- [ ] Preserve stock obfuscation bytes for valid peers.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

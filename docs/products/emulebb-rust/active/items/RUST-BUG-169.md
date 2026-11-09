---
id: RUST-BUG-169
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/270
title: Honor negotiated secure-ident V2 support and LowID challenge addressing
status: OPEN
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/270. This local document owns the durable engineering specification and evidence.

# RUST-BUG-169 - Honor negotiated secure-ident V2 support and LowID challenge addressing

## Summary

The V2-shaped signature is decoded and verified without checking the peer's advertised V2 capability. This is bounded leniency, not proof of authentication bypass.

The REMOTECLIENT reconstruction falls back to unspecified IPv4 and the download handler passes no external address. Verify stock LowID/local-address fallback and implement the actual reachable edge alongside V2 handling.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Current Findings

Current-source inspection; no tests, builds or live campaigns run

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:285`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:379`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/listener/session/secure_ident.rs:146`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:321`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/download/session/secure_ident.rs:110`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 4.3
- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 4.4

## Acceptance Criteria

- [ ] Check negotiated V2 support before accepting a V2 trailer.
- [ ] Cover V1-only, V2-capable and malformed signature cases on both session directions.
- [ ] Preserve the current key pin and first-verdict limits.
- [ ] Demonstrate the LowID REMOTECLIENT case with stock-derived challenge bytes.
- [ ] Pass the correct available local/public address through both handlers.
- [ ] Avoid inventing an address when the platform cannot establish it.

## Dependencies And Coordination

- 195
- 196
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

---
id: RUST-BUG-176
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/278
title: Bound URL-import responses and define destination policy
status: OPEN
priority: Major
category: bug
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/278. This local document owns the durable engineering specification and evidence.

# RUST-BUG-176 - Bound URL-import responses and define destination policy

## Summary

Current fetch buffers response.bytes without a byte ceiling. Authenticated URL imports have no explicit redirect/destination policy; preserve or explicitly decide trusted LAN use rather than copying a blanket private-address ban.

User-import validation only checks text length/control characters, and fetch_url_bytes buffers the entire response. Trusted bootstrap already has HTTPS/redirect/stream-size bounds; reuse or factor the correct shared owner. SSRF destination policy needs an explicit trusted-operator contract, not an arbitrary blanket host ban.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: control-plane.

## Current Findings

confirmed-static; no runtime exploit test

Static source/spec review; no validation executed.

- `repos/emulebb-rust/crates/emulebb-core/src/ed2k_net_drivers.rs:67`
- `repos/emulebb-rust/crates/emulebb-core/src/views.rs:588`
- `repos/emulebb-rust/crates/emulebb-daemon/src/discovery_bootstrap.rs:177`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_rest-api.md` section 3.1
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section security-url-import

## Acceptance Criteria

- [ ] Enforce a streaming byte limit independent of declared response size, timeout and bounded redirect policy.
- [ ] Define explicitly whether trusted operator LAN imports remain supported; validate actual connected destinations and redirects to avoid rebinding bypass.
- [ ] Oversized, malformed and disallowed destination cases fail visibly without losing existing imported state.
- [ ] Allow only intended schemes and validate redirects.
- [ ] Enforce response/body/decompression bounds before allocation.
- [ ] Test oversized/chunked/redirect/malformed input; preserve valid imports.
- [ ] Decide private/local destination policy for explicitly authenticated operators.

## Dependencies And Coordination

- audit rest-api/network import findings
- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

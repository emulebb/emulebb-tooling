---
id: RUST-BUG-178
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/280
title: Warn before creating private diagnostic bundles
status: OPEN
priority: Major
category: bug
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/280. This local document owns the durable engineering specification and evidence.

# RUST-BUG-178 - Warn before creating private diagnostic bundles

## Summary

The existing authenticated diagnostic bundle is intentionally private and full fidelity, including the API key and exact sensitive values. The defect is that the WebUI's generic Capture bundle action immediately downloads it without visibly identifying its private contents or requiring explicit acknowledgement. Beta3 scope is warning, clear labeling and acknowledgement only.

## Release Placement

Beta 3 blocker for Windows/Linux: the private warning/acknowledgement only.

Priority: Major. Delivery lane: diagnostics.

## Current Findings

Deeper current-source revalidation confirmed an intentional unsafe/private export contract and tests requiring exact secrets; no shareable-export promise exists. The missing UI warning/acknowledgement is confirmed statically; no browser reproduction or runtime test was run during intake.

- `repos/emulebb-rust/webui/src/views.tsx:4117`
- `repos/emulebb-rust/webui/tests/unit/diagnostics-view.test.tsx:14`
- `repos/emulebb-rust/crates/emulebb-rest/src/diagnostic_bundle.rs:122`
- `repos/emulebb-rust/crates/emulebb-rest/src/tests/route_app.rs:235`
- `repos/emulebb-tooling/docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml:311`
- `repos/emulebb-tooling/docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml:3658`

The OpenAPI endpoint is explicitly unsafe and requires API-key authentication; its schema requires sensitiveValues=exact and apiKeyIncluded=true. Existing route tests assert that the API key survives. The UI instead labels the action Capture bundle and immediately starts capture/download without a private-content warning.

## Scope Constraints

- Preserve full-fidelity raw local/operator diagnostics and the authenticated private export. Do not force backend redaction, remove its secret field, or weaken existing bounds.
- Do not add a shareable-summary endpoint, general-purpose scrubber, logger rewrite, or global correlation scheme under this Beta3 item. A genuinely shareable allowlisted summary is a design proposal outside Beta3.
- A private bundle must not be labeled safe, sanitized, anonymous, or suitable for public sharing.

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_rest-api.md` section 3.4
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.1
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.2
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.3
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.4
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.5
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.6

All seven original redaction proposals are retained as design/nondefect in RUST-CI-034 after deeper contract revalidation. Their related concrete UI warning outcome keeps this existing stable ID and issue.

## Acceptance Criteria

- [ ] Before capture/download, visibly identify the bundle as private and disclose that it contains the API key, paths, content/peer identifiers, and raw logs/diagnostic payloads.
- [ ] Use an explicit private-bundle action label and require deliberate acknowledgement of the sensitive contents before calling the existing endpoint.
- [ ] Cancel or dismiss the acknowledgement without invoking the capture endpoint, creating a download, or reporting success.
- [ ] Retain the authenticated raw endpoint, exact API-key/sensitive-value contract, caller-owned persistence, byte bounds, and existing full-fidelity operator evidence tests.
- [ ] UI and documentation do not claim sanitization, anonymity, or shareability. A future allowlisted shareable summary remains a design proposal outside Beta3; no new endpoint or backend redaction is required.

## Dependencies And Coordination

- Parent reserves WebUI and diagnostic-contract file ownership before assignment.
- This UI correction does not depend on a shareable exporter or logger refactoring.

## Validation

Extend webui/tests/unit/diagnostics-view.test.tsx to exercise warning visibility, explicit acknowledgement, capture after acknowledgement, and cancellation without an endpoint call or download. Retain REST raw-bundle contract tests requiring exact secrets. Run scoped UI tests and required Windows/Linux validation through the scheduled workspace owner; inspection is not runtime proof.

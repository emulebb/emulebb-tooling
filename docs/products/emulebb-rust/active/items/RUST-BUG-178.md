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

The existing authenticated diagnostic bundle is intentionally private and full
fidelity, including the API key and exact sensitive values. On 2026-11-14 the
operator selected direct diagnostic and shutdown buttons, with no typed phrases
or confirmation dialogs. That decision supersedes this item's earlier
warning/acknowledgement proposal. Preserve the private export contract and make
the direct capture action correctly map its request and raw JSON response.

## Release Placement

The earlier warning/acknowledgement flow is no longer an approved Beta 3 blocker.
The operator-selected direct action and correct contract mapping belong to the
current Android/mobile WebUI delivery chunk under RUST-FEAT-056.

Priority: Major. Delivery lane: diagnostics.

## Current Findings

Deeper current-source revalidation confirmed an intentional unsafe/private export contract and tests requiring exact secrets; no shareable-export promise exists. The missing UI warning/acknowledgement is confirmed statically; no browser reproduction or runtime test was run during intake.

- `repos/emulebb-rust/webui/src/views.tsx:4117`
- `repos/emulebb-rust/webui/tests/unit/diagnostics-view.test.tsx:14`
- `repos/emulebb-rust/crates/emulebb-rest/src/diagnostic_bundle.rs:122`
- `repos/emulebb-rust/crates/emulebb-rest/src/tests/route_app.rs:235`
- `repos/emulebb-tooling/docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml:311`
- `repos/emulebb-tooling/docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml:3658`

The OpenAPI endpoint requires API-key authentication; its schema requires
sensitiveValues=exact and apiKeyIncluded=true. Existing route tests assert that
the API key survives. Source revalidation found two concrete mapping defects:
capture omits the required bounded `maxBytes` request field, and the generic
client unwraps `data` although this endpoint returns raw bundle JSON. Mocked
envelopes concealed both defects. Correct those mappings without changing the
backend contract or adding a confirmation flow.

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

- [ ] A direct capture button calls the authenticated endpoint without typed phrases or a confirmation dialog.
- [ ] Supply the required bounded `maxBytes` field and decode the actual raw bundle response rather than an invented envelope.
- [ ] Realistic mocked-response regressions verify the request, download and failure behavior without collecting operator data.
- [ ] Retain the authenticated raw endpoint, exact API-key/sensitive-value contract, caller-owned persistence, byte bounds, and existing full-fidelity operator evidence tests.
- [ ] UI and documentation do not claim sanitization, anonymity, or shareability. A future allowlisted shareable summary remains a design proposal outside Beta3; no new endpoint or backend redaction is required.

## Dependencies And Coordination

- Parent reserves WebUI and diagnostic-contract file ownership before assignment.
- This UI correction does not depend on a shareable exporter or logger refactoring.

## Validation

Extend webui/tests/unit/diagnostics-view.test.tsx to exercise direct capture,
source-correct request fields, raw response decoding and controlled failures.
Retain REST raw-bundle contract tests requiring exact secrets. Run scoped UI
tests and required validation through the existing workspace owner; inspection
is not runtime proof.

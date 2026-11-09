---
id: RUST-BUG-178
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/280
title: Sanitize shareable diagnostic exports
status: OPEN
priority: Major
category: bug
labels: [rust, audit]
milestone: rust-v0.1.0-beta.3
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/280. This local document owns the durable engineering specification and evidence.

# RUST-BUG-178 - Sanitize shareable diagnostic exports

## Summary

Duplicate of diagnostics-privacy 3.1-3.6; one owning export item.

One export-boundary outcome, overlapping rest-api 3.4. Raw operator logs and protocol-oracle evidence may remain full fidelity locally; basenames and truncated hashes are not sufficient anonymization.

## Release Placement

Beta 3 blocker for Windows/Linux.

Priority: Major. Delivery lane: diagnostics.

## Current Findings

confirmed-static raw-tail export

confirmed-static examples; no export reproduction

- `repos/emulebb-rust/crates/emulebb-rest/src/diagnostic_bundle.rs:769`
- `repos/emulebb-rust/crates/emulebb-core/src/ed2k_net_drivers.rs:107`
- `repos/emulebb-rust/crates/emulebb-daemon/src/logging.rs:42`
- `repos/emulebb-rust/crates/emulebb-core/src/shared_dir_monitor.rs:769`
- `repos/emulebb-rust/crates/emulebb-core/src/delivery.rs:110`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/upload_promote.rs:341`
- `repos/emulebb-rust/crates/emulebb-kad-net/src/wire_dump.rs:1`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_rest-api.md` section 3.4
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.1
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.2
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.3
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.4
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.5
- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section 3.6

## Acceptance Criteria

- [ ] Define a shareable-export contract covering structured fields and free-text messages, including content names, identifiers, endpoints, paths, secrets and packet payloads.
- [ ] Use opaque correlation tokens or omission rather than reversible truncation; keep raw operator diagnostics distinct.
- [ ] Synthetic secret/name/path/network fixtures cannot survive safe export; bounded retention and useful fault correlation remain.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

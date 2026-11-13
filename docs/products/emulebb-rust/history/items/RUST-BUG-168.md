---
id: RUST-BUG-168
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/269
title: Enforce the stock incoming secure-ident public-key size limit
status: DONE
priority: Minor
category: bug
labels: [rust, audit]
milestone: post-beta-compatibility
created: 2026-11-09
source: Operator-authorized audit reconciliation and Windows/Linux Beta 3 prioritization
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/269. This local document owns the durable engineering specification and evidence.

# RUST-BUG-168 - Enforce the stock incoming secure-ident public-key size limit

## Closure And Evidence

[PR #329](https://github.com/emulebb/emulebb-rust/pull/329) integrated the
shared incoming 80-byte limit and state-preserving regressions. The accepted
local source `b73e16e7497766b6ad5f75a19b28b03aa18d9d79` was merged as
`6429b952eac6f19ee9bf084d3a84d5649dfba0c2` with an identical tree. Local proof
belongs to the former commit; hosted actual-main proof belongs to the latter.

Windows/Linux full validation passed under
`reports/local-check/emulebb-rust/20261113T024809Z-2fadee68/results.json`.
Exact-head [CI](https://github.com/emulebb/emulebb-rust/actions/runs/43354578671),
[CodeQL](https://github.com/emulebb/emulebb-rust/actions/runs/43354578672) and
[optional-platform checks](https://github.com/emulebb/emulebb-rust/actions/runs/43354578655)
passed before merge; actual-main qualification also passed. The decoder tests
cover 79/80-byte boundaries, oversized framing, valid SPKI output, rejected
oversized restored pins and preservation of helper identity/pending signatures.
The full package/source qualification does not claim a new live cross-client
campaign or soak.

The parent accepted the [published nightly](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261113.g6429b952)
from source `6429b952`, produced by
[run 43375379055](https://github.com/emulebb/emulebb-rust/actions/runs/43375379055).
Its public-byte and cryptographic acceptance is retained at
`reports/nightly-publication-review/43375379055/final-acceptance.json`.
Issue #269 is closed; this record closes the bounded size-admission defect.

## Original Finding

The inbound decoder verifies its byte prefix but does not apply the existing 80-byte stock cap before RSA parsing. The outbound key cap does not cover this path.

## Release Placement

Parallel follow-up; this item does not block Beta 3.

Priority: Minor. Delivery lane: protocol-hardening.

## Original Source Inspection

The original audit was source inspection, without test, build or live evidence.
The delivery evidence above supersedes that validation status.

- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:253`
- `repos/emulebb-rust/crates/emulebb-ed2k/src/ed2k_tcp/identity.rs:309`

## Audit Provenance

- `emulebb-rust-prompt_audit_findings_secure-ident.md` section 4.1

## Acceptance Criteria

- [x] Reject incoming keys above stock MAXPUBKEYSIZE before parsing.
- [x] Cover valid boundary and oversized key payloads on inbound/outbound handlers.
- [x] Preserve normal stock SPKI key exchange.

## Dependencies And Coordination

- Parent reserves shared contracts and file ownership before assignment.
- Use one managed workstream per independently reviewable outcome; required local checks stay serialized.

## Validation

Add a meaningful regression for the affected behavior. Run scoped required checks and Linux/Windows validation appropriate to the change. Record exact source revisions and evidence; do not claim audit inspection as runtime proof.

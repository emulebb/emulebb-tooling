---
id: RUST-CI-005
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/30
title: Prove negotiated offerfiles capability interoperability
status: OPEN
priority: Major
category: ci
labels: [rust, ed2k, server, protocol, policy, evidence]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review and headless large-library roadmap review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/30. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-005 - Prove negotiated offerfiles capability interoperability

## Summary

Complete the deterministic and cross-client interoperability evidence for the
approved negotiated `offerfiles_v=1` extension. The policy disposition is
closed by `RUST-REF-015` and Rust commit `afb56cb1`; this item now owns only the
proof that the default-on extension remains bounded, connection-scoped, and
stock-compatible when negotiation is absent or rejected.

This evidence is part of the hard Client gate. Policy approval alone is not
enough to close the item or begin Indexer production implementation.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server/offer_policy.rs` defines and validates the
  negotiated capability and its custom fields with fail-closed behavior.
- `crates/emulebb-settings/src/lib.rs` enables the capability by default.
- `policy/rust-client-extensions.toml`, `RELEASE-SCOPE.md`, and closed
  `RUST-REF-015` record the approved default-on policy exception and downgrade
  contract.
- Exact parser and session fixtures cover accepted, absent, unsupported,
  malformed, duplicate, timeout, and first-snapshot-lock behavior.
- A deterministic two-connection server fixture proves that timeout closes the
  advertised connection without sending `OP_OFFERFILES`, reconnects once
  without `offerfiles_v`, and only then publishes a stock-shaped legacy batch.
- The 2026-10-19 latest-source review confirmed that `ST_SOFTFILES` is a
  distinct-hash budget, while every same-hash refresh still consumes packet and
  pacing capacity. RUST-BUG-128 owns the shared publication-state correction.
- A timeout or malformed capability response must not make the client send a
  legacy-sized packet on a connection the server may already have bound to v1.
  Downgrade proof therefore includes a fresh unadvertised connection epoch.
- `docs/WORKSPACE-POLICY.md` requires stock protocol compatibility and explicit
  governance for extensions/default drift.
- The 100,000-file selector fixture proves bounded construction and exact-once
  catalog coverage, but the retained pacing, cancellation, and memory campaign
  is still outstanding.
- The completed implementation does not itself establish stock/current-aMule
  interoperability; those live witnesses remain required.

## Why This Matters

Default-on proprietary behavior can fragment interoperability, create a de
facto private dialect, and make stock compatibility claims conditional in ways
operators cannot see. The approved extension therefore remains incomplete
without explicit downgrade, stock/current-aMule, and large-library evidence.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server\offer_policy.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-settings\src\lib.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`

## Intended Shape

- Retain the approved default-on policy and its machine-readable registry entry;
  changing that decision requires a new tracked product-scope disposition.
- In every retained form, require explicit negotiation, exact field validation,
  per-connection reset, and stock packet behavior when negotiation is absent or
  rejected.
- Treat an explicit first identity without the extension as a definitive legacy
  selection. Treat timeout or malformed negotiation as connection-ambiguous:
  reconnect once without the extension before publishing legacy offers.
- Add a deterministic server fixture that can accept, reject, malformed-reply,
  duplicate, and reconnect the extension negotiation.
- Exercise the 100,000-file model without putting custom fields on a stock peer
  path or weakening server load/pacing bounds.

## Scope Constraints

- No silent capability inference, optimistic send, or sticky state across a new
  server connection.
- A stock eMule/current-aMule server path must remain byte-for-byte within the
  standard protocol surface.
- An approved exception must name owners, default, downgrade behavior, evidence,
  and the condition under which it will be removed or standardized.
- Do not treat successful Rust-to-Rust negotiation as stock interoperability.
- Do not weaken, defer, or exempt the evidence criteria merely because the
  extension already has a policy disposition or is enabled by default.

## Acceptance Criteria

- [x] The extension has an explicit recorded disposition consistent with
      workspace protocol policy.
- [x] Default settings, user-facing configuration, and compatibility claims
      match that disposition.
- [x] Exact fixtures cover acceptance, rejection, unsupported peer, malformed
      fields, duplicate fields, reconnect reset, and downgrade behavior.
- [ ] Stock eMule and current aMule interop witnesses show standard behavior and
      no custom field leakage.
- [ ] A 100,000-file deterministic fixture proves bounded offer construction,
      memory, pacing, reconnect, and cancellation behavior.
- [x] Diagnostics identify whether the standard or negotiated path was selected
      without logging private library contents.

## Implementation Evidence (2026-10-19)

- Rust commit `40fbb3e1` makes timeout and invalid negotiation connection-safe:
  an ambiguous advertised connection cannot publish a legacy batch.
- Rust commit `1ba8bff9` adds the deterministic two-connection timeout witness,
  including v1 tag presence on the first login and absence on the fallback.
- Rust commit `5ec5f4d1` preserves the automatic fallback reason and publication
  counters in live diagnostics on the replacement connection.
- Rust commit `1c808365` records the exact same-connection versus fresh-
  connection downgrade contract in the machine-readable extension registry.
- Canonical `emulebb-ed2k` validation passes: 1,166 unit tests, documentation
  tests, strict Clippy with the repository's known lint-expectation allowance,
  formatting, and whitespace checks.
- Remaining gate evidence is limited to stock eMule/current-aMule live
  interoperability and the retained full 100,000-file pacing, cancellation,
  reconnect, and memory campaign.

## Validation

- Offer-policy unit/property tests for all five fields, bounds, duplication,
  ordering, malformed values, and reset semantics.
- Deterministic server-fixture matrix for negotiated and non-negotiated paths.
- Stock eMule/current-aMule local interop plus the retained large-library
  evidence campaign.
- Backlog/policy documentation check confirming the approved decision is
  reflected in the release scope.

## Notes

Policy disposition is complete. Fail-closed parsing remains an implementation
property, not a substitute for the outstanding interoperability evidence.

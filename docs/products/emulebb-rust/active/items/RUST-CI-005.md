---
id: RUST-CI-005
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/30
title: Disposition and prove the negotiated offerfiles capability
status: OPEN
priority: Major
category: ci
labels: [rust, ed2k, server, protocol, policy, evidence]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review and headless large-library roadmap review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/30. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-005 - Disposition and prove the negotiated offerfiles capability

## Summary

Make an explicit policy decision for Rust's negotiated `offerfiles_v=1`
capability and produce the deterministic interoperability evidence required by
that decision. It is a non-stock ED2K server extension with five custom fields,
currently enabled by default, while workspace policy prohibits proprietary
protocol extensions or default drift without an explicit exception.

## Current State

- `crates/emulebb-ed2k/src/ed2k_server/offer_policy.rs` defines and validates the
  negotiated capability and its custom fields with fail-closed behavior.
- `crates/emulebb-settings/src/lib.rs` enables the capability by default.
- The headless/large-library roadmap describes a 100,000-file deterministic
  model and calls out the missing deterministic server fixture.
- `docs/WORKSPACE-POLICY.md` requires stock protocol compatibility and explicit
  governance for extensions/default drift.
- The negotiation and validation are safer than silent packet drift, but they
  do not themselves establish stock/current-aMule interoperability or authorize
  a default-on extension.

## Why This Matters

Default-on proprietary behavior can fragment interoperability, create a de
facto private dialect, and make stock compatibility claims conditional in ways
operators cannot see. Conversely, removing a useful capability without testing
would discard existing work. This item requires a recorded disposition and
evidence for whichever path is chosen.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_server\offer_policy.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-settings\src\lib.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\active\RUST-HEADLESS-LARGE-LIBRARY-NOW-ROADMAP.md`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\WORKSPACE-POLICY.md`

## Intended Shape

- Choose and record one disposition: remove the extension, ship it default-off,
  or approve a narrowly scoped policy exception with compatibility rationale.
- In every retained form, require explicit negotiation, exact field validation,
  per-connection reset, and stock packet behavior when negotiation is absent or
  rejected.
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

## Acceptance Criteria

- [ ] The extension has an explicit recorded disposition consistent with
      workspace protocol policy.
- [ ] Default settings, user-facing configuration, and compatibility claims
      match that disposition.
- [ ] Exact fixtures cover acceptance, rejection, unsupported peer, malformed
      fields, duplicate fields, reconnect reset, and downgrade behavior.
- [ ] Stock eMule and current aMule interop witnesses show standard behavior and
      no custom field leakage.
- [ ] A 100,000-file deterministic fixture proves bounded offer construction,
      memory, pacing, reconnect, and cancellation behavior.
- [ ] Diagnostics identify whether the standard or negotiated path was selected
      without logging private library contents.

## Validation

- Offer-policy unit/property tests for all five fields, bounds, duplication,
  ordering, malformed values, and reset semantics.
- Deterministic server-fixture matrix for negotiated and non-negotiated paths.
- Stock eMule/current-aMule local interop plus the retained large-library
  evidence campaign.
- Backlog/policy documentation check confirming the approved decision is
  reflected in the release scope.

## Notes

Fail-closed parsing is a useful implementation property, but it does not settle
whether a proprietary capability should be enabled by default.

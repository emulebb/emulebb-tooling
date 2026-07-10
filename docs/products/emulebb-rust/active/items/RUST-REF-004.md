---
id: RUST-REF-004
workflow: local
title: Re-audit every non-SX1 Rust divergence under stock eMule parity policy
status: OPEN
priority: Critical
category: refactor
labels: [parity, omissions, release, protocol]
milestone: release-0.1.0-beta.1
created: 2026-07-08
source: Operator product-direction decision 2026-07-08
---

# RUST-REF-004 - Re-audit every non-SX1 Rust divergence

## Summary

Re-audit every registered `emulebb-rust` divergence except
`sx1-live-source-exchange`. The product target is stock eMule protocol and
behavior parity by default; SX1 is the only pre-approved permanent drop.

## Why This Matters

The old release scope treated many non-SX1 differences as permanent omissions.
That no longer matches product direction. Rust Console Beta may ship with a
signed-off non-critical parity backlog, but it must not ship with ambiguous
divergence policy.

## Disposition Rule

Each non-SX1 registry entry gets exactly one disposition:

- **Fix** - beta blocker or scheduled parity work.
- **Defer** - accepted beta backlog with release placement and rationale.
- **Permanent drop requested** - requires explicit operator approval before it
  can become a permanent omission.

## Acceptance Criteria

- [ ] Every non-SX1 entry in `policy/rust-client-omissions.toml` has a recorded
      disposition.
- [ ] P0 safety and stock-wire-critical findings are either fixed or block the
      beta.
- [ ] Beta-allowed findings have backlog owners and are listed as deferred work
      in the release scope.
- [ ] `policy/rust-client.toml` review reporting excludes only the explicitly
      approved permanent drops.
- [ ] The final release notes summarize remaining beta backlog without implying
      full stock parity where backlog remains.

## Validation

- `python tools\check_rust_client_policy.py`
- `python tools\rust_quality_gate.py quick`
- Rust OpenAPI conformance gate once `RUST-CI-003` lands.

## 2026-07-10 Progress

The protocol/state-machine audit closed the unregistered Kad FINDSOURCE gap
(`RUST-FEAT-035`) and converted three registered deferrals to implemented fixes:
connection-spike suppression (`RUST-PAR-026`), safe server connection cycling
(`RUST-PAR-027`), and UDP server-description polling (`RUST-PAR-028`). The
remaining acceptance criteria stay open for the release-scope and release-notes
reconciliation.

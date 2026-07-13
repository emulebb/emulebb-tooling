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
`sx1-live-source-exchange`. The product target is eD2K/Kad
protocol-operational parity: wire behavior, advertised capabilities, state
machines, persistence needed for network correctness, and safety properties
required to operate cleanly with stock-compatible peers, servers, and Kad nodes.
Rust is not an MFC, stock GUI, legacy WebServer, or legacy preference mirror.
Non-protocol surfaces must be judged as Rust-native async daemon/API/UI design,
not as legacy parity obligations.

## Why This Matters

The old release scope treated many non-SX1 differences as permanent omissions
from a legacy comparison. That no longer matches product direction. Rust Console
Beta may ship with a signed-off non-critical protocol backlog, but it must not
ship with ambiguous divergence policy or no-op legacy REST/preference surface.

## Disposition Rule

Each non-SX1 registry entry gets exactly one disposition:

- **Fix protocol** - beta blocker or scheduled work needed for eD2K/Kad
  protocol-operational parity.
- **Defer protocol** - accepted protocol backlog with release placement and
  rationale; must not break advertised capability or network correctness.
- **Rust-native replace/remove** - non-protocol legacy GUI/controller/preference
  residue that should be removed, renamed, or replaced by a clean Rust async
  daemon/API/UI surface. Do not keep inert compatibility aliases.
- **Permanent protocol drop requested** - requires explicit operator approval
  before a real protocol-operational divergence can become a permanent omission.

## Acceptance Criteria

- [ ] Every non-SX1 entry in `policy/rust-client-omissions.toml` has a recorded
      disposition.
- [ ] P0 safety and eD2K/Kad protocol-operational findings are either fixed or
      block the beta.
- [ ] Beta-allowed findings have backlog owners and are listed as deferred work
      in the release scope.
- [ ] `policy/rust-client.toml` review reporting excludes only the explicitly
      approved permanent drops.
- [ ] Non-protocol legacy REST/preference/API residues are removed or replaced
      with Rust-native names and behavior before beta, unless explicitly retained
      as real product features.
- [ ] The final release notes summarize remaining beta backlog without implying
      full protocol parity where protocol backlog remains.

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

## 2026-07-13 Progress

The active registry was narrowed to current beta decisions only. Implemented or
removed entries moved to `policy/rust-client-omissions-history.toml`, while
`policy/rust-client-omissions.toml` now carries only active protocol defers and
approved protocol drops. `ed2k-preview` was promoted from contradictory defer
text to an approved permanent drop: Rust does not advertise peer preview support
and will not add an untrusted media-decoding surface for beta. The policy checker
now fails active `fixed` entries, active/history ID overlap, and contradictory
machine vs review dispositions.

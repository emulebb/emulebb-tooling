# eMule BB Release Test Strategy

This document records the eMule BB-owned release test model. It is generic
release strategy, not a `0.7.3`-only checklist.

## Decision Log

- eMule BB owns the release campaign model from now on. p2p-overlord inspired
  stable scenario ids, campaign manifests, and evidence matrices, but the eMule
  BB model is intentionally independent and may evolve differently.
- Release tests are organized as campaigns, strict phases, and feature-flow
  scenarios. Current suites and commands are evidence providers for those
  flows, not the taxonomy itself.
- V1 is report-only. It makes the release matrix visible, reads latest known
  evidence when safe, and warns on gaps. Test execution remains with the
  existing supported `python -m emule_workspace` commands.
- Missing evidence is warn-only in V1 because historical reports, local
  live-wire inputs, Arr roots, and package artifacts are operator/environment
  dependent. Future releases may add strict audit mode once the matrix has
  proven stable.
- ARM64 is a release build/package proof, not a live execution proof. Shared
  test execution remains x64-only under current workspace policy.

## Enterprise Practice Inputs

The model follows a layered confidence strategy:

- Google SRE distinguishes unit, integration, system, production/live, and
  stress tests, and emphasizes that live or non-hermetic tests must be treated
  as operational evidence rather than simple unit-style proof:
  <https://sre.google/sre-book/testing-reliability/>.
- Google SRE release engineering emphasizes repeatable release processes,
  hermetic builds where possible, and controlled release evidence:
  <https://sre.google/sre-book/release-engineering/>.
- Google SRE canary guidance supports staged confidence and explicit rollback
  readiness. eMule BB does not canary a service, but the campaign phases serve
  the same purpose for desktop release confidence:
  <https://sre.google/workbook/canarying-releases/>.
- Microsoft guidance favors fast, reliable tests earlier in the pipeline and
  larger integration/system checks later:
  <https://learn.microsoft.com/en-us/devops/develop/shift-left-make-testing-fast-reliable>.
- ISTQB test-level terminology reinforces separating component, integration,
  system, system-integration, and acceptance responsibilities:
  <https://astqb.org/2-2-test-levels-and-test-types/>.

## Strict Phase Taxonomy

All release campaign instances use these phase ids:

| Phase | Purpose |
|---|---|
| `preflight` | Workspace policy, fast validation, buildability, and unit harness confidence. |
| `protocol-parity` | Kad/eD2K compatibility, community comparison, protocol goldens, and live-diff signal. |
| `controller-surface` | REST, qBittorrent-compatible controller behavior, aMuTorrent, and Arr integration. |
| `live-wire-release` | Operator-owned real-network search, transfer, UI, and weak-path release proof. |
| `ui-resource-depth` | Full stock language/resource smoke and release-facing UI depth. |
| `stabilization-stress` | Optional crash, leak, dump, CPU, and concurrency add-on evidence. |
| `packaging-provenance` | x64/ARM64 packages, manifests, hashes, and clean source provenance. |

## Future Direction

The next step after V1 reporting is a strict audit mode that fails on missing
required evidence. A later step can add explicit phase execution, but only once
live-wire input handling, Arr roots, package generation, and long-running
certification semantics are represented without hidden defaults or legacy
compatibility assumptions.

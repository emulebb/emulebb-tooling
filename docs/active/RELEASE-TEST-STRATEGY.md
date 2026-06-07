# eMuleBB Release Test Strategy

This document records the eMuleBB-owned release test model. It is generic
release strategy, not a `0.7.3`-only checklist.

## Decision Log

- eMuleBB owns the release campaign model from now on. p2p-overlord inspired
  stable scenario ids, campaign manifests, and evidence matrices, but the eMule
  BB model is intentionally independent and may evolve differently.
- Post-`0.7.3` p2p-overlord product-family campaigns should reuse common
  scenario ids and evidence structures where they help compare products, while
  keeping Rust agent and backend validation product-specific.
- Release tests are organized as campaigns, strict phases, and feature-flow
  scenarios. Current suites and commands are evidence providers for those
  flows, not the taxonomy itself.
- Campaign manifests use the `emulebb-build-tests.release-campaign.v1`
  namespace, strict phase ids, required proof tiers, stable scenario ids, and
  explicit release-gate mappings.
- V1 supports both reporting and execution through
  `python -m emule_workspace test release-campaign`. It makes the release
  matrix visible, reads latest known evidence when safe, and warns on gaps.
- RC1 is frozen historical evidence. Active campaign modules, command shapes,
  schema details, and tests may evolve for RC2+ without preserving RC1
  compatibility. Any further bugfix or improvement targets RC2+.
- RC2+ release-relevant local/live scenarios should start from the packaged
  PowerShell suite installer by default. This makes package layout, suite
  profile materialization, packaged scripts, manifests, and adjacent PDB
  placement part of normal release validation.
- Local host and Windows VM tests should stay mostly paritetic by sharing
  scenario ids, profile catalogs, release versions, fixture controls, and
  local-swarm modes. VM execution is confidence proof by default and becomes
  blocking only when a package, installer, or guest-only delta invalidates the
  clean guest evidence.
- Missing evidence is warn-only in V1 because historical reports, local
  live-wire inputs, Arr roots, and package artifacts are operator/environment
  dependent. Future releases may add strict audit mode once the matrix has
  proven stable.
- ARM64 is a release build/package proof, not a live execution proof. Shared
  test execution remains x64-only under current workspace policy.
- Archive preview/recovery, IRC and IRC-adjacent chat UI, the legacy Scheduler,
  legacy WebServer HTML templates, and proxy support are frozen surfaces. They
  receive no release-gated support and no new test coverage; see
  [FROZEN-SURFACES](FROZEN-SURFACES.md).

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
  readiness. eMuleBB does not canary a service, but the campaign phases serve
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

### `preflight`

Workspace policy, fast validation, buildability, and unit harness confidence.

### `protocol-parity`

Kad/eD2K compatibility, community comparison, protocol goldens, and live-diff
signal.

### `controller-surface`

REST, qBittorrent-compatible controller behavior, aMuTorrent, and Arr
integration.

### `live-wire-release`

Operator-owned real-network search, transfer, UI, and weak-path release proof.
Public VPN lanes in this phase must separate P2P and non-P2P network policy:
public P2P binds through the configured VPN interface and runs with VPN Guard
enabled, while split-tunnel control/probe surfaces use the operator-provided
LAN bind address when the machine requires it. Local-only eD2K/Kad lanes remain
LAN scoped and do not require VPN Guard.

### `ui-resource-depth`

Full stock language/resource smoke and release-facing UI depth.

### `stabilization-stress`

Bounded RC stress evidence plus optional/full overnight CPU, memory,
real-profile, crash, leak, dump, and concurrency soak.

### `packaging-provenance`

x64/ARM64 packages, manifests, hashes, and clean source provenance.

## Frozen Surface Exclusion

Release campaigns must not add scenarios, live automation, native seams, or
manual evidence rows for frozen surfaces. They may validate only that supported
surfaces still work when frozen code happens to share infrastructure, such as
REST over the WebServer listener. Legacy HTML template behavior, IRC,
scheduler, archive preview/recovery, and proxy behavior are not acceptance
criteria.

## Future Direction

The next step after V1 reporting/execution is a strict audit mode that fails on
missing required evidence once live-wire input handling, Arr roots, package
generation, and long-running certification semantics have enough successful
operator runs to make missing evidence actionable instead of environmental.

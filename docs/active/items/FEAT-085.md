---
id: FEAT-085
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/32
title: Establish a shared campaign core for eMuleBB product-family test orchestration
status: OPEN
priority: Minor
category: feature
labels: [product-family, p2p-overlord, test-campaigns, orchestration, evidence]
milestone: post-0.7.3
created: 2026-05-24
source: operator request to bring p2p-overlord campaigns into one eMuleBB workspace with a uniform common module
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/32. This local document is retained as an engineering spec/evidence record.

# FEAT-085 - Establish A Shared Campaign Core For eMuleBB Product-Family Test Orchestration

## Summary

Create a small shared campaign/runtime core that lets the eMuleBB workspace run
eMuleBB, aMuTorrent, and p2p-overlord test campaigns through one uniform
structure while preserving product-specific runner logic.

The goal is one workspace-level campaign model, one artifact/reporting model,
and one process-cleanup/lifecycle contract. The goal is not to merge the
desktop app, Rust agent, aMuTorrent, or their native harnesses into one
monolithic test suite.

This item refines the product-family testing portion of
[FEAT-073](FEAT-073.md). `FEAT-073` owns the broad product-family boundary;
this item owns the concrete common-module and campaign-runner architecture.

## Current Evidence

- eMuleBB already owns release campaign manifests under
  `repos/emulebb-build-tests/manifests/release-campaigns`.
- eMuleBB release campaign execution currently dispatches supported
  `python -m emule_workspace ...` shell-shaped command strings.
- `p2p-overlord-tooling` has a mature scenario catalog and native pytest E2E
  runners:
  - versioned `scenarios/*/manifest.v1.json` contracts
  - ED2K and KAD2 private and realnet campaign manifests
  - native pytest runner registration through command IDs
  - live-wire seed, VPN/interface, runtime, and artifact helper code
- The eMuleBB workspace already materializes `p2p-overlord-agents` and
  `p2p-overlord-be` through `workspaces/workspace/deps.json`.
- The old `p2p-overlord-tooling` checkout is still external to the eMuleBB
  workspace, so the current shape does not yet provide a single managed
  workspace for both the desktop app and Rust agent campaign proof.

## Intended Architecture

Introduce a shared campaign core in `repos/emulebb-build-tests`, for example:

```text
emule_test_harness/
  campaign_core/
    artifacts.py
    catalog.py
    commands.py
    evidence.py
    live_inputs.py
    process_lifecycle.py
    run_context.py
    run_summary.py
    schemas.py
    workspace.py
  products/
    emulebb.py
    amutorrent.py
    p2p_overlord.py
```

The exact module names may change during implementation, but the ownership
split should remain:

- common core owns structure, contracts, evidence, lifecycle, and reporting
- product adapters own product-specific behavior
- p2p-overlord keeps its scenario catalog and native pytest/Rust-agent runners
  until there is a concrete reason to extract or replace them

## Common Core Responsibilities

The common module should own:

- workspace and `deps.json` path resolution
- campaign manifest loading and validation
- typed command records instead of ad hoc shell command strings
- stable run IDs and artifact directory layout
- JSON run summaries with status, timing, command, product, and evidence links
- latest-artifact pointers for report readers
- evidence readers for JSON status, required files, globs, and manual evidence
- operator-owned live input loading without committing local paths or search
  terms
- process lifecycle policy, including pre-run cleanup hooks and post-run stop
  behavior
- timeout, fail-fast, continue-on-failure, dry-run, and include-nonblocking
  behavior
- canonical environment construction for child product runners
- report rendering for operator-readable and machine-readable campaign output

## Product Adapter Responsibilities

### eMuleBB Adapter

The eMuleBB adapter should expose existing workspace-owned behavior through the
common core:

- `validate`
- native test suites
- protocol parity
- certification profiles
- live E2E profiles and suites
- packaging and provenance commands

The implementation should preserve the existing `python -m emule_workspace`
operator entrypoint.

### aMuTorrent Adapter

The aMuTorrent adapter should wrap existing controller and browser flows:

- clean startup
- eMuleBB UI/browser smoke
- resilience and restart behavior
- REST scheme selection for HTTP and HTTPS
- live-wire input and artifact propagation

### p2p-overlord Adapter

The p2p-overlord adapter should bridge into the existing p2p-overlord campaign
catalog instead of copying tests:

- resolve `p2p-overlord-tooling` from the eMuleBB workspace
- execute one p2p scenario or campaign by stable `scenarioId`
- run pytest markers only through supported adapter commands
- pass `EMULE_WORKSPACE_ROOT` and product-family repo paths explicitly
- map p2p-overlord run summaries into eMuleBB campaign evidence
- keep deterministic private tests separate from realnet confidence tests
- route Rust build checks through `cargo fmt`, `cargo clippy`, and focused
  `cargo test` commands under the agent repo

## Manifest Direction

Future campaign manifests should move away from raw shell-shaped command
strings for product-family work. A scenario should be able to declare a typed
command such as:

```json
{
  "id": "emulebb.flow.p2p-overlord.ed2k.private.v1",
  "product": "p2p-overlord",
  "command": {
    "type": "scenario",
    "scenarioId": "ed2k.campaign.queue-and-slot.v1"
  },
  "evidence": []
}
```

The p2p-overlord `scenarios/*/manifest.v1.json` files remain the Rust-agent
scenario catalog. eMuleBB release/product-family campaigns reference those
scenario IDs instead of duplicating their manifest content.

## Campaign Shape

The common core should support at least these product-family campaign classes:

- quick private smoke:
  deterministic private p2p-overlord cells, Rust build sanity, and no realnet
  prerequisites
- product-family private:
  full deterministic private ED2K/KAD2 p2p-overlord campaign coverage
- product-family overnight:
  realnet confidence, live-wire search/download, and longer resource evidence
- REST subset conformance:
  p2p-overlord claimed `/api/v1` subset checked against the canonical eMuleBB
  OpenAPI contract
- release-adjacent report-only:
  nonblocking product-family evidence visible beside eMuleBB release campaign
  status without entering the desktop RC gate

## Scope Constraints

- Do not copy the whole p2p-overlord pytest harness into
  `emulebb-build-tests`.
- Do not make p2p-overlord test failures block eMuleBB desktop RC packaging
  until the operator explicitly promotes that gate.
- Do not move p2p-overlord runtime logic into the eMuleBB desktop app.
- Do not redefine the eMuleBB REST OpenAPI contract from p2p-overlord.
- Do not persist operator-local live profile paths, VPN interface data, server
  seeds, search terms, or profile roots in tracked source.
- Do not introduce protocol drift or proprietary eD2K/Kad extensions as part of
  the common test architecture.
- Do not make the common core own product-specific behavior that belongs in a
  product adapter.

## Implementation Plan

1. Add `p2p-overlord-tooling` to the managed workspace topology, or otherwise
   define a supported resolver for the external tooling repo while the repo is
   moved under the eMuleBB organization.
2. Add the first `campaign_core` package in `repos/emulebb-build-tests`.
3. Move current release-campaign data structures behind the common core without
   changing operator-visible behavior.
4. Convert eMuleBB release-campaign execution to call an `emulebb` product
   adapter.
5. Add a `p2p_overlord` adapter that invokes the existing p2p-overlord
   scenario registry by `scenarioId`.
6. Normalize p2p-overlord artifacts into the eMuleBB workspace state/report
   tree.
7. Add product-family campaign manifests that reference p2p-overlord scenario
   IDs by name.
8. Add local unit tests for manifest validation, command dispatch, artifact
   mapping, and adapter environment construction.
9. Add one quick deterministic private p2p-overlord smoke command, then expand
   to full private and overnight campaigns once stable.

## Acceptance Criteria

- [ ] A shared `campaign_core` module exists under `repos/emulebb-build-tests`.
- [ ] Existing eMuleBB release-campaign reporting and execution continue to
      work through `python -m emule_workspace test release-campaign`.
- [ ] Product adapters exist for eMuleBB and p2p-overlord, with a clear seam
      for aMuTorrent.
- [ ] p2p-overlord scenarios can be referenced by stable `scenarioId` from an
      eMuleBB-owned campaign manifest.
- [ ] p2p-overlord deterministic private smoke can run from the eMuleBB
      workspace entrypoint without ad hoc absolute paths.
- [ ] p2p-overlord run evidence is normalized into the eMuleBB campaign report
      model.
- [ ] Realnet p2p-overlord scenarios remain opt-in and nonblocking until
      explicitly promoted.
- [ ] Documentation explains the common-core/product-adapter split and the rule
      against copying product harnesses into multiple repos.

## Validation

- `python -m pytest tests/python -q` from `repos/emulebb-build-tests`.
- `python -m emule_workspace test release-campaign --campaign emulebb-0.7.3`
  from `repos/emulebb-build`.
- `python -m emule_workspace test release-campaign --campaign p2p-overlord-post-0.7.3`
  from `repos/emulebb-build`.
- Focused p2p-overlord private smoke through the new adapter once implemented.
- `python scripts/docs-item-taxonomy-check.py` and
  `python scripts/docs-structure-check.py --fail-on-wide-tables` from
  `repos/emulebb-tooling`.

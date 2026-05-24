---
id: FEAT-073
title: Incorporate p2p-overlord into the eMuleBB product family
status: OPEN
priority: Minor
category: feature
labels: [product-family, p2p-overlord, rest, testing, upnp, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-23
source: operator product-family planning for p2p-overlord integration
---

# FEAT-073 - Incorporate p2p-overlord Into The eMuleBB Product Family

## Summary

Bring the relevant p2p-overlord repositories into the eMuleBB product-family
workspace as first-class future integration targets for the post-`0.7.3`
release line.
p2p-overlord remains its own Rust/Node product, similar to how eMuleBB and
aMule remain distinct clients, but it should share contracts, campaign
patterns, and selected dependencies where that reduces drift.

The active ED2K server for eMuleBB remains
`https://github.com/emulebb/goed2k-server`. The obsolete `emulebb-ed2k-server`
fork slug has no current public repository, is not part of this future
integration, and should remain decommissioned.

## Intended Shape

- Track `https://github.com/emulebb/p2p-overlord-agents` and
  `https://github.com/emulebb/p2p-overlord-be` as first-class product-family
  repos.
- Keep `p2p-overlord-tooling` outside the managed topology until the deferred
  shared campaign-core decision is made.
- Keep p2p-overlord's ED2K server lineage out of the active eMuleBB topology;
  use `goed2k-server` as the shared ED2K server fork.
- Treat `docs/rest/REST-API-OPENAPI.yaml` as the shared REST API authority for
  every implementation that claims the eMuleBB-compatible `/api/v1` surface.
- Use `repos/emulebb-build-tests` as the common base for cross-product release
  campaigns, with product-specific variants rather than copied harnesses.
- Converge MiniUPnP source ownership on `repos/third_party/emulebb-miniupnp`,
  while preserving p2p-overlord's Rust build boundaries.

## Scope Constraints

- Do not merge p2p-overlord into the eMuleBB desktop app.
- Do not promote server-only, daemon-only, or headless product scope into the
  eMuleBB `0.7.3` release line.
- Do not broaden eMuleBB wire behavior or introduce proprietary eD2K/Kad
  protocol extensions.
- Do not replace `goed2k-server` with the obsolete
  `emulebb-ed2k-server` fork.
- Do not make p2p-overlord conformance redefine the canonical REST contract;
  OpenAPI remains the authority.

## Acceptance Criteria

- [x] active docs describe the product-family boundary and p2p-overlord's role
- [x] workspace topology exposes `p2p-overlord-agents` and `p2p-overlord-be`
      without materializing obsolete ED2K server repos
- [x] stale `emulebb-ed2k-server` references/remotes are removed or marked
      superseded
- [x] shared test-campaign docs identify p2p-overlord variants and REST
      conformance expectations
- [x] REST docs state how a p2p-overlord implementation proves a claimed
      subset against the canonical OpenAPI contract
- [x] MiniUPnP convergence docs point both products at the shared
      `emulebb-miniupnp` fork

## Validation

- Docs-only slices should pass `git diff --check`.
- Topology slices should pass `python -m emule_workspace validate` from
  `repos/emulebb-build`.
- Test-harness slices should pass the relevant `repos/emulebb-build-tests`
  Python unit tests.
- Future p2p-overlord code slices should pass `cargo fmt --all --check`,
  p2p-overlord's clippy policy, and backend `npm run quality`.

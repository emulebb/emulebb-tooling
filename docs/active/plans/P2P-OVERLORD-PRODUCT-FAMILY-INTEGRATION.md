# p2p-overlord Product-Family Integration Plan

This is the post-`0.7.3` architecture plan for bringing relevant
p2p-overlord work into the eMuleBB product family without merging the products.
The tracking item is [FEAT-073](../items/FEAT-073.md).
The shared campaign-core architecture slice is tracked separately as
[FEAT-085](../items/FEAT-085.md).

## Product Boundary

The product family contains these related but separate products and repos:

| Surface | Role |
|---|---|
| eMuleBB | Full Windows desktop product for eMule broadband edition. |
| aMuTorrent | Web/controller product for eMuleBB and aMule-style clients. |
| eMuleBB aMule fork/builds | Cross-platform eMule-compatible client builds owned under the eMuleBB family. |
| goed2k-server | Active ED2K server fork at `https://github.com/emulebb/goed2k-server`. |
| p2p-overlord | Separate Rust/Node product for headless/server-oriented metadata and network agents under the eMuleBB org. |

p2p-overlord is a peer product, not an eMuleBB desktop-app subsystem.
Integration means shared contracts, shared release-campaign patterns, shared
dependency ownership where sensible, and explicit topology awareness.

## Included Repos

The first-class p2p-overlord repos for this workspace integration are:

- `https://github.com/emulebb/p2p-overlord-agents`
- `https://github.com/emulebb/p2p-overlord-be`

The following are intentionally excluded from active materialization:

- `p2p-overlord-tooling`, pending the deferred shared campaign-core topology
  decision
- p2p-overlord ED2K server lineage, because eMuleBB uses `goed2k-server`
- obsolete `emulebb-ed2k-server` fork lineage, which has no current public
  repository and should remain decommissioned

## Shared Contracts

`docs/rest/REST-API-OPENAPI.yaml` remains the canonical shared REST contract.
Any p2p-overlord agent that advertises the eMuleBB-compatible `/api/v1` surface
must prove the claimed subset against that OpenAPI source rather than defining a
parallel route or DTO contract.

The shared contract model is:

- eMuleBB owns the canonical OpenAPI document.
- aMuTorrent consumes the OpenAPI shape through its adapter.
- p2p-overlord implementations may expose the same surface or a documented
  subset, but must publish subset/conformance evidence.
- Missing p2p-overlord endpoints are implementation gaps, not OpenAPI drift.

## Test Campaign Model

`repos/emulebb-build-tests` remains the common campaign base. Product-specific
variants should reuse shared scenario ids, evidence models, and REST
conformance checks where possible:

- eMuleBB release campaigns continue to validate the desktop app, packages,
  real-profile live-wire runs, and controller flows.
- p2p-overlord campaigns should add Rust agent and backend variants for long
  runs, REST conformance, ED2K/Kad behavior, and coordinator evidence.
- Shared campaign code must keep operator-owned live data in ignored local
  files and must not commit live-wire paths, search terms, or profile roots.

The preferred implementation shape is a small common campaign/runtime core
owned by `repos/emulebb-build-tests`, plus thin product adapters for eMuleBB,
aMuTorrent, and p2p-overlord. The common core owns workspace resolution,
artifact naming, evidence loading, run summaries, process lifecycle policy, and
typed campaign command dispatch. Product adapters own product-specific behavior
such as eMuleBB live E2E profiles, aMuTorrent controller flows, and
p2p-overlord scenario execution by stable `scenarioId`.

Do not copy the p2p-overlord pytest harness into `emulebb-build-tests`. The
eMuleBB campaign layer should reference p2p-overlord scenario manifests by ID
and normalize their evidence into the eMuleBB artifact/report model.

## Dependency Convergence

MiniUPnP source ownership should converge on
`repos/third_party/emulebb-miniupnp`. p2p-overlord may keep Rust crates and build
wrappers, but the C MiniUPnP source tree should resolve from the shared
eMuleBB fork when the convergence slice is implemented.

This does not promote a NAT behavior change by itself. It only removes duplicate
source ownership and makes future UPnP/NAT-PMP evidence easier to compare.

## Implementation Order

1. Done: document this product-family boundary and active backlog item.
2. Done: remove stale `emulebb-ed2k-server` remotes and local topology
   references, or mark historical references as provenance only.
3. Done: move `p2p-overlord-agents` and `p2p-overlord-be` under the `emulebb`
   org.
4. Done: add topology entries for `p2p-overlord-agents` and `p2p-overlord-be`.
5. Done: add product-family validation hooks for `goed2k-server` and
   p2p-overlord repos.
6. Deferred: decide whether `p2p-overlord-tooling` joins this topology or stays
   standalone.
7. Deferred: add a shared campaign-core implementation.
8. Future: add p2p-overlord claimed-subset REST conformance checks.
9. Future: move p2p-overlord MiniUPnP source resolution to the shared fork.

Each slice should be committed and pushed independently.

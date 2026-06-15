# /api/v1 Contract Lineages

Status: governance. Updated 2026-06-15 (split decision). Supersedes the prior
single-shared-contract / two-implementer "compatibility matrix" model.

`/api/v1` used to be one shared contract implemented by **both** eD2K cores so a
controller could drive either interchangeably. With the eMuleBB MFC client's fate
decided (final `0.7.3`, sustainability freeze) and the forward controller
(**TrackMuleBB**) scoped to **emulebb-rust + qBittorrentBB only — never the MFC
client**, that interchangeability requirement is obsolete. The contract is
therefore **split into two independent lineages**.

## The split (decision 2026-06-15)

| Lineage | Owner / implementer | OpenAPI source of truth | Versioning | Evolves? |
|---|---|---|---|---|
| **Frozen `0.7.3`** | eMuleBB **MFC** client + its frozen consumer **aMuTorrent** | `emulebb-tooling/docs/rest/REST-API-OPENAPI.yaml` (`version: 0.7.3`, marked FROZEN) | pinned to `0.7.3` | **No** — maintenance-compat repairs only, never new capability |
| **Forward** | **emulebb-rust** (drives **TrackMuleBB**) | `emulebb-rust/docs/rest/REST-API-OPENAPI.yaml` (`x-contract-version`, semver) | independent **contract semver**, decoupled from product tags | **Yes** — emulebb-rust leads, baselined on the `0.7.3` contract |

The two lineages share a baseline (the forward contract starts as a copy of the
frozen `0.7.3` document) and then diverge. There is **no cross-lineage
interchangeability guarantee** and no shared version range to satisfy.

## Forward contract versioning policy (emulebb-rust)

- The forward contract is versioned as a **contract semver** via
  `x-contract-version`, **independent of any product release tag** and of the
  frozen MFC client. Baseline `1.0.0`.
- Additive endpoints/fields bump the **minor**; breaking changes bump the
  **major** with a documented migration.
- emulebb-rust **advertises its contract version** at runtime (e.g. on `/app` and
  a capabilities surface). **TrackMuleBB targets a contract version range and
  degrades by capability** — it does not pin to a product tag.
- Adapter compatibility (`/api/v2` qBit-compat, Torznab) must not broaden or
  weaken the native forward contract.

## Frozen contract (MFC + aMuTorrent)

- A static artifact describing what the frozen MFC client and frozen aMuTorrent
  speak. It does not gain capability. The `0.7.3` final package ships that frozen
  pair together via the PowerShell bootstrap.
- aMuTorrent is frozen with it; no forward consumer depends on the MFC `/api/v1`.

## Conformance (replaces the hand-maintained matrix)

- The **forward** contract gets an automated OpenAPI conformance/drift check in
  **emulebb-rust CI** (responses validated against
  `emulebb-rust/docs/rest/REST-API-OPENAPI.yaml`). One implementation, one spec —
  the check, not a table, keeps them aligned. (Tracked as a REST contract item.)
- The **frozen** contract needs no drift check beyond not regressing the MFC
  shared listener; it is a snapshot.

## Why this is simpler and more future-proof

- Removes the constraint that created the future-proofness gaps: no need to keep a
  dead client interchangeable, no cross-implementer version negotiation.
- Resolves contract-version-vs-product-tag coupling: the forward line owns its
  own semver; the frozen line is honestly pinned to `0.7.3`.
- Lets emulebb-rust add forward-only capabilities (e.g. cursor pagination for the
  autonomous index, new search evidence) without backward obligations to the MFC.

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md),
[REST-API-CONTRACT](../rest/REST-API-CONTRACT.md) (frozen `0.7.3`),
`emulebb-rust/docs/rest/REST-API-OPENAPI.yaml` (forward).

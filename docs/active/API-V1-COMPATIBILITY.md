# /api/v1 Compatibility Matrix

Status: governance. Captured 2026-06-14. `/api/v1` is the **integration seam** that
makes the family a suite: it is the shared controller contract implemented by
**both** eD2K cores — the eMuleBB MFC app and emulebb-rust — so controllers
(aMuTorrent, the Arr stack) drive either interchangeably. This page tracks which
core implements which version of the contract, and the versioning policy.

The matrix always lists **both eMuleBB (MFC) and emulebb-rust** as the two
implementers of the contract.

## Contract versioning policy

- `/api/v1` is **versioned explicitly** as a contract, independent of any product's
  release tag. The contract spec + OpenAPI live with the MFC app
  (`docs/rest/REST-API-CONTRACT.md`, `docs/rest/REST-API-OPENAPI.yaml`); the
  contract version is the source of truth, not a client version.
- Each implementer advertises the contract version range it supports. Controllers
  target a **range**, not a product tag — so a frozen MFC at `0.7.x` and a
  forward emulebb-rust can both satisfy the same controller.
- Additive endpoints/fields bump the minor contract version; breaking changes bump
  major and require a documented migration. The MFC app (frozen) does not gain new
  capability; emulebb-rust leads contract evolution.
- aMuTorrent pins to the **contract version range**, not to the frozen MFC tag (see
  `amutorrent/docs/SUITE-AUTOMATION.md`).

## Implementation matrix

| Capability area | eMuleBB (MFC) | emulebb-rust |
|---|---|---|
| Contract version | shipped at `0.7.3` (frozen) | tracks forward (leads evolution) |
| Native `/api/v1` REST (search, shared files, transfers, categories, kad) | ✅ | ✅ |
| qBittorrent-compat adapter (`/api/v2`, Arr download client) | ✅ (`WebServerQBitCompat`) | planned (`RUST-FEAT-004`) |
| Torznab indexer adapter | ✅ (`WebServerArrCompat`) | planned (`RUST-FEAT-004`, served from the indexer `RUST-FEAT-002`) |
| Autonomous Kad/eD2K index behind the search surface | — | planned (`RUST-FEAT-002`) |
| Platform | Windows only | multiplatform |

Legend: ✅ implemented · planned = tracked backlog item · — not applicable.

## How to keep it true

- When emulebb-rust lands a `/api/v1` change, update the contract spec + version and
  this matrix in the same change; re-run the REST contract/drift checks.
- The frozen MFC column changes only for maintenance/compat repairs, never new
  capability.
- Controllers and the compatibility matrix are validated against the contract, not
  against product tags.

Related: [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md),
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md), `docs/rest/REST-API-ADAPTERS` (MFC repo).

# REST API Contract Lineage

Status: governance. Rewritten 2026-07-08. This supersedes the 2026-06-16
shared `/api/v1` compatibility model.

## Decision

There are now **two separate OpenAPI contracts**:

- **Frozen emulebb-mfc contract:** `docs/products/emulebb-mfc/api/REST-API-OPENAPI.yaml`
- **Forward Rust contract:** `docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml`

The legacy path `docs/rest/REST-API-OPENAPI.yaml` remains a compatibility alias
for the frozen emulebb-mfc contract because existing emulebb-mfc release,
package, VM, and REST smoke tooling still loads that path. Do not use it as a
shared forward contract.

## emulebb-mfc Contract

The emulebb-mfc contract is pinned to the `0.7.3` line. It is maintained only
for release proof, compatibility repairs, and documentation corrections. It does
not grow new controller capabilities, does not need a `/capabilities` discovery
endpoint, and is not a constraint on TrackMuleBB's forward UI.

Primary consumers:

- emulebb-mfc `0.7.x`
- aMuTorrent `0.7.3` / sustainability maintenance
- emulebb-mfc package and release validation tooling

## Rust Contract

The Rust contract is the forward first-party control API for `emulebb-rust` and
TrackMuleBB. It may evolve freely, including breaking schema or route changes,
while those two products are the only stability audience. The API should model
native eD2K/Kad daemon concepts rather than preserving emulebb-mfc
compatibility.

Primary consumers:

- emulebb-rust
- TrackMuleBB Rust Console UI beta
- first-party local test and release tooling

Any later third-party stability promise requires a separate API-freeze decision,
versioning policy, migration notes, and conformance gate.

## TrackMuleBB Direction

TrackMuleBB's first beta targets `emulebb-rust` only. It no longer needs generic
emulebb-mfc capability negotiation as a product requirement. emulebb-mfc remains
on its own frozen legacy controller path.

The first TrackMuleBB beta is a Rust eD2K/Kad console: status, transfers,
uploads, search, shared files, servers/Kad, and settings. It uses polling first;
SSE/event streaming is deferred until the Rust API and UI behavior settle.

## Conformance

- emulebb-mfc REST conformance validates emulebb-mfc live responses against the
  frozen emulebb-mfc OpenAPI artifact.
- Rust REST conformance validates Rust live responses against the Rust OpenAPI
  artifact.
- TrackMuleBB adapter tests should use Rust contract fixtures for the first beta.
- No conformance test should require a subset relation between emulebb-mfc and
  Rust.

## Migration Notes

- Active product docs for Rust and TrackMuleBB live under
  `docs/products/emulebb-rust` and `docs/products/trackmulebb`.
- Repo-local docs directories in `repos/emulebb-rust` and `repos/trackmulebb`
  are pointers only.
- Historical docs may still mention the old single-contract model as provenance;
  active governance follows this document.

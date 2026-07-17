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
endpoint, and is not a constraint on any future controller UI.

Primary consumers:

- emulebb-mfc `0.7.x`
- aMuTorrent `0.7.3` / sustainability maintenance
- emulebb-mfc package and release validation tooling

## Rust Contract

The Rust contract is the forward first-party control API for `emulebb-rust`, its
embedded SPA WebUI, and first-party tests/tooling. It may evolve freely,
including breaking schema or route changes, while that is the only stability
audience. The API should model native eD2K/Kad daemon concepts rather than
preserving emulebb-mfc compatibility.

Pre-beta rule: there is no external Rust REST consumer and no compatibility
freeze. The Rust daemon, embedded SPA WebUI, OpenAPI artifact, route/body
validators, and first-party tests are one owned surface and may be changed
together whenever that makes the API cleaner. Do not keep aliases, legacy fields,
or awkward route shapes solely for hypothetical external consumers before an
explicit API-freeze decision exists.

The Rust REST API is not an emulebb-mfc, stock GUI, or legacy preference mirror.
It should expose the best Rust-native async daemon model for eD2K/Kad operation.
Legacy names and inert compatibility fields should be removed or replaced with
real Rust-native concepts before beta. Broadband-oriented async IO is the daemon
baseline, not a compatibility preference or runtime toggle.

Primary consumers:

- emulebb-rust
- embedded SPA WebUI
- first-party local test and release tooling

Any later third-party stability promise requires a separate API-freeze decision,
versioning policy, migration notes, and conformance gate.

## Controller Direction

TrackMuleBB is parked future controller work. It no longer needs generic
emulebb-mfc capability negotiation as a product requirement, and it is not a Rust
beta dependency. emulebb-mfc remains on its own frozen legacy controller path.

The active Rust UI target is the embedded SPA WebUI: status, transfers, uploads,
search, shared files, servers/Kad, settings, logs, and diagnostics. SSE/event
streaming is deferred until the Rust API and UI behavior settle.

## Conformance

- emulebb-mfc REST conformance validates emulebb-mfc live responses against the
  frozen emulebb-mfc OpenAPI artifact.
- Rust REST conformance validates Rust live responses against the Rust OpenAPI
  artifact.
- Rust UI/API tests should use Rust contract fixtures for the first beta.
- No conformance test should require a subset relation between emulebb-mfc and
  Rust.

## Migration Notes

- Active product docs for Rust and TrackMuleBB live under
  `docs/products/emulebb-rust` and `docs/products/trackmulebb`.
- Repo-local docs directories in `repos/emulebb-rust` and `repos/trackmulebb`
  are pointers only.
- Historical docs may still mention the old single-contract model as provenance;
  active governance follows this document.

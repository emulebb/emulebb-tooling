# emulebb-rust `/api/v1` Contract

`REST-API-OPENAPI.yaml` here is the source of truth for the forward
emulebb-rust `/api/v1` contract.

Start with the [API-consumer guide](GUIDE-API-CONSUMERS.md) for a private-key
request, response handling, search and event-stream examples. Download the
[raw canonical OpenAPI](https://raw.githubusercontent.com/emulebb/emulebb-tooling/main/docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml)
when configuring tooling; the YAML here remains the owning contract.

This is not a shared emulebb-mfc/Rust superset. The frozen emulebb-mfc contract
lives separately at
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-mfc\api\REST-API-OPENAPI.yaml`.

## Current Stability Audience

The near-term stability audience is first-party only:

- emulebb-rust
- embedded SPA WebUI
- first-party tests and release tooling

Breaking route or schema changes are allowed while the Rust daemon and embedded
SPA WebUI move in lockstep. A later third-party API promise needs a separate
freeze and compatibility decision.

## Sharing Contract

Sharing management is folder-tree only:

- configure individual roots with `/api/v1/library/roots` and `/api/v1/library/roots/{id}`;
- every root is recursively scanned; native watching is opt-in per root and off by default;
- request a scan with `POST /api/v1/library/scan` and read cached progress with `GET /api/v1/library/scan`;
- custom case-insensitive file-name globs and configurable built-in ignores
  apply across every shared tree through `/api/v1/library/ignores`;
- single-file share/unshare/delete-sharing routes are not part of the Rust
  public contract.

## Conformance

Change this spec in the same change as the implementation. The Rust conformance
gate is tracked by
[`RUST-CI-003`](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-CI-003.md).

Every `/api/v1` response carries `X-Contract-Version`, matching
`info.x-contract-version` and `GET /capabilities.data.contractVersion`, so
first-party adapters can gate on the contract without parsing the body first.

Adapter surfaces (`/api/v2` qBit-compat, Torznab) must not broaden or weaken the
native route shape.

## Public foundation

The [public-foundation specification](../design/PUBLIC-FOUNDATION.md) and the
[59-field settings contract](../design/SETTINGS-TARGET.md) landed in [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349).
Update the canonical OpenAPI alongside changes to routes and schemas. Check
the README shipped with a package for the behavior it contains.

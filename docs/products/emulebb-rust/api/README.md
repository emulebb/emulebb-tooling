# emulebb-rust `/api/v1` Contract

`REST-API-OPENAPI.yaml` here is the source of truth for the forward
emulebb-rust `/api/v1` contract.

This is not a shared emulebb-mfc/Rust superset. The frozen emulebb-mfc contract
lives separately at
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-mfc\api\REST-API-OPENAPI.yaml`.

## Current Stability Audience

The near-term stability audience is first-party only:

- emulebb-rust
- emulebb-rust-ui
- first-party tests and release tooling

Breaking route or schema changes are allowed while the Rust daemon and native UI
move in lockstep. A later third-party API promise needs a separate freeze and
migration decision.

## Conformance

Change this spec in the same change as the implementation. The Rust conformance
gate is tracked by
[`RUST-CI-003`](../active/items/RUST-CI-003.md).

Adapter surfaces (`/api/v2` qBit-compat, Torznab) must not broaden or weaken the
native route shape.

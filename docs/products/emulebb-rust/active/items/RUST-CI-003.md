---
id: RUST-CI-003
workflow: local
title: Wire the Rust /api/v1 OpenAPI conformance/drift check into CI
status: OPEN
priority: Minor
category: ci
labels: [rest, contract, openapi, ci, drift]
milestone: phase-0
created: 2026-06-26
source: docs/rest/README.md contract-drift TODO; API lineage reset 2026-07-08
---

# RUST-CI-003 - Wire the Rust /api/v1 OpenAPI conformance/drift check into CI

## Summary

`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\emulebb-rust\api\REST-API-OPENAPI.yaml`
is the source of truth for the Rust-forward `/api/v1` contract. Today nothing
automatically verifies that the daemon's live responses match the document, so
the spec and implementation can silently drift. This item wires a
conformance/drift check into CI so the Rust contract stays honest.

## Why This Matters

The embedded SPA WebUI and first-party tests drive emulebb-rust directly from the
Rust-forward contract. If a response shape diverges from the spec, the owned UI
breaks with no early signal. A drift gate converts the "remember to update the
YAML" convention into an enforced invariant.

This is not an API-freeze item. Before an explicit Rust REST freeze decision,
there is no external consumer to preserve: the daemon, embedded SPA WebUI,
OpenAPI, validators, and tests may change together whenever a cleaner contract
is useful. The gate exists to keep the current chosen contract honest.

## Intended Shape

- Validate live daemon responses against the Rust OpenAPI artifact in tooling
  docs.
- Run it from the shared `emulebb-build-tests` suite against a locally launched
  daemon bound to `X_LOCAL_IP`; do not fork a parallel per-client suite.
- Fail on a response that violates the schema, an implemented route missing
  from the spec, or a spec route missing from the Rust router.
- Keep contract-version handling consistent with
  `docs/active/API-V1-COMPATIBILITY.md`.

## Scope Constraints

- Conformance only; do not broaden or weaken the contract inside this item.
  Separate feature/API changes may intentionally reshape the contract, but must
  update the daemon, embedded SPA WebUI, OpenAPI, validators, and tests together.
- Adapter surfaces (`/api/v2` qBit-compat, Torznab) are out of scope for this
  native-contract gate.
- No new tracked PowerShell; harness in Python via the shared suite.
- emulebb-mfc conformance is a separate frozen-contract gate.

## Acceptance Criteria

- [ ] A conformance check validates live Rust `/api/v1` responses against the
      Rust OpenAPI artifact in tooling docs.
- [ ] It runs in this repo's CI / the shared `emulebb-build-tests` suite, not a
      forked suite.
- [ ] Drift fails the gate (schema violation, implemented-but-unspecified route,
      or specified-but-unimplemented route).
- [ ] The Rust API notes point at this item.

## Validation

- Run the check against a locally launched daemon bound to `X_LOCAL_IP`; confirm
  it passes on a clean HEAD and fails on an injected schema/spec mismatch.

## Notes

- Local item: it records an internal CI gate rather than a product feature.
  Promote to a GitHub-tracked CI item if it needs public workflow visibility.

## 2026-07-18 Progress

Added the first shared-harness drift guard:
`repos\emulebb-build-tests\scripts\check-rust-openapi-routes.py` compares the
emulebb-rust router path/method inventory against the Rust OpenAPI artifact and
fails on implemented-but-undocumented or documented-but-unimplemented route
inventory drift. This covers the route inventory part of the item; live response
schema conformance and CI wiring remain open.

## 2026-07-18 Progress - CI Route Inventory Gate

The static route inventory guard now runs in
`repos\emulebb-build-tests\.github\workflows\fast-harness-ci.yml` after the
shared harness checks out `emulebb-rust` and `emulebb-tooling`. This moves the
implemented/spec route-inventory drift check into CI. Live response schema
validation remains the next uncovered part of this item.

## 2026-07-18 Progress - Static Query Inventory Gate

Extended the shared-harness route drift guard so the same CI step also compares
Rust middleware query-parameter allowlists in
`crates\emulebb-rest\src\route_metadata.rs` against OpenAPI query parameter
names. This covers static query-name drift for implemented/documented routes;
live response schema validation remains open.

## 2026-07-18 Progress - Static Body Inventory Gate

Extended the same shared-harness metadata drift guard to compare Rust top-level
JSON body field allowlists in
`crates\emulebb-rest\src\route_body_metadata.rs` against OpenAPI request-body
schema property names. The CI gate now covers static route, query, and body
metadata drift; live response schema validation remains open.

## 2026-07-18 Progress - Response Schema Validator Primitive

Extracted the REST smoke script's OpenAPI response schema validation into the
importable shared-harness helper
`emule_test_harness\rust_openapi_responses.py`. The helper validates named
response components and operation/status responses against the same OpenAPI
artifact, including component response `$ref` resolution. This gives the live
daemon conformance step a reusable validator, but the full live daemon response
gate remains open.

## 2026-07-18 Progress - Operation Response Validation Wiring

Updated the shared REST completeness smoke path so live responses are validated
against the OpenAPI response schema for the exact operation and HTTP status that
returned, instead of only the named success envelope. The remaining gap is
running that live path as a CI daemon conformance gate under the policy
quickstart.

## 2026-07-18 Progress - Existing Daemon Conformance Command

Added the persisted Python command
`repos\emulebb-build-tests\scripts\check-rust-rest-openapi-responses.py` for
validating an already-running emulebb-rust daemon against the OpenAPI response
schemas. It reuses the shared REST completeness runner and performs no ad-hoc
launching, so CI/profile orchestration can own daemon startup separately.

## 2026-07-18 Progress - Contract Header Metadata Gate

Extended the static OpenAPI drift checker to fail any documented native
operation response that omits `X-Contract-Version`. The shared CI guard now
covers route, query, body, and response-header metadata drift before live daemon
schema conformance runs.

## 2026-07-18 Progress - Soak Describe Conformance Command

The Rust-only persisted profile `--describe` output now includes a
`restOpenApiConformanceCommand` for the already-running daemon. It uses the
reported LAN REST base URL and API key, writes a retained JSON report under the
workspace output root, and keeps launch/validation discoverability inside the
policy-owned Python quickstart path. Full automated live CI orchestration remains
open.

## 2026-07-18 Progress - Conformance Base URL Preflight

Hardened the running-daemon conformance command to reject `--base-url` values
that include a path such as `/api/v1`, preventing accidental `/api/v1/api/v1`
probes and giving operators a clean preflight error instead of a transport
traceback.

## 2026-07-18 Progress - Static Auth Contract Gate

Extended the static OpenAPI drift checker to fail if the native contract loses
its top-level `ApiKeyAuth` requirement, the `X-API-Key` header security scheme,
or per-operation `401` response documentation. This keeps the documented auth
surface aligned with the Rust router's API-key middleware before live response
conformance runs.

## 2026-07-18 Progress - Auth Override Guard

Tightened the same static auth gate so an operation-level OpenAPI `security`
override must still include `ApiKeyAuth`. This prevents a single native route
from silently bypassing the documented `X-API-Key` requirement while the global
security scheme remains valid.

## 2026-07-18 Progress - Live 405 Allow Header Check

Extended the REST smoke harness so the representative native `405
METHOD_NOT_ALLOWED` probe must carry the documented `Allow` header in addition
to the canonical JSON error envelope and contract-version header.

## 2026-07-18 Progress - Static 405 Contract Gate

Extended the static OpenAPI drift checker to fail if any native operation loses
its `405` response or stops referencing `MethodNotAllowedResponse`, and to fail
if that shared response component drops the documented `Allow` header.

## 2026-07-18 Progress - Static Contract-Version Gate

Pinned the OpenAPI contract-version values as schema constants and extended the
shared route drift checker so Rust `CONTRACT_VERSION`, OpenAPI
`info.version`/`info.x-contract-version`, the documented contract-version
header, the capability discovery payload, and harness constants must all agree.
The same gate also rejects inline `X-Contract-Version` response-header
definitions that bypass the shared OpenAPI header component.

## 2026-07-18 Progress - Static Error Response Gate

Extended the static OpenAPI drift checker so every native operation must
document `400`, `401`, `404`, and `default` through the shared `ErrorResponse`
component, and that component must continue to publish the canonical
`ErrorEnvelope` JSON schema. `405` stays on the dedicated
`MethodNotAllowedResponse` gate because it also owns the `Allow` header.

## 2026-07-18 Progress - Static Path Parameter Gate

Extended the static OpenAPI drift checker so every path template placeholder
must have a matching `in: path` parameter document, no extra path parameters are
documented, and every documented path parameter is marked `required: true`.
This catches route-template/documentation drift before live response
conformance runs.

## 2026-07-18 Progress - Static Operation Metadata Gate

Extended the static OpenAPI drift checker so every native operation must carry a
non-empty `operationId` and tag list, and operation IDs must remain unique. This
keeps adapter/code-generator-facing metadata stable while the Rust-forward
contract continues to evolve before freeze.

## 2026-07-18 Progress - Static Success Response Gate

Extended the static OpenAPI drift checker so every native operation must
document exactly one `2xx` response, that success response must reference a
shared response component, and the referenced component must define a concrete
media schema. This keeps success-envelope documentation generator-ready and
prevents route-local inline success shapes from bypassing the shared contract.

## 2026-07-18 Progress - Static Request Body Metadata Gate

Extended the static OpenAPI drift checker so every documented native request
body must explicitly state `required: true` or `required: false`, expose only
`application/json`, and reference a shared schema component. This preserves the
current optional-body route where intentional while keeping JSON request payloads
generator-ready and aligned with the Rust validators.

## 2026-07-18 Progress - Static Component Reference Gate

Extended the static OpenAPI drift checker so every `$ref` must be a local
`#/components/...` reference and must resolve to an existing component. This
gives missing or external schema, response, parameter, and header refs a
precise drift report instead of failing later during response or schema checks.

## 2026-07-18 Progress - Static Parameter Metadata Gate

Extended the static OpenAPI drift checker so every inline or component
parameter must publish an explicit boolean `required` value, a valid `in`
location, a non-empty name, and a schema object. The OpenAPI contract now marks
the existing optional query filters as `required: false` instead of relying on
implicit OpenAPI defaults, which keeps generated clients and adapter manifests
honest without changing Rust runtime behavior.

## 2026-07-18 Progress - Static Tag Taxonomy Gate

Extended the static OpenAPI drift checker so operation tags must be declared in
the top-level tag taxonomy, top-level tags must be unique and named, and unused
declared tags fail the route contract check. This keeps generated client
groupings and power-user documentation navigation aligned with the Rust-native
controller surface.

## 2026-07-18 Progress - Static Response Component Gate

Extended the static OpenAPI drift checker so every shared response component
must have a non-empty description, must carry the shared contract-version
header reference, and must expose the expected media type and schema. The gate
preserves the intentional `EventStreamResponse` `text/event-stream` exception
while keeping all other reusable response components JSON-envelope based.

## 2026-07-18 Progress - Static Operation Summary Gate

Extended the static OpenAPI operation metadata checker so every native
operation must publish a non-empty `summary` alongside its stable `operationId`
and tag list. This keeps generated client documentation and power-user route
catalogs useful as the Rust-forward route surface evolves.

## 2026-07-18 Progress - Static Schema Component Gate

Extended the static OpenAPI drift checker so every shared schema component must
be an object, must not be empty, and must declare a concrete type, composition,
enum, or const shape. Empty enum definitions are rejected as well. This keeps
the schema catalog generator-ready before adapters or power-user clients depend
on it.

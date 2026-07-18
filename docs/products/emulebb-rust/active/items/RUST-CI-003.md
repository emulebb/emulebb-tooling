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

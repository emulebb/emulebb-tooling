---
id: FEAT-122
workflow: local
title: Expose GET /api/v1/capabilities (contract-discovery primitive) under the soft freeze
status: OPEN
priority: Minor
category: feature
labels: [rest, api-v1, capabilities, compatibility]
milestone: 0.7.x
created: 2026-06-16
source: API-V1-COMPATIBILITY capability model (decision 2026-06-16)
---

# FEAT-122 - Expose GET /api/v1/capabilities (contract-discovery primitive) under the soft freeze

## Summary

Add a `GET /api/v1/capabilities` endpoint to the eMuleBB MFC WebServer that
returns the contract version and the capability groups the MFC implements
(`core.*` only — its frozen subset). This lets the suite controller (TrackMuleBB)
discover and drive the MFC the same generic way it drives emulebb-rust, with no
product-specific code. Contract model:
`emulebb-tooling/docs/active/API-V1-COMPATIBILITY.md`.

## Why This Matters

`/capabilities` is a **contract-discovery primitive, not a new product
capability** — so it is allowed as **contract maintenance under the soft freeze**.
Including it guarantees clean evolution: every core (frozen MFC or forward rust) is
discoverable identically, the controller never special-cases a product, and new
capabilities slot in without touching the controller.

## Intended Shape

- Response: `{ "contractVersion": "<pinned>", "capabilities": ["core.search",
  "core.transfers","core.shared","core.kad", ...] }` — exactly the operations the
  MFC `/api/v1` already serves, named by the shared capability vocabulary.
- Frozen subset: the MFC advertises only `core.*` (no `indexing.*`/`arr.*` beyond
  the existing adapters). It does not grow.

## Scope Constraints

- Contract maintenance only — no new product/feature surface; the MFC stays frozen.
- The capability vocabulary + `x-capability` tags are owned by the canonical
  OpenAPI (emulebb-rust superset); the MFC names its existing operations from it.

## Acceptance Criteria

- [ ] `GET /api/v1/capabilities` returns the pinned contract version + the MFC's
      `core.*` capability set.
- [ ] A conformance run validates the MFC's advertised operations against the
      canonical OpenAPI subset.
- [ ] No new non-`core` capability is advertised.

## Notes

- Consumed by `trackmulebb` `TMBB-FEAT-004` (capability negotiation). The forward
  core's matching work is the emulebb-rust REST-contract item.

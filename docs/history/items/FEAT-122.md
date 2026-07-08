---
id: FEAT-122
workflow: local
title: Do not add GET /api/v1/capabilities to emulebb-mfc
status: WONT_DO
priority: Minor
category: feature
labels: [rest, api-v1, capabilities, compatibility]
milestone: 0.7.x
created: 2026-06-16
source: API-V1-COMPATIBILITY capability model (decision 2026-06-16); API lineage reset (2026-07-08)
---

# FEAT-122 - Superseded

## Summary

Do **not** add `GET /api/v1/capabilities` to emulebb-mfc. This item was created
for the retired one-contract capability model. The active decision is now a split
contract lineage:

- emulebb-mfc stays frozen on `docs/products/emulebb-mfc/api/REST-API-OPENAPI.yaml`.
- emulebb-rust evolves through
  `docs/products/emulebb-rust/api/REST-API-OPENAPI.yaml`.
- TrackMuleBB first beta targets emulebb-rust only.

## Reason

The emulebb-mfc `0.7.3` API contract is frozen. Adding a discovery endpoint would
be new controller surface under the retired shared-contract model, and it is no
longer needed for TrackMuleBB.

## Acceptance Criteria

- [x] Active governance says emulebb-mfc does not need `/capabilities`.
- [x] TrackMuleBB first beta no longer depends on emulebb-mfc capability
      negotiation.

## Notes

- Superseded by `docs/active/API-V1-COMPATIBILITY.md` rewritten on 2026-07-08.

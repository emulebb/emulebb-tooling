---
id: FEAT-045
title: REST transfer detail endpoint for controller parity
status: Passed
priority: Major
category: feature
labels: [rest, transfers, controller, amutorrent]
milestone: broadband-release
created: 2026-05-02
source: broadband release live E2E and REST completeness planning
---

## Summary

Add a transfer detail endpoint for controller views that need more than the
current transfer row plus source list.

## Beta 0.7.3 Classification

**Promoted for Release 1.** The native endpoint is implemented and aMuTorrent
now consumes it through capability-gated `AMUT-002` hydration.

Target route:

- `GET /api/v1/transfers/{hash}/details`

## Execution Plan

Historical release context: [Beta 0.7.3 REST and Arr execution plan](../../history/release-0.7.3/RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md).

## Current State

The backend now exposes `GET /api/v1/transfers/{hash}/details` as a dedicated
detail payload with the transfer row, per-part state, and source rows. The
native app advertises the `transferDetails` capability, and aMuTorrent consumes
the endpoint with compatibility fallback for older eMule BB builds.

## Acceptance Criteria

- [x] detail data is exposed through a dedicated endpoint, not by bloating
      `snapshot`
- [x] missing or malformed hashes return the stable REST error envelope
- [x] the endpoint is covered by native route tests, live REST smoke, and the
      contract manifest
- [x] aMuTorrent consumes the endpoint when capability metadata indicates it is
      available

## Progress

- 2026-05-07: Revalidated the native detail route on current `main`. The
  OpenAPI contract includes `GET /api/v1/transfers/{hash}/details`, native route
  seams cover routing and hash validation, and the live REST smoke verifies
  both the missing-transfer error path and the detail payload for an added
  paused transfer.
- 2026-05-07: Controller-side detail hydration was initially deferred because
  `AMUT-001` and Arr gates provided useful release transfer views without
  requiring aMuTorrent to consume the detail endpoint.
- 2026-05-08: Promoted for Release 1 with `AMUT-002`. The native app advertises
  `capabilities.transferDetails`, the aMuTorrent adapter consumes the endpoint
  when that capability is present, and
  `repos/emulebb-build-tests/reports/amutorrent-browser-smoke-latest/result.json`
  records passing browser smoke proof.

## Relationship To Other Items

- feeds `AMUT-002`
- updates `CI-014`

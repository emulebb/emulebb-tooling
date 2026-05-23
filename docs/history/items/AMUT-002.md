---
id: AMUT-002
title: aMuTorrent transfer detail hydration
status: Passed
priority: Major
category: integration
labels: [amutorrent, rest, transfers, controller]
milestone: broadband-release
created: 2026-05-02
source: broadband release live E2E and REST completeness planning
---

## Summary

Hydrate aMuTorrent transfer detail views from eMule BB REST once the backend
exposes the required detail endpoint.

## Beta 0.7.3 Classification

**Promoted for Release 1.** `FEAT-045` now exposes the native detail endpoint,
and aMuTorrent consumes it when eMule BB advertises the `transferDetails`
capability.

## Execution Plan

Historical release context: [Beta 0.7.3 REST and Arr execution plan](../../history/release-0.7.3/RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md).

## Current State

The eMule BB adapter maps transfer rows, detects `transferDetails` capability
metadata, hydrates per-transfer details from
`GET /api/v1/transfers/{hash}/details`, and falls back to source-only hydration
for older builds or transient detail failures.

## Release 1 Decision

Passed for Release 1. The native app advertises `transferDetails`, the
aMuTorrent adapter consumes the endpoint with backward-compatible fallback, and
the browser smoke verifies hydrated detail fields through the REST snapshot and
the browser `segmentData` WebSocket subscription.

## Acceptance Criteria

- [x] adapter detects the transfer-detail capability before calling the new
      endpoint
- [x] detail payload is merged into transfer models without breaking existing
      list rendering
- [x] missing detail support degrades cleanly on older eMule BB builds
- [x] Node adapter tests and browser smoke coverage verify hydrated details

## Progress

- 2026-05-08: Promoted for Release 1 on `main`. eMule BB now advertises
  `capabilities.transferDetails`; aMuTorrent calls the native detail endpoint
  only when that capability is present and falls back to `/sources` for older
  builds.
- 2026-05-08: Verification passed:
  `npm run test:emulebb` in `repos/amutorrent`;
  `python -m emule_workspace build app --config Debug --platform x64`;
  `python -m emule_workspace build app --config Release --platform x64`;
  `python -m emule_workspace build tests --config Debug --platform x64 --test-run-variant main --clean`;
  `python -m emule_workspace build tests --config Release --platform x64 --test-run-variant main --clean`;
  `python -m emule_workspace test all --config Debug --platform x64`;
  `python -m emule_workspace test all --config Release --platform x64`;
  and targeted live proof
  `python -m emule_workspace test live-e2e --config Release --platform x64 --suite amutorrent-browser-smoke`.
  Latest live artifact:
  `repos/emulebb-build-tests/reports/amutorrent-browser-smoke-latest/result.json`.
- 2026-05-09: Fresh Release x64 browser smoke after REST/Arr revalidation
  passed at
  `repos/emulebb-build-tests/reports/amutorrent-browser-smoke/20260509-081711-eMule-main-release/result.json`.
  The report includes hydrated transfer progress/status/source fields and
  segment-subscribed `partStatus`, `gapStatus`, and `reqStatus` evidence.
- 2026-05-09: Beta 0.7.3 controller replay passed at
  `repos/emulebb-build-tests/reports/amutorrent-browser-smoke/20260509-142532-eMule-main-release/result.json`.
  The browser smoke remained green after CI-032 post-tag hardening coverage.

## Relationship To Other Items

- depends on `FEAT-045`
- backs `AMUT-001`

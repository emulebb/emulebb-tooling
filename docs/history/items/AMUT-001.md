---
id: AMUT-001
title: aMuTorrent eMule BB browser smoke coverage
status: Passed
priority: Major
category: integration
labels: [amutorrent, rest, ui-smoke, controller]
milestone: broadband-release
created: 2026-05-02
source: broadband release live E2E and REST completeness planning
---

## Summary

Add a browser smoke lane that runs aMuTorrent against a live eMule BB instance.

## Beta 0.7.3 Classification

**Release Gate.** Full E2E-validated integration with aMuTorrent and the Arr
suite is part of Release 1. This item owns the aMuTorrent side of that gate:
at least one browser smoke against a live instance with request and console
artifacts.

## Execution Plan

Historical release context: [Beta 0.7.3 REST and Arr execution plan](../../history/release-0.7.3/RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md).

## Acceptance Criteria

- [x] aMuTorrent can connect to the eMule BB REST API with configured host,
      port, and API key
- [x] dashboard connection state renders eD2K and Kad status
- [x] transfers, shared files, shared directories, categories, searches, and
      uploads render without adapter exceptions
- [x] create/delete category and shared-directory reload flows are exercised
      through the browser smoke where supported
- [x] failures produce browser console and REST request artifacts

## Completion Evidence

- tests: `affc4d6`, `11365ca`
- command: `python -m pytest tests\python\test_amutorrent_browser_smoke.py tests\python\test_live_e2e_suite.py -q`
- command: `python -m emule_workspace test live-e2e --config Release --platform x64 --suite amutorrent-browser-smoke`
- artifact: `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260506-193606-eMule-main-release\result.json`
- aggregate: `repos\emulebb-build-tests\reports\live-e2e-suite\20260506-193606-eMule-main-release\result.json`
- Follow-up debug live proof:
  `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260508-001203-eMule-main-debug\result.json`.
  The run passed with browser workflows covering automatic, server, and Kad
  search modes twice, and the report now records `launch_inputs` with
  `p2p_bind_interface_name=hide.me` and `enable_upnp=true`. The isolated
  profile used `BindInterface=hide.me`, empty P2P `BindAddr`, WebServer
  `BindAddr=127.0.0.1`, and `EnableUPnP=1`.
- Test commit: `fa55046` keeps the aMuTorrent browser report on native `/api/v1`
  and records live-network launch inputs without ever writing `BindAddr=hide.me`.
- Follow-up delete hardening: live browser smoke now adds a synthetic eD2K
  transfer, deletes it through aMuTorrent's native `/api/v1/downloads/delete`
  bridge, and verifies the next browser snapshot no longer contains that hash.
  aMuTorrent commit `3c23c1b` fixes the stale snapshot cache after mutation
  refreshes; test commit `5a7565d` keeps the browser regression covered.
- Debug live artifact after the delete fix:
  `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260508-004347-eMule-main-debug\result.json`.
  The run passed with delete result `Deleted 1/1 files`, post-delete item count
  `0`, automatic/server/Kad search mode coverage, `BindInterface=hide.me`,
  empty P2P `BindAddr`, and `EnableUPnP=1`.
- Fresh Release x64 revalidation:
  `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260509-081711-eMule-main-release\result.json`.
  The run passed after native REST and Arr adapter revalidation with
  `BindInterface=hide.me`, UPnP enabled, eD2K and Kad connected,
  automatic/server/Kad search modes, category create/delete, shared-files
  reload, synthetic eD2K add/delete, and post-delete snapshot cleanup. Focused
  aMuTorrent tests selected by `amutorrent or browser_smoke or search_modes or
  transfer_detail or segment_snapshot` also passed.
- Beta 0.7.3 controller replay artifact:
  `repos\emulebb-build-tests\reports\amutorrent-browser-smoke\20260509-142532-eMule-main-release\result.json`.
  The run passed through the supported `amutorrent-browser-smoke` suite with
  browser workflows, eMule REST readiness, `BindInterface=hide.me`, empty P2P
  `BindAddr`, and `EnableUPnP=1` evidence.

## Pending Revalidation Focus

This gate proves the UI target, not native API ownership. The next Release 1
hardening pass should rerun the browser smoke after native `/api/v1` and
Arr-adapter validation and confirm:

- [x] aMuTorrent still adapts to final native `/api/v1` routes, envelopes, and
      field names without requiring native compatibility aliases.
- [x] dashboard ED2K/Kad status, ED2K Server vs Kad search selection, and
      download-row delete remain covered.
- [x] progress percentage formatting remains acceptable with the shared
      native/qBit backend progress ratio helper.
- [x] browser console, page, and request artifacts remain sufficient to
      distinguish UI adapter failures from native REST failures.

## Relationship To Other Items

- backs `CI-011`
- complements `ARR-001`
- consumes the native REST contract owned by `FEAT-013` and follow-up items

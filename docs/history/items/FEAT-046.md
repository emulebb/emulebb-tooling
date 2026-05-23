---
id: FEAT-046
title: REST server and Kad bootstrap/import APIs
status: Passed
priority: Major
category: feature
labels: [rest, servers, kad, bootstrap, live-wire]
milestone: broadband-release
created: 2026-05-02
source: broadband release live E2E and REST completeness planning
---

## Summary

Expose native REST operations for controlled server and Kad bootstrap/import
flows.

## Beta 0.7.3 Classification

**Release Candidate.** Server import and Kad bootstrap coverage already exist
on current `main`. Finish Kad import for 1.0 only if live-wire bootstrap needs
a native refresh path; otherwise keep the remaining import work as a follow-up.

Default live sources are the already-persisted eMule Security URLs:

- `https://emule-security.org/`
- `https://upd.emule-security.org/server.met`
- `https://upd.emule-security.org/nodes.dat`

## Execution Plan

Historical release context: [Beta 0.7.3 REST and Arr execution plan](../../history/release-0.7.3/RELEASE-0.7.3-REST-ARR-EXECUTION-PLAN.md).

## Acceptance Criteria

- [x] server import can refresh `server.met` through the same safe validation
      and promotion path used by the app
- [x] Kad import can refresh `nodes.dat` without weakening the existing
      bootstrap-empty guard
- [x] endpoints support configured URLs and do not silently depend on bundled
      external lists
- [x] live E2E records source URL, size, hash, and import outcome
- [x] malformed downloads preserve the previous live files

## Progress

- 2026-05-02: Native `main` added `POST /api/v1/servers/operations/import-met-url`,
  `PATCH /api/v1/servers/{serverId}` property updates, and
  `POST /api/v1/kad/operations/bootstrap`. Route seam and live-smoke contract
  coverage were updated in `emulebb-build-tests`.
- 2026-05-07: Native `main` added `POST /api/v1/kad/operations/import-nodes-url`,
  wired it to the existing validated `nodes.dat` URL import path, and added
  native route plus OpenAPI contract coverage.
- 2026-05-07: Added native malformed `nodes.dat` install preservation coverage
  in `emulebb-build-tests`; this complements existing malformed `server.met`
  preservation coverage.
- 2026-05-07: Import routes now report the synchronous import outcome, and the
  live REST smoke records source URL, byte count, SHA-256, REST route, HTTP
  response, and imported outcome for both `server.met` and `nodes.dat` seed
  imports.

## Relationship To Other Items

- updates `CI-014` and `CI-015`
- complements `BUG-071` and `BUG-072`

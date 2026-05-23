# Review 2026-04-25 - Current Main, eMuleAI v1.4, and Backlog Refresh

## Scope

Rechecked the active app and tests repos against the stale April 20 backlog
state:

- `EMULE_WORKSPACE_ROOT\workspaces\v0.72a\app\eMule-main`
- `EMULE_WORKSPACE_ROOT\repos\emulebb-build-tests`
- `EMULE_WORKSPACE_ROOT\analysis\emuleai`
- `EMULE_WORKSPACE_ROOT\repos\emulebb-tooling`

The app repo is on `main` at `b5d253b` (`POLICY normalize source files to
LF`). The tests repo is on `main` at `cac7b93` (`TEST-034 extend files-page
many-file warm recovery coverage`).

## Landed Since The Previous Backlog Refresh

The backlog was stale after April 20. Current `main` now includes:

- `FEAT-034` shared hash worker, hash-drain reload coalescing, shutdown wait
  bounds, startup-cache interruption handling, and shared-hash completion retry
  hardening through `58d3cfe`
- `BUG-036` atomic `known.met` and `cancelled.met` saves in `f5433e1`
- the first `BUG-037` duplicate shared-path persistence/reuse slice in
  `4c974a3`, `c495525`, and `d7aa382`
- stale-row and teardown hardening from `BUG-038` through `BUG-052`
- eMuleAI v1.4 hardening ports from `BUG-053` through `BUG-059`
- REST/web hardening from `BUG-060`, `BUG-061`, and `BUG-067`
- server retry and delete-confirmation follow-ups in `BUG-062` and `BUG-063`
- the source line-ending policy change in `b5d253b`

## Current Pending Items

`BUG-036` is now `Done`.

`BUG-037` later completed on the same-day hardening line. The duplicate
shared-path sidecar is landed and covered by startup reuse flows, and the
follow-up KnownFile collision slice narrowed `CKnownFileList::SafeAddKFile()`
so live shared/download owners are preserved on same-MD4 collisions.

`FEAT-034` is still `In Progress`. The worker, deferral, backlog, and shutdown
handling slices landed, and TEST-034 coverage expanded substantially. The
remaining risk is blocking filesystem I/O during shared hashing if a read wedges
hard enough to hit the existing timeout/leak-and-exit shutdown path.

`BUG-034` and `BUG-035` are `In Progress`. A bounded diagnostics slice landed,
but a current source scan still finds:

- 540 `ASSERT(0)` matches
- 122 `catch (...)` matches
- 7 `FIXME` matches
- 87 `TODO` matches

These counts are not all defects, but they confirm the broad hardening buckets
are not complete.

## eMuleAI v1.4 Backlog Incorporation

High-value eMuleAI v1.4 fixes that match the branch direction are now reflected
as landed backlog items:

- `.part.met.bak` preservation: `BUG-053`
- shared-file delete confirmation ESC behavior: `BUG-054`
- AICH recovery bounds: `BUG-055`
- Download Clients stale-row guard: `BUG-056`
- orphan Kad keyword searches: `BUG-057`
- tree option separator protection: `BUG-058`
- Remaining column alignment: `BUG-059`
- obfuscated server retry follow-up: `BUG-062`
- shared-directory delete confirmation: `BUG-063`

Feature candidates from eMuleAI v1.4 were incorporated without changing app
code:

- `FEAT-037` now explicitly includes Hide Overshares and default share
  permission controls
- `FEAT-041` tracks Download Inspector stale-download automation and
  majority-name rename
- `FEAT-042` tracks automatic IP-filter update scheduling

Skipped for now: branding, dark mode, translation machinery, broad eMuleAI
project layout changes, and other product features that need explicit scope
approval before implementation.

## Validation Reference

Latest known green app validation after the line-ending policy change:

- Release x64 app build: `OK`, 882 warnings, no failures
- REST live E2E: passed at
  `EMULE_WORKSPACE_ROOT\repos\emulebb-build-tests\reports\rest-api-smoke\20260425-105048-eMule-main-release`
- Shared Files UI E2E: passed for `fixture-three-files`,
  `generated-robustness-recursive`, and `duplicate-startup-reuse`
- source normalizer on app tracked files: 740 scanned, 0 needing normalization

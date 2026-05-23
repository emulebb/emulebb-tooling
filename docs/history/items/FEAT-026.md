---
id: FEAT-026
title: Shared startup cache with known.met lookup index and `sharedcache.dat`
status: Done
priority: Minor
category: feature
labels: [startup, sharing, performance, cache, filesystem]
milestone: ~
created: 2026-04-13
source: current `main` shared-startup line (`fc70cf9`, `ec9e1d5`)
---

## Summary

This feature is merged to `main`.

`eMule-main` now carries a disposable shared-file startup cache plus a known-file lookup
index so shared-directory startup can reuse previously verified inventory instead of
re-walking and linearly re-matching every file on every launch.

## Landed Mainline Shape

Primary files:

- `srchybrid/KnownFileLookupIndex.h`
- `srchybrid/SharedStartupCachePolicy.h`
- `srchybrid/SharedFileList.cpp/.h`
- `srchybrid/KnownFileList.cpp/.h`
- `srchybrid/LongPathSeams.h`

Key flow in `SharedFileList`:

- `TryLoadStartupCache()`
- `FindSharedFiles(bool bAllowStartupCache)`
- `TryRehydrateSharedDirectoryFromCache(...)`
- `SaveStartupCache()`

## Implemented Behavior

Mainline now includes:

- `sharedcache.dat` as a config-directory sidecar cache
- a collision-preserving `KnownFileLookupIndex` keyed by filename/date/size tuples
- cached per-directory file inventories for explicit shared directories
- generic verification fallback when cached state is doubtful
- an NTFS journal fast path when the cached volume guard still matches
- mounted-volume and filesystem-identity validation before trusting cached state
- cache persistence only when the directory snapshot is stable enough to reuse

The cache is intentionally disposable. Any structural mismatch, lookup miss, or
filesystem-validation doubt falls back to the normal rescan path.

## Mainline Status

This item used to track workspace-head-only code. That is no longer true:

- the startup-cache surface is present in current `main`
- later shared-startup follow-up hardening also landed on `main`

The backlog item is therefore closed as **Done**.

## Latest Measured Status (2026-04-18)

Fresh `eMule-main` startup profiling still indicates that the dominant remaining heavy
shared-tree delay is in the hash pipeline rather than shared-files window creation.

From
`EMULE_WORKSPACE_ROOT\repos\emulebb-build-tests\reports\startup-profile-scenarios\20260418-121956-eMule-main-debug\startup-profiles-wrapper-summary.json`:

- `shared_files_ready_absolute_ms = 29360.160`
- `shared.scan.complete = 963.106 ms`
- `CSharedFilesWnd::OnInitDialog total = 139.524 ms`
- top `shared.hash.file.queue_wait(...)` spans were about `28164.869 ms`,
  `27845.748 ms`, and `27634.356 ms`

Current read: now that FEAT-026 is in `main`, the most important remaining heavy-startup
question is hash queue wait in the shared-file pipeline, not shared-files page
construction.

## Relationship To Other Items

- pairs naturally with **FEAT-027**, which cleaned up startup sequencing and profiling
  around the same path
- overlaps **FEAT-024** share-ignore behavior because cached inventories must preserve the
  same share/no-share decisions
- complements **FEAT-028**, which hardened the visible Shared Files control on top of the
  same startup/share model

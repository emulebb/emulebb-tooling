---
id: FEAT-080
title: Refresh protected-volume disk-space snapshots in the background
status: OPEN
priority: Minor
category: feature
labels: [download-queue, disk-space, storage, background-worker, performance, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: review of background parallel processing opportunities
---

# FEAT-080 - Refresh Protected-Volume Disk-Space Snapshots In The Background

## Summary

The download queue periodically checks protected temp, incoming, and config
volumes so it can pause downloads before disk pressure corrupts state. Current
main has already improved this path with cached volume identities and protected
volume snapshots, but the refresh still runs from the download-queue processing
path.

Move expensive or unreliable filesystem/volume probes behind a background
snapshot refresher while keeping the download queue's stop/pause decisions on
the existing owner path.

## Intended Shape

- Maintain a last-known protected-volume snapshot refreshed by a bounded worker.
- Let the download queue consume a recent snapshot during its normal 100 ms
  processing loop.
- Fall back to the current synchronous behavior when no valid snapshot exists.
- Treat unresolved or stale protected-volume data conservatively; never weaken
  the disk-space guard.
- Keep explicit diagnostics for stale snapshots, unresolved volumes, and worker
  refresh failures.

## Scope Constraints

- Do not move download state mutation to the worker.
- Do not weaken disk-space fail-closed behavior.
- Do not make network/removable volume stalls block UI or queue processing when
  a previous safe snapshot is available.
- Do not combine this with temp-directory placement policy changes.

## Acceptance Criteria

- [ ] protected-volume snapshots can refresh in a background worker
- [ ] download queue consumes snapshots without mutating state from the worker
- [ ] stale, missing, or unresolved snapshots remain fail-closed
- [ ] diagnostics distinguish synchronous fallback, worker success, stale data,
      and worker failure
- [ ] tests cover stale snapshot policy, unresolved volume policy, and breach
      action consistency
- [ ] live profile with slow/removable paths does not stall queue processing

## Validation

- `python -m emule_workspace validate`
- focused native disk-space guard seam tests
- live or synthetic slow-volume probe test
- x64 Debug and Release app builds before commit

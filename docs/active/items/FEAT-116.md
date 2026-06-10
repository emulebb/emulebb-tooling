---
id: FEAT-116
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/155
title: Throttle background share scanning on active slow volumes
status: OPEN
priority: Minor
category: feature
labels: [shared-files, scanning, disk-io, storage, hdd, performance, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-10
source: operator I/O and filesystem performance review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/155. This local document is retained as an engineering spec/evidence record.

# FEAT-116 - Throttle Background Share Scanning On Active Slow Volumes

## Summary

Make background shared-directory scans less disruptive on slow or busy storage.
Large recursive trees can generate many directory enumerations, stat calls, and
hash follow-up jobs. On HDDs and SMR disks this can compete with uploads and
downloads that need smoother access to the same volume.

## Intended Shape

- Distinguish explicit user refreshes from background maintenance scans.
- Rate-limit background directory walking when the same volume has active
  transfers or hash/verify work.
- Reuse cached directory state when available instead of repeatedly statting
  unchanged trees.
- Resume long background scans in bounded slices so UI and transfer work can
  stay responsive.
- Add diagnostics for skipped, delayed, resumed, and completed scan slices.
- Prefer per-volume throttling once storage-role hints from `FEAT-115` exist.

## Scope Constraints

- Do not miss files permanently; throttling may delay discovery, not suppress
  it.
- Do not weaken explicit user-requested refresh semantics without visible
  progress/cancellation.
- Do not mutate shared-file maps from background workers without existing owner
  synchronization.
- Do not add filesystem watchers that require new privileges or unreliable
  long-running handles as the only path.
- Do not regress share-ignore, monitored-share, or long-path behavior.

## Acceptance Criteria

- [ ] Background share scans run in bounded slices and can yield to active
      same-volume transfer work.
- [ ] Explicit user refresh remains available and reports progress or delay
      clearly.
- [ ] Directory state caching avoids repeated unchanged-tree work where safe.
- [ ] Throttled scans eventually resume and complete.
- [ ] Diagnostics identify scan throttling reasons and affected volume roles
      without exposing unnecessary private paths.
- [ ] Share-ignore, monitored-share, and long-path tests remain green.

## Validation

- focused tests for scan throttling state transitions
- shared-file reload and monitored-share regression tests
- long-path shared-directory smoke
- large-tree manual or live harness smoke on HDD/slow storage where available
- x64 Debug and Release app builds before implementation commit

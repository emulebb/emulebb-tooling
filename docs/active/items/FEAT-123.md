---
id: FEAT-123
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/148
title: Shared files one-level auto-updater
status: IN_PROGRESS
priority: Major
category: feature
labels: [shared-files, scanning, rc3, compatibility]
milestone: 0.7.3-rc.3
created: 2026-06-20
source: GitHub issue #148 plus operator clarification for RC3
---

# FEAT-123 - Shared files one-level auto-updater

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/148. This local document is retained as an engineering spec/evidence record.

## Summary

Restore the previous-version convenience where new files placed directly inside
already-shared directories are detected automatically. For RC3 this is a
bounded, non-recursive polling feature: it does not promote normal shared
directories into monitored roots and does not change recursive sharing behavior.

## Behavior

- Poll every 5 minutes after normal startup completes.
- Check the main Incoming directory, category Incoming directories, and
  directories listed in `shareddir.dat`.
- Compare directory metadata first; only directories that appear changed are
  enumerated.
- Enumerate only immediate files in changed directories, using the existing
  shared-file intake path for ignore rules, known-file reuse, duplicate handling,
  in-flight hash suppression, async hashing, and UI count refresh.
- Process at most 512 directory metadata checks and 8 changed-directory scans on
  one timer tick.
- Skip the polling pass while shared-file hashing is already active.
- Leave `shareddir.monitored.dat` and `shareddir.monitor-owned.dat` untouched.
- Hidden opt-out: `AutoReloadSharedFiles=0` in `preferences.ini`.

## Acceptance Criteria

- [ ] New files directly under Incoming are picked up without pressing Reload.
- [ ] New files directly under a configured shared directory are picked up
      without pressing Reload.
- [ ] Files in unshared child directories are not picked up.
- [ ] The feature does not write monitored shared-root state.
- [ ] The poller is bounded to the configured per-tick directory limits.
- [ ] Existing shared-file hash queue, ignore, duplicate, and known-file reuse
      behavior remains unchanged.
- [ ] Debug, Release, and diagnostics Release x64 app builds pass before commit.

## Notes

This is separate from FEAT-038. FEAT-038 remains the explicit recursive monitored
shared-root feature; FEAT-123 is only one-level auto-update for existing shared
directories.

---
id: FEAT-075
title: Keep startup progress responsive during daily config backup
status: OPEN
priority: Minor
category: feature
labels: [startup, backup, ui, responsiveness, progress, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-24
source: operator report that the startup dialog freezes while daily config backup runs
---

# FEAT-075 - Keep Startup Progress Responsive During Daily Config Backup

## Summary

The daily config backup currently runs synchronously early in startup after the
startup progress dialog is shown. The backup is intentionally early so it can
snapshot config files before later startup phases load or mutate them, but the
copy/prune loop does not report progress or pump the dialog while I/O is busy.

Improve this without moving the backup off the startup path as a first step:
add progress callbacks around config-backup phases and keep the startup dialog
painting with visible progress while backup work runs.

## Intended Shape

- Keep daily config backup before normal config load/migration/writes.
- Add a testable backup progress callback/seam.
- Report phase-level progress for staging, copying, pruning, completion, and
  failure cleanup.
- Update the early startup progress dialog in marquee/detail mode while backup
  work is active.
- Pump only lifecycle-progress UI messages through the existing startup dialog
  mechanism; do not start normal app timers or network work during backup.
- Consider chunked copy for individual large files only after profiling proves
  one-file stalls remain.

## Scope Constraints

- Do not make the first implementation fully asynchronous.
- Do not weaken the backup snapshot ordering or introduce races with config
  readers/writers.
- Do not change the backup directory naming, retention, or skip policy unless a
  separate bug is found.

## Acceptance Criteria

- [ ] startup dialog remains repaintable while a large config backup is running
- [ ] progress detail reflects backup phases and file/directory counts
- [ ] daily backup output and retention behavior remain unchanged
- [ ] backup failure cleanup behavior remains unchanged
- [ ] native tests cover progress callback delivery for copy, prune, and failure
      paths

## Validation

- `python -m emule_workspace validate`
- `python -m emule_workspace build tests --config Debug --platform x64 --test-run-variant main`
- `python -m emule_workspace test native --config Debug --platform x64 --test-run-variant main --suite-name parity`
- `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`

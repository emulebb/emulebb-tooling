---
id: FEAT-074
title: Add main-window visual evidence for connected LowID state
status: DONE
priority: Minor
category: feature
labels: [ui, connectivity, lowid, tray, status, rc1-polish]
milestone: beta-0.7.3
created: 2026-05-24
completed: 2026-05-24
source: operator request for main UI evidence matching the LowID tray icon
---

# FEAT-074 - Add Main-Window Visual Evidence For Connected LowID State

## Summary

Connected LowID/firewalled state is now visible in the main eMuleBB shell, not
only in the tray icon and compact connection status bar icon. eMuleBB uses a
LowID variant of the main app icon so title bar, taskbar, and Alt-Tab surfaces
show the same abnormal connectivity signal.

## Delivered Shape

- HighID, disconnected, and connecting states keep the normal app icon.
- Connected LowID/firewalled state switches to the LowID app icon.
- Main-window icon handles are separate from tray icon handles.
- Both large and small window icons are updated so Windows shell surfaces agree.
- Repeated connection-state refreshes avoid redundant SetIcon calls.

## Scope Constraints

- No new status-bar text badge was added.
- eD2K/Kad connection-state semantics and tray behavior were not changed.
- No localization-facing text was added.

## Acceptance Criteria

- [x] main app icon remains normal when disconnected, connecting, or connected
      HighID/open
- [x] main app icon switches to a LowID visual when connected firewalled/LowID
- [x] title bar, taskbar, and Alt-Tab use the same effective icon state
- [x] repeated connection refreshes do not churn icon handles or call SetIcon
      unnecessarily
- [x] native seam tests cover the state-selection policy

## Validation

- `python -m emule_workspace validate`
- `python -m emule_workspace build tests --config Debug --platform x64 --test-run-variant main`
- `python -m emule_workspace test native --config Debug --platform x64 --test-run-variant main --suite-name parity`
- `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`

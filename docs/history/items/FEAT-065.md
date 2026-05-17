---
id: FEAT-065
title: Polish the native MiniMule tray popup
status: DONE
priority: Minor
category: feature
labels: [ui-polish, tray, minimule]
milestone: beta-0.7.3
created: 2026-05-17
source: user feedback 2026-05-17
---

# FEAT-065 - Polish The Native MiniMule Tray Popup

## Summary

The restored native MiniMule popup worked functionally but still looked like a
plain fixed-system resource table. This item tracks compact native polish for
the tray popup without changing its behavior or localized strings.

## Outcome

- Keep the existing metrics and Restore, Incoming, and Options actions.
- Add a clearer header, icon, transfer-rate emphasis, spacing, and section
  hierarchy.
- Use system colors and derived dialog fonts so the popup remains native and
  accessible.

## Validation

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`

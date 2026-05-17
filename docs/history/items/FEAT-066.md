---
id: FEAT-066
title: Replace MiniMule chrome with table and speed chart
status: DONE
priority: Minor
category: feature
labels: [ui-polish, tray, minimule]
milestone: beta-0.7.3
created: 2026-05-17
source: user feedback 2026-05-17
---

# FEAT-066 - Replace MiniMule Chrome With Table And Speed Chart

## Summary

Follow-up MiniMule feedback rejected the icon, title header, title bar, and
larger derived font sizes from the first polish pass. This item tracks the
replacement compact native data-table popup with a small speed chart.

## Outcome

- Remove MiniMule icon/header/titlebar treatment and keep standard dialog font
  sizing.
- Present MiniMule status as an aligned label/value table with native borders.
- Add a compact upload/download speed trend chart driven by the existing refresh
  cadence.
- Allow moving the captionless popup by dragging non-button window areas.

## Validation

- `python -m emule_workspace validate`
- `python -m emule_workspace build app --variant main --config Debug --platform x64 --build-output-mode ErrorsOnly`
- `python -m emule_workspace build app --variant main --config Release --platform x64 --build-output-mode ErrorsOnly`

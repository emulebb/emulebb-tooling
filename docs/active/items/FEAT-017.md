---
id: FEAT-017
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/11
title: DPI awareness — Per-Monitor V2 manifest + hardcoded pixel audit
status: OPEN
priority: Major
category: feature
labels: [dpi, hdpi, manifest, ui, win10]
milestone: ~
created: 2026-04-08
source: AUDIT-WWMOD.md (WWMOD_010, P0 severity)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/11. This local document is retained as an engineering spec/evidence record.

## Summary

The project explicitly sets `<EnableDpiAwareness>false</EnableDpiAwareness>` in
the `.vcxproj`, making eMule DPI-unaware on Windows 10+. On high-DPI monitors
(125%–200% scaling) Windows bitmap-stretches the window, producing a blurry,
low-resolution UI. This is a **P0** modernization item — it directly degrades
the user experience on any modern laptop or 4K display.

## Current State

- `emule.vcxproj`: `<EnableDpiAwareness>false</EnableDpiAwareness>`
- No DPI-aware manifest entry
- Multiple hardcoded pixel values in dialog templates and code
- No `GetDpiForWindow()` or `GetSystemMetricsForDpi()` calls

## Fix

### Step 1 — Manifest change

Add `PerMonitorV2` DPI awareness to the application manifest
(`srchybrid/emule.manifest` or equivalent):

```xml
<application xmlns="urn:schemas-microsoft-com:asm.v3">
  <windowsSettings>
    <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">
      PerMonitorV2
    </dpiAwareness>
    <!-- Fallback for pre-1703 Windows (not required for Win10 1703+ target): -->
    <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">
      True/PM
    </dpiAware>
  </windowsSettings>
</application>
```

Remove `<EnableDpiAwareness>false</EnableDpiAwareness>` from `.vcxproj` (the
manifest takes precedence, but the explicit false is misleading).

### Step 2 — Audit hardcoded pixel values

After enabling DPI awareness, items sized in physical pixels will scale
incorrectly on non-100% displays. Audit and fix:

| Category | API to use |
|----------|-----------|
| System metrics (icon size, scrollbar width) | `GetSystemMetricsForDpi(metric, dpi)` |
| Font sizes | `CreateFontIndirect` with logical units (already DPI-scaled) |
| Toolbar/icon bitmaps | Load from image list at appropriate size via `LoadImage` with `LR_DEFAULTSIZE` |
| Dialog template pixel values | Use dialog units (DLUs) — these are already DPI-independent |
| Custom-painted pixel offsets | `MulDiv(value, GetDpiForWindow(hwnd), 96)` |

Primary audit targets:
- `srchybrid/ToolbarWnd.cpp` — toolbar bitmap pixel sizes
- `srchybrid/TransferDlg.cpp` — splitter pixel positions
- `srchybrid/StatisticsDlg.cpp` — graph pixel calculations
- `srchybrid/SearchResultsWnd.cpp` — column width defaults
- Any `Create(... cx, cy ...)` with hardcoded pixel dimensions

### Step 3 — Test on non-100% DPI

Verify on 125% and 150% scaling that:
- All dialogs are legible and not blurry
- Toolbar icons are the correct size
- Splitters and resize handles work correctly
- Column widths in list controls are proportionate

## Files to Modify

| File | Change |
|------|--------|
| `srchybrid/emule.manifest` | Add `PerMonitorV2` dpiAwareness entry |
| `emule.vcxproj` | Remove `<EnableDpiAwareness>false</EnableDpiAwareness>` |
| `srchybrid/ToolbarWnd.cpp` | Use DPI-aware image list sizing |
| `srchybrid/TransferDlg.cpp` | Replace hardcoded splitter pixels |
| Other files surfaced by DPI audit | Replace physical pixel constants |

## Acceptance Criteria

- [ ] Application manifest declares `PerMonitorV2` DPI awareness
- [ ] `<EnableDpiAwareness>false</EnableDpiAwareness>` removed from `.vcxproj`
- [ ] At 100% DPI: UI identical to current
- [ ] At 125% DPI: UI elements are crisp (not bitmap-stretched blurry)
- [ ] At 150% DPI: dialogs, toolbars, and list controls are correctly scaled
- [ ] No hardcoded physical pixel values in the audit targets listed above
- [ ] `GetDpiForWindow()` / `GetSystemMetricsForDpi()` used where system
      metrics are queried programmatically

## Note

This is the highest-severity WWMOD item (P0). It affects every user on a
laptop or monitor above 96 DPI (the current mainstream). DPI-awareness should
be enabled before any other WWMOD UI items so that subsequent UI changes are
developed against the correct rendering model.

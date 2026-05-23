---
id: FEAT-019
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/12
title: Dark mode UI — system-aware Windows 10 dark theme integration
status: OPEN
priority: Minor
category: feature
labels: [ui, dark-mode, dwm, win10, theming]
milestone: ~
created: 2026-04-10
source: eMuleAI (DarkMode.cpp/h, CDarkMode class, 2026)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/12. This local document is retained as an engineering spec/evidence record.

## Summary

Windows 10 (1809+) supports a system-wide dark mode toggle. Applications that do not opt in
display with a white/light window chrome even when the user has selected dark mode, which is
jarring on a dark desktop. eMule currently does not implement any dark mode support.

eMuleAI implements a comprehensive `CDarkMode` class that:
1. Detects the Windows dark mode preference via the registry
2. Hooks into the application's window creation to apply dark theming
3. Provides a full color mapping for all eMule UI elements (custom-drawn list views,
   progress bars, tab borders, server status colors, IRC colors, menu sidebar, etc.)
4. Integrates with `DwmApi` (`Dwmapi.lib`) for dark title bar support

## eMuleAI Reference Implementation

**Source files:**
- `eMuleAI/DarkMode.cpp` — full implementation
- `eMuleAI/DarkMode.h` — class interface and 30+ color constant definitions

**Color system:** eMuleAI defines a parallel color ID space (`COLOR_SHADEBASE=1000`
through `COLOR_IRC_ACTION_MSG=1025`) that overlays the standard MFC color IDs, allowing
existing custom-draw code to query themed colors by constant.

**Custom color IDs:**
```cpp
#define COLOR_SHADEBASE             1000
#define COLOR_SEARCH_DOWNLOADING    1001
#define COLOR_SEARCH_STOPPED        1002
#define COLOR_SEARCH_SHARING        1003
#define COLOR_SEARCH_KNOWN          1004
#define COLOR_SEARCH_CANCELED       1005
#define COLOR_MAN_BLACKLIST         1006
#define COLOR_AUTO_BLACKLIST        1007
#define COLOR_SPAM                  1008
#define COLOR_SERVER_CONNECTED      1009
#define COLOR_SERVER_FAILED         1010
#define COLOR_SERVER_DEAD           1011
#define COLOR_PROGRESSBAR           1012
#define COLOR_SELECTEDTABTOPLINE    1013
#define COLOR_TABBORDER             1014
// + MenuXP sidebar/title gradients, tooltip theme colors
```

**Tooltip theming:** `TooltipThemeColors` struct defines separate dark/light color sets for
tooltip backgrounds and caption backgrounds.

## Dependencies

- `Dwmapi.lib` — `#pragma comment(lib, "Dwmapi.lib")` (always present on Win10)
- `DWM_WINDOW_CORNER_PREFERENCE`, `DwmSetWindowAttribute` — for rounded corners and dark
  title bar (Win10 1809+ / Win11)
- **FEAT-017** (DPI awareness) — dark mode and Per-Monitor V2 DPI should land together;
  a blurry app in dark mode is doubly bad

## Implementation Notes

Dark mode detection in Windows uses the registry:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize
AppsUseLightTheme (DWORD) = 0 → dark mode active
```

Win11 also supports `DwmSetWindowAttribute(DWMWA_USE_IMMERSIVE_DARK_MODE)` to request a
dark title bar from the compositor.

The main challenge is eMule's extensive custom-drawn list controls (`CMuleListCtrl`,
`CListCtrlX`, download/shared lists). Each must be updated to query the themed color instead
of a hardcoded `GetSysColor()` value.

## Priority Note

This is a **Minor** UX feature, but it has high visibility — every Windows 10/11 user with
dark mode enabled immediately notices the mismatch. It pairs naturally with **FEAT-017**
(DPI awareness) as both are "modern Windows UI" improvements.

## Acceptance Criteria

- [ ] System dark mode preference detected at startup and on `WM_SETTINGCHANGE`
- [ ] Title bar rendered in dark mode (via `DwmSetWindowAttribute`)
- [ ] Main window background, list views, tab controls use dark colors when active
- [ ] Status bar, toolbar, progress bars themed
- [ ] Preferences panel indicates current theme
- [ ] No regression in light mode rendering
- [ ] Preferences toggle: force light/dark/auto (follow system)

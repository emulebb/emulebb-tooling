---
id: FEAT-119
workflow: local
github_issue:
title: Quick hide already-known files filter in search results
status: DONE
priority: Minor
category: feature
labels: [ui, search, filter, preferences, localization, 0.8.x]
milestone: 0.8.0
created: 2026-06-11
source: 2026-06-11 operator request for a quick show/hide of already-downloaded / shared / known search results
---

## Problem

Search results color-code files the user already has (downloading, shared,
previously downloaded/"known", cancelled) but there is no way to *hide* them. On a
busy search the rows you already have bury the new ones. Neither beba nor eMuleAI
offers this — they only tint known rows — so this is a new eMuleBB affordance.

## Decision / scope

- Add checkable **Hide from results ▸ Shared / Downloading / Downloaded / Cancelled**
  toggles to the existing results filter box (the magnifier `▾` dropdown), not a new
  toolbar. Default shows everything; the user opts in to hiding.
- The filter predicate classifies each row's known-state from the same
  download-queue / shared-files / known-files hash lookups the row colouring already
  uses, so it does not depend on paint-time `m_eKnown`.
- State persisted as a `CPreferences` bitmask; toggling re-filters the active tab
  immediately. No eD2K/Kad wire change; presentation + preferences only.

## Key files

- `srchybrid\SearchListCtrl.cpp` (`ResolveSearchKnownType` helper,
  `GetSearchItemColor`, `IsFilteredOut`, `AddResult`),
  `srchybrid\Preferences.h`/`.cpp` (`m_uSearchHideKnownStates`),
  `srchybrid\EditDelayed.h`/`.cpp` (generic opt-in menu extension),
  `srchybrid\SearchResultsWnd.h`/`.cpp` (submenu + toggle handling + re-filter),
  `srchybrid\MenuCmds.h`, `srchybrid\UserMsgs.h`, `srchybrid\emule.rc` + 43
  `lang\*.rc`.

## Acceptance criteria

- Filter-box dropdown shows a "Hide from results" submenu with four checkable
  states; toggling hides/shows matching rows in the active search and updates the
  count; column-filter selection and text filtering still work.
- Hidden-state choice persists across restart; default is show-all (no behaviour
  change when unset).
- Other filter boxes (downloads, shared files) are unaffected by the new menu.
- New `IDS_SEARCH_HIDE_FROM_RESULTS` label present in all 43 stock languages;
  `rc-localization-preflight.py` green.
- Debug|x64, Release|x64, Release|x64 diagnostics build clean; native + python
  suites pass; `validate` green.

## Outcome (2026-06-11)

- `SearchListCtrl.cpp`: `ResolveSearchKnownType` factored out of `GetSearchItemColor`
  and reused by `IsFilteredOut`; `AddResult` now always consults the filter; tab
  header count reflects the hide mask. Shared flags `ESearchKnownHideFlags` +
  `SearchKnownHideFlag()` live in `SearchFile.h`.
- Preference `m_uSearchHideKnownStates` (uint8 bitmask) added to `Preferences.h/.cpp`
  (ini key `SearchHideKnownStates`, default 0); registered in the build-tests
  preference inventory + regenerated schema manifest.
- `CEditDelayed` gained an opt-in `SetAllowOwnerMenuExtension`; raises
  `UM_FILTER_MENU_EXTEND` so the owner can append items and forwards foreign menu
  commands to the parent. `SearchResultsWnd` enables it, builds the "Hide from
  results" submenu, toggles the bits, and re-filters via `ReapplyActiveResultFilter`.
- Localization: `IDS_SEARCH_HIDE_FROM_RESULTS` added to `emule.rc` + all 43 stock
  languages; state items reuse existing `IDS_SHARED/DOWNLOADING/DOWNLOADED/CANCELLED`.
- Verification: 3 x64 builds clean; native doctest + python (1333) suites pass;
  `validate` + `rc-localization-preflight.py` green.

## Follow-up (2026-06-11)

Operator review: the dropdown must be **one level** (no flyout submenu) and the
states **single-select**, not independent checkboxes. Reworked to a flat radio group
appended directly to the filter dropdown — `Known` / `Downloaded` / `Shared` /
`Downloaded/Shared` / `No filter` (default) — where `Known` hides all known states
and `Downloaded/Shared` hides both. Added `IDS_SEARCH_HIDE_NO_FILTER` ("No filter")
across all 43 languages; the "Downloaded/Shared" label is composed from the existing
`IDS_DOWNLOADED`/`IDS_SHARED` strings.

Root cause of "filtering didn't work": the hide-command id block started at
`MP_FILTERCOLUMNS + 50` (11350), but `CEditDelayed::OnCommand` claimed
`<= MP_FILTERCOLUMNS + 50` as a filter-column selection, so the boundary hide id was
swallowed instead of forwarded to the parent. Moved the block clear to 11400 and
corrected the off-by-one bound to `< MP_FILTERCOLUMNS + 50`.

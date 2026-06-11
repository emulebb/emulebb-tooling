---
id: FEAT-120
workflow: local
github_issue:
title: Sortable Extension column in search results
status: DONE
priority: Minor
category: feature
labels: [ui, search, 0.8.x]
milestone: 0.8.0
created: 2026-06-11
source: 2026-06-11 operator request for an extension column in search results
---

## Problem

Search results expose a "Type" column (broad file-type group) but no column for the
raw file extension, so results cannot be grouped or sorted by extension (e.g. `pdf`).

## Decision / scope

- Add a new sortable **Extension** column to the search results list showing each
  result's lowercase filename extension without the leading dot (empty when none).
- Sort is case-insensitive with extensionless results at the bottom. Reuses the
  existing `IDS_SEARCHEXTENTION` ("Extension") label, so no new localization.
- Visible by default (placed after Type in the view-preset order); no eD2K/Kad wire
  change.

## Key files

- `srchybrid\SearchListCtrl.cpp` (`SEARCH_COLUMN_EXTENSION`, `GetSearchFileExtension`
  helper, `InsertColumn`, `iSubItems`, `Localize`, render, both sort comparators),
  `srchybrid\MuleListCtrlViewPresets.h` (`kSearchExtendedOrder`).

## Acceptance criteria

- Search results show an "Extension" column with the dot-less lowercase extension
  (e.g. `pdf`); clicking the header sorts ascending/descending; extensionless rows
  sort to the bottom.
- Saved layouts and the other columns are unaffected; the column is filterable via
  the existing filter box.
- Debug|x64, Release|x64, Release|x64 diagnostics build clean; `validate` green.

## Outcome (2026-06-11)

- `SearchListCtrl.cpp`: added `SEARCH_COLUMN_EXTENSION` (16) + `GetSearchFileExtension`
  helper (dot-less lowercase extension); wired `InsertColumn`, `iSubItems`, `Localize`
  (reusing `IDS_SEARCHEXTENTION`), the render switch, and both sort comparators
  (`CompareLocaleStringNoCase` for children, `CompareOptLocaleStringNoCaseUndefinedAtBottom`
  for the main list). `MuleListCtrlViewPresets.h`: `kSearchExtendedOrder` now places
  column 16 after Type, visible by default. No new localization strings.
- Verification: Debug/Release/Release-diagnostics x64 builds clean; `validate` green.

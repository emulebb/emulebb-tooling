---
id: FEAT-091
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/81
title: Downloads list expand/collapse-all peer rows
status: OPEN
priority: Minor
category: feature
labels: [downloads, ui, toolbar, keyboard-shortcuts, sources, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-25
source: operator request to defer downloads-list expand/collapse-all peer controls to future backlog
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/81. This local document is retained as an engineering spec/evidence record.

# FEAT-091 - Downloads list expand/collapse-all peer rows

## Summary

Add Downloads list controls that expand or collapse the source/peer rows for
every download currently shown in the active list view. This is a UI inspection
shortcut only; it must not request more sources, change transfer scheduling, or
mutate peer state.

The feature should expose both toolbar buttons and context-menu commands, with
keyboard shortcuts that fit existing tree/list conventions.

## Intended Shape

- Add `Expand all sources` and `Collapse all sources` commands for the
  Downloads list.
- Scope the action to the currently displayed Downloads list category/filter,
  including downloads not currently scrolled into view.
- Leave hidden categories and filtered-out downloads unchanged.
- Add toolbar buttons using classic eMule-style icons; prefer the existing
  `EXPANDALL` and `COLLAPSE` resources if they remain visually consistent with
  the 2000-era theme.
- Add matching context-menu commands near the existing expand/collapse actions.
- Add shortcuts:
  - `*` and numpad `*` expand all visible download peer rows.
  - `/` and numpad `/` collapse all visible download peer rows.
- Keep existing per-download expand/collapse behavior unchanged, including `+`,
  `-`, Alt+Right, Alt+Left, and double-click behavior.

## Scope Constraints

- Do not query the network, perform source discovery, or ask servers/Kad/peers
  for more sources.
- Do not alter transfer state, source state, priorities, categories, or
  scheduling.
- Do not modernize the toolbar visual style beyond the classic eMule theme.
- Do not combine this item with broad high-volume list virtualization work;
  coordinate with `FEAT-082` if bulk expansion exposes performance issues.

## Candidate Implementation Notes

- Add command IDs in the free range after current home-menu IDs and before
  quick-speed IDs.
- Implement bulk actions in `CDownloadListCtrl` by snapshotting currently
  displayed top-level download rows before inserting or removing source rows.
- Reuse existing `ExpandCollapseItem(..., EXPAND_ONLY)` and `HideSources(...)`
  paths where practical so rendering and stale-row handling stay consistent.
- Route toolbar commands from `CTransferWnd` into `downloadlistctrl`; route menu
  and shortcut commands through the list control command path.
- Extend `DownloadListKeyboardShortcutsSeams` and focused native shortcut tests
  for `*` and `/`.

## Acceptance Criteria

- [ ] The Downloads toolbar exposes expand-all and collapse-all peer-row
      buttons when that toolbar is visible.
- [ ] The Downloads context menu exposes matching commands.
- [ ] `*` and numpad `*` expand source/peer rows for all downloads in the
      current visible category/filter.
- [ ] `/` and numpad `/` collapse expanded source/peer rows for all downloads
      in the current visible category/filter.
- [ ] Hidden categories and filtered-out downloads are unaffected.
- [ ] Existing single-download expand/collapse shortcuts and double-click
      behavior remain unchanged.
- [ ] The commands do not start network source discovery or alter transfer,
      source, priority, or category state.
- [ ] The selected icons match the classic eMule visual style or fall back to
      existing resources.

## Validation

- `python -m emule_workspace validate`
- focused native tests for `DownloadListKeyboardShortcutsSeams`
- manual UI smoke covering toolbar commands, context-menu commands, current
  category scope, hidden category behavior, and existing per-download shortcuts
- x64 Debug and Release app builds before implementation commit

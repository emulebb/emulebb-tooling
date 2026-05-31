---
id: FEAT-101
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/108
title: Add quick filter textbox to Downloads list
status: OPEN
priority: Minor
category: feature
labels: [downloads, ui, filtering, focus, large-lists, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-31
source: operator request for a Downloads-list quick filter textbox
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/108. This local document is retained as an engineering spec/evidence record.

# FEAT-101 - Add Quick Filter Textbox To Downloads List

## Summary

Add a quick filter textbox to the Downloads list so users can narrow visible
transfer rows without changing transfer state. The filter should be a local
view concern: it combines with the active category/list filter, hides
non-matching displayed rows, and restores the same category view when cleared.

This is separate from broad list virtualization work, but it must be designed
so large transfer lists do not rebuild expensively on every keystroke.

## Intended Shape

- Add a compact quick filter textbox in the Downloads view near the existing
  list controls.
- Provide a clear action that empties the filter and restores the active
  category/list view.
- Match visible download text such as filename, status, category, priority,
  size, speed, remaining time, and already materialized peer/source labels where
  practical.
- Combine with the currently selected category/filter instead of replacing it.
- Keep matching case-insensitive and predictable; avoid regex or advanced query
  syntax in the first slice.
- Debounce typing or reuse existing list refresh seams if needed for large
  transfer lists.
- Preserve normal Downloads keyboard navigation. The textbox should have a
  clear focus path back to the list and should not steal existing list shortcuts
  once focus has returned to the list.

## Scope Constraints

- Do not pause, resume, reprioritize, request sources, or mutate category
  membership.
- Do not query the network or perform source discovery.
- Do not replace existing category tabs, transfer filters, or search behavior.
- Do not introduce a heavyweight global search feature under this item.
- Do not couple filtering to persisted preferences unless a later UX pass asks
  for saved filter state.

## Candidate Implementation Notes

- Prefer a display-filter seam that evaluates the current top-level transfer
  rows before list materialization.
- Define explicit behavior for expanded source rows:
  - if a download row matches, its visible expanded source rows may remain shown
  - if only a source row matches, the parent download row should remain visible
    so the match has context
  - clearing the filter should restore previous expansion state where practical
- Preserve selection where the selected row remains visible; otherwise move
  selection to the next visible transfer row without changing transfer state.
- Add focused tests around filter predicates and list-state restoration instead
  of relying only on manual UI smoke.

## Acceptance Criteria

- [ ] Downloads view exposes a quick filter textbox with a clear action.
- [ ] Typing filters displayed download rows within the currently selected
      category/filter.
- [ ] Clearing the textbox restores all rows for the active category/filter.
- [ ] Filtering is case-insensitive and display-only.
- [ ] Selection, focus, and expanded source-row behavior are predictable when
      rows are hidden and restored.
- [ ] Filtering does not mutate transfer, source, priority, or category state.
- [ ] Focused tests cover filter matching, clear behavior, category
      interaction, source-row context, and no transfer-state mutation.

## Validation

- `python -m emule_workspace validate`
- focused native tests for the Downloads filter predicate and list restore path
- manual UI smoke covering category interaction, focus return, clear action,
  expanded source rows, and large-list typing responsiveness
- x64 Debug and Release app builds before implementation commit

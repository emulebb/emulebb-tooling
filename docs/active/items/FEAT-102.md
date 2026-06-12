---
id: FEAT-102
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/116
title: Exclude known files from search results
status: OPEN
priority: Minor
category: feature
labels: [search, filtering, known-files, downloads, shared-files, post-0.7.3]
milestone: post-0.7.3
created: 2026-05-31
source: operator request to focus search results on files not already known locally
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/109. This local document is retained as an engineering spec/evidence record.

# FEAT-102 - Exclude known files from search results

## Summary

Add search-result filtering for files already known to the local profile so the
user can focus on files they do not already have. The filter should support
separate known-file scopes where reliable data is available, starting with
shared files and currently downloading files.

This is a local display filter. It should not change outgoing server/Kad search
requests unless a later protocol-safe design explicitly opts into that.

## Intended Shape

- Add a visible, reversible search-result filter for locally known files.
- Support independent scope choices where practical:
  - shared files
  - currently downloading files
  - completed/known local files
  - cancelled or rejected records only if the identity data is reliable enough
- Prefer file-hash matching as the primary identity check.
- Use conservative visible metadata fallback only when no hash is available;
  avoid hiding rows on weak filename-only guesses by default.
- Preserve hidden rows locally where possible so disabling the filter restores
  results without rerunning the search.
- Make the filter combine predictably with existing result-type, availability,
  and text filters.

## Scope Constraints

- Do not alter search packets sent to servers, Kad, or peers in the first
  implementation slice.
- Do not mutate known-file, shared-file, cancelled-file, transfer, category, or
  priority state.
- Do not treat filename-only matches as authoritative duplicates.
- Do not remove or bypass existing duplicate detection and download-intake
  guards.
- Do not require a full shared-file reload to update the filter state.

## Candidate Implementation Notes

- Build a lightweight known-file identity snapshot for search filtering.
- Source the snapshot from existing shared-file, download, known-file, and
  cancelled-file indexes where they are already maintained.
- Keep scope toggles explicit instead of overloading the existing search text
  box.
- For active downloads, match by part-file hash when available and refresh
  filter state when a pending result becomes a started download.
- Add seam tests for hash-scope filtering before wiring the UI so the behavior
  is locked before visual controls are added.

## Acceptance Criteria

- [ ] Search results can hide files already shared by the local profile.
- [ ] Search results can hide files currently downloading.
- [ ] Shared and downloading scopes can be toggled independently.
- [ ] Additional known-file scopes are only enabled when identity data is
      reliable enough to avoid false hiding.
- [ ] Disabling the filter restores locally retained result rows without
      rerunning the search where practical.
- [ ] Filtering uses hash identity where possible and avoids authoritative
      filename-only duplicate decisions by default.
- [ ] Filtering does not mutate known-file, shared-file, cancelled-file,
      transfer, priority, or category state.
- [ ] Focused tests cover hash matching, scope combinations, restore behavior,
      stale snapshot handling, and no transfer-state mutation.

## Validation

- `python -m emule_workspace validate`
- focused native tests for search-result known-file filter predicates
- focused native tests for scope combinations and result restoration
- manual UI smoke covering shared-file, active-download, mixed-scope, and
  clear-filter behavior
- x64 Debug and Release app builds before implementation commit

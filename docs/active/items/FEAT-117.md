---
id: FEAT-117
workflow: local
github_issue:
title: Indicate already-shared files in the unshared-folder share preview
status: OPEN
priority: Minor
category: feature
labels: [shared-files, ui, ux, share-preview]
milestone: 0.8.x
created: 2026-06-10
source: operator report - unshared folder shows an empty file list when its files are already shared from another folder
---

# FEAT-117 - Indicate Already-Shared Files In The Unshared-Folder Share Preview

## Summary

When a user selects an unshared folder in the Shared Files "All Directories"
tree, the file pane shows that folder's on-disk files with checkboxes so they can
be shared individually (`CSharedFilesCtrl::AddShareableFiles`). Files whose
content is **already shared from another folder** (same eD2K identity) are
silently omitted, so a folder full of files can render as an empty list and look
like a broken view.

Provide a visual affordance that the files exist but are already shared
elsewhere, instead of hiding them.

## Background / Evidence

eMule keys files by content identity, not path. In `AddShareableFiles`
(`srchybrid/SharedFilesCtrl.cpp:2724`) the intake gate is:

```cpp
CKnownFile *toadd = FindKnownFile(name, date, size);
if (toadd == NULL || sharedfiles->GetFileByID(toadd->GetFileHash()) == NULL) { ...add... }
```

Already-shared files fail this test and are skipped, and the global shared list
shows them under their real shared directory, which fails the directory-equality
filter for the browsed folder (`ShouldDisplayFile`, `SharedFilesCtrl.cpp:1017-1023`).

Reproduced operator case: `…\pack 2025.01 [peerius] mp3, music\drudi` (unshared)
holds 7 tracks that are byte-identical (same name, size, and mtime) to tracks
already shared from `…\pack 2022.11 [peerius] mp3, music\…\drudi`. The unshared
folder therefore previews as empty even though the files are present. This is
correct dedup, but the empty list is misleading.

This is stock eMule behavior, not an eMuleBB regression - it is a UX improvement,
not a bug fix.

## Proposed Behavior

Preferred (per-row): in the unshared-folder preview, also list files that are
already shared from another location, rendered as read-only / checked / dimmed
rows with an "already shared (from <directory>)" hint (a column value or
tooltip). The share checkbox is non-interactive for these rows because the
content is already shared via another path and cannot be re-shared under a second
identity.

Lighter fallback (status line): keep hiding the rows but show a one-line note
when a non-empty unshared folder yields zero shareable rows, e.g. "N file(s) in
this folder are already shared from another location."

## Constraints

- UI-only. No change to share/known-file persistence, hashing, or eD2K identity
  behavior. The dedup itself stays intact.
- Minimum drift from stock behavior; preserve current behavior when there is no
  already-shared overlap.
- The virtualized list keys visible rows by pointer
  (`m_mapVisibleFileIndex`), so distinct marker objects for the same hash must
  not corrupt the index or sort.
- Do not let already-shared marker rows be toggled into a confusing single-file
  share/unshare on a duplicate path.

## Acceptance Criteria

- [ ] Selecting an unshared folder whose files are already shared elsewhere no
      longer shows a misleading empty list.
- [ ] Already-shared entries are visually distinct and indicate where the content
      is shared from.
- [ ] Not-yet-shared files keep their normal interactive share checkbox.
- [ ] Toggling is disabled (or clearly explained) for already-shared entries.
- [ ] Folders with no already-shared overlap behave exactly as before.
- [ ] Debug, Release, and diagnostics Release x64 app builds pass before commit.

## Release Note

This is post-0.7.3 UX work. It must not enter the 0.7.3 RC line under the active
release freeze; it targets the 0.8.x modernization line.

---
id: FEAT-010
title: Long path support phase 2 — shell/UI, shared-directory recursion, exact-name paths, and path-helper audit
status: Done
priority: Minor
category: feature
labels: [longpath, max-path, windows, filesystem, shell, ui]
milestone: ~
created: 2026-04-08
source: docs/history/features/GUIDE-LONGPATHS-IMPLEMENTATION.md + feature/windows-long-paths audit
---

## Summary

Core long-path support is already landed on `main` for filesystem operations. Phase 2
shell/UI hardening, exact-name path support, share-recursion unification, and helper
cleanup are now merged to `main`.

The implementation now covers:

- recycle-bin delete through `IFileOperation` instead of `SHFileOperation`
- dynamic path-helper cleanup for shell-facing module/profile/path assembly
- shared `IFileDialog` wrappers for file/folder pickers
- centralized shell icon/display fallback behavior for overlong paths
- silent `.lnk` ignore-by-extension in the relevant share/incoming scans
- dynamic skin-resource path resolution without `MAX_PATH` scratch buffers
- consolidation of generic path semantics into `PathHelpers` and shell/UI policy into `ShellUiHelpers`
- one shared recursive share/unshare engine used by both the options directory selector and the Shared Files tree
- canonical path matching across DOS paths, `\\?\` paths, slash variants, dot-segments, and 8.3 aliases
- migration of persisted 8.3 shared entries to canonical long-name spellings during load
- exact-name namespace handling for paths that need Win32 namespace semantics to preserve leading/trailing spaces, trailing dots, and reserved DOS device-looking names such as `NUL.txt`
- directory recursion guards by filesystem object identity so junction/symlink loops do not explode recursive sharing
- deterministic regression coverage in `emulebb-build-tests` for delete, path-helper, shell/UI, exact-name, and shared-directory recursion behavior

## Already Landed On Main

The following are no longer backlog items:

- `x64` and `ARM64` manifests carry `<ws2:longPathAware>true</ws2:longPathAware>`
- startup detects and logs whether `LongPathsEnabled` is enabled
- `LongPathSeams` centralizes Win32 file APIs, CRT-bypass file descriptors, `FILE*` streams, and MFC safe-file opens
- part files, config files, archive/import flows, ZIP/GZIP, web cert/key output, and similar high-value paths already use the shared long-path model
- real filesystem tests now cover long Unicode paths, Cyrillic/emoji path segments, generated payloads, copy/move/delete flows, and parity-style reference coverage

## Implemented Scope

The active stabilization branches now cover the full FEAT-010 shell/UI and share-state tail:

- `PathHelpers.h`: permanent generic path-helper layer for separator normalization, extended-length prefix handling, directory canonicalization, path joins, dynamic module/shell-folder retrieval, and related path-shape rules
- `ShellUiHelpers.h`: permanent shell/UI helper layer for picker normalization, shell icon/display fallback policy, shortcut ignore rules, and skin-resource resolution
- `Ini2Helpers.h`: INI-specific helper layer trimmed down to config/path decisions that reuse `PathHelpers` instead of duplicating generic path logic
- `OtherFunctions.cpp/.h`: shared `IFileDialog` wrappers for folder pick, file open, and file save; compatibility entrypoints retained for `SelectDir(...)` and `DialogBrowseFile(...)`
- `PartFileConvert.cpp`, `TreeOptionsCtrl.cpp`, `KnownFile.cpp`, `PPgFiles.cpp`, `MuleToolBarCtrl.cpp`, `StatisticsTree.cpp`, `CatDialog.cpp`, `PPgDirectories.cpp`: migrated remaining browse/picker call sites to the shared wrappers
- `DirectoryTreeCtrl.cpp`, `SharedDirsTreeCtrl.cpp`, `Emule.cpp`: centralized icon/display fallback behavior for shell-facing UI
- `PPgDirectories.cpp`, `SharedFileList.cpp`, `SharedFilesCtrl.cpp`: `.lnk` files are now ignored by extension in the relevant share/incoming scans instead of consulting shell metadata
- `FileInfoDialog.cpp`, `MiniMule.cpp`, `OtherFunctions.cpp`: path-helper/module-path tails removed in the earlier FEAT-010 path-helper slice
- `Emule.cpp`, `MuleListCtrl.cpp`: skin resource and background image resolution now use dynamic helper paths rather than `MAX_PATH` buffers
- `TreeOptionsCtrl.cpp/.h`, `OtherFunctions.cpp/.h`: dead legacy picker-era code was removed, including `CTreeOptionsFileDialog`, `SHBrowseSetSelProc`, and the unused raw-buffer `SelectDir(HWND, LPTSTR, ...)` overload
- broader `srchybrid` callers now use shared helper rules instead of duplicated `slosh` / `unslosh` / `MakeFoldername` semantics
- `DirectoryTreeCtrl.cpp`, `SharedDirsTreeCtrl.cpp`, `SharedDirectoryOps.h`: recursive share/unshare and descendant enumeration now go through one shared long-path-aware engine instead of divergent UI-local recursion
- `SharedFileList.cpp`, `SharedFilesCtrl.cpp`, `Preferences.cpp`, `ListenSocket.cpp`, `KnownFileList.cpp`, `CatDialog.cpp`: share-sensitive path matching now uses semantic path equality instead of raw spelling checks
- `LongPathSeams.h`: exact-name prefixing now covers trailing dot, leading/trailing ASCII space, and reserved DOS device-looking path components that require namespace semantics to preserve the real Win32 name
- `LongPathSeams.h`, `SharedDirectoryOps.h`: recursive shared-directory expansion now uses directory object identity (volume serial + file ID) to suppress duplicate-target traversal and stop reparse-point loops
- `SharedFileList.cpp`, `SharedFilesCtrl.cpp`, `PathHelpers.h`: drag/drop intake, single-share handling, and directory/file scans no longer rely on `CFileFind`; path-sensitive probes and enumeration now go through the shared helper/seam stack
- `Preferences.cpp`: loaded shared-directory and single-share entries are opportunistically migrated from 8.3 aliases to canonical long-name spellings

There are no remaining `TODO:MINOR(FEAT-010)` or `TODO:MINOR(longpath)` markers in the audited shell/UI long-path surface.

## Fallback Policy

The Phase 2 implementation uses explicit shell/UI fallback behavior instead of relying on incidental shell success:

- icon lookup uses stable extension/attribute-based queries where possible rather than probing the full overlong path
- shell display names are optional enrichment; when the shell cannot provide one safely, existing caller text is preserved
- picker flows return full `CString` paths from shared modern wrappers instead of caller-owned `MAX_PATH` arrays
- `.lnk` files are ignored by extension in the relevant share/incoming warning flows instead of following shell metadata
- directory-valued paths now share one normalization contract through `PathHelpers` instead of per-call-site trailing-`\` logic
- exact-name paths that cannot be represented safely at shell boundaries stay on the filesystem-facing `LongPathSeams` path and do not get silently normalized into lossy shell spellings

## Test Expansion

The stabilization branches now include:

- deep Unicode delete coverage for recycle-bin-enabled and direct-delete routing
- path-helper coverage for module paths, canonicalization, MediaInfo path joins, and MiniMule resource URLs
- shell/UI seam coverage for shortcut ignore rules, shell display fallback gating, icon-query routing, picker path splitting/finalization, and skin-resource resolution
- real-filesystem coverage for exact-name folders/files beginning or ending with `.`, ASCII space, NBSP, and EM SPACE
- real-filesystem coverage for reserved DOS device-looking names such as `NUL.txt`
- share-list/path-matching coverage for prefixed vs unprefixed, 8.3 vs long-name, and exact-name spellings
- shared-directory recursion coverage for junction alias dedupe and junction-loop suppression by filesystem identity

Remaining optional verification is manual smoke coverage for representative browse/icon flows on a live UI.

## Final Helper Architecture

The active stabilization branches now use a permanent helper split instead of the earlier
transitional seam naming:

- `PathHelpers`: generic path semantics only
- `ShellUiHelpers`: shell/UI policy only
- `OtherFunctionsSeams`: delete-route seam/injection only where tests need it

This cleanup also removes duplicate extended-length prefix handling, duplicate
trailing-separator helpers, and duplicate directory-shape normalization from the audited
and overlapping `srchybrid` long-path surface.

For share-state specifically, the permanent split is now:

- `PathHelpers`: canonical path normalization, comparison, containment, and enumeration helpers
- `LongPathSeams`: filesystem-facing Win32 calls and exact-name namespace preparation
- `SharedDirectoryOps`: the only recursive share/unshare implementation used by both directory trees
- `ShellUiHelpers`: only shell-boundary policy and fallback behavior

## Acceptance Criteria

- [x] Shell icon/display lookup is centralized and no longer scattered across the audited tree/list controls
- [x] Overlong paths still get sensible icons or graceful fallback behavior in directory/file UI
- [x] Browse-dialog flows are audited and routed through shared modern wrappers in the audited files
- [x] Delete-to-recycle-bin behavior for deep paths is explicitly hardened
- [x] Fixed-buffer path composition used in real path construction is reduced or eliminated in the audited files
- [x] Options-tree and Shared Files recursive share/unshare behavior now use one implementation
- [x] Share matching is stable across `\\?\`, 8.3 aliases, exact-name namespace paths, and normal DOS spellings
- [x] Recursive shared-directory expansion does not loop forever through junction/reparse aliases
- [ ] Manual smoke checks cover icon lookup and browse flows for deep Unicode paths where the shell APIs permit it

## Explicit Boundaries

This item intentionally stops short of a full filesystem-object identity model for every path in the app.

- file-level hard-link dedupe is not implemented
- symlinked files outside shared-directory recursion are still matched by canonical path spelling, not file ID
- alternate data streams such as `file.txt:stream` are not first-class app paths
- nonstandard namespaces such as `\\.\`, `\??\`, or `\\?\GLOBALROOT` are not first-class app paths
- no live UNC/SMB share smoke test is recorded in this item yet

## Reference

- Core implementation spec: `docs/history/features/GUIDE-LONGPATHS-IMPLEMENTATION.md`
- Microsoft shell/file API notes:
  - <https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-shfileopstructa>
  - <https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createdirectoryw>
  - <https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew>
  - <https://learn.microsoft.com/en-us/windows/win32/api/shlwapi/nf-shlwapi-pathcanonicalizew>

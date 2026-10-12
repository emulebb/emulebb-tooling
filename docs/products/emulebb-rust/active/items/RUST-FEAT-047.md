---
id: RUST-FEAT-047
workflow: local
title: Recognize already-downloaded files to avoid duplicate downloads
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, dedupe, library]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K download-completeness audit 2026-10-12 vs community-0.72, emulebb-mfc
---

# RUST-FEAT-047 - Recognize already-downloaded files to avoid duplicate downloads

## Summary

When a new download request is created, check whether the file hash is already
present in the local library/shared catalog and, if so, surface that instead of
starting a redundant download. MFC does this through the remembered known files
(`known.met` / `known2.met`); the Rust import machinery exists for sharing but
is not consulted at download-request time.

## Current State

- `crates/emulebb-core/src/shared_directories.rs:826`
  `imported_known_file_identity_index()` and `:1406`
  `promote_imported_known_file()` serve the shared-library import/reload path,
  not download dedupe.
- No explicit "this ED2K link hash is already in my library -> skip/confirm"
  check was found at download-request creation.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `KnownFile.cpp:818` notes that known-file tags are purged only for files not
  seen/shared for a long time; `KnownFileList.cpp:410`
  `AddKnownFileAICHHash` indexes remembered files; `SHAHashSet.h:68-70`
  defines `KNOWN2_MET_FILENAME` / version.

## Why This Matters

Re-adding a link whose content is already present should not silently re-spend
bandwidth and disk. It is both a correctness (duplicate library entries) and a
resource question.

## Representative Sites

- `crates/emulebb-core/src/shared_directories.rs` - imported-known-file index
- `crates/emulebb-core/src/ed2k_sources.rs` - download source acquisition
- `workspaces/workspace/app/emulebb-main/srchybrid/KnownFileList.cpp` -
  remembered-file index

## Intended Shape

- At download-request creation, look up the hash in the local shared catalog
  and the imported known-file index.
- Report `already-present` (with the local path and name) through the
  Rust-native API, with a documented confirm/skip policy rather than a silent
  second copy.

## Scope Constraints

- Do not block share-in-place or prevent an explicit re-download when the
  operator wants one.
- Additive API state only; no wire change.

## Acceptance Criteria

- [ ] A download request whose hash already exists locally is detected and
      reported before any transfer starts.
- [ ] The API exposes the existing path/name and a documented skip or confirm
      behavior.
- [ ] A test covers hash-present and hash-absent request paths.

## Validation

- Runtime test creating a request for an already-imported hash and asserting
  no transfer job is started and the API reports the existing file.

## Notes

First confirm current behavior end-to-end; the import index may already have
the lookup primitive needed.

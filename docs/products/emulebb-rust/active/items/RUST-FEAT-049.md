---
id: RUST-FEAT-049
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/92
title: Add per-file share exclusions with a built-in default ignore set
status: OPEN
priority: Minor
category: feature
labels: [rust, sharing, exclude, watcher, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: feature-backlog chat 2026-10-12 vs emulebb-mfc, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/92. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-049 - Add per-file share exclusions with a built-in default ignore set

## Summary

Let the operator exclude specific files from the shared catalog, persisted
across reloads and restarts, and apply a built-in default ignore set made of
the "usual suspects" (eMule's own data/runtime files that can live inside a
shared root) plus a curated "suggested set" of common noise files. Excluded
files must never re-enter the catalog through the watcher, reload, or ingest.

## Current State

- `crates/emulebb-core/src/shared_directories.rs:18-26`
  `SharedDirectoryRoot` carries only `path`, `monitor_owned`, `shareable`, and
  `accessible`; there is no per-file or per-pattern exclusion.
- No exclusion filtering exists in the shared-directory walk, reload, ingest,
  or watcher paths, so an excluded file would be re-added on the next pass.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `SharedFileList.cpp:3556` `ExcludeFile` adds a file to
  `m_liSingleExcludedFiles` and `AddSingleExcludedFileRuleKey`.
- `SharedFileList.cpp:3097` `HasSingleExcludedFileRule` gates the scan/hash
  paths (used at `:3519`, `:3530`, `:3945`).
- `SharedFileList.cpp:4993` / `:5033` persist exclusions with a `-` prefix in
  preferences and restore them on load.
- `SharedFileList.cpp:2030,2118,3945` `ShouldIgnoreSharedFileCandidate` is the
  built-in "usual suspects" filter applied before the exclusion-rule check.

## Why This Matters

Exclusions only work if the daemon itself enforces them on every ingest path;
an external script cannot stop the watcher from re-adding a file. The built-in
set also prevents the client from publishing its own metadata and common
filesystem noise, which is exactly the eMule/MFC behavior.

## Representative Sites

- `crates/emulebb-core/src/shared_directories.rs` - root model and directory
  walk
- `crates/emulebb-core/src/shared_dir_monitor.rs` - watcher/reload
- `crates/emulebb-core/src/shared_file_api.rs` - shared-file REST surface
- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs` - ingest path
- `workspaces/workspace/app/emulebb-main/srchybrid/SharedFileList.cpp` -
  `ExcludeFile`, `ShouldIgnoreSharedFileCandidate`

## Intended Shape

- Persist per-file excluded-path rules and check them in the shared-directory
  walk, reload, ingest, and watcher so excluded files never become shared
  entries.
- Apply a built-in default ignore set composed of:
  - the "usual suspects": eMule's own data/runtime files that may sit inside a
    shared root (for example `known.met`, `known2_64.met`, `preferences.dat`,
    `clients.met`, `server.met`, `*.part.met`, `*.tmp`);
  - a curated "suggested set": common filesystem noise (for example
    `desktop.ini`, `Thumbs.db`, `.DS_Store`, `._*`, `*.bak`).
- Keep the defaults overridable: exclusions are additive, removable, and
  surfaced through the shared-files API (list / add / remove).

## Scope Constraints

- No wire/protocol change; exclusion only affects local sharing, server
  offerfiles, and Kad publish candidate selection.
- Use the same canonical path identity as RUST-BUG-107 so case and
  normalization cannot dodge a rule.
- Completed download payloads and their delivery are unaffected.

## Acceptance Criteria

- [ ] Excluding a file persists across watcher reloads and daemon restarts.
- [ ] Excluded files never appear in the shared catalog, server offerfiles, or
      Kad publish candidates.
- [ ] The built-in "usual suspects" and "suggested set" are applied by default
      and are individually removable.
- [ ] The API exposes list/add/remove exclusion operations.

## Validation

- Watcher/reload and persistence round-trip tests proving an excluded file is
  not re-ingested.
- Offerfiles and Kad publish-candidate tests asserting excluded hashes are
  absent.
- Case/normalization tests using the RUST-BUG-107 canonical identity.

## Notes

The persisted rule model and canonical keys should land with RUST-BUG-107 so
the exclusion and path-identity work share one definition. Optional
per-directory glob exclusions are a later layer, not part of this item.

---
id: RUST-FEAT-047
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/90
title: Persist completed-file identity to prevent duplicate downloads
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, dedupe, library]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K download-completeness audit 2026-10-12 vs community-0.72, emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/90. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-047 - Persist completed-file identity to prevent duplicate downloads

## Summary

Persist the identity of successfully completed downloads and consult that
history whenever a new transfer is requested. Shared-library and active-transfer
indexes remain useful live evidence, but they cannot remember a completed file
after the operator moves, unshares, or deletes it. The duplicate decision must
therefore survive both file removal and daemon restart.

## Current State

- `crates/emulebb-core/src/shared_directories.rs:826`
  `imported_known_file_identity_index()` and `:1406`
  `promote_imported_known_file()` serve the shared-library import/reload path,
  not download dedupe.
- Active transfer state can reject a duplicate currently in progress, but no
  durable completed-download identity store exists.
- No single transfer-creation authority combines active transfers, the current
  shared catalog, imported known files, and completed history.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `KnownFile.cpp:818` notes that known-file tags are purged only for files not
  seen/shared for a long time; `KnownFileList.cpp:410`
  `AddKnownFileAICHHash` indexes remembered files; `SHAHashSet.h:68-70`
  defines `KNOWN2_MET_FILENAME` / version.

Current aMule additionally writes completed identities to `knownhistory.met`,
which preserves the user-facing "already downloaded" decision independently of
whether the completed payload remains shared.

## Why This Matters

Re-adding a completed hash should not silently re-spend bandwidth and disk just
because the payload was moved out of the shared library. This is a durable user
intent and resource-protection concern, not merely a current-path lookup.

## Representative Sites

- `crates/emulebb-core/src/shared_directories.rs` - imported-known-file index
- `crates/emulebb-core/src/transfer_create_api.rs` - transfer-creation authority
- `crates/emulebb-core/src/ed2k_sources.rs` - download source acquisition
- `workspaces/workspace/app/emulebb-main/srchybrid/KnownFileList.cpp` -
  remembered-file index
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\KnownFileList.cpp` -
  `knownhistory.met` persistence

## Intended Shape

- Add a current-only completed-file identity store keyed by ED2K hash. Store
  the canonical completed name, size, completion time, and known AICH root when
  available; do not make an obsolete path the identity.
- Record completion atomically before active-transfer cleanup removes the only
  durable evidence.
- Route every transfer-creation entry point through one duplicate-decision
  service that checks active transfers, current shared/imported identities, and
  completed history.
- Return a structured conflict describing the matching evidence and require an
  explicit re-download override instead of silently starting or silently
  discarding the request.

## Scope Constraints

- Do not block share-in-place or prevent an explicit re-download when the
  operator wants one.
- No wire change. The beta REST and persistence schemas may break to express a
  clean current model; do not add compatibility aliases or migrations.
- A moved or deleted completed payload remains history, but must not be
  represented as a currently accessible local path.

## Acceptance Criteria

- [ ] Successful completion durably records the ED2K hash and metadata before
      active-transfer cleanup.
- [ ] Duplicate decisions combine active, shared/imported, and completed-history
      evidence before any transfer or source-acquisition work starts.
- [ ] Detection survives daemon restart and removal of the completed payload
      from the shared library.
- [ ] The API returns structured evidence and requires an explicit override to
      re-download; stale history never claims a live path.
- [ ] Tests cover active, shared, historical, absent, restart, removed-file, and
      explicit-override paths.

## Validation

- Persistence and runtime tests proving completion recording, restart survival,
  and duplicate rejection before transfer creation.
- API/OpenAPI/WebUI validation for the structured conflict and explicit
  re-download override.

## Notes

The shared import index may supply one evidence source, but it is not the
completed-history authority.

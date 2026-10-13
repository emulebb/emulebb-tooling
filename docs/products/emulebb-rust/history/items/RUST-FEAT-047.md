---
id: RUST-FEAT-047
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/90
title: Persist completed-file identity to prevent duplicate downloads
status: DONE
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

- Metadata schema `31` owns a pathless `download_history` identity store keyed
  by ED2K hash. The authoritative completion-manifest transaction records it
  only for completed, final-rehash-clean downloads.
- `Ed2kTransferRuntime::download_evidence()` classifies active transfers,
  filesystem-verified current local files, and prior completion history without
  converting stale history into a live-path claim.
- `EmulebbCore::preflight_downloads()` is the single duplicate-decision
  authority for both ED2K-link and search-result creation. A global creation
  gate keeps preflight and mutation ordered across concurrent requests.
- REST exposes `knownFilePolicy=reject|redownload` and typed
  `DOWNLOAD_CONFLICT` evidence. WebUI starts with `reject` and retries with
  `redownload` only after explicit confirmation.

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

- [x] Successful completion durably records the ED2K hash and metadata before
      active-transfer cleanup.
- [x] Duplicate decisions combine active, shared/imported, and completed-history
      evidence before any transfer or source-acquisition work starts.
- [x] Detection survives daemon restart and removal of the completed payload
      from the shared library.
- [x] The API returns structured evidence and requires an explicit override to
      re-download; stale history never claims a live path.
- [x] Tests cover active, shared, historical, absent, restart, removed-file, and
      explicit-override paths.

## Validation

- `cargo test -p emulebb-metadata -p emulebb-ed2k -p emulebb-core -p emulebb-rest`
- `cargo clippy -p emulebb-metadata -p emulebb-ed2k -p emulebb-core -p emulebb-rest --all-targets -- -D warnings -A unfulfilled-lint-expectations`
- `npm run test:unit`, `npm run build`, and `npm run test:e2e` in `webui`.
- OpenAPI YAML parse plus `check-rust-openapi-routes.py`; the checker retains one
  unrelated pre-existing drift for search-result `sort` and `order` query
  parameters.

## Notes

The shared import index may supply one evidence source, but it is not the
completed-history authority.

- Completed on 2026-10-13 in emulebb-rust commits `576f1b53`, `995efd2a`,
  `b09063f7`, `50c14ca1`, `abf711c8`, `b401bf08`, `aeeff64b`, and `35be62f7`,
  with OpenAPI contract commit `6b83783` in emulebb-tooling.
- Final validation passed 38 metadata tests, 1,035 ED2K tests, all 399 core unit
  tests and integrations, 117 REST unit tests and 2 REST integrations, strict
  all-target Clippy for all affected crates, 28 WebUI unit tests, the production
  WebUI build, and all 16 Playwright tests.

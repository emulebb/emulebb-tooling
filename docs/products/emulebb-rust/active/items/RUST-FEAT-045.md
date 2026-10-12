---
id: RUST-FEAT-045
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/88
title: Retain and expose multiple per-source filenames for downloads
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, filename, metadata, api]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K download-completeness audit 2026-10-12 vs community-0.72, emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/88. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-045 - Retain and expose multiple per-source filenames for downloads

## Summary

Keep every distinct filename reported for a download, with source/provenance,
instead of collapsing to one `display_name`. MFC keeps per-source
`GetClientFilename()` names and consumes them for the follow-majority vote and
the UI; Rust discards all but the latest.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/model.rs:20,197,267,399` store a
  single `display_name` on `Ed2kTransferJob`, `Ed2kSharedEntry`, and
  `Ed2kResumeManifest`.
- `crates/emulebb-ed2k/src/ed2k_transfer/manifest.rs:51` and
  `catalog.rs:344` propagate the single name.
- `crates/emulebb-core/src/ed2k_sources.rs:287-292`
  `normalized_optional_display_name` is trim + non-empty only; `:332` selects
  the first non-empty name (`find_map`) with no merge.
- `reconcile_job_metadata` (`ed2k_transfer/metadata.rs:175`) overwrites the
  single name with the latest peer answer.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `PartFile.cpp:6280-6287` iterates live sources and reads
  `cur_src->GetClientFilename()` as the per-source name.

## Why This Matters

ED2K files routinely arrive under several spellings. Showing and reconciling
all of them is the basis for follow-majority naming and lets the user spot
fakes or pick a preferred name. It is also the natural place to hang
provenance so conflicting observations are not silently overwritten.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/model.rs` - single name fields
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs` -
  `reconcile_job_metadata`
- `crates/emulebb-core/src/ed2k_sources.rs` -
  `normalized_optional_display_name`, `select_ed2k_keyword_metadata`
- `workspaces/workspace/app/emulebb-main/srchybrid/PartFile.cpp` -
  `GetMajoritySourceFileName`

## Intended Shape

- Add a bounded list of `{name, source, trust/provenance}` observations to the
  transfer model, with the canonical `display_name` remaining the resolved
  representative.
- Persist the list and expose it additively through the Rust-native REST model
  and OpenAPI/WebUI (no MFC API shape constraint).
- Merge observations with documented rules: exact match collapses, distinct
  spellings retained, normalized comparison for the canonical name.

## Scope Constraints

- Additive API change; do not remove the existing single `display_name`.
- Bound the observation count and name lengths.
- Do not trust a remote name as an independent local observation for rating or
  identity purposes.

## Acceptance Criteria

- [ ] Multiple distinct per-source names survive a download session and a
      persistence round-trip.
- [ ] The Rust-native API/OpenAPI/WebUI exposes the names with provenance.
- [ ] The canonical `display_name` remains correct when no consensus exists
      (first-seen fallback preserved).

## Validation

- Storage/API round-trip tests with conflicting, duplicate, empty, and
  malformed names.
- A download-session test feeding several `OP_REQFILENAMEANSWER` names and
  asserting the observation list.

## Notes

Foundation for RUST-FEAT-044. Composes with RUST-FEAT-046 (normalization) and
RUST-BUG-107 (native path identity).

---
id: RUST-FEAT-046
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/89
title: Repair mojibake and normalize download filenames at intake
status: DONE
priority: Minor
category: feature
labels: [rust, ed2k, filename, unicode, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: ED2K download-completeness audit 2026-10-12 vs community-0.72, emulebb-mfc
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/89. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-046 - Repair mojibake and normalize download filenames at intake

## Summary

Port the MFC incoming-filename repair pipeline and apply it when a download
name is first accepted, not only at delivery. Rust today keeps names verbatim
(trim only) and sanitizes filesystem-unsafe characters only when writing the
completed file, so mojibake, HTML entities, and percent-escapes survive in the
persisted name and on the API.

## Current State

- `crates/emulebb-core/src/ed2k_sources.rs:287-292`
  `normalized_optional_display_name` is `trim` + non-empty only.
- `crates/emulebb-ed2k/src/ed2k_transfer/deliver.rs:376-396`
  `sanitize_file_name` runs only at delivery (invalid characters, trailing
  dots/spaces, Windows reserved leaves, fallback name).

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `FilenameTextRepairSeams.h` `RepairIncomingFilenameText` =
  `DecodeHtmlEntitiesBounded` -> `DecodePercentEncodedUtf8Bounded` ->
  `RepairWindows1252MojibakeBounded` -> `PrecomposeUnicodeText` (Unicode
  precomposition). Mojibake repair is marker-score based, ≤3 passes, segment ≤
  24 chars.
- `PartFile.cpp:439,516,1028` calls `NormalizeDownloadFilename` at part.met
  load, ED2K-link add, and remote-name adoption respectively.

## Why This Matters

Mojibake filenames are endemic on ED2K (UTF-8 decoded as Windows-1252). Without
repair, users get garbled names on disk and in the UI, and the same logical
name appears as several variants, defeating any later consensus logic.

## Representative Sites

- `crates/emulebb-core/src/ed2k_sources.rs` -
  `normalized_optional_display_name`
- `crates/emulebb-ed2k/src/ed2k_transfer/deliver.rs` - `sanitize_file_name`
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs` -
  `reconcile_job_metadata`
- `workspaces/workspace/app/emulebb-main/srchybrid/FilenameTextRepairSeams.h`
- `workspaces/workspace/app/emulebb-main/srchybrid/PartFile.cpp:439,516,1028`

## Intended Shape

- Implement a Rust-native repair pipeline equivalent to
  `RepairIncomingFilenameText`: bounded HTML-entity decode, percent-encoded
  UTF-8 decode, Windows-1252/UTF-8 mojibake repair, and Unicode NFC
  precomposition.
- Apply it at every name intake point: search result, ED2K link, peer filename
  answer, and collection/metadata names.
- Keep the delivery-time filesystem sanitizer as a final, separate step; do
  not perform filesystem sanitization on the stored display name.

## Scope Constraints

- Prefer a pinned Unicode/normalization dependency over hand-rolled NFC.
- Bound entity/segment sizes and repair passes; never degrade already-valid
  text.
- Keep native path identity (RUST-BUG-107) separate from display-name repair.

## Acceptance Criteria

- [x] A Windows-1252 mojibake fixture is repaired to its intended UTF-8 name.
- [x] HTML entities and percent-encoded UTF-8 are decoded at intake.
- [x] The repaired name is what the API exposes and what is written at
      delivery (modulo filesystem sanitization).
- [x] Valid non-ASCII names pass through unchanged.

## Validation

- Unit tests for entity, percent, and mojibake repair plus property-style
  fixtures; delivery round-trip showing the repaired name on disk.

## Evidence

- `normalize_ed2k_file_name` applies bounded HTML decoding, percent-decoded
  UTF-8, Windows-1252 mojibake repair, and Unicode NFC at the shared intake
  boundary.
- Unit tests cover compound repair, invalid/unknown preservation, NFC, CJK, and
  emoji; transfer tests retain raw evidence while voting on normalized names.
- A completed-download round trip proves the repaired canonical name becomes
  the delivered filename on disk and the REST/WebUI display name.
- Rust PR #130 delivered the feature on 2026-10-18 through rebased commits
  `dc324c08`, `65be4f27`, and `85cefaff`; required CI passed strict policy,
  formatting, Clippy, cargo-deny, CodeQL, live REST/OpenAPI conformance, and
  build/test jobs on Ubuntu, macOS, and Windows.
- Contract and harness support landed through tooling PR #34 (`2a6c2a12`) and
  build-tests PR #4 (`e90a06be`).

## Notes

Composes with RUST-FEAT-044 (voting over repaired names) and RUST-FEAT-045.

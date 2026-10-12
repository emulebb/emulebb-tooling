---
id: RUST-FEAT-050
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/93
title: Parse and emit the ED2K link AICH root (h=) section
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, link, aich, parity]
milestone: post-beta-compatibility
created: 2026-10-12
source: feature-backlog chat 2026-10-12 vs emulebb-mfc, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/93. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-050 - Parse and emit the ED2K link AICH root (h=) section

## Summary

Support the AICH root (`h=<base32 AICH root>`) section of ED2K file links.
Large-file links carry this section because MD4 alone is ambiguous above ~4 GB;
the AICH root is the trusted integrity anchor. Rust currently parses
`name|size|hash` and silently drops everything except `sources,...`, so the
root is lost on import, and the emitter never writes it.

## Current State

- `crates/emulebb-core/src/lib.rs:6960` `parse_ed2k_link` reads `name|size|hash`
  and passes the remaining sections to `parse_ed2k_link_sources`.
- `crates/emulebb-core/src/lib.rs:6979` `parse_ed2k_link_sources` only
  recognizes `sources,...` and `continue`s past every other section, so an
  `h=...` section is silently dropped.
- `crates/emulebb-core/src/views.rs:28` `format_ed2k_file_link` emits
  `ed2k://|file|name|size|hash|/` with no `h=` section.
- The transfer model already has the right destination field:
  `crates/emulebb-ed2k/src/ed2k_transfer/model.rs:424`
  `Ed2kResumeManifest.aich_root: Option<String>`.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `ED2KLink.cpp:182-184` parses the `h=` section with
  `DecodeBase32(..., CAICHHash::GetHashSize())` (20 bytes) into
  `m_AICHHash` and marks `m_bAICHHashValid`.
- `ED2KLink.cpp:309` `CED2KFileLink::GetLink` shows the canonical
  `ed2k://|file|name|size|hash|/` shape; modern eMule adds `|h=<base32>|` for
  shared large files where the root is known.

## Why This Matters

For files above the legacy 4 GB MD4 boundary, an ED2K link without the AICH
root cannot reliably identify the file, and dropping the root on import loses
the trusted anchor before transfer start. This is a link-codec interop gap that
no external script can close because the root must land in the daemon's
transfer manifest.

## Representative Sites

- `crates/emulebb-core/src/lib.rs` - `parse_ed2k_link`,
  `parse_ed2k_link_sources`
- `crates/emulebb-core/src/views.rs` - `format_ed2k_file_link`
- `crates/emulebb-core/src/transfer_create_api.rs` - transfer creation from a
  parsed link
- `crates/emulebb-ed2k/src/ed2k_transfer/model.rs` -
  `Ed2kResumeManifest.aich_root`
- `workspaces/workspace/app/emulebb-main/srchybrid/ED2KLink.cpp:182-184`

## Intended Shape

- Parse an `h=` section as base32-decoded 20-byte AICH root, validate the
  length, and populate the transfer's `aich_root` on creation.
- Keep links without `h=` fully accepted (backward compatibility), and reject
  only malformed `h=` values.
- Emit `|h=<base32>|` in `format_ed2k_file_link` when an AICH root is known for
  the shared file.

## Scope Constraints

- No wire change; this is the local ED2K link codec and the transfer-create
  manifest field.
- Preserve the existing `sources,...` parsing exactly.

## Acceptance Criteria

- [ ] A large-file link with a valid `h=` section imports with its AICH root
      set on the transfer manifest.
- [ ] A malformed `h=` section is rejected without corrupting the rest of the
      link.
- [ ] Generated links include `h=` when an AICH root is known.
- [ ] Links without `h=` continue to parse unchanged.

## Validation

- Unit tests for parse (valid, malformed, absent `h=`) and emit (with/without
  root), including a base32 round-trip fixture matching the stock link shape.

## Notes

Complements RUST-FEAT-046 (link filename repair) and shares the transfer
creation path with RUST-FEAT-047.

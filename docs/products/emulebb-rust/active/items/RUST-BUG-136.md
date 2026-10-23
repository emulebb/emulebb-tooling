---
id: RUST-BUG-136
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/162
title: Bound transfer deletion marker validation reads
status: OPEN
priority: Minor
category: bug
labels: [rust, filesystem, deletion, safety, resource-bounds, persistence]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust best-practices and safety audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/162. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-136 - Bound transfer deletion marker validation reads

## Summary

Validate transfer-directory deletion markers with a fixed-size read matching the
16-byte UUID payload, plus one overflow sentinel, instead of reading an
arbitrary regular file to end before authorizing deletion.

## Current State

Transfer deletion creates a no-follow regular marker and writes
`Uuid::as_bytes()`, exactly 16 bytes. Authority validation later reopens the
marker without following links but calls `read_to_end` into an unconstrained
`Vec` before comparing it with the UUID. Filesystem corruption or a local actor
can therefore turn an authority check into an allocation proportional to marker
size.

## Why This Matters

Deletion authorization should fail closed with constant resource use. A
corrupted marker must not create a local memory-exhaustion path during startup,
maintenance, or a user-requested transfer deletion, especially in code whose
purpose is to defend destructive filesystem operations.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs`
  transfer marker creation.
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs`
  `validate_transfer_directory_authority`.
- No-follow regular-file opening in `ed2k_transfer::ingest`.

## Intended Shape

- Read exactly the expected 16 bytes and attempt one additional byte to detect
  oversize content without allocating from file metadata.
- Reject missing, short, long, replaced, non-regular, or unreadable markers as
  invalid authority.
- Keep validation on the opened no-follow file handle and preserve the existing
  stable-directory identity check.
- Use a small fixed array or bounded stack buffer rather than a heap vector.

## Scope Constraints

- Do not weaken the directory identity or no-follow protections added by
  `RUST-BUG-122`.
- Do not authorize deletion based only on marker filename or length.
- UUID bytes are an ownership marker, not a secret; constant-time comparison is
  unnecessary.
- Existing incompatible/corrupt marker state should fail closed rather than be
  migrated during beta.

## Acceptance Criteria

- [ ] Marker validation performs a constant-memory read bounded to 17 bytes.
- [ ] Exactly 16 matching UUID bytes authorize the marker check.
- [ ] Missing, short, oversized, mismatched, symlinked, and non-regular markers
      all reject deletion.
- [ ] Directory identity is checked in addition to marker content.
- [ ] Startup and maintenance retry paths surface or retain failed deletion
      intent without deleting an unauthorised path.

## Validation

- Regression tests for exact, empty, short, oversized, and very large marker
  files.
- Existing symlink/reparse-point and directory replacement adversity tests.
- Restart and maintenance retry coverage for rejected deletion intents.

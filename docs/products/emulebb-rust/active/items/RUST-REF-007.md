---
id: RUST-REF-007
title: Review Rust upload hot-path performance candidates
status: OPEN
priority: Minor
category: refactor
labels: [rust, upload, performance, io, parity]
milestone: post-beta-polish
created: 2026-07-14
source: Operator upload performance review 2026-07-14
---

# RUST-REF-007 - Review Rust upload hot-path performance candidates

## Summary

Track upload-side speed and I/O improvements as **to be reviewed** candidates,
not committed implementation work. Protocol parity is mandatory: any accepted
change must preserve eD2K wire packet shapes, opcode choices, upload queue
semantics, compression eligibility, throttle accounting, and existing diagnostics
meaning.

## Current State

The Rust uploader already keeps one verified-range reader per upload session and
uses read-ahead for contiguous ED2K block requests. Upload payload packets pass
through the shared aggregate upload limiter before the transport write. The
remaining candidate improvements are local CPU/allocation scheduling details,
not protocol gaps.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs`
  `Ed2kVerifiedRangeReader::read_range_with_read_ahead`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session/upload_payload.rs`
  `handle_upload_payload_request`
- `crates/emulebb-ed2k/src/ed2k_tcp/codec/upload.rs`
  `build_upload_part_packets` and `compress_upload_payload`

## Intended Shape

Review these candidates before implementation:

- Borrow cached verified bytes from the read-ahead cache instead of cloning the
  range into a temporary `Vec` before packet construction.
- If diagnostics or profiling show compression CPU stalls upload serving, move
  the same deflate work for larger upload blocks to the blocking pool while
  keeping the existing compression eligibility and encoded packet output.

## Scope Constraints

- Do not change upload wire semantics, opcode selection, request/range handling,
  packet diagnostics, or queue/rate-limit behavior.
- Do not change the compression extension allow/deny behavior unless a separate
  parity item proves that the MFC fork changed.
- Do not pursue larger read-ahead, global file-handle caches, or vectored writes
  under this item unless a focused review proves they preserve lifetime,
  diagnostics, obfuscation, and throttling invariants.

## Acceptance Criteria

- [ ] A measurement or code-review note identifies which candidate, if any, is
      worth implementing.
- [ ] Any implemented candidate is isolated from protocol behavior and carries
      byte-for-byte upload packet tests.
- [ ] Existing upload serving, compression, throttling, and diagnostics tests
      pass with workspace Rust build-output policy.

## Validation

- `git diff --check`
- Scoped Rust tests around upload serving, upload packet encoding,
  compression, and upload throttling.
- Soak diagnostics compare `payloadReadMs`, `readCacheHits`,
  `readCacheMisses`, `readDiskBytes`, `throttleDelayMs`, and aggregate upload
  rate before and after any implementation.

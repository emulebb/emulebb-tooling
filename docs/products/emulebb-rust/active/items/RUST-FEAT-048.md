---
id: RUST-FEAT-048
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/91
title: Use sparse part files without weakening capacity reservations
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, disk, windows, portability]
milestone: post-beta-polish
created: 2026-10-12
source: feature-backlog chat 2026-10-12 vs emulebb-mfc, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/91. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-048 - Use sparse part files without weakening capacity reservations

## Summary

Allocate incomplete-download payload files sparsely where supported so a
high-offset piece does not physically allocate the intervening gap. Keep two
different disk concepts explicit: allocated bytes describe current physical
usage, while completion-capacity reservation remains based on the remaining
logical bytes needed to finish every active download.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs:124-128` and
  `:243-247` open the `pieces.bin` payload with
  `create(true).truncate(false)` and no sparse attribute.
- `crates/emulebb-ed2k/src/ed2k_transfer/salvage.rs:233-236` does the same for
  the salvage payload.
- No `FSCTL_SET_SPARSE`, `fallocate`, `SEEK_DATA/SEEK_HOLE`, or equivalent
  exists anywhere in the tree.
- `crates/emulebb-core/src/disk_guard.rs:196-214` reserves the remaining logical
  bytes (`file_size - durable_present_bytes`). That conservative future-capacity
  invariant is correct and must remain authoritative.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `PartFile.cpp:912-918` applies `FSCTL_SET_SPARSE` when
  `GetSparsePartFiles()` is enabled.
- `PartFile.cpp:6177-6183` and `OtherFunctions.cpp:3240` use
  `GetCompressedFileSize` so sparse/compressed files are accounted by their
  allocated size.
- The `SparsePartFiles` preference lives in `PPgTweaks.cpp`.

## Why This Matters

On Windows NTFS, writing past EOF can allocate the gap unless the file is marked
sparse, so a high-offset piece may consume nearly the full logical size. Unix
filesystems commonly create holes automatically. Measuring allocated bytes is
useful for telemetry and current-volume usage, but substituting that value for
future completion capacity would overcommit the volume across concurrent sparse
downloads and could make completion impossible.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` - payload open paths
- `crates/emulebb-ed2k/src/ed2k_transfer/salvage.rs` - salvage open path
- `crates/emulebb-core/src/disk_guard.rs` - logical-size reservation
- `crates/emulebb-ed2k/src/long_path.rs` - Windows path boundary helper
- `workspaces/workspace/app/emulebb-main/srchybrid/PartFile.cpp:912-918`

## Intended Shape

- Mark new payload files sparse on Windows and rely on normal hole semantics on
  supported Unix filesystems. Unsupported filesystems fall back to dense files
  without changing transfer correctness.
- Add one allocated-size abstraction for telemetry and current-usage reporting,
  with a conservative logical-size fallback when the platform cannot report
  physical allocation.
- Keep admission and resume reservation based on remaining logical completion
  bytes, net of already durable pieces. Never reserve only the currently
  allocated byte count.
- Treat sparse layout as a storage implementation detail rather than adding a
  user-facing compatibility setting during beta.

## Scope Constraints

- No wire/protocol change.
- Preserve resume, verification, completion rehash, and salvage semantics
  exactly; sparse marking must not change logical file content or hashing.
- Preserve the disk guard's aggregate future-completion guarantee across all
  active downloads.
- The hash-named piece store remains a short-path internal path class per
  `policy/rust-client.toml`; apply the sparse helper inside that boundary.

## Acceptance Criteria

- [ ] On NTFS the payload file is marked sparse by default and a high-offset
      piece write does not allocate the intervening gap.
- [ ] Allocated-size accounting is correct on Windows and on sparse-capable
      Unix filesystems, with a safe fallback elsewhere.
- [ ] The disk guard continues to reserve aggregate remaining logical bytes and
      cannot overcommit a volume merely because active payloads are sparse.
- [ ] Resume/verify/rehash behavior is unchanged for both sparse and dense
      payloads.
- [ ] Unsupported sparse marking falls back safely without introducing a
      user-facing compatibility mode.

## Validation

- Platform-gated tests: Windows sparse marking + allocated-size query; Linux
  `SEEK_DATA/SEEK_HOLE` fallback.
- A fixture writes a piece at a far offset and asserts the allocated size stays
  near the downloaded bytes.
- Disk-guard tests with multiple sparse downloads proving current allocation
  never substitutes for required completion capacity.
- Resume tests for sparse and dense fallback payloads.

## Notes

Composes with RUST-REF-009 (native storage domains) and RUST-CI-008 (large
library portability). This is disk I/O outcome work where emulebb-mfc is the
authority.

---
id: RUST-FEAT-048
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/91
title: Sparse part-file allocation for large downloads (multi-platform, default-on)
status: OPEN
priority: Minor
category: feature
labels: [rust, ed2k, download, disk, windows, portability]
milestone: post-beta-polish
created: 2026-10-12
source: feature-backlog chat 2026-10-12 vs emulebb-mfc, aMule
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/91. This local document is retained as the durable engineering spec and evidence record.

# RUST-FEAT-048 - Sparse part-file allocation for large downloads (multi-platform, default-on)

## Summary

Allocate incomplete-download payload files sparsely, default-on, on every
filesystem that supports the concept (NTFS plus any other sparse-capable FS),
and make disk-space accounting use the allocated size rather than the logical
size. This prevents a large download from pinning its full logical size the
moment a high-offset piece is written.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs:124-128` and
  `:243-247` open the `pieces.bin` payload with
  `create(true).truncate(false)` and no sparse attribute.
- `crates/emulebb-ed2k/src/ed2k_transfer/salvage.rs:233-236` does the same for
  the salvage payload.
- No `FSCTL_SET_SPARSE`, `fallocate`, `SEEK_DATA/SEEK_HOLE`, or equivalent
  exists anywhere in the tree.
- `crates/emulebb-core/src/disk_guard.rs:196-214` reserves disk based on
  `manifest.file_size` (logical), not the allocated on-disk size.

Master reference (`workspaces/workspace/app/emulebb-main/srchybrid`):

- `PartFile.cpp:912-918` applies `FSCTL_SET_SPARSE` when
  `GetSparsePartFiles()` is enabled.
- `PartFile.cpp:6177-6183` and `OtherFunctions.cpp:3240` use
  `GetCompressedFileSize` so sparse/compressed files are accounted by their
  allocated size.
- The `SparsePartFiles` preference lives in `PPgTweaks.cpp`.

## Why This Matters

On Windows NTFS, writing past EOF zero-fills and **allocates** the gap, so a
100 GB download can consume ~100 GB of disk almost immediately even with only a
few pieces present. On Unix, hole writes are already sparse, but the allocated-
size accounting still needs to be correct so the disk guard does not
over-reserve or wrongly pause. The operator requirement is multi-platform:
default-on for NTFS and any other filesystem that supports the same concept,
with a graceful no-op elsewhere.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` - payload open paths
- `crates/emulebb-ed2k/src/ed2k_transfer/salvage.rs` - salvage open path
- `crates/emulebb-core/src/disk_guard.rs` - logical-size reservation
- `crates/emulebb-ed2k/src/long_path.rs` - Windows path boundary helper
- `workspaces/workspace/app/emulebb-main/srchybrid/PartFile.cpp:912-918`

## Intended Shape

- Mark the payload file sparse at creation on Windows (default-on), and
  feature-detect other filesystems that support sparse holes so the same
  behavior is applied wherever the concept exists.
- Add a small "allocated size" abstraction: `GetCompressedFileSize` on Windows,
  `SEEK_DATA/SEEK_HOLE` or block-count on Unix, with a conservative fallback to
  logical size when the filesystem cannot report it.
- Use allocated size in the disk guard and completion accounting so sparse
  payloads reserve only what they actually consume.
- Add a `SparsePartFiles`-equivalent setting, default true; unsupported
  filesystems simply fall back to dense files without error.

## Scope Constraints

- No wire/protocol change.
- Preserve resume, verification, completion rehash, and salvage semantics
  exactly; sparse marking must not change logical file content or hashing.
- The hash-named piece store remains a short-path internal path class per
  `policy/rust-client.toml`; apply the sparse helper inside that boundary.

## Acceptance Criteria

- [ ] On NTFS the payload file is marked sparse by default and a high-offset
      piece write does not allocate the intervening gap.
- [ ] Allocated-size accounting is correct on Windows and on sparse-capable
      Unix filesystems, with a safe fallback elsewhere.
- [ ] The disk guard reserves against allocated size for sparse payloads.
- [ ] Resume/verify/rehash behavior is unchanged for both sparse and dense
      payloads.
- [ ] A setting disables sparse allocation and restores dense behavior.

## Validation

- Platform-gated tests: Windows sparse marking + allocated-size query; Linux
  `SEEK_DATA/SEEK_HOLE` fallback.
- A fixture writes a piece at a far offset and asserts the allocated size stays
  near the downloaded bytes.
- Disk-guard and resume tests for sparse and dense payloads.

## Notes

Composes with RUST-REF-009 (native storage domains) and RUST-CI-008 (large
library portability). This is disk I/O outcome work where emulebb-mfc is the
authority.

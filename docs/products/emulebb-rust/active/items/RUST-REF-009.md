---
id: RUST-REF-009
workflow: local
title: Use native storage domains for cross-platform library scheduling
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, io, storage, concurrency, portability]
milestone: post-beta-polish
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

# RUST-REF-009 - Use native storage domains for cross-platform library scheduling

## Summary

Map every shared root to a real storage domain so one sequential hash stream is
used per mechanical disk/filesystem while independent devices can hash in
parallel on Windows, Linux, and macOS.

## Current State

Windows resolves the root once through the volume mount and disk-extents APIs,
then carries the resulting disk key on every scanned file. This correctly avoids
100k repeated volume queries and serializes roots backed by the same ordinary
disk. A striped or spanned volume is classified only by its first extent.

The non-Windows fallback uses the first path component as a mount proxy. Every
absolute Unix path begins at `/`, so roots on independent Linux/macOS mounts are
currently grouped behind one worker. This is safe for correctness but defeats
cross-device concurrency.

## Representative Sites

- `crates/emulebb-core/src/physical_disk.rs` `physical_disk_key`
- `crates/emulebb-core/src/shared_directories.rs`
  `scan_shared_directory_roots` and `hash_reload_targets`

## Intended Shape

- Use `st_dev`/`MetadataExt::dev()` as the baseline Unix storage-domain key.
- Preserve the current one-time root lookup and carry a compact interned domain
  identifier rather than repeating strings for every scanned file.
- Treat Windows multi-extent, Storage Spaces, RAID, removable, and UNC/network
  roots through an explicit conservative policy. Unknown/shared remote storage
  may serialize, but it must be visible in diagnostics rather than collapsing to
  an unexplained catch-all key.
- Stage multi-device work per domain: enumerate and hash sequentially on one
  mechanical device while allowing different devices to progress concurrently.
- Keep SSD/NVMe concurrency a measured optional policy; do not weaken the HDD
  default merely to improve a synthetic SSD number.

## Scope Constraints

- Preserve exactly one active payload reader per identified mechanical storage
  domain by default.
- Do not infer physical topology from drive letters or path strings when a native
  filesystem/device identifier is available.
- Do not start an unbounded real-media scan. Validation uses synthetic mounts or
  the bounded cohorts owned by `RUST-REF-008`.

## Acceptance Criteria

- [ ] Two roots on the same Windows disk or Unix device share one active hash
      worker.
- [ ] Two roots on independent Windows disks or Unix devices can hash
      concurrently.
- [ ] Linux and macOS absolute roots no longer all resolve to `vol:/`.
- [ ] Network, unknown, and multi-extent storage fallbacks are conservative and
      visible in reload diagnostics.
- [ ] Per-domain active counts prove no same-domain payload-read overlap.
- [ ] Bounded two-device evidence records throughput and physical I/O without
      exposing operator paths.

## Validation

- Unit tests through an injectable storage-domain resolver seam.
- Linux mount/device and Windows volume/disk integration tests.
- Capability-gated macOS device identity test.
- Bounded multi-device harness evidence after `RUST-REF-008` instrumentation is
  available.

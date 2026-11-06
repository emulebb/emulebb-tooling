---
id: RUST-REF-009
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/97
title: Use native storage domains for cross-platform library scheduling
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, io, storage, concurrency, portability]
milestone: post-beta-polish
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/97. This local document is retained as the durable engineering spec and evidence record.

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

## Accepted Shared-Scheduler Follow-up (2026-11-06)

This owns approved follow-up 5. Keep the existing storage-domain resolver work
and extend one admission/scheduling service across every hashing entry point.
This is post-beta backlog work, not a data-preservation blocker for the current
stock import or an instruction to hash the remaining operator library.

At review commit `43855fba`, background reload groups targets by disk and runs
one sequential worker per group. The synchronous/offline reload primitive uses
a separate serial file loop, so independent devices can remain idle. Direct
`share_local_file`/`ingest_local_file` requests reach blocking hashing without
that reload job's per-domain gate. A local limit inside one reload is therefore
not a process-wide guarantee: API ingestion can compete with its payload reads.
Watcher ingestion joins this service through RUST-REF-010.

Resolve a storage domain once at the root/admission boundary, then submit owned
hash jobs into bounded per-domain queues with an overall concurrency/queue
budget. Startup/reload, CLI, API, and watcher callers must acquire the same
domain permit. Use the existing hash/read implementation as the worker body;
do not add another MD4/AICH pipeline or parser. Define fair scheduling between
long library work and short interactive/transfer jobs, with observable queue
waits and cancellation states.

Keep the physical storage-domain key distinct from the durable native file
fingerprint. A scheduling-topology refresh must not itself invalidate accepted
hashes or become evidence of changed payload bytes. `st_dev` is a Unix baseline,
not proof that two partitions/mounts occupy independent mechanical disks; use
read-only topology evidence or conservative visible grouping where necessary.

Additional representative sites:

- `crates/emulebb-core/src/shared_directories.rs`: offline
  `reload_shared_directories`, background `hash_reload_targets`, and reload gate.
- `crates/emulebb-core/src/shared_file_api.rs`: direct sharing requests.
- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs`: shared worker implementation.
- `crates/emulebb-core/src/shared_dir_monitor.rs`: watcher admission.

Additional acceptance criteria:

- [ ] Reload plus direct API jobs on the same identified disk never create
      overlapping payload hash readers merely because callers differ.
- [ ] CLI and daemon callers use the same queues, with concurrent progress on
      independently identified disks and bounded process-wide admission.
- [ ] Unknown/shared/multi-extent topology stays conservative and observable.
- [ ] Cancellation releases queued jobs promptly and releases running-job permits
      only when their blocking work actually ends; shutdown has explicit rules.
- [ ] Fairness, saturation, repeated admission, and restart tests preserve MD4,
      full available AICH, no-rehash reuse, and one-pass read accounting.
- [ ] Tests use synthetic resolver seams and bounded cohorts, never the complete
      real-media library as an implicit benchmark.

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

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

## Comparative Measurement Acceptance

- [ ] Retain storage-domain ownership while measuring same-device serialization
      and independent-device parallelism with exact source/hardware/filesystem
      and cache-state records; do not conflate logical/process I/O with disk I/O.
- [ ] Use bounded synthetic workloads and existing harness/orchestration. Measure
      useful throughput, physical I/O and API responsiveness before changes.
- [ ] Coordinate with large-library batching and the shared persistence owner;
      intake changes no operator storage backing, environment variable, machine
      capacity or wire behavior.

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

## Accepted Transfer and Delivery Scheduling Follow-up (2026-11-07)

At branch `58595576`, the per-disk worker guarantee remains local to background
library reload. Direct and watcher ingestion, download finalization, explicit
rechecks, AICH/ICH payload reads, upload readers, and staging copies do not all
share that admission. A per-transfer lifecycle lock serializes one transfer,
not unrelated work on the same physical disk. The synchronous reload primitive
also uses a globally serial loop and leaves independent disks idle.

Extend the same storage service across these callers rather than adding a
second hash scheduler. Keep the core/transfer dependency direction intact:
provide a narrow typed scheduling interface where protocol code needs
admission; do not make the ED2K crate depend on the core implementation.
Resolve each operation's actual source/destination storage at admission and
retain the native file identity checks at execution/publication. A topology
key must not become durable content identity.

Operation classes include background full-file hash/recheck, short part
verification/salvage, foreground transfer reads/writes, and copy read/write.
Use one sequential background full-file reader per identified mechanical
domain by default. This does not mean every network upload must wait behind
an exclusive permit held for a very large complete-file hash. Define foreground
priority and fair bounded service windows; cooperative yield/checkpoints at
chunk or part boundaries must preserve incremental digest/tree state without
restarting the payload pass. Prevent both foreground starvation and permanent
background starvation. Already-running OS I/O may finish after cancellation.

Copies consume source and destination resources; same-disk copies use one
domain's combined read/write budget. Acquire overlapping resource sets atomically
or in a documented deadlock-free order. Windows multi-extent/Storage Spaces/
RAID volumes must not be declared independent merely because their first
extent differs. Track overlapping backing sets when available or use an
explicit conservative fallback. Handle mounts beneath a configured root and
topology changes without per-block device queries.

For Unix, the existing `volume_key` uses `st_dev` for free-space accounting,
while `physical_disk_key` still groups absolute paths as `vol:/`. Reuse native
device facts appropriately without equating free-space pools with spindle
independence. Partitions, logical volumes, containers/bind mounts, and multiple
network mounts may share backing resources. Unknown topology remains visible,
conservative, and retryable; no machine-specific path heuristic belongs in the
product. SSD/NVMe concurrency is a measured optional policy after the HDD lane.

Bound domain queues, total bytes/buffers, running jobs, and CPU admission
separately. The Tokio blocking pool is an executor, not a physical-drive policy.
Metadata-only AICH proof reconstruction uses its bounded CPU/SQLite lane and
must not reserve a payload disk stream or trigger payload hashing. FULL SQLite
commits, media probes, and scanning are measured contention sources; coordinate
their priorities without weakening durability or globally serializing all work.

Additional acceptance criteria:

- [ ] Reload, direct/watcher ingest, finalization, rechecks, and delivery use
      one storage-domain admission service with bounded queue/memory budgets.
- [ ] Two full-file background jobs on one HDD do not create independent
      competing streams; independently identified disks progress concurrently.
- [ ] A short foreground transfer/part job is serviced within a measured bound
      while a large background hash retains progress and is not restarted.
- [ ] Reverse-direction two-disk copies, same-domain copies, shared backing
      sets, cancellation, and shutdown cannot deadlock or leak permits.
- [ ] Unix device/mount fixtures no longer collapse all independent roots into
      `/`; partitions and shared backing devices do not falsely prove independence.
- [ ] Per-operation/per-domain reports show queue wait, read/write bytes, active
      counts, service windows, topology confidence, and foreground latency.
- [ ] Synthetic overlap and generation tests preserve one-pass MD4/AICH,
      current payload authority, native path identity, and optional-cache behavior.

Validation uses injected resolver/resource seams first, then capability-gated
Windows/Unix mapping and bounded synthetic multi-device cohorts. Persisted
harnesses own any performance/live campaign and record device facts plus
logical/physical I/O separately. This entry does not start such a campaign.

## Scope Constraints

- Preserve one sequential background full-file reader per identified mechanical
  storage domain by default, with bounded fair service for foreground work.
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

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.

### Scoped Follow-up Acceptance

- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-REF-009.md

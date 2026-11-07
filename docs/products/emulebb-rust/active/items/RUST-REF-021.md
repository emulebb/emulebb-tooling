---
id: RUST-REF-021
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/254
title: Reduce delivery verification reads without weakening publication authority
status: OPEN
priority: Major
category: refactor
labels: [rust, delivery, io, integrity, performance]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/254. This local document owns the durable engineering specification and evidence.

# RUST-REF-021 - Reduce delivery verification reads without weakening publication authority

## Summary

Measure and reduce avoidable complete-payload reads between verified download
completion and durable delivery. Preserve the final completion barrier,
independent destination ownership, no-clobber publication, native identity,
mutation detection, and recovery/deletion safety. This is a performance item,
not permission to remove integrity checks merely because adjacent passes
usually see cached bytes.

## Revalidated Findings and Read Accounting

On branch `fix/stock-hash-share-tree` at `58595576`, a normal bitmap download
reads a completed part back for MD4 verification. The final completion barrier
then rereads the complete payload, computing MD4 and AICH in one pass.
`deliver_payload_file` creates a durable attempt, copies the source into an
independent staging file, hashes the staged file through
`open_verified_staging_file`, atomically installs it, and calls
`capture_published_fingerprint`. That last function hashes the same retained
file handle again and verifies its final native-path identity.

For that simple non-retry path the code therefore exposes approximately five
payload-equivalent logical read passes across the download lifecycle: summed
part verification, final combined verification, source copy, staged MD4, and
published MD4. This is a source-path accounting example, not a measured fivefold
physical read claim. Cache hits, sparse extents, short files, alternate receive
paths, retries, and filesystem behavior change actual physical I/O. The copy
also writes a complete destination and performs required durability operations.

RUST-BUG-158's latest recovery changes remove a separate AICH payload pass and
reuse delivered-file fingerprints on later library reload. Preserve both
improvements. The delivery source/staging/publication structure also exists on
main `e3372aba`; revalidate current main and platform semantics before changes.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/requested_block.rs`: normal completed
  part readback and verification.
- `completion_rehash.rs`: mandatory whole-file completion barrier.
- `deliver.rs`: `materialize_completed_payload`, `deliver_payload_file`,
  `stage_delivery_payload`, `open_verified_staging_file`,
  `capture_published_fingerprint`, and restart artifact classification.
- `fs_durability.rs`: no-replace moves and file/directory sync ownership.
- `tests/deliver_runtime.rs` and `tests/completion_rehash.rs`: race, mutation,
  replacement, collision, restart, and ownership regressions.

## Intended Shape

First label/count each logical read/write phase and measure physical I/O per
source/destination storage domain under RUST-REF-008's existing harness. Include
same-disk and cross-disk delivery, cold/warm cache, and a file larger than the
controlled test cache when feasible. Record checksum CPU, queue wait, fsync,
copy throughput, and verification bytes independently. Do not tune the digest
buffer or replace the file API before identifying the actual dominant cost.

Evaluate combining digest calculation with bytes already read for copy and
carrying an opened, verified staging object's identity through publication.
Hashing the source copy stream proves source bytes, not independently that
destination bytes were durably stored correctly. Document which checks still
require a destination read and which repeated read can be replaced by a proven
retained-handle/native-generation invariant. On platforms without sufficient
write exclusion or trustworthy change evidence, retain the necessary read.

An atomic rename preserves object identity but does not by itself prove no
concurrent writer changed the object. Preserve handle-based verification,
before/after metadata checks, final path-to-handle binding, and platform-specific
mutation protection. A failed identity or digest check cannot be treated as a
successful installation or grant deletion ownership of a foreign object.

Keep source/destination resource admission in RUST-REF-009. Preserve sequential
bursts on a shared HDD and independent-disk concurrency, with deadlock-free
multi-resource copies and foreground service. Keep required FULL metadata
commits and file/directory syncs; RUST-REF-016 owns their execution boundary.
RUST-REF-019 owns digest offloading. Cache retention and async offloading do not
alone establish fewer physical reads.

Do not silently replace the independent destination copy with a hard link to a
mutable piece store, or delete source bytes before crash-safe ownership and
retirement are committed. A move/reflink strategy requires its own demonstrated
identity, independence, crash, and cross-filesystem contract within this item;
it is not a shortcut around existing safety tests.

## Acceptance Criteria

- [ ] Phase counters and a current-head bounded baseline account for source,
      staging, published, part, and finalizer reads separately from physical I/O.
- [ ] The normal delivery path demonstrably reduces redundant logical read or
      checksum work on supported platform paths, with measured physical-I/O
      disposition and explicit retained checks where no safe reduction exists.
- [ ] MD4 remains mandatory; trusted AICH enforcement from RUST-BUG-165 is not
      weakened or replaced by metadata-only acceptance of changed bytes.
- [ ] Retained-handle, same-size overwrite, replacement, rename/unlink, and
      concurrent-write tests reject changed/foreign objects before publication
      or ownership is committed.
- [ ] Crash injection at prepared, copied, staged, installed, published, and
      retired boundaries remains idempotent with no data loss or foreign deletion.
- [ ] Existing-destination collisions and same-/cross-volume delivery preserve
      no-clobber semantics, independent output ownership, and native paths.
- [ ] Later unchanged library reload/import still reuses the delivered hashsets
      and fingerprint without payload hashing.
- [ ] Resource/latency evidence covers shared and independent disks with bounded
      buffers and no CPU work on cooperative network/API threads.

## Validation and Dependencies

Extend existing delivery and completion tests rather than introducing a second
materialization implementation. Use injected copy/read counters and deterministic
mutation barriers, then capability-gated native Windows/Unix filesystem tests.
Extend the persisted shared-library I/O harness with bounded synthetic delivery
cohorts; no unbounded real-media run is authorized. RUST-BUG-159 owns filename
allocation and RUST-REF-022 owns partial recheck selection. Keep those scopes
separate while preserving the same publication and verification authorities.

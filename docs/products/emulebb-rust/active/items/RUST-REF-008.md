---
id: RUST-REF-008
workflow: local
title: Reduce large-library metadata and scan I/O amplification
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, performance, io, sqlite, storage]
milestone: post-beta-polish
created: 2026-10-03
source: 100k SSD campaign, interrupted multi-HDD campaign, and 2026-10-03 I/O review
---

# RUST-REF-008 - Reduce large-library metadata and scan I/O amplification

## Summary

Reduce the database, catalog, and filesystem-metadata amplification that now
dominates large-library cold ingestion and mutation. The combined MD4/AICH
payload path is already close to one physical read of the library; the next
large gain is to preserve that behavior while avoiding per-file durable commits,
repeated stale-source scans, and unnecessary media-enrichment I/O.

Retain bounded, representative multi-HDD measurement as the final proof lane.
Do not restart an unbounded real-media scan under this item.

## Current State

The deterministic 100,000-file SSD fixture passed initial scan, warm reload,
one-percent mutation, long-path, watcher, persistence, and cleanup checks:

- The 10.49 GB cold library produced about 10.75 GB of physical reads, showing
  that MD4 and AICH already share one effective payload pass.
- Cold ingestion took about 905 seconds and produced about 16.13 GB of physical
  writes even though the final database was about 134 MB.
- A warm unchanged reload reused all 100,000 files in about 2.06 seconds without
  payload hashing.
- Rehashing a 1,000-file, 100 MB mutation reported about 25.56 GB of process
  reads and about 399.8 MB of physical writes.

Each new share currently commits a `synchronous=FULL` manifest transaction and
normally follows it with a separate media-metadata update. Stale-hash removal
queries `shared_file_sources` by `known_file_id`, but that column has no dedicated
index, and removes hashes one transaction at a time. These sites are the first
attribution targets; the process logical-read counter must still be traced
before every byte is assigned to a cause.

An intentionally stopped real-media HDD campaign committed 4,947 unique hashes
covering about 589 GB with no invalid hash or scan failures. That is sufficient
correctness evidence, not authorization for another complete media-library run.

## Why This Matters

Per-file WAL flushes and repeated metadata scans make a library of many small
files much slower than its payload size suggests. If the profile database and
shared library occupy the same mechanical disk, alternating payload reads and
database flushes can also create avoidable seeks. This is the largest measured
remaining large-library I/O cost.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/store.rs`
  `store_manifest_unlocked`
- `crates/emulebb-ed2k/src/ed2k_transfer/shared_catalog.rs`
  `upsert_verified_catalog_entry`
- `crates/emulebb-metadata/src/transfer_store.rs`
  `upsert_transfer_manifest`, `update_transfer_media_metadata`, and
  `delete_transfer_manifest`
- `crates/emulebb-metadata/src/schema.sql` `shared_file_sources`
- `crates/emulebb-core/src/shared_directories.rs`
  `forget_stale_shares` and `hash_reload_targets`
- `repos/emulebb-build-tests/emule_test_harness/rust_shared_library_io.py`

## Intended Shape

- Add the missing lookup support for stale-source operations and batch stale
  removal so a mutation does not repeatedly scan a 100k-row source table.
- Introduce a bounded single metadata-writer path for initial share ingestion.
  Preserve `synchronous=FULL`, but commit small file/time-bounded groups instead
  of one transaction per file. Keep the first publishable cohort responsive.
- Do not let a large transaction monopolize the shared SQLite connection; record
  commit latency and keep REST/network metadata operations responsive.
- Publish the hash/name/size entry before optional media enrichment. Persist
  derived media fields through the bounded writer, or combine them with the
  manifest transaction when doing so does not delay first publication.
- Instrument SQLite transaction count, WAL bytes, statement/page reads, media
  probe bytes, and stale-removal work so logical-read amplification is attributed
  rather than inferred.
- Extend the existing Python harness with per-physical-disk file and byte
  ceilings, deterministic selection, resumable checkpoints, and redacted
  per-disk evidence.

## Scope Constraints

- Preserve one sequential payload hash stream per mechanical storage domain.
- Do not weaken download-manifest crash consistency or change ED2K/AICH results.
- Do not delay connectivity or the progressive startup publication delivered by
  `RUST-BUG-106`.
- Real-media runs are read-only and bounded by default. Do not retain private
  media names, complete paths, or content-derived details in committed evidence.
- Storage-domain mapping and native path identity are owned by
  `RUST-REF-009` and `RUST-BUG-107`; watcher rescan policy is owned by
  `RUST-REF-010`.

## Acceptance Criteria

- [ ] `shared_file_sources` stale-source lookups are indexed and a 1,000-file
      mutation no longer performs per-hash full-table work.
- [ ] Initial share persistence uses bounded batching while keeping committed
      manifests crash-consistent and the first publication cohort prompt.
- [ ] Optional media enrichment does not block a newly hashed file from entering
      the live publication catalog.
- [ ] The harness records payload bytes, process/physical reads and writes,
      SQLite transactions/WAL growth, wall time, throughput, and failures.
- [ ] A repeated 100k SSD cold/warm/mutation campaign shows a material reduction
      in cold physical writes and mutation logical reads against the retained
      baseline without increasing payload physical reads materially.
- [ ] The Python harness can select deterministic bounded cohorts per physical
      HDD and resume them from checkpoints.
- [ ] A bounded multi-HDD report proves one sequential hasher per mechanical
      storage domain and concurrency only across independent domains.

## Validation

- Metadata schema/query-plan tests for source lookup and batch deletion.
- Crash/restart tests around partial batches and first-cohort publication.
- Hash/ingest equivalence tests preserving MD4, ED2K part hashes, AICH, media
  metadata, long paths, and catalog contents.
- Python harness tests for counters, cohort limits, checkpoints, and redaction.
- Bounded SSD comparison followed by bounded multi-HDD evidence below
  `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

## Notes

The retained SSD baseline is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-io-20261003T153209Z-11012.json`.
The startup-publication overlap report is
`${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-shared-library-lan-startup-20261003T183046Z-16340.json`.

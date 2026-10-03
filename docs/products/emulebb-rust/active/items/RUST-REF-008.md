---
id: RUST-REF-008
workflow: local
title: Measure and reduce large-library scan I/O amplification
status: OPEN
priority: Minor
category: refactor
labels: [rust, sharing, performance, io, storage]
milestone: post-beta-polish
created: 2026-10-03
source: Operator 100k SSD campaign and interrupted multi-HDD campaign
---

# RUST-REF-008 - Measure and reduce large-library scan I/O amplification

## Summary

Retain the next large-library I/O work after the completed 100,000-file SSD
campaign. Use bounded, representative cohorts on each physical HDD instead of
walking complete media libraries, and determine whether the observed process
logical-read total represents real duplicate payload reads or only counter
semantics.

## Current State

The deterministic 100,000-file SSD fixture passed initial scan, warm reload,
one-percent mutation, long-path, watcher, and strict cleanup checks. Physical
reads stayed close to the 10.49 GB fixture payload, while the process logical
read counter reported about 64.85 GB. An intentionally stopped real-media HDD
campaign committed 4,947 unique hashes covering about 589 GB with no invalid
hash or scan failures, which is enough to establish correctness but not a safe
basis for an unbounded full-library performance run.

## Intended Shape

- Extend the existing Python shared-library harness with per-physical-disk file
  and byte ceilings, deterministic selection, and resumable checkpoints.
- Exercise one sequential hash stream per mechanical disk while retaining
  concurrency across independent disks.
- Attribute the logical-read amplification to specific hash, AICH, media-probe,
  SQLite, or counter behavior before proposing product changes.
- If payload bytes are genuinely read more than required, consolidate the read
  path without changing ED2K/AICH results or media metadata semantics.

## Scope Constraints

- Real-media runs are read-only and bounded by default; do not restart a full
  library scan without an explicit operator request.
- Do not retain private media names, full paths, or content-derived details in
  committed evidence.
- Preserve one active hasher per physical disk and parallelism only across
  independent disks.
- Do not change publishing or wire-protocol behavior under this item.

## Acceptance Criteria

- [ ] The Python harness can select deterministic representative cohorts with
      explicit maximum files and bytes per physical disk and resume them from
      checkpoints.
- [ ] A bounded multi-HDD report records per-disk payload bytes, physical I/O,
      logical I/O, wall time, throughput, failures, and cleanup state without
      mutating source media.
- [ ] The logical-read amplification is attributed to counter semantics or
      concrete read sites with reproducible evidence.
- [ ] Any real duplicate-payload-read fix preserves MD4, ED2K part hashes, AICH,
      media metadata, long paths, and per-disk scheduling in focused tests.
- [ ] Cold, warm, and mutation results are compared against the retained SSD
      baseline before the item is closed.

## Validation

- Python harness unit tests for cohort selection, limits, checkpoints, and
  redaction.
- Focused Rust hash/ingest equivalence tests for any product-code change.
- Bounded SSD and multi-HDD evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

## Notes

The existing SSD baseline report is
`reports/emulebb-rust/shared-library-io/rust-shared-library-io-20261003T153209Z-11012.json`
below the configured output root. This item deliberately defers the HDD and
logical-read investigation; it does not reopen the completed 100,000-file SSD
correctness campaign.

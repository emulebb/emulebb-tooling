---
id: RUST-BUG-106
workflow: local
title: Large-library startup delayed connectivity and first publication
status: DONE
priority: Major
category: bug
labels: [sharing, startup, ed2k, kad, io, large-library]
milestone: post-0.1.0-beta.2
created: 2026-10-03
source: 100k-file SSD shared-library I/O campaign and LAN-only eD2K/Kad follow-up
---

# RUST-BUG-106 - Large-library startup delayed connectivity and first publication

## Summary

The daemon could bind REST and spawn networking independently from a configured
shared-directory reload, but core construction still synchronously materialized
the entire persisted shared catalog. A cold profile also walked the complete
configured tree before hashing its first file. At 100k+ files, those two startup
barriers could delay useful eD2K/Kad publication even though networking itself
was ready.

The daemon now exposes a bounded publishable cohort immediately and loads the
remaining work progressively. Persisted libraries synchronously hydrate one
200-entry legacy server-offer batch, then continue in 1,024-entry keyset pages
after REST has bound. Empty catalogs select at most 200 small files from a
bounded metadata-only candidate walk (maximum 4,096 entries / 2,048 file
candidates / 256 MiB), hash that cohort with the existing one-worker-per-disk
scheduler, and then perform the authoritative full scan. Each completed file is
available to both publishing loops immediately.

## Scope Constraints

- Existing non-daemon constructors retain eager catalog loading for compatibility.
- The bounded bootstrap is non-authoritative and never prunes unseen sources.
- The exhaustive scan and normal incremental-reuse rules remain authoritative.
- The change adds no cross-disk concurrency beyond the existing one sequential
  reader per physical disk policy.
- The implementation uses portable Rust filesystem and async primitives; the
  retained live storage evidence for this item is from the Windows SSD lane.

## Acceptance Criteria

- [x] REST and network startup do not synchronously wait for all persisted
  completed shares to enter memory.
- [x] A cold large library exposes a bounded first publication cohort before the
  full reload completes.
- [x] Remaining persisted catalog rows hydrate through bounded keyset pages.
- [x] eD2K publication reaches the LAN-only server while initial ingestion is
  still active.
- [x] Both LAN-only Kad peers connect and the target starts keyword and source
  publishing while initial ingestion is still active.
- [x] Long-path files remain part of the exact 100k-file fixture and the normal
  authoritative scan path.
- [x] Unit/integration tests and a staged Release build pass.

## Validation

Product commit `bc921cae` contains the progressive catalog and cold-start cohort
implementation. Harness commit `87c32a7` adds the `lan-startup` command to the
existing Python shared-library I/O harness.

The retained LAN-only report is outside the source tree under the canonical
workspace output root:

`reports/emulebb-rust/shared-library-io/rust-shared-library-lan-startup-20261003T183046Z-16340.json`

It passed after 67.413 seconds against the prepared SSD fixture: 100,000 files,
10,485,760,000 bytes, and 1,000 long-path files. At the accepted overlap point:

- the reload was still hashing with 8,393 of 99,800 full-pass hashes complete;
- only 8,596 of 100,000 files were in the live shared catalog;
- eD2K was connected and the local server had accepted 200 target publications;
- both isolated Kad peers were connected with one local contact each;
- target Kad keyword and source publish workers were active; and
- both Rust peers shut down through REST with exit code zero.

Focused validation passed for `emulebb-metadata` (35 tests), `emulebb-ed2k`
(887 tests), `emulebb-core` (350 unit tests plus integrations), and
`emulebb-daemon` (60 tests). The staged Windows Release build completed with
zero warnings, and the extended Python harness module passed 26 tests plus Ruff
format/lint checks.

The two-peer local Kad topology proves connection and early publish scheduling;
it is not an acknowledgement-depth test. A future broader Kad swarm can add
successful STORE acknowledgement coverage without changing this startup gate.

---
id: RUST-CI-008
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/84
title: Prove Unicode and long-path large-library behavior across platforms
status: OPEN
priority: Major
category: ci
labels: [rust, sharing, harness, unicode, long-path, portability]
milestone: post-beta-polish
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/84. This local document is retained as the durable engineering spec and evidence record.

# RUST-CI-008 - Prove Unicode and long-path large-library behavior across platforms

## Summary

Extend the existing Python shared-library harness with deterministic Unicode,
normalization, case, and native path-limit cohorts, then run the initial scan,
warm reload, mutation, watcher, persistence, and publication checks on Windows,
Linux, and macOS.

This evidence is part of the hard Client gate. Every Windows, Linux, and macOS
x64/ARM64 package requires compile/test viability and packaged lifecycle smoke;
deep public-network evidence remains concentrated on Windows x64 and Linux x64.

## Current State

The Windows SSD campaign proves 100,000 files, 10.49 GB, and 1,000 long paths.
The production fixture now reserves a deterministic 16-file cohort spanning
NFC/NFD, compatibility, case, accented, CJK, emoji, bracketed, and long-Unicode
names without changing the established file-count, byte-count, or size-bucket
contract. Validation reports Windows lengths in UTF-16 code units and Unix
lengths in encoded bytes, including component maxima and explicit native
case/normalization capability dispositions.

Portable fixture and path-capability tests run on Windows, Linux, and macOS in
the fast harness workflow. The full initial-scan, warm-reload, mutation, watcher,
restart, and cleanup campaign remains an operator evidence lane; physical-disk
counters remain Windows-oriented. macOS watcher deletion is still explicitly
ignored even though release packaging emits macOS artifacts.

## Intended Shape

- Add a deterministic Unicode cohort without changing the established payload
  size distribution or making fixture validation depend on locale.
- Include synthetic NFC/NFD, compatibility-equivalent, case-variant, accented,
  CJK, emoji, bracketed, and long-Unicode paths. Create collision pairs only
  when the target filesystem can represent both.
- Measure Windows paths in UTF-16 code units and Unix paths/components in encoded
  bytes. Respect component limits independently from total-path limits.
- Add capability reporting so unsupported filesystem cases are explicit skips,
  not silent omissions.
- Keep a smaller hosted-CI lane and a full 100k operator evidence lane. The full
  lane must use persisted Python scripts and output-root reports.

## Scope Constraints

- Use only synthetic names and payloads. Never copy operator media names into
  fixtures, logs, or reports.
- Do not require identical case/normalization behavior from filesystems with
  different native rules; require correct capability-aware behavior.
- Do not make a 100k run mandatory for ordinary pull requests.
- Product fixes discovered by the matrix remain owned by `RUST-BUG-107`,
  `RUST-REF-009`, and `RUST-REF-010`.
- Run the full cross-platform matrix after those path, storage-domain, and
  watcher fixes are available; do not use stale red evidence as their proxy.

## Acceptance Criteria

- [x] The fixture deterministically creates and validates its Unicode cohorts
      without disturbing the existing 100k size/long-path contract.
- [x] Path lengths are reported in the platform-native units relevant to actual
      filesystem limits.
- [ ] Windows, Linux, and macOS lanes cover initial scan, warm reload, one-percent
      mutation, watcher create/rename/delete, restart, and cleanup.
- [ ] Unicode filenames survive SQLite persistence, REST/catalog display,
      eD2K server offers, and Kad publication encoding.
- [ ] Capability-gated normalization/case collision cases cannot overwrite or
      alias the wrong durable source row.
- [x] Reports contain no private paths or content-derived names.
- [ ] The macOS watcher support claim is reconciled with its release-package
      status and backed by an explicit passing or accepted-degradation result.

## Validation

- Python unit tests for cohort mapping, native-unit length accounting,
  capability detection, validation, and report redaction.
- Small hosted Windows/Linux/macOS fixture lanes.
- Retained full 100k evidence on each supported platform where suitable runner
  storage is available.

## Evidence

- `emulebb-build-tests` PR #4 merged as `e90a06be` with fixture implementation
  commits `2116ab2` and `b6c2908`.
- Follow-up PR #5 merged as `94122a74`, aligning metadata seeders and bounded
  migrations with schema 44, materializing the pinned PCP/NAT-PMP source, and
  stabilizing protected-root fingerprints against deferred Windows directory
  timestamp updates.
- The hosted portability matrix passed on Ubuntu 24.04, macOS, and Windows 2022.
- The coordinated fast workflow passed the complete Python harness on Windows
  2022 and Windows 2025/VS2026, plus portability lanes on Ubuntu 24.04, macOS,
  and Windows 2022, at PR #5 head `ac9d4a9`.
- The focused local shared-library suite passed 29 tests, including deterministic
  cohort mapping, native-unit accounting, capability cleanup, and report
  redaction.
- The remaining unchecked criteria require the retained cross-platform lifecycle
  campaigns and macOS watcher disposition; this item stays open until that
  evidence exists.

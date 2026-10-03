---
id: RUST-CI-008
workflow: local
title: Prove Unicode and long-path large-library behavior across platforms
status: OPEN
priority: Major
category: ci
labels: [rust, sharing, harness, unicode, long-path, portability]
milestone: post-beta-polish
created: 2026-10-03
source: 2026-10-03 large-library I/O and portability review
---

# RUST-CI-008 - Prove Unicode and long-path large-library behavior across platforms

## Summary

Extend the existing Python shared-library harness with deterministic Unicode,
normalization, case, and native path-limit cohorts, then run the initial scan,
warm reload, mutation, watcher, persistence, and publication checks on Windows,
Linux, and macOS.

## Current State

The Windows SSD campaign proves 100,000 files, 10.49 GB, and 1,000 ASCII long
paths up to 420 display characters. Smaller Rust tests cover accented, CJK, and
bracketed names. The scale fixture itself does not contain Unicode names, and its
long-path contract counts Python characters rather than Windows UTF-16 code
units or Unix encoded bytes.

The Rust CI matrix builds/tests Windows, Linux, and macOS, but the 100k I/O
harness and physical-disk counters are Windows-oriented. macOS watcher deletion
is explicitly ignored even though release packaging emits macOS artifacts.

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

## Acceptance Criteria

- [ ] The fixture deterministically creates and validates its Unicode cohorts
      without disturbing the existing 100k size/long-path contract.
- [ ] Path lengths are reported in the platform-native units relevant to actual
      filesystem limits.
- [ ] Windows, Linux, and macOS lanes cover initial scan, warm reload, one-percent
      mutation, watcher create/rename/delete, restart, and cleanup.
- [ ] Unicode filenames survive SQLite persistence, REST/catalog display,
      eD2K server offers, and Kad publication encoding.
- [ ] Capability-gated normalization/case collision cases cannot overwrite or
      alias the wrong durable source row.
- [ ] Reports contain no private paths or content-derived names.
- [ ] The macOS watcher support claim is reconciled with its release-package
      status and backed by an explicit passing or accepted-degradation result.

## Validation

- Python unit tests for cohort mapping, native-unit length accounting,
  capability detection, validation, and report redaction.
- Small hosted Windows/Linux/macOS fixture lanes.
- Retained full 100k evidence on each supported platform where suitable runner
  storage is available.

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
- Lossless storage from completed `RUST-BUG-107` is the baseline. Product fixes
  belong to `RUST-BUG-159` (delivery name budgets), `RUST-BUG-160` (import name
  matching), `RUST-BUG-161` (filesystem comparisons), `RUST-FEAT-064` (lossless
  API locators), `RUST-REF-009`, or `RUST-REF-010` as appropriate.
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

## Accepted macOS Filesystem Matrix Follow-up (2026-11-06)

This owns approved follow-up 10. Preserve the existing cross-platform fixture
work instead of opening a second evidence issue. It remains post-beta backlog
work; this update does not claim that the Windows/WSL import campaign proves
native macOS behavior or that older hosted fixture tests never passed.

Record native macOS runtime evidence on the architectures for which packages
are claimed. Exercise APFS case-sensitive and case-insensitive volumes where
available and report the actual capabilities of each fixture volume. Measure
representable component and whole-path boundaries in the platform/filesystem's
units; do not copy a Windows character limit or an ext4 byte limit into APFS
expectations without evidence.

The matrix must cover:

- Actual native-byte storage, Unicode display, SQLite reopen, and serving of
  the exact file across restart and rename. Invalid-byte/code-unit cases are
  tested only where representable, with an explicit unsupported disposition.
- NFC/NFD and compatibility-equivalent names, case variants, accented/CJK/emoji
  names, combining sequences, bracketed names, and long directory hierarchies.
- Capability-gated collision pairs with distinct contents: listing, root
  consolidation, import matching, collision-safe delivery, and API operations
  must not alias or overwrite the wrong file.
- Native name-budget delivery, extension/collision suffix boundaries, and
  differences between a long path and an oversized single component.
- Stock/exchange import with path remapping and normalization changes, repeated
  import, and unchanged-file reconciliation with zero payload reads.
- Watcher create/modify/rename/delete and a defined fallback for delayed or
  coalesced FSEvents. RUST-REF-010 owns the production recovery design.
- Packaged startup, authenticated REST, WebUI, local transfer, and clean
  shutdown, separately from the fixture-generator's hosted Python checks.

Use synthetic names and payloads, record native length accounting, skip reasons,
hash/AICH equality, payload bytes, and filesystem case/normalization behavior.
Owned fixture volumes may use capability probes; operator media trees remain
read-only. Keep a small hosted smoke and optional full 100K synthetic campaigns;
no complete real-media rehash is authorized by this backlog item.

- [ ] Each claimed macOS lane has explicit package/runtime and filesystem
      capability evidence, rather than inheriting a Windows/WSL result.
- [ ] NFC/NFD/case, name-length, collision, opaque-path API, and import/reuse
      cases link to their product owner's regressions and record clear results.
- [ ] Unsupported native names and unavailable volume types are documented
      capability dispositions; unexpected filesystem failures remain failures.
- [ ] Delayed/coalesced watcher results have a proved recovery/degradation
      disposition before the corresponding support claim is made.

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

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_diagnostics-privacy.md` section evidence-gap (existing): Owning harness/current-head evidence must distinguish raw local captures from scrubbed shared artifacts; coordinate with testing-harness report.
- `emulebb-rust-prompt_audit_findings_multi-platform.md` section platform-evidence (existing): Windows/Linux are Beta 3 gates. macOS and extended target qualification continue in parallel, with per-target limitations and no stronger support claim than retained runtime evidence.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.

### Scoped Follow-up Acceptance

- [ ] Shared evidence omits operator-private values; raw captures never become public issue attachments by default.
- [ ] Required Windows/Linux proof is recorded under the candidate owner.
- [ ] Optional target status distinguishes compile, package and runtime evidence.
- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-CI-008.md

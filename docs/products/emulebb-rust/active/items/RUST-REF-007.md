---
id: RUST-REF-007
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/95
title: Review Rust upload hot-path performance candidates
status: OPEN
priority: Minor
category: refactor
labels: [rust, upload, performance, io, parity]
milestone: post-beta-polish
created: 2026-07-14
source: Operator upload performance review 2026-07-14
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/95. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-007 - Review Rust upload hot-path performance candidates

## Comparative Measurement Acceptance

- [ ] Use a bounded, synthetic, matched upload workload on the same hardware,
      storage, network and settings with exact Rust/current-stable aMule revisions.
- [ ] Record useful payload throughput, CPU, allocation/RSS and control-plane
      latency while preserving queue, compression, credit and throttle semantics.
- [ ] Route measured repairs here; no duplicate optimization program, blanket
      speed claim, paid capacity or long soak is activated by distribution intake.

## Summary

Track upload-side speed and I/O improvements as **to be reviewed** candidates,
not committed implementation work. Protocol parity is mandatory: any accepted
change must preserve eD2K wire packet shapes, opcode choices, upload queue
semantics, compression eligibility, throttle accounting, and existing diagnostics
meaning.

## Release Triage (2026-09-30)

**Post-beta.** The current upload path is protocol-correct and passed the beta
test matrix. These are measurement-led optimization candidates, not release
defects; no implementation should begin without profiling evidence.

## Current State

The Rust uploader already keeps one verified-range reader per upload session and
uses read-ahead for contiguous ED2K block requests. Upload payload packets pass
through the shared aggregate upload limiter before the transport write. The
remaining candidate improvements are local CPU/allocation scheduling details,
not protocol gaps.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs`
  `Ed2kVerifiedRangeReader::read_range_with_read_ahead`
- `crates/emulebb-ed2k/src/ed2k_tcp/listener/session/upload_payload.rs`
  `handle_upload_payload_request`
- `crates/emulebb-ed2k/src/ed2k_tcp/codec/upload.rs`
  `build_upload_part_packets` and `compress_upload_payload`

## Intended Shape

Review these candidates before implementation:

- Borrow cached verified bytes from the read-ahead cache instead of cloning the
  range into a temporary `Vec` before packet construction.
- If diagnostics or profiling show compression CPU stalls upload serving, move
  the same deflate work for larger upload blocks to the blocking pool while
  keeping the existing compression eligibility and encoded packet output.

## Scope Constraints

- Do not change upload wire semantics, opcode selection, request/range handling,
  packet diagnostics, or queue/rate-limit behavior.
- Do not change the compression extension allow/deny behavior unless a separate
  parity item proves that the MFC fork changed.
- Do not pursue larger read-ahead, global file-handle caches, or vectored writes
  under this item unless a focused review proves they preserve lifetime,
  diagnostics, obfuscation, and throttling invariants.

## Acceptance Criteria

- [ ] A measurement or code-review note identifies which candidate, if any, is
      worth implementing.
- [ ] Any implemented candidate is isolated from protocol behavior and carries
      byte-for-byte upload packet tests.
- [ ] Existing upload serving, compression, throttling, and diagnostics tests
      pass with workspace Rust build-output policy.

## Validation

- `git diff --check`
- Scoped Rust tests around upload serving, upload packet encoding,
  compression, and upload throttling.
- Soak diagnostics compare `payloadReadMs`, `readCacheHits`,
  `readCacheMisses`, `readDiskBytes`, `throttleDelayMs`, and aggregate upload
  rate before and after any implementation.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A19-obfuscation (existing): RC4 speed changes require measurement under the existing hot-path owner. Obfuscated-server timeout/fallback is a protocol transition to verify through the parity catalog, not an automatic downgrade feature.

### Scoped Follow-up Acceptance

- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.
- [ ] Benchmark before adopting crypto-loop changes.
- [ ] Prove accepted retry/fallback semantics and avoid weakening required obfuscation.

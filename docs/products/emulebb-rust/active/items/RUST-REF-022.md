---
id: RUST-REF-022
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/255
title: Restrict incomplete download rechecks to verified payload ranges
status: OPEN
priority: Minor
category: refactor
labels: [rust, downloads, io, hashing, integrity]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/255. This local document owns the durable engineering specification and evidence.

# RUST-REF-022 - Restrict incomplete download rechecks to verified payload ranges

## Summary

Revalidate an incomplete download's persisted verified pieces without scanning
unverified regions or computing an unused complete recovery tree. Preserve the
separate mandatory whole-file completion check. This is a bounded I/O
improvement for explicit rechecks, not a blocker for ordinary beta operation.

## Revalidated Findings

On Rust branch `58595576`, `final_recheck_transfer` chooses a full finalizer for
completed/fully verified payloads and `recheck_verified_partial_pieces` for
incomplete payloads. The latter returns early if there are no verified pieces,
but otherwise invokes `compute_final_rehash(path, expected_size)`.

That helper seeks to zero and processes the expected file sequentially until
the complete expected payload or an early EOF. It computes MD4 for every read
part and SHA-1 leaves/root material even for unverified regions. The partial
caller uses the result to inspect only persisted verified pieces. A pre-sized
or sparsely populated file can therefore cause a recheck of a small verified
subset to read a much larger logical range and allocate unused recovery data.
Without the branch's combined recovery change, main `e3372aba` already uses the
whole-file helper for partial rechecks; revalidate current main before work.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/completion_rehash.rs`:
  `final_recheck_transfer`, `recheck_verified_partial_pieces`,
  `compute_final_rehash`, and damaged-verified-piece selection.
- `piece_store.rs::recheck_transfer` in that directory: runtime entrypoint.
- `crates/emulebb-core/src/transfer_control_api.rs`: pause/recheck/resume and
  per-transfer coordination.
- `ed2k_transfer/tests/completion_rehash.rs`: targeted damage and restart tests.
- `ed2k_transfer/hashset.rs`: reusable part digest and tree geometry.

## Intended Shape

Take a revisioned snapshot of the verified piece indexes and required MD4/
trusted-AICH authority. Open the current payload once through the existing
handle/native-identity boundary, select only those complete part ranges, and
process them in ascending order. Coalesce adjacent ranges when useful without
reading intervening unverified gaps. Bound retained buffers/results by the
selected work, not the file's full expected size.

Calculate MD4 and any available trusted AICH part evidence from the same owned
buffer under RUST-BUG-165's contract. Root-only multi-part evidence cannot
localize a part check without corresponding trusted part hashes; do not scan
unverified bytes just to manufacture that authority. A single-part trusted
master has its normal direct verification semantics. Do not build or persist
an alleged complete recovery set from a verified subset.

A short file or EOF inside a selected verified range demotes that affected
piece according to existing corruption/recovery rules. Valid earlier/later
selected pieces retain their independent disposition. Preserve missing/foreign
payload handling, stable opened-path identity, source mutation checks, and the
generation check before publishing results. Do not accidentally apply full-file
expected-size assertions to a legitimately incomplete shorter piece store.

A recheck must not race live writers or overwrite newer verified state. Use the
existing pause/lifecycle mechanism plus per-file revision checks, and discard
stale results after delete/recreate, trust changes, or resumed writes. Storage
admission uses RUST-REF-009; substantive digest work uses RUST-REF-019's bounded
blocking lane. Cancellation retains the running worker's permit until it exits.

This path only refreshes already-verified authority: it never promotes missing
or partially received data, marks the download complete, or clears the final
completion barrier. When all parts are present, the existing full-file MD4/
AICH finalizer remains mandatory and retains its crash-consistency contract.

## Acceptance Criteria

- [ ] Instrumented partial recheck reads exactly the selected verified ranges
      apart from bounded metadata operations, with zero reads of unverified gaps.
- [ ] No-verified-piece, first/last/discontiguous pieces, exact-part boundaries,
      sparse/pre-sized files, and >4-GiB offsets have bounded read behavior.
- [ ] Same-size corruption, EOF/truncation, missing payload, and replaced native
      objects receive correct targeted demotion without losing unaffected pieces.
- [ ] Selected pieces obey MD4 plus available trusted-AICH verification without
      an additional payload pass or fabricated complete recovery metadata.
- [ ] Pause/resume, concurrent-write, delete/recreate, trust-change, cancel, and
      shutdown races cannot publish results for a stale piece generation.
- [ ] Full-file completion and restart finalization are unchanged and still
      detect mutation of an earlier verified part before delivery.
- [ ] A bounded synthetic comparison records logical reads, physical-I/O
      disposition, checksum CPU, buffers, and queue wait against current head.

## Validation and Dependencies

Use deterministic positioned-read counters and barriers rather than wall-clock
assertions. Extend existing completion tests with a sparse large expected file
and a small verified subset, including later valid ranges beyond an earlier
damaged range. Add platform-capability tests for sparse allocation without
requiring it on every filesystem. RUST-FEAT-048 owns sparse-file creation,
RUST-BUG-165 owns integrity acceptance, and RUST-REF-009/019 own admission and
CPU placement. No public-network or operator-library campaign is required.

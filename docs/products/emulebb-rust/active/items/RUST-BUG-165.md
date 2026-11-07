---
id: RUST-BUG-165
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/249
title: Require trusted AICH and MD4 agreement during download verification
status: OPEN
priority: Major
category: bug
labels: [rust, aich, integrity, parity, downloads]
milestone: post-beta-compatibility
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/249. This local document owns the durable engineering specification and evidence.

# RUST-BUG-165 - Require trusted AICH and MD4 agreement during download verification

## Summary and Disposition

Apply available trusted AICH evidence as an independent integrity check during
part verification, recheck, and completion while retaining mandatory MD4 file
identity. Gate a claim of stock-equivalent AICH integrity on this result. The
finding does not demonstrate routine corrupted-file acceptance in current beta
use; it identifies a missing independent guard and explicit conflicting-root
behavior. RUST-BUG-164 must establish trust before this enforcement is enabled.

## Revalidated Findings

On Rust branch `fix/stock-hash-share-tree` at `58595576`,
`manifest.rs::verify_piece_against_manifest` calculates only MD4. At completion,
`whole_file_matches` checks size and eD2K MD4 identity. A mismatching acquired
AICH root can be preserved while MD4 completion succeeds and recovery serving
is unavailable. If only a root is present, the local computation can replace it
because `aich_hashset_acquired` is false. Root-only authoritative input and an
untrusted candidate must not share an implicit overwrite rule.

`completed_manifest_preserves_remote_aich_identity_over_local_rebuild` explicitly
expects a completed MD4-valid payload whose computed AICH differs from the
preserved acquired root. Updating implementation requires revising that
expectation deliberately, not silently dropping its coverage. Main `e3372aba`
also uses MD4-only ordinary part verification; revalidate current main before
implementation.

MFC `CPartFile::HashSinglePart` calculates available AICH and MD4 evidence and
returns failure if either disagrees. Its final/rehash comparison also checks
available AICH. A valid root alone suffices for a single-part file; a multi-part
file needs a trusted complete part set to localize a part failure. Whole-file
completion can compare a trusted master even before per-part evidence exists.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/manifest.rs`: verification result.
- `piece_store.rs`, `requested_block.rs`, `salvage.rs`, and `ich_salvage.rs`
  in that directory: all transitions that mark a piece verified.
- `completion_rehash.rs`: combined computation, damage localization,
  `final_rehash`, and incomplete rechecks.
- `hashset.rs` and `aich_recovery.rs`: existing stock-compatible tree geometry.
- `tests.rs::completed_manifest_preserves_remote_aich_identity_over_local_rebuild`
  and `tests/completion_rehash.rs`.
- Stock/MFC `PartFile.cpp::HashSinglePart` and final hash-result handling.

## Intended Behavior and I/O Contract

Use a structured verification outcome that distinguishes MD4 failure, trusted
AICH failure, unavailable optional evidence, and storage failure. An untrusted
candidate never becomes an integrity authority. Absence of optional AICH must
not reject an otherwise valid MD4 transfer. A disagreement with available
trusted evidence must not mark the affected part/file complete or publish it.

Calculate part AICH from the same owned byte buffer already used for MD4.
For final verification, use the existing combined sequential reader and its
computed root/part roots. Do not add a separate file read for the second digest.
Use the asymmetric stock tree shape, exact part boundaries, and the existing
special treatment of eD2K exact-part multiples; AICH has no synthetic empty MD4
part. Place substantive CPU work behind RUST-REF-019's bounded worker boundary.

When localization is possible, retain unaffected verified parts and enter the
existing bounded recovery path. If only a master conflict is known, preserve
evidence and fail safely without arbitrarily blaming a peer or repeatedly
redownloading the same bytes without a diagnostic disposition. The outcome
must cover explicit link roots, consensus, and acquired part sets consistently.

An optional recovery-cache storage failure is different from cryptographic
disagreement. Preserve the latest branch's completion-crash fixes: attempt to
retain available computed recovery before publishing completion; a failed or
aborted optional transaction must not prevent durable valid MD4 completion or
force payload verification to repeat on every restart. Tests for the successful
cache-before-completion crash window and nonfatal cache failure remain required.
Do not restore the superseded save-completion-before-cache crash window.

## Acceptance Criteria

- [ ] MD4-valid/AICH-invalid parts and complete files fail trusted-AICH
      verification; AICH-valid/MD4-invalid data still fails mandatory MD4.
- [ ] Matching evidence passes and absent/untrusted AICH leaves MD4 behavior
      intact. A root-only authoritative mismatch is never silently overwritten.
- [ ] Single-block, partial-block, exact-part, uneven multi-part, and >4-GiB
      fixtures produce the same stock-derived roots and acceptance decisions.
- [ ] Every piece-promotion path, ICH/AICH salvage completion, operator recheck,
      and restart finalizer uses the same verification contract.
- [ ] Localized failures retain good pieces; an unlocalized root conflict has
      an explicit bounded disposition and does not fabricate peer blame.
- [ ] Read counters prove no extra payload pass for adding AICH verification.
- [ ] Optional-cache write failure/transaction abort and successful-cache crash
      tests preserve the current durable completion and recovery guarantees.
- [ ] Existing tests that intentionally accept conflicting acquired AICH are
      replaced with explicit trusted/untrusted/conflicting-state coverage.

## Validation and Dependencies

Add deterministic part, finalizer, salvage, and restart tests plus stock/MFC
goldens through RUST-CI-031. Inject a self-consistent trusted AICH tree for other
bytes while keeping the payload's MD4 correct; do not require a real MD4
collision fixture to test the disagreement branch. Count payload reads and CPU
jobs before/after. RUST-BUG-164 owns trust; RUST-REF-019 owns executor placement;
RUST-REF-022 owns reducing incomplete-recheck ranges; RUST-FEAT-065 owns visible
conflict state. No new protocol extension or MFC implementation change belongs
to this item.

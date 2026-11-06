---
id: RUST-BUG-160
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/243
title: Reuse stock hashes across unambiguous Unicode filename normalization
status: OPEN
priority: Minor
category: bug
labels: [rust, import, unicode, hashes, portability]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/243. This local document owns the durable engineering specification and evidence.

# RUST-BUG-160 - Reuse stock hashes across unambiguous Unicode filename normalization

## Summary

Own approved follow-up 7. Reuse trusted stock/MFC hashes when equivalent
Unicode spellings identify the same migrated target file, while rejecting
ambiguous associations. Preserve exact native path bytes and the original
archive records. This is post-beta backlog work, not a regression claim against
the already validated Windows/Docker import cohort.

## Current Findings

Review branch `43855fba` imports a read-only exchange archive directly into
live metadata. Its per-path admission compares the path basename with
`displayName` as an exact Rust string, alongside size and stock modification
time. Source path discovery also uses exact name/size/time keys. Composed and
decomposed names can therefore miss a valid association when a copy or target
filesystem changes the spelling.

This is a conditional portability risk, not proof that every macOS copy fails:
a filesystem may resolve equivalent input spellings itself. Existing unchanged
Unicode paths already work. RUST-BUG-107's exact NativePath storage remains the
correct foundation; do not reopen or replace it with normalized identity.

## Representative Sites

- `crates/emulebb-daemon/src/profile_import.rs`: `merge_exchange_batch`
  and basename/size/time admission.
- `crates/emulebb-metadata/src/profile_import.rs`: live binding/conflict rules.
- `crates/emulebb-metadata/src/native_path.rs` and `text.rs`.
- `repos/emulebb-build-tests/emule_test_harness/profile_exchange.py`
  and `profile_import_audit.py`: artifact preparation and independent audits.

## Intended Shape

Keep the archive's source record and explicit target-path-to-record association
authoritative. Prefer exact matches, then allow a separate canonical Unicode
comparison key only for a unique compatible association. NFC is a candidate;
search NFKC and heuristic network mojibake/HTML/percent repair must never become
filesystem identity.

Detect incompatible records that converge on one target path or native file
identity before accepting a fallback association. Apply case equivalence only
when RUST-BUG-161 provides evidence for the target semantics. Leave ambiguity
unresolved with a precise report instead of selecting a candidate or hashing
payloads automatically.

Use the same documented comparison contract in export discovery, Rust
admission, and independent validation. Prefer existing archive IDs/path links
over a format change. Any required format change is a clean new exchange
version regenerated from stock; it is not a runtime compatibility shim.

## Scope Constraints

- No NFC/NFKC rewrite, rename, or lossy conversion of native path storage.
- Keep stock hashes trusted by default, verify size/time and native target
  fingerprints, and preserve conflicting existing live bindings/preferences.
- Keep unmatched records in the read-only archive; no native staging tables.
- Native Rust database upgradeability remains separate from stock/MFC import.

## Acceptance Criteria

- [ ] A unique compatible NFC/NFD association reuses MD4 and available full AICH
      with zero payload reads on supported target filesystems.
- [ ] Canonically equivalent conflicting records, target aliases, and same
      size/time collision cases remain explicitly unresolved.
- [ ] Compatibility-only pairs such as circled digits versus ASCII, literal
      percent/entity text, and distinct native byte names do not falsely match.
- [ ] Repeated and merge imports preserve existing accepted identities and
      richer hashsets; source/archive checksums remain unchanged.
- [ ] Reports distinguish exact reuse, normalization-based reuse, ambiguity,
      changed metadata, and unavailable paths without automatic rehashing.

## Validation

Use synthetic stock metadata/exchange fixtures and remapped Windows/Linux/macOS
targets. Test both normalization-preserving and normalization-insensitive
filesystems when available, recording unsupported capabilities explicitly.
Retain end-to-end evidence in RUST-CI-008 and preserve RUST-BUG-158's no-rehash
contract.

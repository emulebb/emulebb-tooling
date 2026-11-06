---
id: RUST-BUG-161
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/244
title: Respect filesystem case semantics when consolidating shared roots
status: OPEN
priority: Major
category: bug
labels: [rust, sharing, paths, unicode, portability]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/244. This local document owns the durable engineering specification and evidence.

# RUST-BUG-161 - Respect filesystem case semantics when consolidating shared roots

## Summary

Own approved follow-up 8. Make root comparison reflect the relevant filesystem
or directory semantics, preserving distinct configured trees and collapsing
only proven ancestors/aliases. This is post-beta backlog work.

## Current Findings

The root work at `43855fba` centralizes consolidation for imports, API
mutations, and effective scan roots. Its comparison key canonicalizes when
possible, lowercases on Windows, and compares exact text elsewhere.

That OS-wide rule does not establish the behavior of case-sensitive Windows
directories or case-insensitive macOS volumes, especially for unavailable
paths. It also does not establish Windows ordinal comparison equivalence for
every Unicode character. Raw native path storage is already lossless; this
item fixes comparison policy rather than storage encoding.

Canonicalization may resolve some aliases/casing on accessible paths, but must
not be treated as a universal case/normalization capability detector.

## Representative Sites

- `crates/emulebb-core/src/shared_directories.rs`:
  `shared_root_comparison_key`, consolidation, implicit/effective roots.
- `crates/emulebb-core/src/shared_file_api.rs`: root add/remove/replace.
- `crates/emulebb-daemon/src/shared_directory_import.rs` and
  `profile_import.rs`: callers of the same root policy.
- `crates/emulebb-metadata/src/native_path.rs`: exact identity to retain.

## Intended Shape

Use read-only native capability information and canonical filesystem identity
where available. Windows may require directory-level case-sensitivity evidence;
Unix/macOS behavior must follow the mounted filesystem rather than an OS label.
Cache capability observations at the appropriate volume/directory scope and
perform blocking discovery through RUST-REF-018.

Keep exact native paths independent of comparison keys. Preserve component
boundaries and common parent/child policy across every entry point. When
identity or case semantics are unknown, avoid collapsing potentially distinct
trees on a guessed case fold; expose the unresolved capability. An exact native
ancestor remains a valid recursive ancestor.

Do not create probe files in user libraries to discover capabilities. Synthetic
write probes belong only to test-owned fixture roots. Reconcile previously
unavailable roots without discarding accepted file hashes.

## Scope Constraints

- Preserve RUST-BUG-107's NativePath BLOB identity and fingerprint safeguards.
- No global lowercasing or Unicode normalization of stored paths.
- No independent REST, CLI, or import comparison implementations.
- Path equality does not replace native fingerprint checks for serving files.

## Acceptance Criteria

- [ ] A representable case-sensitive Windows pair remains two distinct roots.
- [ ] Case-insensitive equivalent roots on supported volumes collapse correctly.
- [ ] A true listed parent covers its child in either insertion order, while
      prefix siblings remain distinct and no unlisted parent is invented.
- [ ] Case/normalization aliases, inaccessible roots, and capability changes have
      explicit conservative behavior without wrong-tree removal or overwrite.
- [ ] Add/remove/bulk/import and scan selection use the same comparison policy.
- [ ] Capability discovery is bounded, off the executor, and read-only for
      operator trees; unchanged file hashes survive root reconciliation.

## Validation and Dependencies

Use resolver seams for deterministic capability states plus real Windows
directory-case, Linux native, and case-sensitive/case-insensitive APFS fixtures
where available. Test aliases and NFC/NFD pairs separately from case folding.
Coordinate root execution with RUST-REF-018, normalized import admission with
RUST-BUG-160, and cross-platform evidence with RUST-CI-008.

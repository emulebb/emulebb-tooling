---
id: RUST-BUG-159
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/242
title: Respect destination filename limits during download delivery
status: OPEN
priority: Major
category: bug
labels: [rust, delivery, paths, unicode, portability]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/242. This local document owns the durable engineering specification and evidence.

# RUST-BUG-159 - Respect destination filename limits during download delivery

## Summary

Own approved follow-up 6. Materialize downloads under a valid, collision-safe
destination filename even when the advertised name or a collision suffix
exceeds the destination's component budget. Preserve the canonical/original
name separately from the chosen physical leaf. This is post-beta backlog work.

## Current Findings

On main `e3372aba` and review branch `43855fba`,
`sanitize_file_name` replaces reserved characters, strips trailing spaces/dots,
handles Windows device basenames on every platform, and supplies a nonempty
fallback. Delivery then appends ` (n)` before the extension on collisions.
Neither step budgets the resulting filename for the destination filesystem.

Windows extended-length paths solve the legacy whole-path limit, not the
individual filename limit. NTFS commonly allows 255 UTF-16 code units per
component; ext4 commonly allows 255 encoded bytes. A repeated CJK or emoji name
therefore consumes different budgets across targets. The network-name intake's
4096-byte input bound is not a valid filesystem-component budget.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/deliver.rs`:
  `sanitize_file_name`, `split_stem_extension`, and production
  `deliver_payload_file`.
- `crates/emulebb-ed2k/src/file_name.rs`: network/canonical name preparation.
- `crates/emulebb-ed2k/src/long_path.rs`: whole-path access only.
- `crates/emulebb-ed2k/src/ed2k_transfer/tests/deliver_runtime.rs`.

## Intended Shape

Build one reusable delivery-leaf allocator that takes the canonical name,
destination capabilities, extension, and collision discriminator. Establish
limits in the units the target filesystem/API actually enforces; document any
stricter portable-naming policy instead of assuming 255 Unicode characters.

Reserve space for the extension and each suffix before shortening the stem.
Do not split UTF-8 sequences or UTF-16 surrogate pairs; prefer whole grapheme
boundaries where practical. Specify behavior for a very long extension,
combining text, non-BMP characters, and names that become reserved after
shortening. Keep a stable bounded discriminator so distinct long names sharing
a prefix cannot overwrite one another.

Preserve the original/canonical metadata and expose the actual delivered name.
Keep atomic no-clobber installation, durable delivery-attempt ownership,
staging verification, and retry/restart semantics. Check whole-path failure
separately from component overflow, including staging names.

## Scope Constraints

- Do not rename existing shared files or alter content hashes.
- No lossy conversion of native paths, arbitrary truncation of database path
  identity, or automatic native-profile migration.
- Unsupported/unknown destination capabilities must produce a documented safe
  policy or actionable error, never silent overwrite or data loss.

## Acceptance Criteria

- [ ] Boundary and over-boundary ASCII, accented, CJK, emoji, combining, and
      long-extension names produce valid leaves or explicit safe errors.
- [ ] Length accounting uses destination-native units and includes all suffixes.
- [ ] Distinct names with the same shortened prefix remain collision-safe under
      concurrent delivery and case/normalization-equivalent target names.
- [ ] Reserved names, trailing dots/spaces, empty names, and extensions retain
      their existing safety guarantees after shortening.
- [ ] Restart and collision retries preserve verified payloads, ownership of
      temporary artifacts, and the recorded final native path.
- [ ] Existing long-directory delivery and MD4/AICH results remain unchanged.

## Validation and Dependencies

Add allocator unit/property tests and native filesystem delivery tests under
owned synthetic output roots. Use capability-gated Windows, Linux, and macOS
limits rather than a universal constant. Coordinate comparison semantics with
RUST-BUG-161 and retain platform evidence in RUST-CI-008.

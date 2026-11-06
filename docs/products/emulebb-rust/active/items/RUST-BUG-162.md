---
id: RUST-BUG-162
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/246
title: Bound profile archive fields before allocating import buffers
status: OPEN
priority: Minor
category: bug
labels: [rust, persistence, imports, robustness]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved stock profile import branch review, finding 6
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/246. This local document owns the durable engineering specification and evidence.

# RUST-BUG-162 - Bound profile archive fields before allocating import buffers

## Summary

Enforce archive input limits before Rust or SQLite materializes oversized
values. This is an approved post-beta hardening follow-up, separate from the
completed hash consistency, merge, and recovery persistence fixes.

## Current Findings

`crates/emulebb-daemon/src/profile_import.rs` opens the archive read-only and
streams known records and recovery sets in bounded batches. However:

- The header is read into an unrestricted String before JSON parsing.
- Known-record Strings and packed MD4/AICH Vecs are allocated by `row.get`
  before their 64 KiB and 1,000,000-byte checks.
- Recovery leaves are allocated before their 1,060-byte part limit is checked.
- Archive paths and header root collections lack a complete admission budget.
- Raw packed-byte batch accounting does not describe JSON/hex expansion,
  decoded arrays, or peak SQLite allocation for an individual value.

The normal Python producer emits bounded records. A malformed or unusually
large archive can nevertheless exceed the reader's intended memory envelope
before the current checks reject it. Import is offline and operator-selected;
this finding is not a public peer-input vulnerability claim.

## Intended Shape

Define one reader-owned set of field and batch limits against supported eD2K
file geometry, native path limits, root counts, and 100,000-file archives.
Check borrowed row values or SQL lengths before owned copies. Where supported,
apply a source-connection SQLite length limit as well: a Rust-only copy check
does not bound SQLite's own row/VM allocation. Do not apply interchange limits
globally to the live metadata store.

Bound the header and collection cardinalities before expanding them. Account
for decoded/hex representations and the largest permitted single file, not
only packed input bytes. Retain streaming queries, bounded transactions,
bounded diagnostics, and the archive's read-only contract.

Structural invalidity is an explicit import failure. Rejected optional recovery
data retains usable accepted MD4 knowledge. Earlier committed batches remain
available for an explicit merge retry; no schema reset or automatic rehash is
introduced.

## Acceptance Criteria

- [ ] Header, records, hash arrays, recovery parts, and paths have documented
      admission limits enforced before avoidable owned allocation.
- [ ] SQLite and Rust allocation limits are measured and distinguished.
- [ ] Expanded representations and maximum valid per-file geometry fit the
      stated memory budget, including one oversized relative-to-batch file.
- [ ] Oversized values fail with a bounded, actionable diagnostic; rejection
      reasons cannot retain unbounded input strings.
- [ ] Valid 100,000-file exports, long-path fixtures, aliases, and full AICH
      imports remain supported with zero payload reads.
- [ ] Rejected input never modifies the archive or creates native staging
      tables, migrations, compatibility readers, or automatic repair hashing.

## Validation

Use synthetic SQLite archives with oversized header text, records, packed
hashsets, recovery leaves, and paths. Exercise size boundaries, truncated and
wrong-typed values, large valid files, and large root collections. Measure
process RSS as well as Rust allocations so SQLite's native memory is covered.
Retain the existing 100,000-record streaming and MD4-preservation regressions;
inject oversized optional recovery between valid neighboring sets and verify
exact retained/accepted outcomes. Run Windows and Linux import lanes through
the persisted harness without opening payloads or networking.

## Dependencies and Scope

Keep protocol geometry and hash reconstruction in the eD2K layer. Coordinate
database execution with RUST-REF-016 without making this fix depend on a global
async persistence rewrite. This item does not implement profile upgradeability
or change the one-way archive-to-live-table design.

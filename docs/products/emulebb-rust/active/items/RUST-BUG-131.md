---
id: RUST-BUG-131
workflow: github
product: emulebb-rust
phase: Phase 0
github_issue: https://github.com/emulebb/emulebb-rust/issues/153
title: Make category deletion and transfer remap atomic
status: OPEN
priority: Major
category: bug
labels: [rust, categories, sqlite, transactions, persistence, beta]
milestone: rust-v0.1.0-beta.3
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/153. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-131 - Make category deletion and transfer remap atomic

## Summary

Apply category deletion, category ordering changes, and affected transfer
assignments as one durable operation. A failure at any intermediate statement
must leave both the running client and the restart state on the old category
snapshot.

## Current State

`crates/emulebb-core/src/category_runtime.rs` deletes the selected category,
deletes shifted rows, persists replacement category rows one at a time, and then
updates affected transfer manifests one at a time. The metadata APIs used by
that sequence own separate transactions. A mid-sequence error can therefore
leave missing or reinterpreted category indexes and transfer assignments that
do not match the in-memory snapshot.

`RUST-BUG-053` established the required user-visible behavior: transfers in the
deleted category return to default and later categories shift down. This item
preserves that behavior while fixing the durability boundary.

## Why This Matters

Category deletion is a compound state transition. Partial persistence can move
downloads into the wrong logical category after restart, which is a data-model
correctness defect rather than a recoverable display issue.

## Representative Sites

- `crates/emulebb-core/src/category_runtime.rs` category deletion and remap.
- `crates/emulebb-metadata/src/profile_store.rs` category row writes.
- `crates/emulebb-metadata/src/transfer_store.rs` transfer category updates.
- `crates/emulebb-ed2k/src/ed2k_transfer/metadata.rs` manifest category writes.

## Intended Shape

- Expose one metadata transaction that applies the category snapshot and every
  affected transfer assignment before commit.
- Publish the new in-memory snapshot only after the durable transaction commits.
- Prefer stable internal category identity plus a separate display/order field,
  projecting stock/MFC positional semantics at the API boundary, if that makes
  the schema and future reordering safer.
- If positional identifiers remain durable, update them in one set-oriented
  transaction with constraints that reject invalid references.

## Scope Constraints

- Preserve the `RUST-BUG-053` deletion result visible to users and imported MFC
  profiles.
- The beta schema and API may change when a stable identity model produces the
  cleaner long-term design; do not retain a fragile schema for compatibility.
- Do not hold the global async core-state lock while SQLite waits or flushes;
  coordinate that boundary with `RUST-REF-016`.
- Do not silently repair ambiguous partial state after commit; prevent it from
  being committed.

## Acceptance Criteria

- [ ] Category deletion and every affected transfer assignment commit in one
      atomic durable transaction.
- [ ] Failure injection at each write boundary leaves the pre-delete snapshot
      intact both in memory and after restart.
- [ ] Successful deletion resets transfers in the removed category and shifts
      later user-visible categories exactly once.
- [ ] Category identifiers cannot refer to a different logical category after
      crash, rollback, retry, or restart.
- [ ] Concurrent category and transfer mutations are serialized through an
      explicit ownership boundary instead of incidental global locking.

## Validation

- Metadata transaction tests with statement-by-statement failure injection.
- Core restart tests for first, middle, last, populated, and empty category
  deletion.
- Concurrent category edit and transfer update tests.
- Imported MFC profile regression preserving expected positional behavior.

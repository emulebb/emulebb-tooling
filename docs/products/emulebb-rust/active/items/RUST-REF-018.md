---
id: RUST-REF-018
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/240
title: Keep shared-root filesystem work outside async state locks
status: OPEN
priority: Major
category: refactor
labels: [rust, sharing, async, io, concurrency]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/240. This local document owns the durable engineering specification and evidence.

# RUST-REF-018 - Keep shared-root filesystem work outside async state locks

## Summary

Own approved follow-ups 1 and 2: root-status lock scope and async root
operations. Keep slow directory probes, canonicalization, and root persistence
outside Tokio executor threads and global state locks. This is post-beta
backlog work, not a blocker for the validated stock-import workflow.

## Current Findings

The review used Rust main `e3372aba` and the import/root work at `43855fba`.
In `shared_file_api.rs`, `shared_directories()` holds the core state guard
while `refresh_shared_directory_row` calls blocking filesystem metadata APIs.
Root removal also performs filesystem-backed comparison under that guard.
Add and bulk-replace operations synchronously canonicalize/inspect directories.
The common consolidation helper uses filesystem canonicalization, including
when invoked from async effective-root selection and mutations.

A disconnected share or slow disk can therefore occupy an executor thread and
hold unrelated core operations behind a filesystem wait. The cached
`shared_directory_reload_progress()` accessor already avoids these probes;
retain that fix rather than reopening its completed CLI progress issue.

## Representative Sites

- `crates/emulebb-core/src/shared_file_api.rs`: status, add, remove, replace,
  `canonical_shared_directory_root`, and `removable_shared_directory_root`.
- `crates/emulebb-core/src/shared_directories.rs`: root refresh, implicit
  roots, `consolidate_shared_directory_roots`, and comparison keys.
- `crates/emulebb-daemon/src/shared_directory_import.rs`: synchronous offline
  adapter to the same consolidation policy.

## Intended Shape

### A. Root status and lock scope

Snapshot root configuration and its revision under a short state lock, then
release the guard before probing. Refresh accessibility through a bounded
blocking lane. Frequent status requests should read cached observations with
explicit freshness and unknown/pending/error semantics, rather than each
request probing every configured volume.

Publish results only if the root identity and configuration revision still
match. A stale probe must not resurrect a removed root or overwrite a newer
edit. Reuse watcher/degraded-root information from RUST-REF-010 without making
watcher delivery the sole authority.

### B. Root mutations and validation

Capture owned inputs, resolve and inspect them in bounded blocking jobs, then
apply the one common recursive-root policy. Recheck the configuration revision
before committing/publishing the new state. Persistence uses RUST-REF-016;
filesystem placement and SQLite scheduling have separate ownership.

Keep add-child as a successful no-op when a shared parent covers it, collapse
existing explicit children when adding a parent, retain siblings, and preserve
mandatory Incoming/category origins. Do not copy the policy into REST handlers.

Bound queued probes and concurrent filesystem jobs. Request timeout or
cancellation must not be described as cancellation of an already-running
blocking OS call: retain its resource permit until it actually completes.

## Scope Constraints

- Synchronous filesystem helpers remain valid inside a blocking worker and
  exclusive offline commands. No async conversion of every small helper.
- No lock held across filesystem work, database wait, or worker join may be a
  global core/search/index lock.
- Preserve exact NativePath identity, no-rehash reuse, and one root policy.
- Keep native-profile schema upgrades and stock parsing outside this item.

## Acceptance Criteria

- [ ] Root status returns cached observations while an injected filesystem
      probe is blocked; unrelated REST work and executor heartbeats continue.
- [ ] Add/remove/bulk validation and implicit/effective-root preparation perform
      blocking probes off the executor without holding shared state.
- [ ] Root revisions prevent stale status publication and lost concurrent edits.
- [ ] Queue saturation and unavailable volumes have explicit bounded behavior.
- [ ] Cancellation cannot leak permits, grow replacement workers without bound,
      or publish a partially validated root set.
- [ ] Parent/child/sibling, Incoming/category, alias, and repeated-update tests
      preserve roots and hashes without payload reads for unchanged files.

## Validation and Dependencies

Use deterministic slow-probe barriers, a single-worker Tokio liveness test,
concurrent-edit tests, and existing root/API/import regressions. Use synthetic
unavailable roots, never an unbounded operator-library campaign. Coordinate
database commits with RUST-REF-016, path comparison with RUST-BUG-161, and
watcher refresh with RUST-REF-010.

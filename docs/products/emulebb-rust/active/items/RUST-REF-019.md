---
id: RUST-REF-019
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/241
title: Offload remaining transfer and large-library CPU bursts
status: OPEN
priority: Minor
category: refactor
labels: [rust, async, hashing, performance, sharing]
milestone: post-beta-polish
created: 2026-11-06
source: Operator-approved Rust async I/O and path portability review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/241. This local document owns the durable engineering specification and evidence.

# RUST-REF-019 - Offload remaining transfer and large-library CPU bursts

## Summary

Own approved follow-up 4. Keep substantial part verification and large-library
index/sort work off cooperative network/API executor threads, with bounded
admission and evidence of useful latency improvement. This is post-beta backlog
work; whole-file MD4/AICH hashing is already correctly offloaded.

## Current Findings

At review commit `43855fba`, local ingest computes MD4, AICH, and recovery
material in one sequential blocking-worker read. Result persistence and media
extraction are also offloaded. Preserve those paths.

Some download piece-completion paths call `verify_piece_against_manifest`
inline after an async read; it calculates MD4 over a complete eD2K part.
The verified-local reload index builds its HashMap after the database worker
returns. The full scan also sorts, deduplicates, and inspects the returned file
vector on its async caller. These operations can be substantial at 100K+
entries, although the review did not establish a new measured latency budget.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs`: piece completion.
- `crates/emulebb-ed2k/src/ed2k_transfer/manifest.rs`:
  `verify_piece_against_manifest`.
- `crates/emulebb-ed2k/src/ed2k_transfer/reload_index.rs`:
  `verified_local_reload_index`.
- `crates/emulebb-core/src/shared_directories.rs`: `scan_shared_files`
  and reload planning.
- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs`: existing correct model.

## Intended Shape

Move owned complete-part buffers into bounded CPU jobs without an additional
full-buffer copy. Return the digest/verdict and preserve the per-file ordering
and generation checks needed before publishing verified state. A per-file
ordering guard may span the worker wait when required; a global state lock may
not.

Build the reload index within its existing blocking fetch job where practical.
Keep large scan post-processing inside a coarse blocking boundary or bounded
chunks, avoiding a task for every file or path component. Measure before
changing already-cheap comparisons, decoding, or tiny hash operations.

Share resource admission with RUST-REF-009. A large-library hash must not
starve short transfer verification jobs. Record queue wait, execution duration,
executor heartbeat latency, peak memory, and payload read bytes.

## Scope Constraints

- No ED2K/AICH result, piece verification, ICH, or crash-ordering change.
- Keep one-pass whole-file MD4/AICH and buffered sequential worker I/O.
- No unbounded CPU/task fan-out or extra whole-file payload pass.
- Ingest batching and logical-I/O amplification remain in RUST-REF-008.

## Acceptance Criteria

- [ ] Complete-part verification cannot monopolize a Tokio worker and retains
      identical accepted/rejected results for existing cryptographic fixtures.
- [ ] Global async state locks are not held during CPU-job waits.
- [ ] The 100K-entry index/sort path has a measured executor-latency disposition;
      material bursts are offloaded without a second whole-tree data graph.
- [ ] CPU job concurrency and queue depth are bounded; cancellation and shutdown
      do not fabricate completion or lose required verification results.
- [ ] Existing one-pass hashing, memory bounds, and payload-read counts survive.

## Validation

Use deterministic worker barriers plus single-worker executor liveness tests,
existing part/hash/ICH regressions, and synthetic small/100K metadata cohorts.
Compare latency and memory before/after. No real-media rehash campaign is
required to prove executor placement.

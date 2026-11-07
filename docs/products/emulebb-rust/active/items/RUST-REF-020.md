---
id: RUST-REF-020
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/252
title: Reuse validated incoming AICH recovery proofs within bounded ownership
status: OPEN
priority: Minor
category: refactor
labels: [rust, aich, recovery, caching, performance]
milestone: post-beta-polish
created: 2026-11-07
source: Operator-approved AICH and physical-drive I/O review
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/252. This local document owns the durable engineering specification and evidence.

# RUST-REF-020 - Reuse validated incoming AICH recovery proofs within bounded ownership

## Summary

Retain validated received recovery evidence so another recovery attempt for the
same trusted content and part need not request the hashes again. Match MFC's
use of available in-memory part recovery data, with explicit byte bounds and
trust/generation ownership. This is an efficiency improvement, not a public
release blocker or a substitute for request admission and payload verification.

## Revalidated Findings

At Rust branch `58595576`, `trusted_part_block_hashes_from_recovery` reconstructs
and validates the received proof in a temporary tree. `begin_part_salvage` uses
the returned block hashes to inspect current local bytes, but does not retain
those hashes for a subsequent recovery request. The persistent complete-set
store and the process-wide bounded answer cache primarily support serving
other peers; they do not provide a transfer's retained incoming partial-proof
contract. A downloaded block bitmap records presence, not trusted hash leaves.

MFC `CPartFile::RequestAICHRecovery` checks `IsPartDataAvailable` before asking
another client. Rust's request scheduler can make the same useful local check
after RUST-BUG-167 establishes one recovery demand authority. These are source
findings, not measured bandwidth savings. Revalidate current main before work;
do not reopen RUST-BUG-158's completed complete-set persistence work.

## Representative Sites

- `crates/emulebb-ed2k/src/ed2k_transfer/aich_recovery.rs`: proof validation and
  trusted block-hash extraction.
- `salvage.rs` in that directory: local comparison and state publication.
- `crates/emulebb-ed2k/src/ed2k_tcp/download/aich_request.rs`: local lookup before
  network dispatch through RUST-BUG-167.
- `crates/emulebb-ed2k/src/ed2k_transfer/aich_answer_cache.rs`: existing bounded
  outbound cache; reuse mechanisms where appropriate, not its authority model.
- `crates/emulebb-metadata/src/aich_recovery_store.rs`: complete sets only.

## Intended Shape

After RUST-BUG-166 correlates a solicited answer and validates it against an
active trusted master, retain the compact ordered hashes or canonical proof.
Key reusable evidence by master, file size, and part geometry, with a separate
binding to the current transfer/trust generation. Paths, names, sockets, and a
previous bitmap verdict must not become reusable content identity.

Before another network request, inspect eligible local evidence. Reuse only
the hashes: compare them with the current payload bytes again before retaining
blocks, and preserve the mandatory MD4 plus trusted-AICH verification contract
from RUST-BUG-165. Receiving a valid proof does not establish that any local
payload block is present, correct, durable, or shareable.

Use a process-wide byte budget and bounded entry/bookkeeping allocation, not
an unbounded cache per transfer. Coalesce work without unbounded waiters and
define eviction as a harmless optimization loss. Release transfer references
on retirement and invalidate activation on trust changes; immutable validated
content evidence may survive an alias change without rebinding a native path.
Bound concurrent revalidation with RUST-REF-019/RUST-REF-009.

Session-memory reuse is the minimum outcome. Persist partial proofs only with
measured justification and an explicit schema contract in the same native
SQLite database. A partial proof must never satisfy the complete-set marker or
be inserted as a fake complete set. Any schema change requires a fresh profile;
no automatic profile repair, migration, or hidden payload rehash is permitted.

## Acceptance Criteria

- [ ] A repeated recovery of the same trusted part reuses validated evidence
      with no additional AICH request when the evidence remains eligible.
- [ ] Wrong-root/size/part proofs and unrequested answers never populate the
      reusable cache; changed trust cannot activate an old proof.
- [ ] Reused hashes are checked against current local bytes, not old bitmap
      decisions, including mutation and intervening redownload cases.
- [ ] Cache bytes, retained allocation, entry count, references, and in-flight
      work stay bounded across many transfers and library aliases.
- [ ] Eviction, transfer deletion, cancellation, and shutdown cause normal
      request/fallback behavior without losing verified payload authority.
- [ ] Complete-set serving/import, no-payload-read outbound answers, and
      existing two-job/64-MiB responder limits retain their guarantees.
- [ ] Counters distinguish validated reuse, miss, eviction, rejection, and
      avoided requests without claiming avoided payload reads where salvage
      still must read the current part.

## Validation and Dependencies

Use deterministic incoming proofs for repeated, mutated, evicted, and
root-changed transfers. Count network requests, current payload reads, actual
retained bytes, and final MD4/AICH results. Run corruption attribution tests to
ensure repeated use never double-debits old senders. RUST-BUG-164/165/166/167
own trust, integrity, admission, and lifecycle respectively; RUST-FEAT-065 owns
operator diagnostics. No new live campaign is required for cache correctness.

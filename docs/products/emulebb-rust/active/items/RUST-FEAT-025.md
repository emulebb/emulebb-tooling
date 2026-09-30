---
id: RUST-FEAT-025
workflow: local
title: Validate conformant duplicate-block rejection diagnostics
status: OPEN
priority: Minor
category: feature
labels: [ed2k, upload, anti-abuse, diagnostics, parity]
milestone: post-beta-polish
created: 2026-07-05
source: FEAT-025 revert 045a781 (oracle non-conformance); defensive-measures wave RUST-FEAT-024..029; 0.1.0-beta.1 release program (2026-07-05)
---

> This is a local post-beta evidence item. File a GitHub issue only when the
> bounded diagnostic campaign is scheduled.

# RUST-FEAT-025 - Validate conformant duplicate-block rejection diagnostics

## Summary

The product implementation is complete: duplicate-done and duplicate-queued
requests are rejected through separate plan arms, both diagnostic events use a
bounded process-global ledger with the conformant body shape, and queued keys
survive across request packets until their generation drains. This item now
tracks only the two remaining evidence checks; it is not a beta blocker.

## Release Triage (2026-09-30)

**Post-beta evidence.** Commits `b1c732c` and `1ea5c15` implement the behavior;
current unit coverage proves process-global counting and queued-vs-completed
classification, the offline oracle diff is clean, and the full candidate test
matrix passed. No retained campaign record contains either diagnostic event,
so a feature-enabled body capture and a bounded live Rust/MFC count comparison
remain explicit rather than being inferred from implementation tests.

## Why the first attempt was reverted (045a781)

The `4ff79d4` emitter carried only `{action, reason, startOffset, endOffset,
partIndex}`; the oracle event also carries `repeatCount` and `windowSeconds`,
so the rust⊇oracle body-key check in `diag_event_diff` failed. Root causes to
avoid this time:

1. **Ledger scope:** MFC counts **rejections** in a **process-global** ledger
   (`g_badPeerBehaviorLedger`, `UpdateBehaviorLedger` keyed
   `peerKey|block|fileHash|start|end`, window `MIN2MS(60)` -> 3600 s, 60 s
   cleanup sweep) that survives reconnects. A per-connection or per-request
   count skews `repeatCount`.
2. **Body shape:** the harness adapter sets `behavior` only for
   `repeat_block_request`/`repeat_file_request`; this event's body must **not**
   include a `behavior` key.

## Intended Shape

- Global rejection ledger in
  `crates/emulebb-ed2k/src/ed2k_transfer/diag_bad_peer.rs`: key
  `peer|file|start|end`, window `REPEAT_BLOCK_WINDOW_SECS` (3600), counts
  rejection events, pruned and bounded.
- Emitter body: `{action: "reject_block_request", reason: "Duplicate upload
  block request already completed in slot", repeatCount, windowSeconds: 3600,
  startOffset, endOffset, partIndex}` (partIndex = start / ED2K_PART_SIZE).
- Emit sites in
  `crates/emulebb-ed2k/src/ed2k_tcp/listener/session/upload_payload.rs`:
  duplicate-done only on the `(Granted, DuplicateDone)` plan arm; the
  intra-packet dedupe arm gets the sibling
  `upload_duplicate_queued_block_rejected` (reason "...already queued in
  slot") — MFC has both events (`UploadClient.cpp:752,771`) and the reverted
  code mislabeled the queued branch.
- Existing observe-only `repeat_block_request` emission stays untouched.

## Acceptance Criteria

- [x] Ledger unit tests: first rejection => repeatCount 1, second => 2, window
      prune, bounded size.
- [x] Listener/queue tests assert queued and completed duplicates are rejected
      and classified separately across packet generations.
- [ ] With packet diagnostics enabled, capture an event body containing
      `repeatCount: 1, windowSeconds: 3600` and **no** `behavior` key.
- [x] Offline oracle-conformance diff (`emulebb-build-tests` `diag_event_diff`)
      clean for both events — the exact check that caught the revert.
- [ ] Run a bounded live converged-soak witness that observes and compares
      `repeatCount` alignment with MFC.

## Notes

- Implementation landed in emulebb-rust commits `b1c732c` and `1ea5c15`; only
  the two evidence checks above remain before archival.

- Oracle references: `srchybrid/UploadClient.cpp:752` (done), `:771` (queued),
  `srchybrid/BadPeerDiagnosticsSeams.cpp:400-455`
  (`LogUploadBlockRequestBehavior` + `UpdateBehaviorLedger`).
- Adapter mapping: `emule_test_harness/mfc_diag_adapter.py` passes the event
  name through and maps `repeat_count/window_seconds/...` to camelCase.

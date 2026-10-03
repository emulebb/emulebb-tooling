---
id: RUST-BUG-102
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/23
title: Require a stock-compatible final completion rehash
status: OPEN
priority: Major
category: bug
labels: [rust, ed2k, transfer, integrity, aich, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/23. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-102 - Require a stock-compatible final completion rehash

## Summary

Do not expose a completed download until a whole-file MD4/ED2K rehash has
validated the assembled bytes. Rust currently verifies each part as it arrives
and records completion, but delivery trusts the persisted completed manifest.
Stock eMule and current aMule both retain a distinct final hashing/completing
transition before the file becomes deliverable.

## Current State

- `crates/emulebb-ed2k/src/ed2k_transfer/piece_store.rs` verifies a completed
  part by reading it back, then marks the part complete. It also exposes a
  manual `recheck_transfer` path.
- `crates/emulebb-core/src/delivery.rs` accepts the completed-part manifest as
  sufficient for delivery; no automatic final whole-file recheck is required.
- Stock eMule enters its completing state and hashes the assembled file in
  `workspaces\workspace\app\emulebb-main\srchybrid\PartFile.cpp` before the
  completed file transition.
- Current aMule follows the same completion-after-rehash model in
  `analysis\amule\src\PartFile.cpp` and can use AICH recovery when rehashing
  identifies damaged data.

The gap matters even when every inbound part initially verified: storage can be
mutated after verification, state can survive a crash, and a stale or damaged
manifest can be loaded on restart.

## Why This Matters

Publishing or moving bytes under the expected ED2K identity without validating
the final assembled file violates the integrity boundary users expect from
stock clients. It can also make later corruption look like remote peer failure
rather than local persistence damage.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-ed2k\src\ed2k_transfer\piece_store.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\delivery.rs`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\PartFile.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\PartFile.cpp`

## Intended Shape

- Add an explicit completing/hashing state between all-parts-present and
  deliverable.
- Automatically calculate and compare the complete ED2K MD4 identity before
  first delivery, including recovery after restart into a pending-delivery
  state.
- If the check fails, demote the affected part or parts from complete and make
  them eligible for download again; use available AICH information to localize
  or recover corruption without weakening MD4 acceptance.
- Persist the transition so a crash cannot skip the final check or make a
  partially delivered file appear complete.
- Keep the existing manual recheck as an operator action, but do not rely on it
  for the normal completion guarantee.

## Scope Constraints

- Preserve the ED2K part hash and AICH verification already applied on receipt.
- Do not deliver, share, or announce the destination file before the final
  identity check succeeds.
- Do not accept an AICH result as a substitute for the ED2K file hash.
- Recovery must be bounded and must not silently discard a user's valid file.

## Acceptance Criteria

- [ ] Normal completion automatically enters a visible completing/hashing state
      and performs a full assembled-file ED2K rehash.
- [ ] Delivery is impossible until the final identity check succeeds.
- [ ] Mutating a previously verified part before the last part arrives causes
      completion to fail and the damaged range to become incomplete again.
- [ ] Restarting with every part marked complete but damaged bytes on disk
      performs the same check before delivery.
- [ ] A clean restart in the pending-delivery state completes without
      redownloading valid data.
- [ ] AICH-assisted localization/recovery, when available, retains the MD4 file
      hash as the final acceptance authority.

## Validation

- Focused state-machine and piece-store tests for clean completion, last-part
  completion, crash/restart, and final-hash failure.
- Mutation tests that alter a verified early part immediately before completion
  and between process shutdown and restart.
- Local stock eMule/current-aMule transfer witnesses confirming the Rust client
  exposes only the rehashed file and can recover the corrupted part.

## Notes

This is an integrity and lifecycle gap, not a request to replace the existing
per-part verification. Packed-frame caps, compressed-part bounds, short hashset
rejection, and the current AICH trust logic remain strong and are non-goals here.

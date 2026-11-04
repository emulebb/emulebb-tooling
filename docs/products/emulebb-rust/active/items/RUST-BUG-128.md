---
id: RUST-BUG-128
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/136
title: Preserve incremental ED2K offer publication
status: IN_PROGRESS
priority: Major
category: bug
labels: [rust, ed2k, protocol, server, beta]
product: emulebb-rust
phase: Phase 0
milestone: rust-v0.1.0-beta.3
created: 2026-10-19
source: Lugdunum anti-republication warning and retained public-server soak evidence
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/136. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-128 - Preserve incremental ED2K offer publication

## Summary

Preserve connection-scoped ED2K server publication state across shared-catalog
refreshes. Unchanged wire records must not be repeatedly re-offered merely
because the catalog fingerprint, ordering, or rank changed. New and materially
changed records remain eligible for incremental publication.

The same publication selector serves stock fallback and the negotiated
`offerfiles_v=1` path. The negotiated path must independently bound total
records per packet and previously unseen hashes per connection.

## Confirmed Defect

- A public Lugdunum 17.15 server returned `Too many files republished by your
  client software. Please upgrade it.` to the Rust publishing session.
- Retained soak evidence recorded 1,954 offered records across 42 batches for a
  final 53-file catalog, consistent with repeated near-full-catalog offers.
- The pre-fix catalog refresh cleared publication state instead of retaining
  unchanged wire records.
- Current aMule history identifies the exact warning as its incremental
  publication bug 303 and fixes it with per-file publication state.
- The item was reopened on 2026-11-04 because the stock fallback path still
  applies `ST_SOFTFILES` as a per-packet cap. A legacy session can therefore
  publish another batch after exhausting the server-advertised cumulative raw
  candidate budget.

## Current Slice Binding

- Catalog ID: `server.offer.legacy-soft-budget`.
- Authority: stock/community eMule's connection-scoped legacy publication
  behavior, checked against Lugdunum and the maintained local `ed2k-server`.
- Start/stimulus: authenticated legacy session, `ST_SOFTFILES=350`, 1,000 raw
  catalog candidates; pump publication to exhaustion and reconnect once.
- Expected result: packets contain 200 then 150 candidates and stop; rejected
  or duplicate raw candidates retain stock budget semantics; reconnect starts
  a fresh 350-candidate epoch.
- Clients/runner: focused Rust state-machine tests, then the canonical local
  ED2K server-session runner against `repos/ed2k-server`.
- Green gates: focused ED2K tests, full Rust gates, catalog validation, and the
  selected deterministic server-session campaign before delivery.

## Current Protocol Evidence

- Latest `ed2k-server` v0.9.83 counts distinct indexed hashes against
  `ST_SOFTFILES`; a same-hash refresh consumes packet and pacing capacity but
  not another soft slot.
- aMule PR 1715 implements the same separate packet and distinct-candidate
  budgets for its experimental `offerfiles_v=1` client path.
- The Rust client logs the Lugdunum `OP_SERVERMESSAGE` text verbatim; the text
  is evidence of server rejection, not a client-side error category.

## Remaining Live Evidence Gap

The 2026-11-04 local-server scale campaign proves negotiated
`offerfiles_v=1` cancellation, reconnect, pacing, and complete 100,000-record
publication. Focused Rust tests prove the corrected legacy packet and
connection-budget logic, but no dedicated live session disabled the extension
and observed the legacy 200-plus-150 sequence on the wire. This item remains
open until the existing canonical local ED2K server-session runner covers that
legacy mode; the v1 scale result cannot stand in for it.

## Intended Shape

- Reconcile the old and refreshed ranked catalogs by hash and exact wire entry.
- Keep unchanged hashes published; reopen only new or materially changed
  records.
- Retain the set of every distinct hash offered during the connection even if
  a hash later leaves the local catalog; removal does not reclaim server soft
  budget.
- Let same-hash refreshes use packet capacity after the distinct soft budget is
  exhausted, while blocking additional unseen hashes.
- Clamp every packet to the negotiated or legacy packet ceiling and below a
  known hard limit.
- Stop the publication pump when pending entries exist but none is eligible
  under the remaining connection budget.
- Reset publication state only for a new server connection epoch.

## Scope Constraints

- Do not suppress or special-case server error text.
- Do not infer server acceptance from queueing a TCP write; diagnostics report
  offered candidates, not server-indexed files.
- Preserve stock-shaped `OP_OFFERFILES` records in every mode.
- Keep `offerfiles_v=1` default-on as recorded by RUST-REF-015; RUST-CI-005 owns
  negotiated, fallback, reconnect, stock, and scale proof.

## Acceptance Criteria

- [x] Catalog reorder and unchanged refresh send no duplicate offers.
- [x] New and materially changed records are offered exactly once per current
      wire state.
- [x] Same-hash refreshes remain eligible after soft-budget exhaustion without
      consuming another distinct slot.
- [ ] Legacy raw candidates stop cumulatively at the connection-scoped
      `ST_SOFTFILES` limit, independently of the packet ceiling.
- [ ] A 350-candidate budget produces packets of 200 and 150, then no empty or
      repeated publication pump.
- [ ] Rejected and duplicate raw candidates retain the stock legacy accounting
      behavior.
- [ ] Reconnect resets the legacy publication budget.
- [ ] A dedicated local-server session with `offerfiles_v1=false` observes the
      legacy 200-plus-150 packet sequence, cumulative 350-candidate stop, no
      empty/repeated pump, and a fresh budget after reconnect.
- [x] Every packet stays below the hard limit and local packet ceiling.
- [x] Exhausted budgets do not create empty publication timer loops.
- [x] Reconnect resets publication and distinct-hash state.
- [x] Canonical Rust validation and the applicable RUST-CI-005 evidence pass.

## Implementation Evidence (2026-10-19)

- Rust commit `e3cbd847` preserves unchanged publication state across catalog
  refreshes and reopens only new or materially changed wire records.
- Rust commit `0a1240e4` separates per-packet capacity from the connection-
  scoped distinct-hash budget, clamps legacy packets, and stops exhausted
  pumps without empty sends.
- Rust commits `40fbb3e1`, `1ba8bff9`, and `5ec5f4d1` make negotiation fallback
  connection-safe, prove the two-login transition on the wire, and retain the
  fallback cause in diagnostics.
- Focused regressions and the complete 1,166-test `emulebb-ed2k` suite pass with
  strict Clippy, formatting, and whitespace checks.
- `emulebb-build-tests` merge `34d87b8` and retained runs
  `20261021T191131Z-x64-release-10424` and
  `20261021T191802Z-x64-release-13356` prove stock eMule 0.72a and current aMule
  `3.1.0-411-g2d8e97aa9` complete the transfer path while every custom v1
  negotiation counter remains zero.
- `emulebb-build-tests` merges `aaf77b3` and `3ae00e3` provide the applicable
  retained RUST-CI-005 scale campaign and corrected live-session evidence.
- Retained run `20261021T204449Z-15648` published exactly 100,000 records in
  505 bounded batches after reconnect. It used the negotiated 200-record,
  500 ms envelope, left connection/global wait and oversized counters at zero,
  settled client and server publication state at 100,000 records, and remained
  below the 512 MiB memory ceiling.
- The retained report is
  `${EMULEBB_WORKSPACE_OUTPUT_ROOT}\reports\emulebb-rust\shared-library-io\rust-offerfiles-scale-20261021T204449Z-15648.json`.

## Validation

- Focused catalog reconciliation, mutation, soft-budget, hard-boundary, and
  empty-pump regressions.
- Canonical `emulebb-ed2k` unit suite and Rust static validation.
- Existing deterministic local ED2K server-session runner configured for
  legacy publication; do not introduce a parallel harness.
- RUST-CI-005 retained large-library pacing, cancellation, reconnect, and
  memory evidence.

---
id: RUST-BUG-128
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/136
title: Preserve incremental ED2K offer publication
status: OPEN
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
- Catalog refresh currently clears publication state instead of retaining
  unchanged wire records.
- Current aMule history identifies the exact warning as its incremental
  publication bug 303 and fixes it with per-file publication state.

## Current Protocol Evidence

- Latest `ed2k-server` v0.9.83 counts distinct indexed hashes against
  `ST_SOFTFILES`; a same-hash refresh consumes packet and pacing capacity but
  not another soft slot.
- aMule PR 1715 implements the same separate packet and distinct-candidate
  budgets for its experimental `offerfiles_v=1` client path.
- The Rust client logs the Lugdunum `OP_SERVERMESSAGE` text verbatim; the text
  is evidence of server rejection, not a client-side error category.

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

- [ ] Catalog reorder and unchanged refresh send no duplicate offers.
- [ ] New and materially changed records are offered exactly once per current
      wire state.
- [ ] Same-hash refreshes remain eligible after soft-budget exhaustion without
      consuming another distinct slot.
- [ ] New hashes stop at the connection-scoped soft limit.
- [ ] Every packet stays below the hard limit and local packet ceiling.
- [ ] Exhausted budgets do not create empty publication timer loops.
- [ ] Reconnect resets publication and distinct-hash state.
- [ ] Canonical Rust validation and the applicable RUST-CI-005 evidence pass.

## Validation

- Focused catalog reconciliation, mutation, soft-budget, hard-boundary, and
  empty-pump regressions.
- Canonical `emulebb-ed2k` unit suite and Rust static validation.
- RUST-CI-005 deterministic server-fixture and retained interoperability
  evidence.

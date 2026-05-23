---
id: FEAT-043
title: Known Clients history and incremental list refresh performance
status: OPEN
priority: Minor
category: feature
labels: [clients, known-clients, history, list-performance, ui, emuleai]
milestone: ~
created: 2026-04-26
source: eMuleAI v1.4 release notes and source comparison
---

## Summary

Track eMuleAI's large Known Clients responsiveness work as a future
broadband-friendly performance candidate.

The goal is not to import the whole eMuleAI client-history product surface
blindly. The useful slice is to avoid full list churn and unnecessary resorting
while active clients refresh inside very large known-client histories.

## Current Main Evidence

Current `emulebb-main` has stale-row safety fixes for Known Clients, but
`CClientListCtrl` is still a simple pointer-backed list:

- `RefreshClient(...)` locates one row and calls `Update(...)`
- `ShowKnownClients()` rebuilds the visible list from `theApp.clientlist->list`
- there is no archived client-history map or sort-impact-aware refresh path

## eMuleAI Reference

eMuleAI v1.4 adds a broader client-history/list model:

- `clienthistory.met`
- active and archived client maps keyed by runtime id
- `RefreshClient(..., uSortImpactFlags)`
- sort-impact masks so non-sort-affecting updates do not force expensive
  reorder work
- immediate list/counter refresh after Known Clients punishment changes while
  Bad Client filtering is active

## Stock/Community Comparison

Stock/community 0.72 does not carry this history model. This is therefore an
optional product/performance feature, not stock parity.

## Broadband Fit

Large queues, long-running sessions, and many seen clients are realistic
broadband-edition workloads. A narrow implementation should favor incremental
refresh and bounded history retention without changing default network
behavior.

## Scope Constraints

- keep the feature opt-in or conservative by default if it persists more
  history than stock
- do not change credit semantics or ban policy
- avoid coupling this to the broader CShield/protection panel unless `FEAT-011`
  is intentionally pursued
- preserve existing stale-row guards from `BUG-041`

## Acceptance Criteria

- [ ] Known Clients refreshes do not require full rebuilds for non-structural
      active-client updates
- [ ] list resort happens only when the current sort key can change
- [ ] optional persisted history has bounded retention and migration behavior
- [ ] Bad Client filter counters refresh immediately after manual punishment
      changes
- [ ] large-history UI stress tests cover sorting, filtering, punishment
      changes, and shutdown

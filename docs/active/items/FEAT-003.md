---
id: FEAT-003
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/8
title: Kad — Add response usefulness scoring and subnet-diversity search fanout
status: OPEN
priority: Minor
category: feature
labels: [kad, search, routing, quality]
milestone: ~
created: 2026-04-08
source: AUDIT-KAD.md (AUD_KAD_008, AUD_KAD_009)
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/8. This local document is retained as an engineering spec/evidence record.

# FEAT-003 - Kad — Add response usefulness scoring and subnet-diversity search fanout

## Summary

Search progression currently relies on XOR closeness, pending/timeout state,
and duplicate suppression. There is no model for how *useful* a responder was.
A node that consistently returns dead, duplicate, or low-diversity contacts
receives the same treatment as a node that returns fresh, close, high-quality
ones.

## Current Weak Points (AUD_KAD_008, AUD_KAD_009)

- No explicit usefulness score for responders.
- No explicit low-yield penalty beyond short-lived problematic state.
- No route-quality memory by subnet/prefix.
- No adaptive query fanout based on current quality conditions.

## Proposed Improvements

### Response Usefulness Scoring

Track per-node response quality:
- Score **up**: returned closer contacts, returned live contacts, returned
  novel (non-duplicate) contacts.
- Score **down**: returned dead contacts, returned duplicates, returned no
  closer contacts than already known.
- Use score as a tie-breaker when selecting next candidates.

### Subnet Diversity Cap

During search:
- Maintain a per-search per-subnet counter.
- Cap contacts from any single `/24` to a configurable limit (e.g. 3).
- Prefer contacts from underrepresented subnets when selecting next hops.

### Adaptive Fanout

Track timeout rate and answer quality during a search:
- If timeout rate is high → increase parallel queries (more fanout).
- If answer quality is low → prefer diversity over closeness.
- Converge to normal fanout as conditions improve.

## Protocol Compatibility

All changes are local — no Kad packet changes, no protocol-observable effects.

## Files

- `srchybrid/kademlia/kademlia/SearchManager.h` / `.cpp`
- `srchybrid/kademlia/routing/RoutingZone.h` / `.cpp`
- `srchybrid/kademlia/utils/SafeKad.h` / `SafeKad.cpp` — integrates short-lived problematic state

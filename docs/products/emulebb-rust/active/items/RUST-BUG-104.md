---
id: RUST-BUG-104
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/25
title: Preserve Kad AICH publisher provenance and result consensus
status: OPEN
priority: Major
category: bug
labels: [rust, kad, aich, integrity, parity]
milestone: post-beta-compatibility
created: 2026-10-03
source: Stock compatibility review against eMule 0.72a and current aMule 3.1
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/25. This local document is retained as the durable engineering spec and evidence record.

# RUST-BUG-104 - Preserve Kad AICH publisher provenance and result consensus

## Summary

Track Kad AICH roots by publisher and carry version-gated AICH candidates from
keyword storage through search results into the existing trust machinery. Rust
currently remembers publisher IP/name but collapses AICH storage to one value,
emits a fixed count/popularity, and drops AICH when mapping Kad search results.
That loses the provenance and independent-vote semantics used by stock eMule
and current aMule to resist conflicting or stale roots.

## Current State

- `crates/emulebb-index/src/kad_store/keyword.rs` tracks publisher identity but
  stores/extracts one AICH value and writes fixed count/popularity values.
- `crates/emulebb-kad-dht/src/types.rs` decodes file name, size, source count,
  and raw tags but does not expose a typed AICH candidate.
- `crates/emulebb-core/src/search_query.rs` maps Kad results with an empty AICH,
  unknown file type, and zero rating.
- `crates/emulebb-kad-dht/src/publish.rs` already emits the outbound AICH tag;
  publication is not the missing half.
- Stock eMule's Kad `Entry.cpp` retains publisher-to-root information and emits
  aggregate root information. Current aMule version-gates the result data and
  treats the received root as one candidate vote rather than trusting a
  reported count as multiple independent publishers.

## Why This Matters

Without provenance, conflicting roots can overwrite each other or appear more
authoritative than the evidence supports. Dropping the candidate at the search
boundary also prevents the existing AICH trust model from accumulating a valid
root before transfer.

## Representative Sites

- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-index\src\kad_store\keyword.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-kad-dht\src\types.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-kad-dht\src\publish.rs`
- `EMULEBB_WORKSPACE_ROOT\repos\emulebb-rust\crates\emulebb-core\src\search_query.rs`
- `EMULEBB_WORKSPACE_ROOT\workspaces\workspace\app\emulebb-main\srchybrid\kademlia\kademlia\Entry.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\kademlia\kademlia\Entry.cpp`
- `EMULEBB_WORKSPACE_ROOT\analysis\amule\src\kademlia\kademlia\Search.cpp`

## Intended Shape

- Store each active publisher's optional AICH root, update it when that
  publisher changes its claim, and remove it on publisher expiry/removal.
- Derive a bounded aggregate of candidate roots and popularity from live
  publishers without converting a remote reported count into synthetic votes.
- Strictly decode AICH result tags only for protocol versions known to carry
  them, including the Kad-version gate used by compatible clients.
- Preserve the responding peer/publisher identity as the provenance for one
  candidate observation and feed it into the existing AICH trust accumulator.
- Reject malformed roots without rejecting an otherwise usable search result.

## Scope Constraints

- The responder contributes at most one independent observation per candidate;
  a popularity/count field is metadata, not extra votes.
- Bound publisher/root state and expire it with the enclosing Kad entry.
- Do not weaken the current AICH trust threshold or MD4 authority.
- Preserve interoperability with pre-AICH/pre-version-gated Kad peers.

## Acceptance Criteria

- [ ] Keyword storage maintains publisher-to-optional-root state across add,
      refresh, root change, removal, and expiry.
- [ ] Aggregate result encoding is deterministic, bounded, and derived only
      from current publishers.
- [ ] A valid result from a supported Kad version reaches the internal search
      result as one provenance-bearing AICH candidate.
- [ ] Conflicting publishers remain distinct candidates; no last-writer-wins or
      count-to-votes conversion occurs.
- [ ] Malformed and pre-version-gate AICH tags are ignored safely and covered by
      tests.
- [ ] The existing AICH trust layer can accept multiple independent search or
      source observations without double-counting a responder.

## Validation

- Unit tests for conflicting roots, one publisher changing roots, publisher
  removal/expiry, duplicate observations, and bounded state.
- Codec tests for valid, malformed, truncated, and pre-gate result packets.
- Local Kad fixture with stock eMule/current aMule publishers advertising the
  same and conflicting roots, followed through the Rust search API.

## Notes

The outbound AICH publication and current transfer-time AICH trust checks are
useful foundations and should be reused rather than replaced.

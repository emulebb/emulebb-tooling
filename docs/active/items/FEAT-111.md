---
id: FEAT-111
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/130
title: Add peer and queue diagnostics columns
status: OPEN
priority: Minor
category: feature
labels: [diagnostics, peer-ui, uploads, queue, observability, post-0.7.3]
milestone: post-0.7.3
created: 2026-06-03
source: operator request after eMuleAI and mods-archive review
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/130. This local document is retained as an engineering spec/evidence record.

# FEAT-111 - Add Peer And Queue Diagnostics Columns

## Summary

Add optional diagnostics columns and REST fields that explain peer, upload,
download, and queue state without changing queue policy, scoring, protocol
behavior, or default list shape.

The goal is operator visibility. eMuleBB should make it easier to answer:

- why a peer is waiting
- why a peer is uploading or not uploading
- which file a peer requested
- whether a low-ratio or scarce file is influencing priority as expected
- whether upload slots are empty because there is no demand, stale state, socket
  backpressure, disk I/O pressure, limits, or queue admission policy
- whether stale unavailable shared files are still represented in queue state

This item borrows the useful diagnostic idea from historical mods while
rejecting client emulation, anti-leecher scoring, community preference, and
punishment systems.

## Intended Shape

Expose additional display-only fields in peer-heavy views where they help
operators inspect live behavior:

- Uploading list
- Upload Queue list
- download peer/source rows where the existing Transfers view already exposes
  peer rows
- client/details dialogs
- REST/status endpoints that already expose peer, transfer, or queue state

The first implementation should start with a small number of high-signal fields
on one upload/queue surface. Broader UI and REST exposure should happen only
after the field ownership and refresh cost are understood.

## Candidate Fields

Candidate peer identity and connection fields:

- raw peer IP and port
- optional reverse DNS name if `FEAT-104` is enabled and already has a cached
  result
- user hash presence or short display value where already available
- secure-ident state
- client software name and version as claimed by the peer
- mod/client string as claimed by the peer, clearly labeled as claimed
- LowID/HighID and callback state where already known
- obfuscation/encryption state where already known

Candidate upload and queue fields:

- requested file name
- requested file hash
- requested file shared-state summary
- whether the requested file is complete, part file, stopped for upload, or no
  longer available
- upload state
- queue rank
- queue wait time
- queue score
- score reason summary
- friend slot flag
- credit/secure-credit indicator where stock-compatible credit state already
  exists
- banned or filtered state, if already used by current eMuleBB behavior
- current upload data rate
- session bytes uploaded to this peer
- total bytes uploaded to this peer where already tracked
- active slot age

Candidate download/source fields:

- download state
- source state reason such as connecting, on queue, downloading, no needed
  parts, too many connections, queue full, low-to-low, or banned
- requested block count where already available
- A4AF ownership/alternate-file state where already displayed or tracked
- last request/reask age where already tracked
- stale-source repair or cleanup reason if diagnostics added under
  `REF-054`

Candidate aggregate queue diagnostics:

- waiting queue size
- active upload slot count
- configured upload slot cap
- effective upload slot cap
- upload bandwidth target and current usage
- count of queued clients by requested-file state
- count of queued clients for stopped/unavailable files
- count of candidate clients rejected by soft queue policy
- count of active slots blocked by bandwidth, socket, disk, or no-demand reasons
  where existing diagnostics can support it

## Scope Constraints

- Do not change upload queue scoring, queue admission, source selection, upload
  slot policy, download source policy, or Kad/eD2K behavior.
- Do not introduce client emulation, mod spoofing, community preference, or
  anti-leecher punishment behavior.
- Do not use claimed client/mod names as trust, ban, score, scheduling, or
  routing inputs.
- Do not use reverse DNS names for trust, ban, score, scheduling, routing, or
  protocol decisions.
- Do not block list rendering, sorting, transfer processing, socket handling,
  startup, shutdown, or REST requests on DNS, geolocation, file I/O, or slow
  formatting.
- Do not add broad virtual-list or list-control framework work under this item.
  Keep each list on its current shape unless a focused, measured bottleneck is
  found in that list.
- Do not make high-cardinality diagnostics visible by default if they make the
  UI noisy or expensive.
- Do not expose sensitive peer identifiers in default logs beyond current
  behavior; richer peer identity should be opt-in, diagnostics-only, or REST
  authenticated where appropriate.

## Relationship To Existing Items

- `FEAT-104` owns optional reverse DNS. This item may display cached names but
  must not own DNS lookup behavior.
- `FEAT-105` owns the stopped shared-file upload state. This item should make
  stopped/unavailable requested-file state visible in queue diagnostics once the
  state exists.
- `FEAT-106` and `FEAT-107` own upload bandwidth ramp-up and under-target
  diagnostics. This item may expose their results in UI/REST, but should not
  redefine their diagnostics.
- `BUG-142` owns soft-queue admission policy consistency for low-ratio boosted
  candidates. This item may show admission/rejection diagnostics but must not
  change admission policy.
- `BUG-143` owns stale waiting-queue entries for deleted or stopped shared
  files. This item may show stale/unavailable counts but must not be the cleanup
  implementation.
- `REF-053` owns upload queue and upload list lookup overhead. If a diagnostics
  column creates measurable lookup cost, fix the local lookup path there or in a
  focused slice, not through a generic list rewrite.
- `REF-054` owns download queue diagnostics and A4AF stale ownership
  hardening. Download-source diagnostics should reuse that work.

## Candidate Implementation Notes

- Start with a diagnostic snapshot helper for upload/queue rows. It should read
  already-owned state and return cheap display values.
- Prefer stable enums or reason codes internally, then format localized display
  text at the UI edge.
- Keep raw values available to REST where useful, for example state ids plus
  display labels.
- Cache expensive display strings per refresh tick when the source value is
  unchanged.
- Treat client/mod names as untrusted display strings. Clamp length and sanitize
  control characters before showing them in list cells, tooltips, logs, or REST.
- Keep reverse DNS integration one-way: display a cached value if already
  present; never trigger lookup from paint, sort, queue selection, or REST row
  enumeration.
- Add optional columns behind the existing column chooser or hidden-by-default
  behavior where available.
- Consider a compact "Why" column for queue/source reason summaries rather than
  many always-visible narrow columns.
- Prefer details dialogs or tooltips for verbose multi-reason explanations.
- Preserve sort behavior. Sorting by diagnostics columns should use cached
  primitive values and must not trigger live recomputation.
- Add diagnostics counters only where they answer a specific operator
  question.

## Suggested First Slice

The first practical slice should focus on upload queue observability:

1. Add a cheap upload queue row diagnostic snapshot.
2. Expose requested file, requested-file availability state, queue wait time,
   queue score, and a short queue reason summary.
3. Keep new columns hidden by default if the existing UI supports hidden
   columns; otherwise add them only to a details dialog or tooltip first.
4. Add REST fields for the same values if the current endpoint already exposes
   queue rows.
5. Add tests for formatting and state classification using seams, without live
   network dependency.

## Acceptance Criteria

- [ ] Peer/queue diagnostics are display-only and do not affect scoring,
      admission, source selection, slot selection, routing, trust, bans, Kad, or
      eD2K behavior.
- [ ] At least one upload or queue surface exposes requested file, peer state,
      queue wait time, queue score or rank, and a short reason summary.
- [ ] Claimed client/mod strings are clearly treated as untrusted display data.
- [ ] Claimed client/mod strings are sanitized and length-bounded before UI,
      tooltip, log, or REST exposure.
- [ ] Optional reverse DNS names are shown only from cached `FEAT-104` results
      and never trigger synchronous lookup.
- [ ] Stopped or unavailable requested-file state is visible once `FEAT-105` and
      related cleanup paths provide that state.
- [ ] Diagnostics columns or fields do not require a broad virtual-list rewrite.
- [ ] Sorting, painting, and REST enumeration do not perform DNS, filesystem
      I/O, or expensive live recomputation.
- [ ] Existing list refresh cadence remains honored.
- [ ] REST output, if extended, exposes machine-readable state ids as well as
      display labels where practical.
- [ ] Focused tests cover state classification, untrusted string sanitization,
      disabled/absent DNS-name behavior, stopped/unavailable requested-file
      classification where available, and no policy mutation.

## Validation

- focused native tests for row diagnostic snapshot classification
- focused native tests for claimed client/mod string sanitization and clamping
- focused native tests proving diagnostics helpers do not mutate queue or peer
  policy state
- REST contract tests if REST fields are added
- manual UI smoke for Uploading, Queue, and Details surfaces touched by the
  implementation
- manual upload queue smoke with active, waiting, unavailable-file, and
  stopped-file scenarios when those states exist
- x64 Debug and Release app builds before implementation commit

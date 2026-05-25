---
id: FEAT-068
title: Bound REST large-list memory and latency for very large profiles
status: OPEN
priority: Minor
category: feature
labels: [rest, shared-files, transfers, uploads, performance, memory, controller-surface]
milestone: post-0.7.3
created: 2026-05-21
updated: 2026-05-24
source: eMuleAI issue #86/#79 triage plus current REST large-list review
---

## Summary

Add focused guards for large lists exposed through REST. The initial risk was
the full shared-files response, but the same controller-surface pattern also
applies to transfer, upload, and waiting-queue lists on very large live
profiles. The goal is to avoid high transient memory use, repeated live-graph
walks, and long request-thread stalls.

This is controller-surface maintenance, not a new product UI expansion.

## Current Mainline Evidence

`srchybrid/WebServerJson.cpp` builds several full-list responses synchronously:

- shared files: copies the current shared-file map and serializes every entry
  into one JSON response
- transfers: walks `theApp.downloadqueue` and serializes every matching
  `CPartFile`
- uploads/waiting queue: walks the upload queue lists and serializes every
  visible peer row

That is convenient for small and moderate profiles, but it can spike memory and
latency for very large shared trees or controller polling loops.

The 2026-05-26 native v1 API review kept this performance work separate from
the RC1 contract-freeze standardization tracked in `REF-047`. Any paging or
bounded-list change made here must preserve the final public v1 contract chosen
there.

## Scope

- Add paging, cursoring, limit/offset, or another bounded response mode for
  shared-files REST listing.
- Add snapshot or dirty-flag-backed caches for read-heavy controller lists where
  repeated polling would otherwise walk live structures every time.
- Keep snapshot building separate from live app mutation: workers may build
  immutable response records from an already captured snapshot, but request
  handlers must not hold live locks for long JSON serialization.
- Keep the existing response shape available where compatibility requires it,
  or version the change explicitly.
- Add stress coverage for a large synthetic shared-file map.
- Preserve authenticated controller behavior and `/api/v1` compatibility.

## Non-Goals

- Do not redesign shared-file hashing or reload behavior here; that remains
  tracked by `FEAT-034`.
- Do not reintroduce a legacy HTML shared-files UI.
- Do not change share policy or publish semantics.
- Do not mutate upload/download/shared state from REST snapshot workers.

## Upstream Signals

- eMuleAI issue #86: high RAM usage reported around large `known.met` and large
  shared/file-history cases.
- eMuleAI issue #79: large shared-library automation reports UI and shared-files
  pressure.

The exact eMuleAI failure may not be the same as eMuleBB, but the large-list
memory risk maps directly to the current REST serialization shape.

## Acceptance Criteria

- [ ] Shared-files REST listing has a bounded mode suitable for very large
      libraries.
- [ ] transfer, upload, and waiting-queue REST list paths have bounded or
      cached behavior suitable for heavy polling
- [ ] Controller compatibility is documented and tested.
- [ ] A large-library synthetic test proves memory and latency stay bounded.
- [ ] The implementation does not alter normal sharing or hashing behavior.

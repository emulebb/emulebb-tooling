---
id: FEAT-068
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/66
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


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/66. This local document is retained as an engineering spec/evidence record.

# FEAT-068 - Bound REST large-list memory and latency for very large profiles

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

- [x] Shared-files REST listing has a bounded mode suitable for very large
      libraries.
- [x] transfer, upload, and waiting-queue REST list paths have bounded or
      cached behavior suitable for heavy polling
- [x] Controller compatibility is documented and tested.
- [x] A large-library synthetic test proves memory and latency stay bounded.
- [x] The implementation does not alter normal sharing or hashing behavior.

## Implementation Status (2026-06-13)

Bounded paging is implemented and guarded:

- **Shared files** — `GET /api/v1/shared-files` pages through
  `CSharedFileList::CopySharedFilePage` (`srchybrid/SharedFileList.cpp`): it
  indexes straight to `offset`, copies at most `limit` pointers, sets `total`
  to the full library size, and holds `m_mutWriteList` only for the pointer
  copy — JSON serialization runs after the lock is released. Cost per request
  is O(limit), independent of library size.
- **Snapshot polling** — `snapshot/get` applies the caller-visible `limit`
  (default 100) to every live collection (`BuildSharedFilesListJson(0,
  maxEntries)`, transfers, uploads, waiting queue), so the hot controller poll
  never serializes a full large profile.
- **Transfers / upload-queue** — paged server-side via the shared
  `BuildPagedItemsEnvelope` path with `total` reflecting the filtered count.
- **Contract** — the common pagination shape (`items`/`total`/`offset`/`limit`)
  and a stable-ordering guarantee are documented in `REST-API-CONTRACT.md`.
- **Controller (aMuTorrent)** — `_fetchAllPages` walks pages bounded by
  `AMUTORRENT_EMULEBB_SHARED_MAX_ITEMS` (default 2000), surfaces the full `total`,
  and flags truncation in the stats tree and logs. All adapter list bounds (page
  size, snapshot/logs limits, shared/transfers caps, refresh throttle) live
  centrally in `config.js` `EMULEBB_REST`, overridable via `AMUTORRENT_EMULEBB_*`.

Coverage: `test_shared_file_list_source.py` guards the C++ bounded-paging and
snapshot-bounding invariants; aMuTorrent `emulebbManager.test.js` proves a
50,000-file library is fetched in bounded page count and capped without walking
the whole library. A live in-app RAM/latency benchmark against a real 50k
profile remains an optional future addition (not required for the bounded
guarantees above).

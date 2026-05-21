---
id: FEAT-068
title: Bound REST shared-files memory use for very large libraries
status: OPEN
priority: Minor
category: feature
labels: [rest, shared-files, performance, memory, controller-surface]
milestone: post-beta-0.7.3
created: 2026-05-21
source: eMuleAI issue #86/#79 triage against current REST shared-files code
---

## Summary

Add a focused guard for large shared-file libraries exposed through REST. The
goal is to avoid high transient memory use when controllers request the full
shared-files list from libraries with tens or hundreds of thousands of entries.

This is controller-surface maintenance, not a new product UI expansion.

## Current Mainline Evidence

`srchybrid/WebServerJson.cpp` builds the shared-files list by copying the
current shared-file map and serializing every entry into one JSON response.
That is convenient for small and moderate libraries, but it can spike memory
and latency for very large shared trees.

## Scope

- Add paging, cursoring, limit/offset, or another bounded response mode for
  shared-files REST listing.
- Keep the existing response shape available where compatibility requires it,
  or version the change explicitly.
- Add stress coverage for a large synthetic shared-file map.
- Preserve authenticated controller behavior and `/api/v1` compatibility.

## Non-Goals

- Do not redesign shared-file hashing or reload behavior here; that remains
  tracked by `FEAT-034`.
- Do not reintroduce a legacy HTML shared-files UI.
- Do not change share policy or publish semantics.

## Upstream Signals

- eMuleAI issue #86: high RAM usage reported around large `known.met` and large
  shared/file-history cases.
- eMuleAI issue #79: large shared-library automation reports UI and shared-files
  pressure.

The exact eMuleAI failure may not be the same as eMule BB, but the large-list
memory risk maps directly to the current REST serialization shape.

## Acceptance Criteria

- [ ] Shared-files REST listing has a bounded mode suitable for very large
      libraries.
- [ ] Controller compatibility is documented and tested.
- [ ] A large-library synthetic test proves memory and latency stay bounded.
- [ ] The implementation does not alter normal sharing or hashing behavior.

---
id: FEAT-078
workflow: github
github_issue: https://github.com/emulebb/emulebb/issues/25
title: Persist auto-browse inventories in a local queryable database
status: OPEN
priority: Minor
category: feature
labels: [browse, cache, sqlite, database, ui, privacy]
milestone: post-0.7.3
created: 2026-05-24
source: user-requested future backlog item for cached auto-browse results
---


> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb/issues/25. This local document is retained as an engineering spec/evidence record.

## Summary

Persist successful remote shared-file browse results in a local queryable store
so auto-browsed peer inventories can be searched, deduplicated, expired, and
inspected without repeatedly hitting the same remote client.

This item builds on [FEAT-031](FEAT-031.md). `FEAT-031` owns the compatible
peer discovery and safe auto-browse scheduler; this item owns the storage model
for cached browse results once the feature produces useful inventories.

## Intended Shape

- Store cached remote inventory snapshots in a local database rather than
  ad-hoc per-client files.
- Track peer identity, browse time, source client hints, file hash, file name,
  size, type/category, and expiry metadata.
- Keep cache writes bounded, transactional, and safe across app shutdown.
- Add cache retention controls before collecting large inventories.
- Keep manual browse and live peer state separate from cached historical
  snapshots.

## eMuleAI Reference Scope

eMuleAI demonstrates the peer-history and remote-shared-file surface that can
feed this cache, but it does not settle the eMuleBB storage backend. Use the
code as source of fields and workflows, not as a persistence-format mandate:

- remote shared-files and client-history preference surface:
  [`PPgMod.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/eMuleAI/PPgMod.cpp#L748)
- client-history structures:
  [`ClientList.h`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.h#L319)
- persisted client history behavior:
  [`ClientList.cpp`](https://github.com/emulebb/emulebb-ai/blob/8e34bdec2b7e4fe9e4307df9d80f691804be99ed/srchybrid/ClientList.cpp#L2010)

## Constraints

- Do not auto-download, auto-queue, or alter sharing behavior from cached data.
- Do not expose cached peer inventories through REST or UI until privacy,
  retention, and redaction rules are explicit.
- Do not change eD2K/Kad protocol semantics; this is local persistence only.
- Avoid making this a general metadata intelligence expansion.

## Acceptance Criteria

- [ ] Cached browse inventories persist to a queryable local store.
- [ ] Cache records include enough provenance to distinguish stale data from
      live peer state.
- [ ] Retention/expiry prevents unbounded database growth.
- [ ] Startup and shutdown remain responsive with a large browse cache.
- [ ] Manual cache purge and per-peer purge paths are defined.
- [ ] Live-network validation proves at least one compatible peer inventory can
      be cached and read back.

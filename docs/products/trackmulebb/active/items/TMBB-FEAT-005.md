---
id: TMBB-FEAT-005
workflow: github
github_issue: TBD - file on emulebb/trackmulebb when scheduled
title: Delta-sync the qBittorrentBB transfers lane (/sync/maindata) instead of full-poll
status: OPEN
priority: Minor
category: feature
labels: [controller, performance, bittorrent, rest]
milestone: phase-2
created: 2026-06-16
source: MVP unified transfers dashboard (commit f8a327d); design ref docs/design/MVP-UNIFIED-TRANSFERS.md
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-005 - Delta-sync the qBittorrentBB transfers lane instead of full-poll

## Summary

The unified transfers dashboard MVP polls qBittorrentBB with `GET /api/v2/torrents/info`
(the full torrent list) every cycle. Replace that with qBittorrent's native delta
endpoint `GET /api/v2/sync/maindata?rid=N`, which returns only what changed since
the last `rid`. The adapter keeps a raw per-infohash field cache, merges partial
updates into it, and normalizes from the cache — so `list_transfers()` keeps
returning a full snapshot and nothing downstream (projection, engine, UI) changes.

## Why This Matters

`/torrents/info` re-serializes every torrent each poll; with large swarms this is
wasted bandwidth/CPU on both client and controller. `/sync/maindata` is the path
qBittorrent's own WebUI uses and scales with churn, not library size. The adapter
boundary already isolates this, so it is a self-contained efficiency win.

## Scope Constraints

- qBittorrentBB lane only. emulebb-rust exposes no delta-sync endpoint, so its
  lane stays full-poll (`GET /api/v1/transfers`) — unchanged.
- The `ClientAdapter.list_transfers()` contract (full normalized snapshot) must
  not change; the engine still replaces the backend's namespace per snapshot.

## Acceptance Criteria

- [ ] `QBittorrentAdapter` maintains a `rid` and a raw per-infohash field cache.
- [ ] Partial `torrents` updates are **merged** into the cache (never replace a
      whole entry); `torrents_removed` prunes the cache; `full_update` re-baselines.
- [ ] On a connection error / restart, `rid` resets to 0 (full re-baseline).
- [ ] `list_transfers()` returns the same `UnifiedTransfer` snapshot as today;
      projection/engine/UI require no changes.
- [ ] Tests cover partial-merge, removal, and `full_update` re-baseline.

## Notes

- Watch the partial-merge footgun: `/sync/maindata` sends only changed fields per
  torrent, so normalizing a partial directly would null unchanged fields — always
  merge into the cached full entry first.

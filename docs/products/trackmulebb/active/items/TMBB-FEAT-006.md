---
id: TMBB-FEAT-006
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/5
title: Meta-search + cross-network dedup (native clients + Prowlarr, tag-excluded)
status: OPEN
priority: Major
category: feature
labels: [search, prowlarr, dedup, cross-network, suite]
milestone: phase-2
created: 2026-06-16
source: suite bundle notes 1-2 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-006 - Meta-search + cross-network dedup (native clients + Prowlarr, tag-excluded)

## Summary

Aggregate search across all networks: query the connected clients **natively** (emulebb-rust index + qBittorrentBB harvest, via a native path, not Torznab) **and** Prowlarr for third-party/Usenet indexers, **excluding the TrackMuleBB-tagged indexers** in Prowlarr to avoid double-counting. Deduplicate the merged results.

## Why This Matters

One cross-network search pane; Prowlarr is the extensibility point for any third-party indexer the user adds, without duplicating the clients TrackMuleBB already drives.

## Intended Shape

- Native path to rust/qbbb (more flexible than their Torznab).
- Prowlarr query **excludes** the indexers TrackMuleBB registered, identified by a **tag** TrackMuleBB applies on registration.
- **Dedup:** exact hash collapses within a network; cross-network results **merge into one row** when the metadata-fabric **equivalence map** relates them (authoritative), falling back to **exact file size + normalized name**. Non-destructive: the user can **expand** the merged group.

## Acceptance Criteria

- [ ] Search returns native rust/qbbb results + Prowlarr (third-party) results.
- [ ] TrackMuleBB-tagged Prowlarr indexers are excluded per query (no duplicates).
- [ ] Cross-network matches merge into one expandable row (equivalence map first, exact-size+name fallback).

## Notes

- Dedup source = the metadata fabric equivalence map (emulebb-tooling SUITE-METADATA-FABRIC).

---
id: TMBB-FEAT-007
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/6
title: Dynamic global bandwidth coordination across three networks
status: OPEN
priority: Major
category: feature
labels: [bandwidth, scheduling, cross-network, suite]
milestone: phase-2
created: 2026-06-16
source: suite bundle notes 3,5 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-007 - Dynamic global bandwidth coordination across three networks

## Summary

Coordinate bandwidth across **three networks** (eD2K/rust, BitTorrent/qBittorrentBB, Usenet/SABnzbd) by **dynamically rebalancing per-client limits** under a configurable global cap, with priority between networks. Upload-coordination is **eD2K + BT only** (Usenet is download-only).

## Why This Matters

A single global budget across heterogeneous clients is something no single client can do; it is the single-pane value. TrackMuleBB orchestrates via each client limit API.

## Intended Shape

- Control loop sets each client down/up limit (rust /api/v1, qbbb WebUI, SAB API) to keep global usage under a configurable cap.
- **Configurable schedule** pushed to all clients.
- Priority policy between networks; upload only on eD2K+BT.

## Acceptance Criteria

- [ ] A global down cap is honored by rebalancing per-client limits in real time.
- [ ] Configurable schedule applies across clients.
- [ ] Upload coordination only touches eD2K + BT.

## Notes

- Genuine control loop, the hardest piece. Bandwidth settings reach via TMBB-FEAT-009.

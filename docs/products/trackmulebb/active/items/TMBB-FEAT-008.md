---
id: TMBB-FEAT-008
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/7
title: SABnzbd adapter - third download client (Usenet)
status: OPEN
priority: Major
category: feature
labels: [sabnzbd, usenet, adapter, download-client, suite]
milestone: phase-2
created: 2026-06-16
source: suite bundle note 3 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-008 - SABnzbd adapter - third download client (Usenet)

## Summary

Add SABnzbd as a **third download client** (Usenet) beside emulebb-rust (eD2K) and qBittorrentBB (BT): unified transfers view + bandwidth control via the SAB HTTP API. SAB is download-only; Usenet **search** comes from Prowlarr (Newznab) then grab then SAB.

## Why This Matters

Completes the three-network single pane. SAB is the download client for nzb, not a search source.

## Intended Shape

- SAB adapter (apikey HTTP API): queue/history into the unified grid; pause/resume; set speed limit (TMBB-FEAT-007).
- SAB is **additive**: it does not satisfy the bundle >=1-P2P-client rule alone.

## Acceptance Criteria

- [ ] SAB transfers appear in the unified grid with pause/resume.
- [ ] TrackMuleBB sets SAB speed limit (bandwidth coordination).
- [ ] SAB is not a search source (Usenet search stays in Prowlarr).

## Notes

- Third adapter beside rust + qbbb; same adapter model.

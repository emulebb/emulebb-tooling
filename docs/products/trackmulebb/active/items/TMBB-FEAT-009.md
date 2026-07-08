---
id: TMBB-FEAT-009
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/8
title: Unified settings - full for emulebb-rust, bandwidth-only for qBittorrentBB/SAB
status: OPEN
priority: Minor
category: feature
labels: [settings, single-pane, suite]
milestone: phase-2
created: 2026-06-16
source: suite bundle note 5 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-009 - Unified settings - full for emulebb-rust, bandwidth-only for qBittorrentBB/SAB

## Summary

The web UI is the settings single pane, **scoped**: **full configuration only for emulebb-rust** (headless, first-party, no other UI), **bandwidth only for qBittorrentBB and SABnzbd** (the minimum the coordinator needs), **nothing for Arr** (deep-link).

## Why This Matters

Avoids re-implementing rich native UIs while owning what matters: rust full config (no other home) and the bandwidth knobs for TMBB-FEAT-007.

## Intended Shape

- rust: full settings via /api/v1.
- qbbb/SAB: bandwidth limit only (rest via native UI).
- Arr/Plex: no settings management; deep-link.

## Acceptance Criteria

- [ ] emulebb-rust fully configurable from the web UI.
- [ ] qbbb/SAB expose only bandwidth controls.
- [ ] Arr/Plex deep-linked, not duplicated.

## Notes

- Web UI = settings only; install/lifecycle is the CLI (TMBB-FEAT-010).

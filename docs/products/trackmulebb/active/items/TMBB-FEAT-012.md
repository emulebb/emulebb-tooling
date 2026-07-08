---
id: TMBB-FEAT-012
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/11
title: Bountarr bundle integration (household media-grab UI over Arr)
status: OPEN
priority: Minor
category: feature
labels: [bountarr, arr, node, bundle]
milestone: phase-2
created: 2026-06-16
source: suite bundle note 6 (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-012 - Bountarr bundle integration (household media-grab UI over Arr)

## Summary

Integrate **Bountarr** (itlezy/bountarr, TS/Node) into the bundle as the **household media-grab UI** over Radarr/Sonarr(+Plex), distinct from TrackMuleBB operator orchestration. The setup CLI installs it (with a self-contained Node) and pre-wires its .env to the Arr stack.

## Why This Matters

Bountarr is the 'what content do I want' front-end; TrackMuleBB is the 'how it downloads across networks' orchestrator. Bountarr grabs compose **under** TrackMuleBB coordination (shared download clients).

## Intended Shape

- Selecting Bountarr **requires Radarr/Sonarr** (dependency-enforced).
- **Only Node** component: setup installs a self-contained Node (v22+) only when Bountarr is chosen.
- Pre-wire RADARR_URL/API_KEY, SONARR_*, optional PLEX_* (claim manual).

## Acceptance Criteria

- [ ] Bountarr installs with a self-contained Node and pre-wired Arr .env.
- [ ] Selecting Bountarr pulls in Radarr/Sonarr.
- [ ] Bountarr grabs flow through the shared download clients (under TrackMuleBB).

## Notes

- Distinct UX from TrackMuleBB (household vs operator). Node confined to Bountarr.
- Docker form: the bountarr GHCR image is one of the four prerequisite images;
  tracked in `itlezy/bountarr` (issue
  [#1](https://github.com/itlezy/bountarr/issues/1)) and wired by the Docker
  delivery (TMBB-FEAT-013).

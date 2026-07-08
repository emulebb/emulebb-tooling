---
id: TMBB-FEAT-003
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/3
title: Coordinate emulebb-rust + qBittorrentBB over REST (adapters) with direct-Arr invariant
status: OPEN
priority: Major
category: feature
labels: [controller, integration, rest, suite]
milestone: phase-2
created: 2026-06-15
source: SUITE-JOINT-ROADMAP Decision 2026-06-15; design ref AMUT-FEAT-003
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-003 - Coordinate emulebb-rust + qBittorrentBB over REST (adapters) with direct-Arr invariant

## Summary

The REST adapter + coordinator layer: drive emulebb-rust (native `/api/v1` +
qBittorrent-WebUI-emulating API) and qBittorrentBB (qBittorrent WebUI API) as the
two managed clients, behind a single integrated web UI. emulebb-rust presents as
"a qBittorrent" to Arr-style consumers, so this is integration + coordination, not
new protocol work.

## Why This Matters

Makes the forward eD2K core and the BitTorrent companion first-class managed
clients in one controller, with zero bespoke per-client protocol work — the
foundation the cross-network automation (TMBB-FEAT-001/002) builds on.

## Scope Constraints

- **Direct-Arr-without-controller invariant (hard rule):** Sonarr/Radarr/Prowlarr
  point directly at the clients and complete search → grab → monitor → import with
  TrackMuleBB stopped. Any aggregated Arr endpoint TrackMuleBB offers is optional
  convenience, never the only path.
- Only emulebb-rust + qBittorrentBB. Python-only (NiceGUI + FastAPI; SQLite state).
  Control plane binds `X_LOCAL_IP`; carries no P2P data plane.

## Acceptance Criteria

- [ ] TrackMuleBB can add/list/pause/resume/remove transfers on both clients via
      their REST APIs.
- [ ] Both clients appear in the controller UI with live status.
- [ ] **Invariant:** with TrackMuleBB stopped, each client's Arr workflow still
      completes end-to-end.

## Notes

- Depends on the emulebb-rust Arr surfaces (`RUST-FEAT-004`).

---
id: TMBB-FEAT-001
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/1
title: Cross-network "download the torrent instead" intent handoff (rust → qBittorrentBB)
status: OPEN
priority: Major
category: feature
labels: [controller, cross-network, intent, suite]
milestone: phase-2
created: 2026-06-15
source: SUITE-JOINT-ROADMAP Decision 2026-06-15; design ref AMUT-FEAT-001
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-001 - Cross-network "download the torrent instead" intent handoff (rust → qBittorrentBB)

## Summary

emulebb-rust surfaces a file→torrent membership offer ("this file is part of
torrent X"). TrackMuleBB receives the intent (`user wants infohash X`) over REST
and actuates it by adding the torrent to qBittorrentBB. Design origin (frozen
aMuTorrent reference): `amutorrent/docs/SUITE-AUTOMATION.md`.

## Why This Matters

The suite's headline cross-network moment: discover a file on eD2K, pivot to the
full bundle on BitTorrent. Generalizes "clients surface intents; the controller
actuates" — the cross-network logic no single client can own.

## Intended Shape

- Accept an intent payload (infohash + provenance) from emulebb-rust.
- Add the torrent to the configured qBittorrentBB over its REST API.
- Membership data comes from the Python metadata fabric (live-library torrents
  only; harvested torrents never generate an offer).

## Scope Constraints

- **Additive, never a required hop.** With TrackMuleBB stopped, the client path
  still works direct-to-client.
- Only emulebb-rust + qBittorrentBB; no MFC, no other clients.

## Acceptance Criteria

- [ ] An intent carrying an infohash adds the torrent to qBittorrentBB.
- [ ] Offer is built only from live-library membership (fabric); harvested
      torrents excluded.
- [ ] With TrackMuleBB absent, the equivalent client-direct flow still works.

## Notes

- Depends on the metadata fabric (`SUITE-METADATA-FABRIC`) producing
  `file_membership`, and on emulebb-rust emitting the intent.

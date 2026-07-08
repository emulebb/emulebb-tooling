---
id: TMBB-FEAT-013
workflow: github
github_issue: https://github.com/emulebb/trackmulebb/issues/12
title: Docker delivery - compose + profiles + Gluetun + GHCR trackmulebb image
status: OPEN
priority: Major
category: feature
labels: [docker, ghcr, compose, gluetun, bundle]
milestone: phase-2
created: 2026-06-16
source: SUITE-DOCKER design (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# TMBB-FEAT-013 - Docker delivery - compose + profiles + Gluetun + GHCR trackmulebb image

## Summary

The **Docker form** of the suite bundle: a committed `docker-compose.yml` driven by
**compose profiles** + `.env`, an optional **Gluetun** namespace for the P2P
clients, and the minimal **`trackmulebb` GHCR image** (`ghcr.io/emulebb/trackmulebb`).
The setup CLI generates/updates the compose (`setup --target docker`, TMBB-FEAT-010)
so there is one source of truth, no wiring drift. Design:
[`emulebb-tooling/docs/active/SUITE-DOCKER.md`](../../../../active/SUITE-DOCKER.md).

## Why This Matters

Gives the suite a second runtime substrate (containers) sharing the same
TrackMuleBB brain and selectable bundle. The `trackmulebb` image is one of the
four enabling-prerequisite images for the Docker bundle.

## Intended Shape

- Compose in `trackmulebb/docker/`; TrackMuleBB runs as a **plain service** (no
  `docker.sock`).
- **Profiles per component** (`rust,qbbb,trackmulebb,prowlarr,sonarr,radarr,
  sabnzbd,bountarr,plex,gluetun`); TrackMuleBB always present, **>=1 P2P client**,
  dependency enforcement.
- **Single `/data` volume** (`torrents/ usenet/ ed2k/ media/`) → hardlinks +
  atomic move (Model 1: eD2K through Arr).
- **Optional Gluetun:** only P2P containers use `network_mode: "service:gluetun"`;
  their ports published on the gluetun service; control plane reaches them at
  `gluetun:<port>`. hide.me via Gluetun **custom** OpenVPN mode (no auto
  port-forward).
- Publish `ghcr.io/emulebb/trackmulebb` (Python via uv) from this repo's CI.
- Bind-mounts under the project dir (`./config/<app>`, `./data`); Plex in bridge +
  ports.

## Acceptance Criteria

- [ ] `ghcr.io/emulebb/trackmulebb:latest` + version tag pushed by CI.
- [ ] `docker/` compose + profiles + `.env` start the selected bundle; >=1 P2P client enforced.
- [ ] Optional Gluetun routes only the P2P clients (fail-closed); control plane wired to `gluetun:<port>`.
- [ ] `setup --target docker` emits/updates the compose (no hand-editing required).

## Notes

- Companion to the Windows-local form (TMBB-FEAT-010). The bountarr image is
  tracked in `itlezy/bountarr` and bundled via TMBB-FEAT-012.

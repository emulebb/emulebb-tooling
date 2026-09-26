---
id: RUST-FEAT-006
workflow: github
github_issue: https://github.com/emulebb/emulebb-rust/issues/6
title: Publish a linuxserver-style GHCR Docker image
status: IN_PROGRESS
priority: Major
category: feature
labels: [docker, ghcr, packaging, bundle]
milestone: release-0.1.0-beta.1
created: 2026-06-16
source: SUITE-DOCKER design (2026-06-16)
---

> Workflow status is tracked in GitHub. This local document is retained as an engineering spec/evidence record.

# RUST-FEAT-006 - Publish a linuxserver-style GHCR Docker image

## Summary

Publish a **linuxserver-style** Docker image for the emulebb-rust headless eD2K/Kad
core to **GHCR** (`ghcr.io/emulebb/emulebb-rust`, `latest` + versioned), built and
pushed by this repo's CI. Design:
[`emulebb-tooling/docs/active/SUITE-DOCKER.md`](../../../../active/SUITE-DOCKER.md).

## Why This Matters

The **enabling prerequisite** for the suite Docker bundle: without this image the
Docker form of the bundle cannot start. It is the eD2K core in the container set
(MFC is Windows-only, so Docker is rust-only for eD2K).

## Intended Shape

- **linuxserver convention:** s6-overlay, `PUID`/`PGID`, `TZ`, `/config` (state) +
  `/data` (downloads).
- Writes downloads under `/data/ed2k` so hardlink + atomic-move to `/data/media`
  works across the single shared volume (Model 1: eD2K promoted through Arr).
- Runs behind an **optional Gluetun** namespace (`network_mode: "service:gluetun"`);
  no own ports — `/api/v1` + eD2K TCP + Kad UDP are published on the fronting
  service.
- linux/amd64 and linux/arm64 in beta.1; publish the versioned beta tag only,
  reserving `latest` for a stable release.
- Use an independent Gluetun instance and configuration for release proof;
  never edit or restart the operator's existing P2P stack.

## Acceptance Criteria

- [ ] CI builds and pushes `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1`
      as a two-architecture manifest after native packages and image smoke pass.
- [ ] Image honours `PUID`/`PGID`/`TZ`; state under `/config`, downloads under `/data`.
- [ ] `/api/v1` + eD2K TCP + Kad UDP reachable when ports are published on a fronting service.
- [ ] A separate Gluetun tunnel-down test records zero off-tunnel P2P egress.

## Notes

- One of the four prerequisite images (with `qbittorrentbb-nox`, `trackmulebb`,
  `bountarr`). Coheres with the VPN fail-closed model (RUST-FEAT-003/005) — Gluetun
  is the Docker analog of the Windows hide.me split-tunnel.

## 2026-09-26 Candidate Evidence

- A manual release-workflow candidate built and smoked the two-architecture OCI
  archive without publishing it. The final reviewed-head candidate run remains
  part of RUST-FEAT-033's pre-tag gate.
- Container smoke has verified the configured UID/GID, `/config` state, `/data`
  download persistence, and REST/WebUI launch shape.
- The isolated Docker-over-Gluetun tunnel-down campaign proved its positive
  sensor and recorded zero off-tunnel P2P packets after tunnel loss.
- Publication is intentionally pending. This item closes only after the
  separately approved `rust-v0.1.0-beta.1` tag run publishes and verifies the
  versioned multi-architecture GHCR manifest.

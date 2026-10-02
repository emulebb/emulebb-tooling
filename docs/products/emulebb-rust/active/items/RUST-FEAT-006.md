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
core to **GHCR** (`ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1`), built and pushed
by this repo's CI. The beta publishes only the versioned tag; `latest` remains
reserved for a stable release. Design:
[`emulebb-tooling/docs/active/SUITE-DOCKER.md`](../../../../active/SUITE-DOCKER.md).

## Release Triage (2026-09-30)

**Beta blocker.** The approved tagged workflow built, smoked, and pushed the
two-architecture `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1` manifest. GitHub
created the organization package private by default, so anonymous inspection
still returns HTTP 401. Keep this item open and beta-attached until a package
administrator changes visibility to public and the anonymous registry API
verifies the digest, platforms, and absence of a `latest` tag.

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

- [x] CI builds and pushes `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1`
      as a two-architecture manifest after native packages and image smoke pass.
- [ ] Anonymous GHCR inspection verifies the published digest, amd64/arm64
      platforms, and that the package exposes only the versioned beta tag, not
      `latest`.
- [x] Image honours `PUID`/`PGID`/`TZ`; state under `/config`, downloads under `/data`.
- [x] `/api/v1` + eD2K TCP + Kad UDP reachable when ports are published on a fronting service.
- [x] A separate Gluetun tunnel-down test records zero off-tunnel P2P egress.

## Notes

- One of the four prerequisite images (with `qbittorrentbb-nox`, `trackmulebb`,
  `bountarr`). Coheres with the VPN fail-closed model (RUST-FEAT-003/005) — Gluetun
  is the Docker analog of the Windows hide.me split-tunnel.

## 2026-09-26 Candidate Evidence

- Manual release-candidate run `36234229443` built and smoked the linux/amd64
  and linux/arm64 OCI archive on exact Rust candidate `5c5bf7f` without
  publishing it. Both publication jobs were intentionally skipped.
- Container smoke has verified the configured UID/GID, `/config` state, `/data`
  download persistence, and REST/WebUI launch shape.
- The isolated Docker-over-Gluetun tunnel-down campaign proved its positive
  sensor and recorded zero off-tunnel P2P packets after tunnel loss.
- At this 2026-09-26 snapshot, publication was intentionally pending and the
  item remained open for the separately approved tag run.

## 2026-10-02 Tagged Publication Evidence

- The board gave the separate explicit tag approval, and annotated tag
  `rust-v0.1.0-beta.1` resolves to approved Rust commit
  `28a0703561f135b03ffcca94527ceb538ef9012e`.
- [Tagged workflow run `36993503619`](https://github.com/emulebb/emulebb-rust/actions/runs/36993503619)
  passed the native package dependencies, two-platform candidate smoke, and
  `Publish versioned GHCR image` job.
- The push log contains only
  `ghcr.io/emulebb/emulebb-rust:0.1.0-beta.1`, at manifest-list digest
  `sha256:8ddcb65b209e490405e037e78bb4c004574a5c07ee85c2dd829e16bd21f888f2`;
  it contains no `latest` push.
- GitHub's default-private package visibility currently prevents independent
  anonymous registry inspection. Public visibility and the resulting anonymous
  tag/manifest verification remain required before this item can close.

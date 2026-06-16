# Ecosystem Suite Bootstrap Plan

Status: planning only. This document records intended post-0.7.3 ecosystem
packaging direction. It does not describe the current 0.7.3 RC2 bootstrapper or
any shipped release asset.

> **Installer & bundle direction (updated 2026-06-16):** the canonical design is
> now [SUITE-INSTALLER](../SUITE-INSTALLER.md). The Windows one-liner
> (`irm https://emulebb.github.io/install.ps1 | iex`) is a **minimal bootstrap**
> (installs `uv` self-contained, fetches TrackMuleBB, runs its setup CLI); the real
> install is the **Python setup CLI inside TrackMuleBB** (TUI + `suite.toml`),
> which installs/auto-wires the **ready-to-use bundle** across **three networks**
> (eD2K, BitTorrent, Usenet) plus the Arr stack, Bountarr, and (Docker) Plex —
> self-contained, no host interference, `-Core mfc|rust`, decoupled from any
> product release train. The RC-coupled `Bootstrap-eMuleBBSuite.ps1` is superseded.
> The packaging-intent sections below stay valid; SUITE-INSTALLER is the delivery.

## Summary

The eMuleBB suite should grow from a Windows desktop client plus controller
stack into a broader local-machine and headless ecosystem:

- eMuleBB MFC remains the default Windows core until a later release proof
  explicitly promotes another default.
- qBittorrentBB is the first planned Windows bootstrap expansion. It becomes a
  BitTorrent companion in the suite: optional in the model, but preselected for
  normal local-machine `Full` installs.
- qBittorrentBB ships early with the fork identity enabled: DHT harvester/index,
  DHT Index UI/RSS, and Torznab endpoint are part of the planned companion
  package rather than deferred mesh-only features.
- `emulebb-rust` follows as an alternative eD2K/Kad core behind the common
  `/api/v1` controller contract after the qBittorrentBB companion path is
  packaged and proven.
- Gluetun ships as a separate fully headless Docker bundle with VPN routing,
  `emulebb-rust`, qBittorrentBB headless/nox, and controller services.

## Windows Bootstrap Direction

The Windows bootstrapper should keep the existing `Core`, `Controller`, and
`Full` bundle names. The first future `Full` local-machine expansion should
preselect eMuleBB MFC, aMuTorrent, qBittorrentBB, Prowlarr, and the default Arr
apps. Operators can still remove qBittorrentBB through explicit app selection.

Future installer shape:

- Add qBittorrentBB package source, bind, port, start, status, and stop entries
  parallel to other selected services.
- Add a qBittorrentBB WebUI/API readiness check and suite summary entry.
- Keep qBittorrentBB's fork features enabled in the planned package profile.
- Later, add a core selector such as `-CoreClient mfc|rust`, defaulting to
  `mfc`.
- Keep the active eMule-family endpoint named `emulebb` in suite config so
  controller scripts can target one `/api/v1` service regardless of core.
- Preserve the existing RC bootstrap behavior until the new package assets and
  proof exist.

## Package And Release Assets

The suite needs separate release assets before bootstrapper installation is
safe:

- qBittorrentBB Windows x64 ZIP, manifest, SBOM, and provenance metadata. This
  is the first package asset to promote for the expanded Windows suite.
- `emulebb-rust` package assets with Rust repo version and commit provenance
  recorded independently from the MFC app version. These follow qBittorrentBB
  in the suite sequence.
- Gluetun headless ZIP containing Docker Compose files, `.env` templates,
  scripts, manifests, SBOM, and operator-readable setup notes. This follows the
  Windows companion and Rust package lanes.

qBittorrentBB is a companion product with its own compatibility and release
evidence. It should not be described as part of the eD2K/Kad protocol surface,
and the eMuleBB qBittorrent-compatible `/api/v2` adapter remains an Arr-facing
compatibility layer rather than a full qBittorrent clone.

The early qBittorrentBB package should not be reduced to a vanilla upstream
build. The DHT harvester/index, DHT Index UI/RSS feed, and qBittorrentBB Torznab
endpoint are part of the planned companion identity and need package smoke
coverage.

## Gluetun Headless Bundle

The Gluetun bundle is separate from the Windows PowerShell bootstrapper. It
expects an existing Docker runtime and should not install Docker Desktop in its
first version.

Initial service intent:

- `gluetun` owns VPN routing for the headless stack.
- `emulebb-rust` provides the eD2K/Kad core and `/api/v1`.
- `qbittorrentbb-nox` provides the BitTorrent-side companion service.
- `amutorrent` provides the controller surface across selected clients.
- Prowlarr and Arr apps are optional profile services after the core bundle is
  proven.

The bundle must keep operator-owned VPN credentials and live search terms in
local ignored files or runtime environment, never in tracked docs or templates.

## Validation Expectations

Before this plan can move from documentation to implementation, create or link
the active backlog item that owns the slice. The first implementation proof
should include:

- Docs checks that keep current release setup text separate from future suite
  claims.
- Package content checks for qBittorrentBB Windows x64 assets.
- Bootstrap dry runs proving default `Full` includes qBittorrentBB and explicit
  app selection can omit it.
- Runtime smoke evidence for qBittorrentBB WebUI/API, DHT Index UI/RSS, and
  Torznab endpoint readiness.
- Later Rust proof that controllers can reach the selected eMule-family core
  through `/api/v1`.
- Later `docker compose config` validation for the Gluetun bundle.

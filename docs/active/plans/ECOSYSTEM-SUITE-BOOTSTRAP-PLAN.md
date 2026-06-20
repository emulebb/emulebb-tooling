# Ecosystem Suite Bootstrap Plan

Status: planning only. This document records intended `0.8.*`-program ecosystem
packaging direction (it begins after `0.7.3` ships). It does not describe a
shipped release asset.

> **Current release installer (updated 2026-06-19):** for `0.7.3-rc.3` and
> stable `0.7.3`, the public Pages one-liner remains a PowerShell wrapper around
> the GitHub Release `Bootstrap-eMuleBBSuite.ps1`. That bootstrapper installs the
> MFC eMuleBB package, the aMuTorrent controller package (actively maintained
> until `0.7.3` final), and the local Arr plumbing. It does **not** install
> qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, or the Python setup CLI.
>
> **Future installer direction:** after `0.7.3`, [SUITE-INSTALLER](../SUITE-INSTALLER.md)
> owns the TrackMuleBB/`uv`/Python setup design. The packaging-intent sections
> below stay valid for that future delivery.

## Summary

The eMuleBB suite should grow from a Windows desktop client plus controller
stack into a broader local-machine and headless ecosystem:

- eMuleBB MFC remains the default Windows core until a later release proof
  explicitly promotes another default.
- qBittorrentBB is a first-wave `0.8.*`-program Windows bootstrap expansion. It becomes a
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

The future Windows bootstrapper should keep the existing `Core`, `Controller`,
and `Full` bundle names. The first `0.8.*`-program `Full` local-machine expansion
should preselect eMuleBB MFC, qBittorrentBB, Prowlarr, and the
default Arr apps (with TrackMuleBB as the controller in place of aMuTorrent). Operators can still remove qBittorrentBB through explicit app
selection.

The `0.7.3-rc.3`/final PowerShell bootstrapper must preserve the existing
MFC+aMuTorrent+Arr behavior and keep qBittorrentBB unselectable.

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
- Future bootstrap dry runs proving default `Full` includes qBittorrentBB and explicit
  app selection can omit it.
- Runtime smoke evidence for qBittorrentBB WebUI/API, DHT Index UI/RSS, and
  Torznab endpoint readiness.
- Later Rust proof that controllers can reach the selected eMule-family core
  through `/api/v1`.
- Later `docker compose config` validation for the Gluetun bundle.

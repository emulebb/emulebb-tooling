# Ecosystem Suite Bootstrap Plan

Status: planning only. This document records intended post-0.7.3 ecosystem
packaging direction. It does not describe the current 0.7.3 RC2 bootstrapper or
any shipped release asset.

## Summary

The eMuleBB suite should grow from a Windows desktop client plus controller
stack into a broader local-machine and headless ecosystem:

- eMuleBB MFC remains the default Windows core until a later release proof
  explicitly promotes another default.
- `emulebb-rust` becomes an alternative eD2K/Kad core behind the common
  `/api/v1` controller contract.
- qBittorrentBB becomes a BitTorrent companion in the suite. It is optional in
  the model, but preselected for normal local-machine `Full` installs.
- Gluetun ships as a separate fully headless Docker bundle with VPN routing,
  `emulebb-rust`, qBittorrentBB headless/nox, and controller services.

## Windows Bootstrap Direction

The Windows bootstrapper should keep the existing `Core`, `Controller`, and
`Full` bundle names. The future `Full` local-machine install should preselect
eMuleBB MFC, aMuTorrent, qBittorrentBB, Prowlarr, and the default Arr apps.
Operators can still remove qBittorrentBB through explicit app selection.

Future installer shape:

- Add a core selector such as `-CoreClient mfc|rust`, defaulting to `mfc`.
- Keep the active eMule-family endpoint named `emulebb` in suite config so
  controller scripts can target one `/api/v1` service regardless of core.
- Add qBittorrentBB package source, bind, port, start, status, and stop entries
  parallel to other selected services.
- Preserve the existing RC bootstrap behavior until the new package assets and
  proof exist.

## Package And Release Assets

The suite needs separate release assets before bootstrapper installation is
safe:

- qBittorrentBB Windows ZIP, manifest, SBOM, and provenance metadata.
- `emulebb-rust` package assets with Rust repo version and commit provenance
  recorded independently from the MFC app version.
- Gluetun headless ZIP containing Docker Compose files, `.env` templates,
  scripts, manifests, SBOM, and operator-readable setup notes.

qBittorrentBB is a companion product with its own compatibility and release
evidence. It should not be described as part of the eD2K/Kad protocol surface,
and the eMuleBB qBittorrent-compatible `/api/v2` adapter remains an Arr-facing
compatibility layer rather than a full qBittorrent clone.

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
- Package content checks for qBittorrentBB and `emulebb-rust` assets.
- Bootstrap dry runs proving default `Full`, explicit app omission, and Rust
  core selection behavior.
- `docker compose config` validation for the Gluetun bundle.
- Smoke evidence that controllers can reach the selected eMule-family core
  through `/api/v1` and qBittorrentBB through its own service endpoint.

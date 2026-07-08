# TrackMuleBB Active Backlog — Issue Index

Active local/spec layer for **TrackMuleBB**, the eMuleBB Suite forward
cross-network controller (Python; coordinates emulebb-rust + qBittorrentBB only).
Follows the eMuleBB backlog convention
([`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md),
[`BACKLOG-ITEM-TEMPLATE`](../../../reference/BACKLOG-ITEM-TEMPLATE.md)).

## Current Snapshot

**Source of truth:** code in `EMULEBB_WORKSPACE_ROOT\repos\trackmulebb`
(`main` branch); active docs in
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\trackmulebb`.
**Phase:** first beta is the Rust Console UI; later suite phases add the
cross-network controller surface.
**Scope:** first beta targets emulebb-rust only as a Rust eD2K/Kad console over
the Rust-forward `/api/v1` contract. qBittorrentBB, SABnzbd, installer, and
cross-network automation remain later suite work. emulebb-mfc stays on its
legacy controller path.
**Beta acceptance:** the first beta requires the full Rust console surface:
status, transfers, uploads, search/download, shared files, servers/Kad, and
settings. TrackMuleBB remains source-run for the first Rust prerelease; the
`rust-v0.1.0-beta.1` release notes name the compatible TrackMuleBB commit rather
than tagging or packaging TrackMuleBB.
**Tracking:** issues live in `emulebb/trackmulebb` and aggregate on the org
**eMuleBB Suite** board (`https://github.com/orgs/emulebb/projects/3`,
`Product = TrackMuleBB`).
**Design origin:** the automation design is carried over from the frozen
aMuTorrent reference `amutorrent/docs/SUITE-AUTOMATION.md` (items `AMUT-FEAT-*`).

## ID Taxonomy

Item IDs carry the product prefix `TMBB-<CLASS>-<NNN>` (classes `BUG`, `FEAT`,
`REF`, `CI`). Other products use `RUST-`, `QBBB-`, `GOED2K-`, `AMUT-`.

## Features (`FEAT`)

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| [TMBB-FEAT-001](items/TMBB-FEAT-001.md) | Major | OPEN | Cross-network "download the torrent instead" intent handoff (rust → qBittorrentBB) |
| [TMBB-FEAT-002](items/TMBB-FEAT-002.md) | Major | OPEN | Suite automation: cross-network grab + reconcile/orphan actuation |
| [TMBB-FEAT-003](items/TMBB-FEAT-003.md) | Major | OPEN | Coordinate emulebb-rust + qBittorrentBB over REST (adapters) with direct-Arr invariant |
| [TMBB-FEAT-004](items/TMBB-FEAT-004.md) | Major | OPEN | Rust API alignment — remove legacy capability-negotiation assumptions |
| [TMBB-FEAT-005](items/TMBB-FEAT-005.md) | Minor | OPEN | Delta-sync the qBittorrentBB transfers lane (/sync/maindata) instead of full-poll |
| [TMBB-FEAT-006](items/TMBB-FEAT-006.md) | Major | OPEN | Meta-search + cross-network dedup (native clients + Prowlarr, tag-excluded) |
| [TMBB-FEAT-007](items/TMBB-FEAT-007.md) | Major | OPEN | Dynamic global bandwidth coordination across three networks |
| [TMBB-FEAT-008](items/TMBB-FEAT-008.md) | Major | OPEN | SABnzbd adapter — third download client (Usenet) |
| [TMBB-FEAT-009](items/TMBB-FEAT-009.md) | Minor | OPEN | Unified settings — full for emulebb-rust, bandwidth-only for qBittorrentBB/SAB |
| [TMBB-FEAT-010](items/TMBB-FEAT-010.md) | Major | OPEN | Suite setup CLI — self-contained installer (TUI + suite.toml, install/update/repair) |
| [TMBB-FEAT-011](items/TMBB-FEAT-011.md) | Minor | OPEN | Profile import — allowlisted keys + path-rewrite into the install dir |
| [TMBB-FEAT-012](items/TMBB-FEAT-012.md) | Minor | OPEN | Bountarr bundle integration (household media-grab UI over Arr) |
| [TMBB-FEAT-013](items/TMBB-FEAT-013.md) | Major | OPEN | Docker delivery — compose + profiles + Gluetun + GHCR trackmulebb image |
| [TMBB-FEAT-014](items/TMBB-FEAT-014.md) | Minor | OPEN | Push-capable transfer adapters — capability-gated SSE subscribe with poll fallback |
| [TMBB-FEAT-015](items/TMBB-FEAT-015.md) | Major | OPEN | Long-term cross-network analytics — GeoIP (country/city/ASN) over a DuckDB store |

## Bugs (`BUG`)

| ID | Priority | Status | Title |
|----|----------|--------|-------|
| _none yet_ | | | |

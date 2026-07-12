# TrackMuleBB Parked Backlog — Issue Index

Parked local/spec layer for **TrackMuleBB**, the future eMuleBB Suite
cross-network controller (Python; coordinates emulebb-rust + qBittorrentBB only
if reactivated).
Follows the eMuleBB backlog convention
([`BACKLOG-PROCESS`](../../../reference/BACKLOG-PROCESS.md),
[`BACKLOG-ITEM-TEMPLATE`](../../../reference/BACKLOG-ITEM-TEMPLATE.md)).

## Current Snapshot

**Source of truth:** code in `EMULEBB_WORKSPACE_ROOT\repos\trackmulebb`
(`main` branch); active docs in
`EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs\products\trackmulebb`.
**Phase:** parked Phase 2 future work. TrackMuleBB resumes only after
qBittorrentBB progresses enough to make cross-network controller work concrete.
**Scope:** not part of the current emulebb-rust headless client + Rust-native UI
beta. qBittorrentBB, SABnzbd, installer, and cross-network automation remain
later suite work. emulebb-mfc stays on its legacy controller path and is not
linked to TrackMuleBB.
**Beta acceptance:** no current TrackMuleBB beta gate. The first Rust prerelease
is gated by emulebb-rust daemon and Rust-native UI proof.
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
| [TMBB-FEAT-004](items/TMBB-FEAT-004.md) | Major | DEFERRED | Parked Rust API alignment — remove legacy capability-negotiation assumptions |
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

# eMuleBB (MFC) Future Roadmap

> **eMuleBB — the C++ MFC desktop app — is closing with `0.7.3` final and
> entering permanent `0.7.x` maintenance.** Forward development has shifted to
> **emulebb-rust** (the multiplatform eD2K/Kad core), **qBittorrentBB**, and the
> suite integrations. The active forward program lives in
> [SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md). This document now governs only
> what remains for the MFC app: `0.7.x` maintenance plus the family/packaging
> tracks the MFC participates in as a packaged component.

This is the post-0.7.3 roadmap for the eMuleBB MFC desktop app. It is not a
`0.7.3` release-candidate gate (that is owned by [RELEASE-0.7.3](RELEASE-0.7.3.md)).
With the forward focus on emulebb-rust, the MFC product surface is intentionally
frozen at `0.7.3`: new product, UI, protocol, and configuration work is out of
scope for this app and — where still wanted — is tracked on the rust/suite
roadmap instead. See [Frozen Surfaces](FROZEN-SURFACES.md) for the
compatibility-preserved legacy baggage versus supported behavior split.

For a shorter public-readable overview, use
[Roadmap Summary](../reference/ROADMAP-SUMMARY.md).

## Release Line Model

- `0.7.3` is the **final eMuleBB MFC feature release**. The fixed candidate train
  is `0.7.3-rc.1`, `0.7.3-rc.2`, `0.7.3-rc.3`, then stable `0.7.3`. Each candidate
  absorbs only release blockers, proof refreshes, packaging fixes, and approved
  regression fixes.
- After stable `0.7.3`, `release/0.7.x` is the **permanent maintenance line** and
  `main` carries only `0.7.x` maintenance. Allowed: compatibility-preserving,
  low-risk bug fixes on supported surfaces plus security, crash/data-loss,
  packaging, update-check, release-proof, and release-documentation fixes. Not
  allowed: new product surface, new controller/API capability, or feature
  expansion.
- Frozen legacy surfaces stay frozen; they are not fixed in `0.7.x` unless the
  issue affects supported shared infrastructure, security, or app stability.
- Stable patch maintenance increments the patch number (for example
  `emulebb-v0.7.4`) for hotfixes on the maintenance line.
- **`0.8.0` (MFC modernization) is ON HOLD / UNDER REVIEW — not retired, not
  active.** The previous plan to open `main` for a `0.8.0` MFC modernization wave
  (frozen-surface removal first, then product lanes) is **suspended** pending a
  decision on whether the MFC app continues at all given the emulebb-rust pivot.
  Do not start `0.8.0` MFC work without an explicit operator decision to revive
  the line. The frozen-surface inventory is retained in
  [Frozen Surfaces](FROZEN-SURFACES.md) for that future decision.

## GitHub Workflow Authority

Roadmap workflow is GitHub-primary. Promoted MFC slices are tracked as issues in
`emulebb/emulebb` and as items in the public `eMuleBB Roadmap` org project (#2).
Local item docs remain engineering specs and evidence records; for files marked
`workflow: github`, current status, priority, release placement, discussion,
ownership, and PR linkage live in GitHub. The forward program (emulebb-rust,
qBittorrentBB) is tracked separately on the public **eMuleBB Suite** board
(`https://github.com/orgs/emulebb/projects/3`); see
[SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md#backlog--tracking-structure).

Use `python scripts\github-roadmap-sync.py` from `repos\emulebb-tooling` to
preview or apply the MFC import, and `python scripts\github-roadmap-check.py` to
validate migrated metadata.

## Product Boundary

eMuleBB remains a Windows MFC desktop client with a first-class UI, tray workflow,
and in-process REST surface for controllers. Headless-only, daemon,
cross-platform, server-only, and mobile-controller product tracks belong outside
this app — they are the emulebb-rust / qBittorrentBB / Gluetun tracks of the
broader product family. `emulebb-rust` is the headless eD2K/Kad core behind the
shared `/api/v1` contract and is now the **forward core**; qBittorrentBB is the
BitTorrent companion; the Gluetun bundle is a headless Docker packaging track.
p2p-overlord is a separate Rust/Node product in the family that can share REST
contracts, test infrastructure, and selected dependency forks without becoming
part of the desktop app. See
[ECOSYSTEM-SUITE-BOOTSTRAP-PLAN](plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md) and
[SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md).

## Active Lanes (MFC, slimmed)

Only the lanes below remain in scope for the MFC app. Everything else from the
prior roadmap is superseded by the rust/suite program (see Superseded Lanes).
Lanes are grouped intentionally: do not create a new detailed `FEAT-*` file from a
lane until the operator approves that specific slice.

### Security And Operations (0.7.x maintenance)

IP-filter input policy, PeerGuardian-style imports, whitelist/private-network
policy, dependency/DLL loading hardening, diagnostics, the bound VPN public-IP
guard, and release-proof automation. This is maintenance, not feature expansion.

Existing anchors: `FEAT-044`, `FEAT-056`, `FEAT-098`, `REF-028`, `REF-038`,
`REF-039`, `REF-040`, `REF-041`, `REF-042`, `REF-052`.

### Controller Surface Performance (bounded maintenance)

REST/controller maintenance that bounds memory use and latency for large profiles
without expanding the public capability surface, only where it protects the
shipped `0.7.3` controller. Snapshot workers may build immutable response records;
live app objects stay owned by their normal app/UI/protocol paths. New forward
controller capability belongs on emulebb-rust, not here.

Existing anchors: `FEAT-068`, `FEAT-099`.

### Product-Family Integration

Post-`0.7.3` alignment for p2p-overlord repos, shared REST conformance, shared
campaign variants, shared campaign/runtime core infrastructure, and shared
MiniUPnP source ownership — without merging products.

Existing anchors: `FEAT-073`, `FEAT-085`.

### Ecosystem Suite Packaging (forward focus)

The MFC app as a packaged suite component: the Windows bootstrap, local Arr
integration, and aMuTorrent. The suite itself (emulebb-rust core, qBittorrentBB
companion, Gluetun headless bundle) is governed by
[SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md) and
[ECOSYSTEM-SUITE-BOOTSTRAP-PLAN](plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md), not by
this MFC roadmap.

Existing anchors: `plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md`,
`active/EMULEBB-RUST-SCOPE.md`, `ideas/IDEA-QBITTORRENTBB-MESH.md`.

### Post-0.7.3 Tooling And Security (workspace hygiene)

Release-proof, CI, diagnostics, security, dependency, and generated-output hygiene
that improves the workspace without changing the `0.7.3` public product surface
(CodeQL, static analysis, release-proof UX, deterministic materialization,
dependency hardening, REST semantic proof that does not expand capability).

## Superseded Lanes (retired from the MFC roadmap)

These prior product lanes are **no longer MFC roadmap scope**. Where the value is
still wanted it is carried by the rust/suite program; the rest is dropped. None is
promoted on the MFC app without an explicit operator decision to revive it.

| Retired lane | Disposition |
|---|---|
| Connectivity Modernization (IPv6, NAT/LowID, µTP, UPnP/PCP) | Dropped for MFC; ideas only (`IDEA-IPV6-KAD-NETWORK`, `IDEA-NAT-TRAVERSAL-UTP`). rust is IPv4-only. |
| Search And Trust Clarity (fake-file confidence, Kad popularity, remote inventory) | Superseded by the rust Kad/eD2K indexer (FEAT-002) + the suite metadata fabric. |
| Local State And Configuration Planning (SQLite metadata, JSON/TOML config) | Superseded by emulebb-rust `emulebb-metadata` and the qBittorrentBB harvester index. |
| UI Power-User Polish (dark mode, Per-Monitor DPI, category/table polish) | Dropped — MFC-GUI-specific on a closing app. |
| Startup And Storage Performance | Dropped, except crash/data-loss/stability fixes, which fall under `0.7.x` maintenance. |
| Upload Policy Clarity (broadband slots, friend slots) | Dropped; may inform emulebb-rust upload policy later. |
| Narrow Anti-Leecher Review (CShield) | Dropped. |

The `FEAT-*`/`REF-*` anchors previously listed under these lanes remain in the
backlog index as records; they are not active MFC roadmap work unless re-promoted.

## Explicit Non-Goals

Do not add these to the eMuleBB MFC backlog unless the operator explicitly reopens
them:

- New MFC product/feature work in any Superseded Lane above.
- `0.8.0` MFC modernization or frozen-surface removal until the line is explicitly
  revived (it is on hold, not active).
- Headless core, server-only mode, cross-platform client work, or mobile-first
  controller scope inside the MFC desktop app. These are emulebb-rust /
  qBittorrentBB / Gluetun family tracks.
- New REST capability expansion beyond contract maintenance, drift checks, bug
  fixes, and compatibility repairs. Forward controller capability is emulebb-rust.
- Historical releaser controls (PowerShare, Share Only The Need, release bonus,
  default share-permission rewrites). `FEAT-083` and `FEAT-084` remain `WONT_DO`.
- Protocol forks, proprietary Kad/eD2K extensions, opcode/packet/tag shape
  changes, Kad state-machine drift, or transport rewrites that cannot be validated
  against current community semantics.
- Distinct IPv6 Kad network behavior. It stays in
  `ideas/IDEA-IPV6-KAD-NETWORK.md` until explicitly promoted (and on a forward
  core, not the MFC app).
- Metadata/file-intelligence expansion in the MFC app. MediaInfo stays an external
  DLL; the indexing/metadata direction is the rust/suite program.

## Promotion Rules

- This roadmap is grouped intentionally. Do not create a new detailed `FEAT-*`
  file from a lane until the operator approves that specific slice.
- MFC promotions are limited to `0.7.x` maintenance plus the four active lanes
  above. Anything resembling a Superseded Lane is re-homed to the rust/suite
  roadmap, not promoted here.
- A promoted MFC slice must have an `emulebb/emulebb` issue and `eMuleBB Roadmap`
  (#2) project item before implementation starts.
- Before implementation, revalidate the slice against current `main`, current
  dependency pins, and `WORKSPACE-POLICY.md`.
- Prefer narrow, observable maintenance over behavioral rewrites; keep
  stock/community eD2K/Kad behavior intact.

## GitHub-Primary Backlog Highlights

The GitHub sync owns all active backlog items under `docs/active/items`. The table
below is a compact list of cross-cutting MFC highlights; it is not the sync
boundary.

| Lane | Scope | Items |
|---|---|---|
| Security and operations | Bound VPN public-IP guard for interface-bound profiles | `FEAT-098` |
| Controller surface performance | Bounded large-list REST memory/latency | `FEAT-068`, `FEAT-099` |
| Product-family integration | Shared campaign core; p2p-overlord alignment | `FEAT-073`, `FEAT-085` |

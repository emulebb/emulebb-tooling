# eMuleBB (MFC) Future Roadmap

> **Current direction (operator decision 2026-07-12):** emulebb-mfc closes its
> `0.7.x` feature line with stable `0.7.3`. The MFC `0.8.x` roadmap and lean/
> async ideas remain recorded here, but no MFC `0.8.x` lane is active. The MFC
> client is valuable but expensive to evolve cleanly, so near-term forward
> development focuses on **emulebb-rust** headless client stabilization and
> embedded SPA WebUI. **qBittorrentBB** is future companion work; **TrackMuleBB** is
> parked until qBittorrentBB progresses. Larger evolution should move out of MFC
> unless a later explicit decision reactivates a narrow MFC lane.

This is the post-0.7.3 roadmap for the emulebb-mfc desktop app. It is not a
`0.7.3` release-candidate gate (that is owned by [RELEASE-0.7.3](RELEASE-0.7.3.md)).
The MFC product surface stays **frozen for the `0.7.x` line** — new product, UI,
protocol, and configuration work is out of scope there. The recorded `0.8.x`
ideas are retained as roadmap material, not as an active commitment. See
[Frozen Surfaces](FROZEN-SURFACES.md) for the compatibility-preserved legacy
baggage versus supported behavior split that would inform any later MFC `0.8.x`
decision.

For a shorter public-readable overview, use
[Roadmap Summary](../reference/ROADMAP-SUMMARY.md).

## Release Line Model

- `0.7.3` is the **final `0.7.x` feature release**. The fixed candidate train is
  `0.7.3-rc.1`, `0.7.3-rc.2`, `0.7.3-rc.3`, then stable `0.7.3`. Each candidate
  absorbs only release blockers, proof refreshes, packaging fixes, and approved
  regression fixes.
- After stable `0.7.3`, `release/0.7.x` is the **permanent maintenance line**
  (compatibility-preserving, low-risk bug fixes plus security, crash/data-loss,
  packaging, update-check, release-proof, release-documentation fixes, and
  non-behavior-expanding diagnostics/instrumentation; no new product surface,
  controller/API capability, or feature expansion). `main` remains a maintenance
  integration branch, not an MFC feature lane.
- Frozen legacy surfaces stay frozen; they are not fixed in `0.7.x` unless the
  issue affects supported shared infrastructure, security, or app stability.
- Stable patch maintenance increments the patch number (for example
  `emulebb-v0.7.4`) for hotfixes on the maintenance line.
- **`0.8.0` (MFC modernization) is an open question (operator decision
  2026-07-05).** The prior 2026-06-20 revival decision is superseded for planning
  purposes. The frozen-surface removal, performance, and async plans remain useful
  design material, but they are not active implementation commitments. A later
  operator decision must explicitly reopen MFC `0.8.x` before broad MFC evolution
  starts.
- **Forward sequencing (operator decision 2026-07-12):** after stable `0.7.3`,
  focus moves to `emulebb-rust` headless client stabilization and embedded SPA
  WebUI.
  qBittorrentBB is later BitTorrent-side companion work, and TrackMuleBB is
  parked future controller work.

## GitHub Workflow Authority

MFC roadmap workflow is archived. The `emulebb/emulebb` issues and public
`eMuleBB Roadmap MFC (archive)` org project (#2) are provenance for the frozen
line. New MFC items require a critical-maintenance or diagnostic/instrumentation
justification. Forward program work (emulebb-rust now; qBittorrentBB and
TrackMuleBB later) is tracked on the public **eMuleBB Suite** board
(`https://github.com/orgs/emulebb/projects/3`) and in the owning product repo; see
[SUITE-JOINT-ROADMAP](SUITE-JOINT-ROADMAP.md#backlog-tracking-structure).

Treat `python scripts\github-roadmap-sync.py` and
`python scripts\github-roadmap-check.py` as legacy MFC archive tooling until the
sync path is generalized for product-owned Suite work.

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

### Performance And Async (0.8.x modernization)

The first specified `0.8.x` MFC lane content (operator decision 2026-06-24): make
startup reach an interactive window fast, move the networking off the UI message
pump, and move the 100ms `Process()` scheduling loop off the UI thread. This
**revives** the previously *Dropped* "Startup And Storage Performance" lane (see
Superseded Lanes) under the revived `0.8.x` line — it opens on `main` only after
stable `0.7.3` and the `release/0.7.x` split, and is **out of scope for the `0.7.x`
maintenance line** (see Explicit Non-Goals). The network half is a **forward-port of
the operator's own tested `WSAPoll` network-thread migration** from the
`v0.72a-broadband-dev` lineage (`analysis/stale-v0.72a-experimental-clean`), not a
from-scratch design; full IOCP stays a later `0.8.x` end-state. eMuleBB additionally
keeps the web server / `/api/v1` REST the reference removed, so the port adds
controller-surface read-locking.

Lane spec and design docs: [MFC-0.8.0-PERF-ASYNC-PLAN](plans/MFC-0.8.0-PERF-ASYNC-PLAN.md),
[startup](plans/MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md),
[network core thread](plans/MFC-0.8.0-NETWORK-CORE-THREAD.md),
[Process() migration](plans/MFC-0.8.0-PROCESS-LOOP-MIGRATION.md).

### Lean line — frozen-surface removal (0.8.x modernization)

The companion `0.8.x` lane (operator decision 2026-06-24): once `0.7.3` final ships
and `0.7.x` becomes the **LTSC** line, `0.8.0` deletes the dead/legacy subsystems
instead of carrying them forward. Scope consolidates the existing removal items —
IRC/Scheduler/wizard/legacy-splash/SMTP (`REF-025`), legacy WebServer HTML templates
keeping REST (`REF-043`), SOCKS/proxy (`REF-051`), archive preview/recovery
(`REF-052`) — plus operator additions: **drop mbedTLS and serve REST over plaintext
HTTP bound local-only** (proposed `REF-060`), and remove 3D-preview-control, id3lib,
and TextToSpeech/SAPI. The supported controller/protocol surface (REST listener +
`/api/v1`/`/api/v2`, MiniMule, `LifecycleProgressDlg`, UPnP/VPN-guard) is **kept**.
Removals land on `main` only — never on the `0.7.x` LTSC line.

Lane spec: [MFC-0.8.0-LEAN-REMOVAL-PLAN](plans/MFC-0.8.0-LEAN-REMOVAL-PLAN.md);
register: [FROZEN-SURFACES](FROZEN-SURFACES.md).

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
| Startup And Storage Performance | **Revived for `0.8.x`** (operator decision 2026-06-24) as the [Performance And Async](#performance-and-async-08x-modernization) lane. Remained `0.7.x`-maintenance-only for crash/data-loss/stability fixes. |
| Upload Policy Clarity (broadband slots, friend slots) | Dropped; may inform emulebb-rust upload policy later. |
| Narrow Anti-Leecher Review (CShield) | Dropped. |

The `FEAT-*`/`REF-*` anchors previously listed under these lanes remain in the
backlog index as records; they are not active MFC roadmap work unless re-promoted.

## Explicit Non-Goals

Do not add these to the emulebb-mfc backlog unless the operator explicitly reopens
them:

- New MFC product/feature work in any Superseded Lane above.
- `0.8.x` MFC modernization or frozen-surface removal work landing on the
  shipping `0.7.x` line. The `0.8.x` line is currently an open question
  (decision 2026-07-05); keep it out of the `0.7.x` maintenance line unless a
  later operator decision explicitly reopens MFC evolution.
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
- A promoted MFC slice must have an `emulebb/emulebb` issue and archived
  Project #2 item before implementation starts, unless the operator explicitly
  keeps the item local-only.
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

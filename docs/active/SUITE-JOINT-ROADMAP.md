# Suite Joint Roadmap (post-0.7.3)

Status: planning / direction. This is the cross-product forward program for the
BB suite captured from an operator design session (2026-06-14). It is **not** a
0.7.3 gate and it does **not** touch the frozen eMuleBB MFC app.

## Naming (exact, do not conflate)

- **eMuleBB** = the **C++ MFC Windows desktop app** (`emulebb-main`). The current
  flagship eD2K/Kad client.
- **emulebb-rust** = the **Rust eD2K/Kad core** — headless, multiplatform. The
  strategic forward core (and the autonomous indexer of notes 13–15).
- **qBittorrentBB** = the BitTorrent-side client (fork) with the DHT harvester +
  Torznab index.
- **aMuTorrent** = the cross-network web-UI controller.

## Freeze scope (read first)

The only frozen product is the **eMuleBB (MFC) app**, which closes out with
`0.7.3` final (see [FUTURE-ROADMAP](FUTURE-ROADMAP.md) and
[FROZEN-SURFACES](FROZEN-SURFACES.md)). Every other product in the family —
`emulebb-rust`, `qBittorrentBB`, `goed2k-server`, the Python metadata-fabric
tooling, and `amutorrent` — is in **full development mode, no limits**. This
program lives entirely in that unfrozen space and begins after `0.7.3` ships.

**eMuleBB 0.7.3 final scope:** the PowerShell suite bootstrap + local Arr
integration + aMuTorrent. That is the whole of it — no further MFC feature scope.
**`0.7.3` may be the last eMuleBB (MFC) release:** the strategic direction is to
move heavily to **emulebb-rust** as the forward eD2K/Kad core. Consequently the
metadata-fabric eD2K integrations (notes 1/5/6) target **emulebb-rust's
`emulebb-metadata` SQLite as the primary** share/hash source; MFC `known.met` is a
compatibility path only.

## North star

> A full, safe, peer-to-peer file-sharing suite for sharing professionals, with
> no strict reliance on eD2K servers or indexers — fully distributed, anonymous,
> multiplatform, and maximally automated.

Each clause is a load-bearing constraint, not a slogan:

- **Full suite** — integrated set, not isolated clients: eD2K/Kad client
  (`emulebb-rust`), BT client (`qBittorrentBB`), optional server
  (`goed2k-server`), indexers (Torznab/Prowlarr), Python tooling, and the
  `amutorrent` controller. The notes 1–6 metadata fabric is what makes it a
  *suite* rather than two unrelated clients.
- **Safe** — operationally (VPN-fail-closed binding, control plane on the local
  IP, data plane pinned to the tunnel) and content-wise (harvested content is
  strictly separated from shared content; private torrents never leave the box).
- **No strict reliance on servers/indexers** — Kad and the BitTorrent mainline
  DHT are first-class; servers and tracker/indexer sites are conveniences, never
  dependencies. The suite builds its **own** discovery (the indexers) and becomes
  its own Torznab indexer to the Arr stack.
- **Fully distributed** — DHT/Kad-native discovery, peer cooperation between
  clients, server-to-server peering in `goed2k-server`. No central coordinator
  (explicitly not the p2p-overlord Postgres model — indexers stay local).
- **Anonymous** — defined as **network-level** anonymity: the real IP never
  reaches a swarm; everything egresses the VPN tunnel, fail-closed. This is the
  agreed definition; there is **no** I2P/onion-overlay track. The work is to
  *maintain and verify* the binding discipline, not to build a new anonymity
  layer.
- **Multiplatform** — the strategic reason the forward program is rust- and
  qBittorrentBB-centric: the eD2K client future is portable `emulebb-rust`, not
  the Windows-only MFC app. The MFC app is the one Windows-only piece, and it is
  frozen out of this program by design.
- **Highest automation** — the controller plus report-only tooling plus
  autonomous indexing: the operator sets policy and the suite discovers,
  reconciles, downloads, shares, and bridges across networks unattended.

## Layered architecture

```
Policy / orchestration ── amutorrent controller (optional layer)         notes 6,16,17
Discovery / index ─────── rust Kad/eD2K indexer + qBittorrentBB DHT       notes 11-15
                          harvester + Prowlarr federation
Clients / transport ───── emulebb-rust (eD2K/Kad) + qBittorrentBB (BT)    Phase 0/1
Bridging / library ────── Python fabric + branded export + membership DB  notes 1-6
Safety substrate ──────── VPN-fail-closed binding; harvested != shared    cross-cutting
```

## Deliverable ordering (strict, component-level)

The operator set a strict serial order at the component level: **rust →
qBittorrentBB → everything else.**

### Phase 0 — `emulebb-rust` perfectly functional (gate)

"Perfectly functional" = client parity **plus the indexer role**. Both are inside
deliverable #1; the indexer is not a later phase.

- Client parity: connect (server + Kad), search (server + Kad/global), download
  end-to-end from multiple sources including queue/reask, upload/share + serve
  sources.
- **Enable UDP source-reask (FEAT-001).** Code-complete off by default; remaining
  work is live validation (Rust↔Rust, then gentle Rust↔stock) before flipping
  `enable_udp_reask` on. See `emulebb-rust` `docs/design/udp-source-reask.md`.
- **Finish the VPN egress pin for eD2K TCP** (Kad UDP is done; eD2K TCP pending).
  Close the network-level anonymity guarantee.
- **The autonomous Kad/eD2K indexer** (note 13). Passive-first snoop of routed
  Kad traffic + gentle/compliant active replay and extension sweeps + opportunistic
  source capture + optional server-search enrichment → one FTS SQLite index. See
  `emulebb-rust` `docs/design/kad-ed2k-indexer.md`.
- **Arr surfaces** (note 15): native `/api/v1` REST (control + search) + a Torznab
  endpoint + a qBittorrent-WebUI-emulating download-client API, so the Arr stack
  and `amutorrent` drive rust exactly as they drive a qBittorrent (same pattern
  eMuleBB already proved with its `/api/v2` compat layer).

### Phase 1 — `qBittorrentBB`

- Mature the DHT harvester ([qbittorrentbb-dht-harvester]; already implemented,
  green, running).
- **Branded idempotent export** of the *live* torrent library → eMuleBB share
  (note 1).
- **Persist harvested torrents to a sharded on-disk store** for reconciliation
  (note 3) — strictly local, never shared.
- Torznab + qBittorrent-API + Prowlarr-indexer parity with rust (note 14/15).
- See `qBittorrentBB` `docs/BB-TORRENT-EXPORT-AND-HARVEST.md`.

### Phase 2 — everything else

- **Python metadata fabric** (notes 1–6): reconcile, orphan/mixed-content scan,
  torrent⇄collection converters, file→torrent membership. See
  [SUITE-METADATA-FABRIC](SUITE-METADATA-FABRIC.md).
- **Library publishing + cooperative discovery** (notes 11–12): BEP-46 mutable
  library pointer under a minted publisher key, resolving to v2/hybrid catalog
  torrents; cooperative-client mechanisms. See
  [ideas/IDEA-COOPERATIVE-DHT-COOPERATION](../ideas/IDEA-COOPERATIVE-DHT-COOPERATION.md).
- **`amutorrent` suite automation** (notes 6, 16, 17): cross-network grab
  decisions, reconcile/orphan actuation, "download the torrent instead" handoff.
  Optional layer — clients + Prowlarr stay fully standalone. See `amutorrent`
  `docs/SUITE-AUTOMATION.md`.

## Cross-cutting principles (decided this session)

- **Disk is the pivot.** Torrents, eMule collections, and eD2K shares are
  interconvertible *views of the same files on disk*. You cannot derive a BT hash
  from an eD2K hash or vice-versa; the bytes on disk are the only bridge.
- **Two keys join everything:** BT `infohash` and eD2K hash. One parseable `bb:`
  tag convention (in torrent comments and collection names) makes the suite
  self-recognizing across every tool.
- **Two strictly separate libraries:** the **live/shared** library (only your own
  qBittorrentBB torrents; branded; flows to eMuleBB) and the **harvested**
  library (the DHT firehose; quarantined to your machine; never shared, never
  branded). They never mix.
- **Clients surface intents; the controller actuates** — but the controller is an
  **optional** layer. Clients + Prowlarr must function with no controller present.
- **Tooling is report/produce-only.** Reconcile and scan emit reports; the
  controller (or operator) decides actions.
- **Indexer design parity is a living goal, not a frozen schema.** rust and
  qBittorrentBB co-evolve their indexer schema + Torznab contract; revisit
  per-field as we build.
- **Brand + website are operator config**, never hardcoded; the publisher private
  key and operator data live under the user data path, never in build output,
  never committed.

## Active vs Parked (scope ledger)

This program has a deliberately small **active** surface. Everything else we have
written down is an **idea, parked** — captured so it is not lost, explicitly not
scheduled, and not in any backlog or GitHub board until an operator promotes a
specific slice.

### Active (the only scheduled work)

- Close **eMuleBB (MFC) 0.7.3 final**: PowerShell bootstrap + local Arr +
  aMuTorrent. Then frozen.
- **Phase 0 — emulebb-rust** perfectly functional: enable UDP reask (FEAT-001),
  eD2K TCP VPN egress pin, download/upload parity hardening, the Kad/eD2K indexer,
  Arr surfaces. Tracked in `emulebb-rust/docs/active`.
- **Phase 1 — qBittorrentBB**: branded export, harvested disk store, indexer /
  Torznab parity. Tracked in `qbittorrentbb/docs/active`.
- **Phase 2 — metadata fabric + aMuTorrent automation** (notes 1–6, 16–17).

### Parked (ideas only — not scope, not backlog)

Promote a slice into a product backlog before any of these becomes work.

| Parked idea | Doc |
|---|---|
| Cooperative-DHT mechanisms (15-item menu) + BEP-46 library publishing (notes 11–12) | `ideas/IDEA-COOPERATIVE-DHT-COOPERATION.md` |
| libtorrent fork for the deep cooperation plays | `ideas/IDEA-COOPERATIVE-DHT-COOPERATION.md`, `ideas/IDEA-EMULEBB-LIBTORRENT-FORK.md` |
| eD2K↔BT mesh at scale: surrogate overlay, gateway/republisher, transfer bridging | `ideas/IDEA-LIBTORRENT-MESH.md`, `ideas/IDEA-QBITTORRENTBB-MESH.md` |
| IPv6 Kad network | `ideas/IDEA-IPV6-KAD-NETWORK.md` |
| Kad protocol modernization | `ideas/IDEA-KAD-PROTOCOL-MODERNIZATION.md` |
| NAT traversal / µTP | `ideas/IDEA-NAT-TRAVERSAL-UTP.md` |
| aMule watchlist | `ideas/IDEA-AMULE-WATCHLIST.md` |
| Broad modernization / restructure surveys | `ideas/IDEA-MODERNIZATION-2026.md`, `ideas/IDEA-RESTRUCTURE.md` |
| A4AF cross-file source dedup (rust) | `emulebb-rust/docs/design/source-management-and-a4af.md` |
| aMuTorrent owning all generic download rules (scope split) | `amutorrent/docs/SUITE-AUTOMATION.md` |

eMuleBB-MFC `FUTURE-ROADMAP.md` lanes (dark mode, IPv6 dual-stack, µTP, NAT-PMP,
etc.) are **parked-by-freeze**: `0.8.x` material only if the MFC app is not
retired in favour of emulebb-rust.

## Backlog & tracking structure

Decided + set up 2026-06-14:

- **Issues live in each product's own repo** (release-train correctness): rust →
  `emulebb/emulebb-rust`, qBittorrentBB → `emulebb/qbittorrentbb`. The local MD
  item under `docs/active/items` is the durable engineering spec; the GitHub issue
  owns workflow state (`workflow: github`).
- **One org board aggregates them:** **eMuleBB Suite**,
  `https://github.com/orgs/emulebb/projects/3`, with single-select fields
  `Product` (eMuleBB-MFC / emulebb-rust / qBittorrentBB / aMuTorrent / tooling) and
  `Phase` (Phase 0/1/2). Phase 0 = rust issues #1–#4; Phase 1 = qBittorrentBB
  issues #1–#3.
- **The MFC `eMuleBB Roadmap` board (#2) stays as-is** for the frozen 0.7.x line;
  it is not polluted with forward work.
- **Parked ideas stay out of the tracker** — they remain `IDEA-*.md` and become
  backlog only when a slice is promoted.

**Pending tooling task (not yet done):** generalize the GitHub sync scripts
(`emulebb-tooling/scripts/github_roadmap_common.py`, `github-roadmap-sync.py`,
`github-roadmap-check.py`) from their hardcoded single product
(`OWNER`/`ISSUE_REPO=emulebb/emulebb`/`PROJECT_TITLE=eMuleBB Roadmap`, scanning
only `emulebb-tooling/docs/active/items`) to a **per-product config** (repo +
items path + project + Product/Phase field mapping), so each product's
`docs/active/items` syncs to its own repo issues and onto the Suite board. This
mutates live GitHub state, so it needs its own focused, tested change — do not
bolt it on untested.

## Index of program docs

| Area | Doc | Repo |
|---|---|---|
| This roadmap | `docs/active/SUITE-JOINT-ROADMAP.md` | emulebb-tooling |
| Metadata fabric (notes 1–6) | `docs/active/SUITE-METADATA-FABRIC.md` | emulebb-tooling |
| Cooperative DHT (note 12) | `docs/ideas/IDEA-COOPERATIVE-DHT-COOPERATION.md` | emulebb-tooling |
| Kad/eD2K indexer (notes 13–15) | `docs/design/kad-ed2k-indexer.md` | emulebb-rust |
| Branded export + harvest store (notes 1,3) | `docs/BB-TORRENT-EXPORT-AND-HARVEST.md` | qBittorrentBB |
| Suite automation (notes 6,16,17) | `docs/SUITE-AUTOMATION.md` | amutorrent |
| Library publishing (note 11) | `docs/ideas/IDEA-COOPERATIVE-DHT-COOPERATION.md` | emulebb-tooling |
| Suite packaging | `docs/active/plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md` | emulebb-tooling |

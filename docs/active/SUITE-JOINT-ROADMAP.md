# Suite Joint Roadmap (0.8.* forward program)

Status: planning / direction. This is the **canonical top-level roadmap** for the
BB suite, which is delivered in the **`0.8.*` program** that begins after `0.7.3`
ships. The MFC [FUTURE-ROADMAP](FUTURE-ROADMAP.md) is the companion annex for the
MFC modernization half of that same `0.8.*` program. Companion governance:
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md), [QUALITY-GATES](QUALITY-GATES.md),
[API-V1-COMPATIBILITY](API-V1-COMPATIBILITY.md). It is **not** a `0.7.3` gate and
does **not** touch the shipping `0.7.x` MFC line.

## Decision (2026-06-15): forward stack supersedes the prior controller plan

This decision supersedes the earlier framing below where aMuTorrent was the
forward cross-network controller "in full development mode".

1. **eMuleBB (MFC) `0.7.3` is the final `0.7.x` feature release** — MFC then
   continues in the revived `0.8.x` modernization line (decision 2026-06-20), so
   it is *not* the end of MFC development. Through the `0.7.x` line the MFC app's
   package, delivered via the proven PowerShell suite bootstrap, bundles the MFC
   client, the aMuTorrent controller (actively maintained until `0.7.3` final),
   and the Arr setup plumbing only. **qBittorrentBB, emulebb-rust, TrackMuleBB,
   `uv`, and the Python setup CLI are not in the `0.7.3-rc.3`/final bootstrap** —
   they ship in the `0.8.*` program after this release train. The `0.7.x` bundle's
   eD2K side is the MFC client itself.
2. **aMuTorrent closes out on the `0.7.3` line** — it ships with the final MFC
   package and is **not** the forward controller. *(Timing refined by Decision
   2026-06-20 below: it stays actively maintained and upstream-synced until `0.7.3`
   final, and only then freezes into sustainability-only maintenance.)*
3. **The forward stack is: emulebb-rust + qBittorrentBB + TrackMuleBB** — a new
   Python coordination controller with an integrated web UI (Python-only, e.g.
   NiceGUI; no Node/JS toolchain). Product **TrackMuleBB** (repo `trackmulebb`,
   first-party, `-BB` family). **Scope is capability-driven** (decision
   2026-06-16): TrackMuleBB drives **any `/api/v1` core by advertised capability**
   — emulebb-rust (full) and the eMuleBB MFC (frozen subset) — plus qBittorrentBB
   over its own API. MFC support is free fallout of the capability-gated contract
   (see [API-V1-COMPATIBILITY](API-V1-COMPATIBILITY.md)), so **aMuTorrent is
   deprecated** as a separate controller; one controller (TrackMuleBB) covers all.
4. Per qBittorrentBB's core-vs-REST policy, orchestration the generic Arr/REST
   stack can express stays external; the Python controller owns only the
   cross-network (eD2K <-> BT) suite logic that no single client can.
5. The **cross-network metadata-fabric automation** (notes 1–6) is a
   **forward-only** experience (emulebb-rust + qBittorrentBB + TrackMuleBB). The
   frozen Windows bundle gives side-by-side dual management via the frozen
   aMuTorrent, **not** the new fabric.

## Decision (2026-06-20): the `0.8.*` program runs MFC modernization and the forward suite together

This refines the sequencing of the Decision (2026-06-15) without changing the
product roles. The plan is: **ship `0.7.3` eMuleBB MFC first, then start the
`0.8.*` program** — and that program runs MFC modernization **together with**
qBittorrentBB and TrackMuleBB (TrackMuleBB replacing aMuTorrent), with
emulebb-rust as the forward eD2K/Kad core TrackMuleBB drives.

1. **qBittorrentBB, emulebb-rust, and TrackMuleBB stay out of the entire `0.7.x`
   line** (RC3, stable `0.7.3`, and `0.7.x` maintenance). They are **part of the
   `0.8.*` program**, which begins after `0.7.3` ships — not "post-`0.8.*`" and not
   strictly after MFC `0.8.x` work. The `0.7.x` bundle is and remains MFC client +
   aMuTorrent + Arr plumbing, delivered by the Pages `install.ps1` thin wrapper
   over the release `Bootstrap-eMuleBBSuite.ps1`.
2. **The `0.8.*` program is a single concurrent wave** (operator decision
   2026-06-20): the revived `0.8.x` MFC modernization line (this reactivates the
   previously on-hold `0.8.0`; see
   [FUTURE-ROADMAP](FUTURE-ROADMAP.md#release-line-model)) **plus** qBittorrentBB,
   TrackMuleBB, and emulebb-rust. Order is: `0.7.x` maintenance → `0.8.*` program.
   Detailed `0.8.x` MFC lane content is still to be specified by the operator; do
   not infer it beyond the retained frozen-surface-removal plan.
3. **TrackMuleBB replaces aMuTorrent** as the suite controller in the `0.8.*`
   program; `uv` and the Python installer are part of that same program.
4. **aMuTorrent is not frozen yet.** Refining point 2 of the 2026-06-15 decision:
   aMuTorrent stays **unfrozen and actively maintained — kept up to date with
   upstream `got3nks/amutorrent` plus eMuleBB controller fixes and small
   improvements — until eMuleBB `0.7.3` final ships**. It freezes into
   sustainability maintenance (bug fixes only, superseded as forward controller by
   TrackMuleBB) **at `0.7.3` final**, not now.

## Naming (exact, do not conflate)

- **eMuleBB** = the **C++ MFC Windows desktop app** (`emulebb-main`). The current
  flagship eD2K/Kad client.
- **emulebb-rust** = the **Rust eD2K/Kad core** — headless, multiplatform. The
  strategic forward core (and the autonomous indexer of notes 13–15).
- **qBittorrentBB** = the BitTorrent-side client (fork) with the DHT harvester +
  Torznab index.
- **aMuTorrent** = the cross-network web-UI controller of the `0.7.3` line.
  **Actively maintained / upstream-synced until `0.7.3` final, then frozen**
  (sustainability only) — see Decision (2026-06-20). Superseded as the forward
  controller by the Python coordinator after `0.7.3` final.
- **TrackMuleBB** = the forward, capability-driven controller (Python-only,
  integrated web UI, no Node; repo `trackmulebb`). Drives any `/api/v1` core by
  advertised capability (emulebb-rust full, eMuleBB MFC frozen subset) + qBittorrentBB.
  Deprecates aMuTorrent as a separate controller.

## Freeze scope (read first)

The **eMuleBB (MFC) app** closes its `0.7.x` *feature* line at `0.7.3` and then
**continues in the revived `0.8.x` modernization line** — it is not a frozen
product. **aMuTorrent** is the only product that freezes: per Decision 2026-06-20
it stays **actively maintained and upstream-synced until `0.7.3` final**, then
enters sustainability maintenance (bug fixes only) and is replaced as the suite
controller by TrackMuleBB in the `0.8.*` program. See
[FUTURE-ROADMAP](FUTURE-ROADMAP.md) and [FROZEN-SURFACES](FROZEN-SURFACES.md). The
forward products — `emulebb-rust`, `qBittorrentBB`, `TrackMuleBB`,
`goed2k-server`, and the Python metadata-fabric tooling — are in **full
development mode, no limits**. This program (together with the `0.8.x` MFC
modernization) **is the `0.8.*` program; it begins after `0.7.3` ships**.

**eMuleBB 0.7.3 final scope:** the PowerShell suite bootstrap + local Arr
integration + aMuTorrent. That is the whole of it — **no further `0.7.x` feature
scope** (new MFC feature work resumes in the `0.8.x` modernization line).
**Forward eD2K/Kad direction:** alongside the `0.8.x` MFC modernization, the
strategic forward core is **emulebb-rust**. Consequently the metadata-fabric eD2K
integrations (notes 1/5/6) target **emulebb-rust's `emulebb-metadata` SQLite as
the primary** share/hash source; MFC `known.met` is a compatibility path only.

## Future suite bundle & three networks (decision 2026-06-16, deferred after 0.7.3)

After `0.7.3`, the suite grows into a **ready-to-use bundle** spanning **three networks** —
eD2K (emulebb-rust / eMuleBB MFC), BitTorrent (qBittorrentBB), Usenet (SABnzbd) —
plus the Arr automation stack, **Bountarr** (our household media-grab UI over
Radarr/Sonarr+Plex), and (Docker) Plex.

- **TrackMuleBB is the future single pane and installer.** Its Python setup CLI
  installs/auto-wires the bundle; its web UI is the runtime single pane (unified
  transfers/search, **dynamic global bandwidth coordination**, cross-network
  **dedup** via the equivalence map). The PowerShell one-liner becomes a **minimal
  bootstrap** only after the future installer is release-proven. Full design:
  [SUITE-INSTALLER](SUITE-INSTALLER.md).
- **Search** aggregates the clients natively (rust index + qBittorrentBB harvest,
  via a native path) plus **Prowlarr** for third-party/Usenet indexers, excluding
  the **tagged** TrackMuleBB indexers to avoid duplicates.
- **Phasing:** automate our components first (rust/MFC/qBittorrentBB/TrackMuleBB/
  Bountarr) + pre-configure base settings for the third-party stack; deeper
  third-party automation later. **Self-contained, no host interference**
  (uv-managed Python, Node only for Bountarr).

## North star

> A full, safe, peer-to-peer file-sharing suite for sharing professionals, with
> no strict reliance on eD2K servers or indexers — fully distributed, anonymous,
> multiplatform, and maximally automated.

Each clause is a load-bearing constraint, not a slogan:

- **Full suite** — integrated set, not isolated clients: eD2K/Kad client
  (`emulebb-rust`), BT client (`qBittorrentBB`), optional server
  (`goed2k-server`), indexers (Torznab/Prowlarr), Python tooling, and the
  **TrackMuleBB** controller. The notes 1–6 metadata fabric is what makes it a
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
Policy / orchestration ── TrackMuleBB controller (optional layer)        notes 6,16,17
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
  and **TrackMuleBB** drive rust exactly as they drive a qBittorrent (same pattern
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
- **TrackMuleBB suite automation** (notes 6, 16, 17): cross-network grab
  decisions, reconcile/orphan actuation, "download the torrent instead" handoff.
  Optional layer — clients + Prowlarr stay fully standalone. Design reference
  (carried over from aMuTorrent): `amutorrent/docs/SUITE-AUTOMATION.md`.

## Phase exit criteria (Definition of Done)

Each phase has a measurable, checkable DoD. A phase is "done" only when all its
criteria pass. Phase ↔ the board `Phase` field ↔ a release milestone are the same
axis: an item's `Phase` on the eMuleBB Suite board must match the phase it serves
here, and a phase closes a suite milestone.

**Phase 0 — emulebb-rust perfectly functional (gate for everything after):**
- [ ] Connects (server + Kad), handles HighID/LowID.
- [ ] Searches (server + Kad/global) and returns results.
- [ ] Downloads a file end-to-end from ≥3 real sources, including queue/reask with
      `enable_udp_reask` **on** and live-validated (`RUST-FEAT-001`).
- [ ] Uploads/shares and serves sources.
- [ ] **Network Safety green:** eD2K TCP egress pinned to the tunnel
      (`RUST-FEAT-003`) and the automated leak-test passes blocking (`RUST-FEAT-005`).
- [ ] Autonomous Kad/eD2K indexer populates the index and serves Torznab
      (`RUST-FEAT-002`).
- [ ] Arr drives rust as a qBittorrent download client (`RUST-FEAT-004`).
- [ ] CI quality bar green (clippy `-D warnings`, cargo-deny advisories,
      `kad_swarm` blocking or `RUST-BUG-001` resolved).

**Phase 1 — qBittorrentBB:**
- [ ] Branded idempotent export of non-private live torrents to the eD2K share
      (`QBBB-FEAT-001`).
- [ ] Harvested torrents persisted to the sharded local store (`QBBB-FEAT-002`).
- [ ] Indexer/Torznab parity with rust (`QBBB-FEAT-003`).
- [ ] **Network Safety green:** `vpnReady()` truly fail-closed + leak-test
      (`QBBB-FEAT-004`).

**Phase 2 — fabric + controller:**
- [ ] Python fabric produces reconcile/orphan reports + torrent⇄collection +
      `file_membership` (notes 1–6).
- [ ] TrackMuleBB actuates a cross-network intent handoff and acts on a fabric
      report (design captured in `AMUT-FEAT-001`/`AMUT-FEAT-002`), staying an
      optional layer.

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

- Close **eMuleBB (MFC) 0.7.3 final** (the `0.7.x` feature line): PowerShell
  bootstrap + local Arr + aMuTorrent. After `0.7.3` final, aMuTorrent freezes and
  the MFC continues in the `0.8.x` modernization line (part of the `0.8.*` program
  below).
- **Phase 0 — emulebb-rust** perfectly functional: enable UDP reask (FEAT-001),
  eD2K TCP VPN egress pin, download/upload parity hardening, the Kad/eD2K indexer,
  Arr surfaces. Tracked in `emulebb-rust/docs/active`.
- **Phase 1 — qBittorrentBB**: branded export, harvested disk store, indexer /
  Torznab parity. Tracked in `qbittorrentbb/docs/active`.
- **Phase 2 — metadata fabric + TrackMuleBB automation** (notes 1–6, 16–17).

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
| Broad modernization / restructure surveys (archived — MFC frozen) | `history/ideas/IDEA-MODERNIZATION-2026.md`, `history/ideas/IDEA-RESTRUCTURE.md` |
| A4AF cross-file source dedup (rust) | `emulebb-rust/docs/design/source-management-and-a4af.md` |
| TrackMuleBB owning all generic download rules (scope split) | `amutorrent/docs/SUITE-AUTOMATION.md` (frozen-aMuTorrent design reference) |

eMuleBB-MFC `FUTURE-ROADMAP.md` lanes (dark mode, IPv6 dual-stack, µTP, NAT-PMP,
etc.) are **parked-by-freeze**: `0.8.x` material only if the MFC app is not
retired in favour of emulebb-rust. **Exception (operator decision 2026-06-24):** the
first specified `0.8.x` MFC lane is now active — **Performance & Async** (fast
startup, networking + `Process()` off the UI thread), forward-porting the tested
`WSAPoll` network-thread migration from the `v0.72a-broadband-dev` lineage. See
`FUTURE-ROADMAP.md` and
[MFC-0.8.0-PERF-ASYNC-PLAN](plans/MFC-0.8.0-PERF-ASYNC-PLAN.md).

## Backlog & tracking structure

Decided + set up 2026-06-14:

- **Issues live in each product's own repo** (release-train correctness): rust →
  `emulebb/emulebb-rust`, qBittorrentBB → `emulebb/qbittorrentbb`. The local MD
  item under `docs/active/items` is the durable engineering spec; the GitHub issue
  owns workflow state (`workflow: github`).
- **One org board aggregates them:** **eMuleBB Suite**,
  `https://github.com/orgs/emulebb/projects/3`, with single-select fields
  `Product` (eMuleBB-MFC / emulebb-rust / qBittorrentBB / TrackMuleBB / aMuTorrent /
  tooling) and
  `Phase` (Phase 0/1/2). Phase 0 = rust issues #1–#4; Phase 1 = qBittorrentBB
  issues #1–#3.
- **The MFC `eMuleBB Roadmap` board (#2) stays as-is** for the frozen 0.7.x line;
  it is not polluted with forward work.
- **Parked ideas stay out of the tracker** — they remain `IDEA-*.md` and become
  backlog only when a slice is promoted.

**Approved but deferred migration — move the MFC backlog into the `emulebb`
repo.** The eMuleBB MFC app backlog currently lives in
`emulebb-tooling/docs/active/items` (a structural smell: the frozen app's backlog
sits in the tooling repo). The agreed end state is to move it into the `emulebb`
repo, leaving only cross-cutting/workspace items in `emulebb-tooling`. This is a
127-item cross-repo move that also rewires the GitHub sync (`github_roadmap_common.py`
`ACTIVE_ITEMS` path + the Project #2 linkage), so it must be a **focused, tested
migration**, not a blind bulk move. Deferred deliberately; do it as its own task.

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

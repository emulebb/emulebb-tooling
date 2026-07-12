# Suite Joint Roadmap (Rust-first forward program)

Status: planning / direction. This is the **canonical top-level roadmap** for the
BB suite after stable `0.7.3`. The current implementation focus is
**emulebb-rust**: stabilize the headless eD2K/Kad client and the Rust-native UI.
MFC is frozen on the `0.7.x` line. **qBittorrentBB** remains future companion
work, and **TrackMuleBB** is parked until qBittorrentBB progresses enough to
justify a cross-network controller. The MFC
[FUTURE-ROADMAP](FUTURE-ROADMAP.md) records retained ideas and any later MFC
decision. Companion governance:
[PRODUCT-PORTFOLIO](PRODUCT-PORTFOLIO.md), [QUALITY-GATES](QUALITY-GATES.md),
[API-V1-COMPATIBILITY](API-V1-COMPATIBILITY.md). It is **not** a `0.7.3` gate and
does **not** touch the shipping `0.7.x` MFC line.

## Decision (2026-07-12): rust headless + native UI is the active lane

The MFC roadmap is archived as **eMuleBB Roadmap MFC (archive)**. MFC `0.7.3`
and its matching aMuTorrent package are the shipped line; MFC accepts only
critical maintenance and non-behavior-expanding diagnostics/instrumentation. Do
not create or schedule MFC feature backlog by default.

Forward development concentrates on `emulebb-rust`: the headless client,
protocol parity/stability, persistence, safety gates, REST contract, and the
Rust-native UI in `emulebb-rust-ui`. The Suite board is the active cross-product
board, but only the Rust phase is active now.

`qBittorrentBB` is still the intended BitTorrent-side companion, but it is not
the current implementation priority. `TrackMuleBB` is on hold as a future
controller/integration layer; it should not be linked to MFC, and it should not
drive Rust beta scope until the qBittorrentBB side is ready to make a controller
useful.

## Decision (2026-07-05): focus rust and qBittorrentBB first

Superseded by the 2026-07-12 decision above. The useful part remains: stable
`0.7.3` promotes the MFC client into the frozen `0.7.x` compatibility line, and
larger eD2K/Kad evolution moves to `emulebb-rust`. The qBittorrentBB companion
track remains real future work, but it is no longer named as an equal current
focus beside Rust.

This supersedes the 2026-06-20 planning assumption that MFC `0.8.x` and the
forward suite begin together. A later explicit operator decision is required
before MFC `0.8.x` becomes active implementation work again.

## Decision (2026-06-15): forward stack supersedes the prior controller plan

This decision supersedes the earlier framing below where aMuTorrent was the
forward cross-network controller "in full development mode".

1. **eMuleBB (MFC) `0.7.3` is the final `0.7.x` feature release**. MFC `0.8.x`
   is not active; the 2026-07-12 focus decision puts near-term evolution on
   `emulebb-rust`. Through the `0.7.x` line the MFC app's
   package, delivered via the proven PowerShell suite bootstrap, bundles the MFC
   client, the frozen aMuTorrent `0.7.3` controller companion, and the Arr setup
   plumbing only. **qBittorrentBB, emulebb-rust, TrackMuleBB, `uv`, and the
   Python setup CLI are not in the stable `0.7.3` or `0.7.x` bootstrap**. The
   `0.7.x` bundle's eD2K side is the MFC client itself.
2. **aMuTorrent closes out on the `0.7.3` line** — it ships with the final MFC
   package and is **not** the forward controller. *(Timing refined by Decision
   2026-06-20 below: it stays actively maintained and upstream-synced until `0.7.3`
   final, and only then freezes into sustainability-only maintenance.)*
3. **The forward stack is staged, not concurrent**. `emulebb-rust` is active now
   and owns the forward eD2K/Kad client plus Rust-native UI. qBittorrentBB is
   later BitTorrent-side companion work. TrackMuleBB is parked future controller
   work and must not be wired into MFC or treated as Rust beta scope.
4. Per qBittorrentBB's core-vs-REST policy, orchestration the generic Arr/REST
   stack can express stays external; the Python controller owns only the
   cross-network (eD2K <-> BT) suite logic that no single client can.
5. The **cross-network metadata-fabric automation** (notes 1–6) is a future
   forward-only experience. It resumes only after the Rust client is stable and
   qBittorrentBB is active enough to make cross-network automation concrete.

## Historical Decision (2026-06-20): the `0.8.*` program ran MFC modernization and the forward suite together

This decision is superseded by the 2026-07-05 focus decision above. It refined
the sequencing of the Decision (2026-06-15) without changing the product roles.
The earlier plan was: **ship `0.7.3` emulebb-mfc first, then start the
`0.8.*` program** — and that program runs MFC modernization **together with**
qBittorrentBB and TrackMuleBB (TrackMuleBB replacing aMuTorrent), with
emulebb-rust as the forward eD2K/Kad core TrackMuleBB drives.

1. **qBittorrentBB, emulebb-rust, and TrackMuleBB stay out of the entire `0.7.x`
   line** (stable `0.7.3` and `0.7.x` maintenance). They are **part of the
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

- **eMuleBB** = the **C++ MFC Windows desktop app** (`emulebb-main`). The shipped
  `0.7.3` Windows client, frozen on the `0.7.x` line.
- **emulebb-rust** = the **Rust eD2K/Kad core** — headless, multiplatform. The
  strategic forward client, including the Rust-native UI work in
  `emulebb-rust-ui`.
- **qBittorrentBB** = the BitTorrent-side client (fork) with the DHT harvester +
  Torznab index. Future companion work, not the current implementation lane.
- **aMuTorrent** = the cross-network web-UI controller of the `0.7.3` line.
  Frozen with the MFC `0.7.3` release.
- **TrackMuleBB** = parked future controller work (Python-only, integrated web UI,
  no Node; repo `trackmulebb`). It is not linked to MFC and is not current Rust
  beta scope.

## Freeze scope (read first)

The **eMuleBB (MFC) app** closes its `0.7.x` *feature* line at stable `0.7.3`.
Further MFC evolution is not active; retained `0.8.x` ideas must not be treated
as implementation commitments without a later operator decision. **aMuTorrent**
freezes with `0.7.3`. See [FUTURE-ROADMAP](FUTURE-ROADMAP.md) and
[FROZEN-SURFACES](FROZEN-SURFACES.md). The active evolution track is
`emulebb-rust` headless + Rust-native UI. qBittorrentBB and TrackMuleBB are
future/parked tracks.

**eMuleBB 0.7.3 final scope:** the PowerShell suite bootstrap + local Arr
integration + aMuTorrent. That is the whole of it — **no further `0.7.x` feature
scope**.
**Forward eD2K/Kad direction:** the strategic forward client is
**emulebb-rust**. Its immediate scope is headless stability, safety, protocol
parity, persistence, REST, and Rust-native UI. Metadata-fabric integrations
remain future work.

## Future suite bundle & three networks (parked)

This remains the long-range direction, not current implementation scope. The
suite can later grow into a **ready-to-use bundle** spanning eD2K/Kad
(`emulebb-rust`), BitTorrent (qBittorrentBB), Usenet (SABnzbd), the Arr
automation stack, **Bountarr** (our household media-grab UI over
Radarr/Sonarr+Plex), and (Docker) Plex.

- **TrackMuleBB may become the future single pane and installer**, but it is on
  hold. Do not spend implementation effort there until qBittorrentBB is active
  and the cross-network workflow is concrete. Full design reference:
  [SUITE-INSTALLER](SUITE-INSTALLER.md).
- **Search** may later aggregate clients natively (rust index + qBittorrentBB
  harvest) plus **Prowlarr** for third-party/Usenet indexers.
- **Phasing:** stabilize Rust first; then revisit qBittorrentBB; then decide
  whether TrackMuleBB and the metadata fabric are justified.

## North star

> A full, safe, peer-to-peer file-sharing suite for sharing professionals, with
> no strict reliance on eD2K servers or indexers — fully distributed, anonymous,
> multiplatform, and maximally automated.

Each clause is a load-bearing constraint, not a slogan:

- **Full suite** — integrated set, not isolated clients: eD2K/Kad client
  (`emulebb-rust`), later BT client (`qBittorrentBB`), optional server
  (`goed2k-server`), indexers (Torznab/Prowlarr), Python tooling, and a possible
  future **TrackMuleBB** controller. The notes 1–6 metadata fabric is what would
  make it a *suite* rather than two unrelated clients.
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
- **Multiplatform** — the strategic reason the active program is Rust-first: the
  eD2K client future is portable `emulebb-rust`, not the Windows-only MFC app.
  The MFC app is the one Windows-only piece, and it is frozen out of this program
  by design.
- **Highest automation** — the controller plus report-only tooling plus
  autonomous indexing: the operator sets policy and the suite discovers,
  reconciles, downloads, shares, and bridges across networks unattended.

## Layered architecture

```
Policy / orchestration ── TrackMuleBB controller (parked optional layer)  future
Discovery / index ─────── rust Kad/eD2K indexer now; qBittorrentBB DHT     future
                          harvester + Prowlarr federation later
Clients / transport ───── emulebb-rust (eD2K/Kad) active; qBittorrentBB    Phase 0/1
                          (BT) later
Bridging / library ────── Python fabric + branded export + membership DB  future
Safety substrate ──────── VPN-fail-closed binding; harvested != shared    cross-cutting
```

## Deliverable ordering (strict, component-level)

The operator set a strict serial order at the component level:
**emulebb-rust headless + Rust-native UI → qBittorrentBB → TrackMuleBB/fabric**.

### Phase 0 — `emulebb-rust` headless + Rust-native UI (active gate)

"Perfectly functional" means the Rust daemon is credible as a real local eD2K/Kad
client and the Rust-native UI can operate it without depending on TrackMuleBB.

- Client parity: connect (server + Kad), search (server + Kad/global), download
  end-to-end from multiple sources including queue/reask, upload/share + serve
  sources.
- **Enable UDP source-reask (FEAT-001).** Code-complete off by default; remaining
  work is live validation (Rust↔Rust, then gentle Rust↔stock) before flipping
  `enable_udp_reask` on. See `emulebb-rust` `docs/design/udp-source-reask.md`.
- **Finish the VPN egress pin for eD2K TCP** (Kad UDP is done; eD2K TCP pending).
  Close the network-level anonymity guarantee.
- Rust-native UI: status, searches, transfers, uploads, shared files, server/Kad
  state, settings, logs, and diagnostics needed for daily operation.
- **Autonomous Kad/eD2K indexer** and Arr-facing surfaces remain tracked Rust
  capabilities, but they should not outrank core client stability and UI
  usability.

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

**Phase 0 — emulebb-rust headless + Rust-native UI (active gate):**
- [ ] Connects (server + Kad), handles HighID/LowID.
- [ ] Searches (server + Kad/global) and returns results.
- [ ] Downloads a file end-to-end from ≥3 real sources, including queue/reask with
      `enable_udp_reask` **on** and live-validated (`RUST-FEAT-001`).
- [ ] Uploads/shares and serves sources.
- [ ] **Network Safety green:** eD2K TCP egress pinned to the tunnel
      (`RUST-FEAT-003`) and the automated leak-test passes blocking (`RUST-FEAT-005`).
- [ ] Rust-native UI covers daily operation: status, searches, transfers,
      uploads, shared files, server/Kad state, settings, logs, and diagnostics.
- [ ] Autonomous Kad/eD2K indexer backlog is dispositioned against current beta
      scope (`RUST-FEAT-002`).
- [ ] Arr/qBittorrent-compatible surfaces are dispositioned against current beta
      scope (`RUST-FEAT-004`).
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

- **Phase 0 — emulebb-rust**: headless client stabilization, safety gates,
  protocol parity, persistence, REST correctness, release proof, and
  Rust-native UI. Tracked in `emulebb-rust/docs/active` and the Suite board.
- **MFC 0.7.x maintenance only**: critical fixes plus
  non-behavior-expanding diagnostics/instrumentation for the shipped `0.7.3`
  line. The MFC roadmap board is archive/provenance.

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
| qBittorrentBB branded export, harvested store, and Torznab parity | qBittorrentBB product backlog, to be reactivated after Rust stabilizes |
| TrackMuleBB controller and setup CLI | TrackMuleBB product backlog, to be reactivated only after qBittorrentBB progresses |

eMuleBB-MFC `FUTURE-ROADMAP.md` lanes (dark mode, IPv6 dual-stack, µTP, NAT-PMP,
etc.) are **parked-by-freeze**. The earlier 2026-06-24 Performance & Async lane
is now archived with the rest of the MFC `0.8.x` notes; it is not active
implementation work. See `FUTURE-ROADMAP.md` and
[MFC-0.8.0-PERF-ASYNC-PLAN](plans/MFC-0.8.0-PERF-ASYNC-PLAN.md).

## Backlog & tracking structure

Current structure after the 2026-07-12 cleanup:

- **Issues live in each product's own repo** (release-train correctness): rust →
  `emulebb/emulebb-rust`, qBittorrentBB → `emulebb/qbittorrentbb`, TrackMuleBB →
  `emulebb/trackmulebb` when reactivated. The local MD item is the durable
  engineering spec; the GitHub issue owns workflow state (`workflow: github`).
- **One org board aggregates them:** **eMuleBB Suite**,
  `https://github.com/orgs/emulebb/projects/3`, with single-select fields
  `Product` (eMuleBB-MFC / emulebb-rust / qBittorrentBB / TrackMuleBB / aMuTorrent /
  tooling) and
  `Phase` (Phase 0/1/2). Phase 0 is the active Rust lane. Phase 1/2 are future
  planning buckets until explicitly promoted.
- **The MFC `eMuleBB Roadmap MFC (archive)` board (#2)** is archive/provenance
  for the frozen MFC line; it is not used for forward work.
- **Parked ideas stay out of the tracker** — they remain `IDEA-*.md` and become
  backlog only when a slice is promoted.

**MFC backlog migration is no longer a forward requirement.** The MFC GitHub
backlog is closed and the Project #2 board is archived. Local MFC item files can
be retained as engineering/spec provenance unless a later archival cleanup moves
them under `docs/history`.

**Pending tooling task (not yet done):** generalize the GitHub sync scripts
(`emulebb-tooling/scripts/github_roadmap_common.py`, `github-roadmap-sync.py`,
`github-roadmap-check.py`) from their hardcoded single product
(`OWNER`/`ISSUE_REPO=emulebb/emulebb`/`PROJECT_TITLE=eMuleBB Roadmap`, scanning
only `emulebb-tooling/docs/active/items`) to a **per-product config** (repo +
items path + project + Product/Phase field mapping), so each product's
`docs/active/items` syncs to its own repo issues and onto the Suite board. This
mutates live GitHub state, so it needs its own focused, tested change — do not
bolt it on untested. Treat the existing Project #2 sync path as legacy MFC
archive tooling until generalized.

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

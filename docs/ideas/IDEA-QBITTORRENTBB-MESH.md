# IDEA: qBittorrentBB — A Forked BitTorrent Client For The BB Mesh

> **Exploratory proposal only.** Analysis and design exploration, not approved
> scope or a current branch direction. Nothing here is committed until a future
> active item promotes a specific slice. Captured 2026-06-13.

## Why this exists

Widen the org's blast radius beyond the eD2K/Kad world into BitTorrent by
standing up a **forked, full-fledged BT client** — `qBittorrentBB`, a fork of
[qbittorrent/qBittorrent](https://github.com/qbittorrent/qBittorrent) — that
gains two BB-specific capabilities:

1. **DHT indexing** — crawl the mainline BitTorrent DHT to build a torrent index
   and an `eD2K ↔ btih` content-equivalence map.
2. **eMuleBB REST coordination** — speak to eMuleBB over its existing REST
   surface so content can eventually be auto-shared across the two worlds in both
   directions.

The BT engine underneath is itself forked — see
[IDEA-EMULEBB-LIBTORRENT-FORK](IDEA-EMULEBB-LIBTORRENT-FORK.md) — so the indexing
hooks live in the engine, not bolted onto the client.

## Current ecosystem packaging note

The first promoted product-family step is narrower than the mesh idea in this
document: qBittorrentBB should become a Windows suite companion, optional in the
model but preselected for a normal local-machine `Full` install. The current
planning home for that packaging direction is
[ECOSYSTEM-SUITE-BOOTSTRAP-PLAN](../active/plans/ECOSYSTEM-SUITE-BOOTSTRAP-PLAN.md).
The DHT indexing and equivalence-map work below remains exploratory until a
separate active item promotes it.

## Relationship to IDEA-LIBTORRENT-MESH (deliberate divergence)

This **supersedes the "dual-network client" building block** of
[IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md), which argued for *embedding*
libtorrent headless inside `emulebb-rust` and explicitly warned against putting a
"Boost/libtorrent beast" inside a client. The operator has chosen the opposite
shape on purpose: a **standalone forked client** is the BT-side citizen of the
org, coordinated with eMuleBB over REST rather than fused into it.

Consequences of that choice:

- **`emulebb-rust` stays eD2K/Kad-focused.** It does **not** embed libtorrent.
  The BT stack's home is `qBittorrentBB` + the forked engine.
- The **content-mesh analysis** in `IDEA-LIBTORRENT-MESH` (the core obstacle,
  verify-don't-derive, surrogate overlay, v1/v2, determinism, honest ceilings)
  **still holds and is the theory base** for this work — only the *packaging*
  (where the engine lives) changes. Read that doc for the cryptographic framing;
  this doc is the product/integration shape.

## v1 scope — index/discovery ONLY

v1 is deliberately the *safe, no-transfer* slice. It builds knowledge, it does
not move bytes between networks.

**In scope:**

- **DHT crawl → torrent index.** Harvest from the mainline DHT
  (`get_peers`/`announce_peer` traffic + iterative lookups) a local index of
  `{ infohash, name, size, piece-length/layout, first-seen, last-seen,
  peer-count estimate }`. The harvesting seam comes from the forked engine, not a
  re-implemented DHT.
- **`eD2K ↔ btih ↔ v2-file-root` equivalence map.** Populated **only** by:
  - *Discovery* — reading a `TAG_BT_INFOHASH`-style tag published under a file's
    ed2k hash in Kad (the read side of the bridge described in
    `IDEA-LIBTORRENT-MESH` "Discovery via Kad"), and
  - *Verify-by-hash when bytes are already local* — if the client already holds
    the bytes, hash them against a candidate's piece hashes to confirm a mapping.
  - The map is **never derived** (`btih` is not computable from `ed2k`); unproven
    links are best-effort hints, ground truth is final hash verification.
- **Read-only surfacing.** Expose the index + map for query (local DB and/or REST)
  so other org components can consume it.

**Explicitly OUT of scope for v1** (future phases, each its own promotion):

- Joining or seeding real public swarms.
- The gateway / republisher (auto-generating canonical torrents for eD2K shares).
- Surrogate-overlay *transfers* (`H(ed2k)` as a `get_peers` accelerator).
- Mutable items (BEP 44/46) bridging.
- Any new BT extension wire protocol (BEP-10 equivalence gossip).

## eMuleBB REST coordination (reuse, don't rebuild)

eMuleBB already ships a comprehensive control surface — design against it, do not
invent a new one:

- **Native `/api/v1`** — `srchybrid/WebServer*.{h,cpp}` (default port 4711,
  `X-API-Key` auth): searches, shared-files, transfers, categories, and a `kad`
  publish/connect surface. Contract: `docs/rest/REST-API-CONTRACT.md` +
  `docs/rest/REST-API-OPENAPI.yaml`.
- **qBittorrent-compat `/api/v2`** — eMuleBB *already* answers a qBittorrent-shaped
  `/api/v2` (`srchybrid/WebServerQBitCompat.{h,cpp}`) for the Arr stack, and a
  **Torznab** indexer (`srchybrid/WebServerArrCompat.{h,cpp}`). It already knows
  how to round-trip a BTIH-shaped magnet carrying an `x.emulebb-ed2k` marker back
  to a native eD2K link.
- **qBittorrent's own WebUI `/api/v2`** on the BT side.
- **`amutorrent`** already brokers both worlds today
  (`server/modules/emulebbManager.js` talks `/api/v1`; it also drives qBittorrent).

### Coordination topology — OPEN QUESTION (document, don't decide)

How the two clients actually wire together is intentionally left open for a later
promotion. Candidates and trade-offs:

1. **Direct peer (embedded REST clients).** `qBittorrentBB` embeds an eMuleBB
   `/api/v1` client; eMuleBB reciprocally drives `qBittorrentBB`'s WebUI
   `/api/v2`. Simplest topology, no broker — but couples two release trains
   directly and splits the equivalence map's ownership.
2. **Dedicated bridge service.** A new headless coordinator (Rust) owns the
   equivalence index and brokers both sides. Cleanest separation and a single
   home for the map — at the cost of one more component to ship and operate.
3. **Extend amutorrent as broker.** Grow the existing unified manager (already
   fluent in both eMuleBB and qBittorrent) to host the auto-share/equivalence
   logic. Reuses a proven seam — but loads product logic into what is today a
   thin UI/controller fork.

No decision here. The v1 index/discovery slice can land behind any of these;
picking one is a promotion-time concern.

## Phasing

`v1 index/discovery` → (future) *verified equivalence at scale* (crowd-publish +
import of verified `ed2k ↔ btih` links) → (future, opt-in) *transfer bridging /
republish* into real swarms. Each step inherits the **honest ceilings** of
`IDEA-LIBTORRENT-MESH`: discovery getting easier never changes *who is on the
other end*; real interop needs content that exists on both networks, and coverage
of the long-tail eD2K-exclusive catalogue is the true limiter.

## Org integration (DEFERRED — gated on the RC2 freeze lifting)

> The workspace is in an **RC2 code soft freeze**; this whole initiative is
> post-0.7.3. The checklist below is recorded now and executed only once the
> freeze lifts and an active item promotes it. The fork mechanism is
> topology-driven, with `amutorrent` as the reference fork pattern.

1. **Register `qBittorrentBB`** as a `ManagedRepo` in `canonical_topology()`
   (`repos/emulebb-build/emule_workspace/topology.py`, `repos=()` tuple): org URL
   `emulebb/qbittorrentbb`, `relative_path repos\qbittorrentbb`, `branch main`,
   `additional_remotes` → `AdditionalRemote("upstream",
   "https://github.com/qbittorrent/qBittorrent.git")`. Add to
   `SHARED_HOOK_REPO_NAMES` if it takes shared hooks.
2. **Register the engine fork** per
   [IDEA-EMULEBB-LIBTORRENT-FORK](IDEA-EMULEBB-LIBTORRENT-FORK.md).
3. **Materialize:** `python -m emule_workspace sync` (auto-clones, writes
   `workspaces\workspace\deps.json`).
4. **Build wiring** (`emule_workspace/build.py`): the engine fork builds as a
   CMake/Boost dependency; `qBittorrentBB` builds as a Qt + CMake app consuming
   it. All outputs land **only** under `%EMULEBB_WORKSPACE_OUTPUT_ROOT%` (never
   under `c:\prj`). MSVC v143, x64 + ARM64, no Win32. Every build goes through
   `python -m emule_workspace build …` — no ad-hoc MSBuild/CMake from a worktree.
5. **Fork hygiene:** add `fork-delta.json` + `AGENTS.md` to the fork
   (amutorrent precedent), plus a nightly upstream-rebase workflow analogous to
   amutorrent's `nightly-upstream.yml`.
6. **Release packaging** (`emule_workspace/release.py`): `qBittorrentBB` follows
   its **own independent release lifecycle** — **not** version-paired to eMuleBB
   (unlike amutorrent's `…-emulebb-v0.7.x` tags). It tags on its own train
   (e.g. `qbittorrentbb-vX.Y.Z`) and is **loosely coupled** to eMuleBB:
   compatibility is advertised via a supported REST/API-version *range*, not a
   lockstep tag. Artifacts are **unsigned**; ship ZIP + manifest + SBOM + SHA-256.
7. **Certification:** extend `test certification --profile fast` with a
   `qBittorrentBB` smoke (build-green + a REST handshake against eMuleBB) once it
   ships.

## Licensing & policy

- **qBittorrent is GPL-2.0** — compatible with the org's GPL-2.0 posture. The fork
  lives under the **emulebb** org. Keep the `LICENSE` as verbatim GNU GPLv2 text
  (any preamble/SPDX header makes GitHub report NOASSERTION).
- Artifacts are always **unsigned**; do not propose or enable code signing.
- Tracked text is **LF**; run `helpers/source-normalizer.py` on new files.
- No private data and no real media titles anywhere — synthetic placeholders only.

## Open questions to resolve at promotion (not now)

- Coordination topology (direct peer vs. bridge service vs. amutorrent).
- Where the equivalence index physically lives (`qBittorrentBB`-local SQLite vs.
  reuse `emulebb-rust`'s `emulebb-index` / `emulebb-metadata` SQLite store).
- ARM64 buildability of the Qt + Boost + libtorrent stack on the org toolchain.

## Relationship to other items

- BT-engine half: [IDEA-EMULEBB-LIBTORRENT-FORK](IDEA-EMULEBB-LIBTORRENT-FORK.md).
- Theory base / supersedes the "embed in emulebb-rust" packaging of
  [IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md).
- Connectivity context: [IDEA-NAT-TRAVERSAL-UTP](IDEA-NAT-TRAVERSAL-UTP.md).

# IDEA: emulebb-libtorrent — A libtorrent Fork Tuned To The BB World

> **Exploratory proposal only.** Analysis and design exploration, not approved
> scope or a current branch direction. Nothing here is committed until a future
> active item promotes a specific slice. Captured 2026-06-13.

## Why this exists

[qBittorrentBB](IDEA-QBITTORRENTBB-MESH.md) needs a BitTorrent engine, and v1
wants the engine to do two things stock
[arvidn/libtorrent](https://github.com/arvidn/libtorrent) does not expose
cleanly. Rather than vendor upstream untouched and fight it from the outside, we
**fork it** — `emulebb-libtorrent` — and keep the fork delta deliberately small,
small enough to rebase on upstream regularly (the `amutorrent` model).

This is the engine half of the BT initiative; the client/integration half is
[IDEA-QBITTORRENTBB-MESH](IDEA-QBITTORRENTBB-MESH.md).

## Why fork (the v1 deltas)

1. **DHT indexing hooks.** An observation/callback seam over the mainline DHT —
   inbound `get_peers` / `announce_peer` traffic and the routing-table churn — so
   a crawler can **harvest infohashes + contacts** to feed the
   [qBittorrentBB](IDEA-QBITTORRENTBB-MESH.md) index *without re-implementing the
   DHT*. Stock libtorrent runs the DHT for its own peer discovery and does not
   surface this stream as a first-class, low-overhead tap. The fork adds the seam
   (read-only observation; it must not change DHT wire behaviour or make the node
   a worse mainline citizen).
2. **Param tuning for the BB workload.** Tuned defaults (DHT bootstrap/announce
   cadence, routing-table sizing, query concurrency, queue/rate logic) suited to
   an indexing-heavy node rather than a single-torrent leecher. Defaults only — no
   protocol change.

Keeping these *in the engine* (not bolted onto the client) means the hooks sit
where the DHT actually lives, and `qBittorrentBB` consumes a clean engine API.

## Explicit non-goals for v1

- **No new BT extension protocol.** BEP-10 equivalence gossip (clients exchanging
  verified `ed2k ↔ btih` mappings peer-to-peer) is a compelling *future* item, but
  v1 is index/discovery only — no new wire messages.
- **No transfer-path changes** beyond the tuned parameters above. No custom piece
  selection, no surrogate-hash transfer, no republisher.
- **No protocol fork.** The fork stays wire-compatible with the public network;
  the deltas are an observation seam + defaults, nothing a remote peer can detect.

## Hybrid v1 + v2 (recorded for future scope)

From [IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md): libtorrent generates
**hybrid v1+v2 torrents natively**, and BT v2's per-file SHA-256 merkle roots are
the clean content-addressed per-file identity that makes *verify-by-hash* exact
even inside multi-file torrents. That is the right foundation for the future
verified-equivalence and canonical-generation phases — **but it is not v1 scope**.
v1 only *reads* the DHT and *verifies when bytes are already local*; it does not
generate or seed canonical torrents.

## Fork hygiene

Mirror the `amutorrent` fork discipline so upstream rebases stay conflict-driven,
not memory-driven:

- **`fork-delta.json`** (analogue of `repos/amutorrent/fork-delta.json`): record
  the `upstream` remote + base tag, and classify every touched path as
  `forkOwned` (the DHT-hook seam, tuned-default config), `sharedSeams`, or
  `upstreamOwned`. The goal is a *tiny* `forkOwned` set.
- **`AGENTS.md`**: local guidance for working in the fork (where the hook seam is,
  what must never diverge from upstream, how to validate).
- **Nightly upstream-rebase workflow** analogous to amutorrent's
  `.github/workflows/nightly-upstream.yml`: check `upstream/main` (or the tracked
  release tag), rebase a sync branch, build, and only advance on green.

## Org integration (DEFERRED — gated on the RC2 freeze lifting)

> Recorded now, executed only post-0.7.3 once an active item promotes it.

- **Register as a third-party `ManagedRepo`** in `canonical_topology()`
  (`repos/emulebb-build/emule_workspace/topology.py`, `third_party_repos` tuple),
  `relative_path repos\third_party\emulebb-libtorrent`, with an
  `UpdatePolicy(upstream_url="https://github.com/arvidn/libtorrent.git",
  tracking_mode="tag", baseline_ref=<pinned tag>, version_pattern=…)` — the same
  shape as the other `repos\third_party\emulebb-*` deps (mbedtls / zlib pattern).
  It is a **dependency** of `qBittorrentBB`, not a standalone app.
- **Build** as a CMake/Boost dependency through `python -m emule_workspace build`;
  outputs land only under `%EMULEBB_WORKSPACE_OUTPUT_ROOT%`. MSVC v143, x64 +
  ARM64, no Win32.

## Licensing & policy

- **libtorrent is BSD-3-Clause** — compatible with the org's GPL-2.0 posture
  (BSD-3 code links cleanly into a GPL-2.0 program). Preserve the upstream BSD-3
  `LICENSE` and copyright notices in the fork; do not relicense upstream files.
- Artifacts are always **unsigned**; do not propose or enable code signing.
- Tracked text is **LF**; honor upstream's own normalization where it differs and
  keep the fork delta minimal.

## Relationship to other items

- Client / integration half:
  [IDEA-QBITTORRENTBB-MESH](IDEA-QBITTORRENTBB-MESH.md).
- Cryptographic / content-mesh theory base:
  [IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md).

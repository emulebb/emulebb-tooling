# Suite Metadata Fabric (notes 1–6)

Status: design / direction. Captured 2026-06-14. Post-0.7.3; full development
mode. Part of the [Suite Joint Roadmap](SUITE-JOINT-ROADMAP.md), Phase 1–2.

The metadata fabric is a disk-grounded, hash-keyed layer that makes torrents,
eMule collections, and eD2K shares **interconvertible views of the same files on
disk**, all cross-referenced by one parseable tag convention. It is built mostly
as a **report/produce-only Python tooling package**; clients read what it writes,
and the controller (`amutorrent`) actuates.

## Naming (exact)

**eMuleBB** = the C++ MFC desktop app. **emulebb-rust** = the Rust eD2K/Kad core.
Where this doc says "the eD2K share" or "the eD2K shared-hash DB," the **primary
target is emulebb-rust's `emulebb-metadata` SQLite** (the strategic forward core;
emulebb-mfc `known.met` is a compatibility path only). "eMuleBB stack" below means
whichever eMule-family core is active, named `emulebb` in suite config.

## Foundational invariants

- **Disk is the pivot.** A BT `infohash` cannot be derived from an eD2K hash or
  vice-versa (different hash functions over the same bytes). The bytes on disk are
  the only bridge. Every converter is therefore "given files-on-disk described in
  format X, also describe them in format Y."
- **Two keys:** BT `infohash` and eD2K hash.
- **Two strictly separate libraries:**
  - **Live / shared library** — only your own qBittorrentBB torrents. Branded,
    exported, and offered through the eMuleBB stack.
  - **Harvested library** — the DHT firehose persisted locally for reconciliation
    only. **Never shared, never branded, never exported.**
- **One parseable tag.** A stable `bb:` key=value convention stamped into torrent
  comments and collection names, e.g.
  `<configured brand> — <configured website>  [bb:v=1;k=<infohash>;src=qbbb]`.
  `comment`/`created by` live *outside* the torrent `info` dict, so stamping them
  never perturbs the infohash and never splits swarms. `v=` pins the schema so
  the tag can evolve. One parser serves the whole suite.

## Note 1 — Idempotent branded export (qBittorrentBB → eMuleBB)

Export every **non-private** (`info.private != 1`) torrent in the live library to
a canonical `.torrent` in a user-data export library (sibling to shared files,
**not** build output), stamped with the parseable branded comment, and surfaced
through the eMuleBB shared path so the underlying files are hashed and offered on
eD2K/Kad.

- **Format is preserved, never converted.** v1 stays v1; v2/hybrid stays as-is.
  The exporter is a *materializer*, not a converter. (Torrents authored from
  scratch — note 11 — may default to v2; that is a separate path.)
- **Idempotent** by two layers: skip-by-identity (target exists and infohash
  matches → no-op) and deterministic bencode serialization (sorted keys, fixed
  `created by`, pinned/omitted `creation date`, stable `comment`). Only a real
  metadata change rewrites a file, keeping reconciliation churn-free.
- **Machine-parseable comment** is the join key for the whole fabric.
- Owner: qBittorrentBB. See `qBittorrentBB` `docs/BB-TORRENT-EXPORT-AND-HARVEST.md`.

## Note 2 — Disk⇄torrent reconciliation (autotorrent-style)

Walk the **export (live) library** + operator base paths and produce a
**present / partial(n/m) / missing** report per torrent, keyed on infohash.
**Report-only**, **seed in-place** (no link farm).

- Library scope is **our own exported torrents only** — so the matcher's primary
  path is the fast identity path (the `bb:` tag), not autotorrent's brute-force
  size/hash ladder. (Foreign-torrent cross-seed matching is out of scope; can be
  added later.)
- Matching ladder for verification: exact (path+size) → size+name anywhere → hash
  (always definitive for v2 via per-file root). v1 falls back to size+name +
  optional piece verification.
- No actions taken; adding/seeding decisions belong to `amutorrent`.

## Note 3 — Persist harvested torrents to disk (sharded)

When the DHT harvester obtains full metadata for an infohash, also serialize
`torrent_file()` → bencode → write a `.torrent` into a **sharded local store**:

```
harvested/<aa>/<bb>/<infohash>.torrent
```

`aa`/`bb` = first two hex byte-pairs of the infohash (git-object / magnetico
fan-out). The path is a pure function of the infohash, so tooling derives it
arithmetically. Persist **all** full-metadata torrents (they are a few KB each).
Record the on-disk path back in the harvester SQLite row.

- **Strictly local and separate from the live/shared library.** Harvested
  torrents are an index + reconciliation input only; their contents are untrusted
  and are never shared, branded, or exported.
- Owner: qBittorrentBB harvester.

## Note 4 — Orphan / mixed-content scan

The inverse of note 2, from the same single scan: which files under the base
paths belong to **no live torrent**. **Strict accounting — all files count** (no
whitelist; `.nfo`, subtitles, artwork, `Thumbs.db`, everything). Report-only.

- Per-file orphan list + **per-directory rollup** (the real signal: a directory
  that mixes seeded and non-seeded files is flagged as mixed-content).
- **Harvest cross-check:** an orphan file that matches a *harvested* torrent's
  file entry is tagged `orphan→harvest-matched` — high-value "you are holding the
  data for a torrent you have indexed but are not seeding; adopt it."
- So orphans split into `orphan` (true stray / mixed content) and
  `orphan→harvest-matched` (adoptable data).

Notes 2 + 4 are one indexing pass (live torrent index + harvested index + disk
walk) producing three correlated reports.

## Note 5 — Torrent ⇄ eMule collection converters (both directions)

An `.emulecollection` is a small binary eD2K structure: version + optional name +
per-file (ed2k hash, filename, size). Converters are symmetric and both require
**files on disk** (disk is the pivot):

- `torrent → collection`: torrent file list ⋈ ed2k hashes → `.emulecollection`.
- `collection → torrent`: files a collection references (resolved to disk paths)
  → `create_torrent` → `.torrent`.
- **ed2k hashes** come from a **join with recompute fallback**: read from the
  active core's shared-hash store (primarily emulebb-rust `emulebb-metadata`; MFC
  `known.met` as compat) when the file is already shared (note 1), recompute from
  disk bytes otherwise.
- Collection name carries the suite brand **and** a parseable tag back to the
  source torrent infohash (and the created torrent's comment references the
  source); exact tag schema TBD but extends the `bb:` convention.

## Note 6 — File→torrent membership ("download the torrent instead")

Persist the note-5 join as a membership relation in the eMuleBB shared-files
metadata DB and surface it in the clients:

```
file_membership(ed2k_hash, torrent_infohash, file_index, torrent_name,
                file_count, total_size, first_seen_ms, last_seen_ms)
```

- **`file_membership` IS the local `eD2K ↔ btih ↔ v2-file-root` equivalence map**
  from [IDEA-LIBTORRENT-MESH](../ideas/IDEA-LIBTORRENT-MESH.md), populated the
  "verify, don't derive" way: a BT infohash is never computed from an ed2k hash;
  the link is proven by hashing the bytes that are local (the torrent's files on
  disk) — which is exactly what notes 2/5 already do. Treat this table as that
  map's local store, not a second parallel structure.
- **TrackMuleBB search dedup consumes this map** as the **authoritative** source:
  cross-network results (an eD2K hit and a BT hit for the same content) **merge**
  into one row when the map relates them; unmapped results fall back to **exact
  file size + normalized name** (non-destructive — the user can expand the merged
  group). See [SUITE-INSTALLER](SUITE-INSTALLER.md) and the TrackMuleBB backlog.
- Many-to-many (one file can belong to several torrents → the offer may present
  several options).
- **Live-library torrents only.** "Download the torrent instead" only ever offers
  real, reachable, branded torrents; harvested torrents never generate an offer.
- UX: on a search result / file detail, if membership rows exist, show "part of N
  torrent(s): <name> (M files, S total)" with a **get-the-torrent** action.
- **Handoff routes through `amutorrent` when present**, degrading to direct-to-
  client when it is not. The client emits an *intent* ("user wants infohash X");
  the controller actuates. Tooling writes `file_membership`; the C++/rust clients
  read it. See `amutorrent` `docs/SUITE-AUTOMATION.md`.

## Where the tooling lives

A Python package in the suite tooling (sibling to `emule_test_harness` /
`emule_workspace`). One scan builds the indexes; multiple reports/products come
out of it. It reads the export library, harvested store, eMuleBB shared-files DB,
and operator base paths; it talks to qBittorrentBB and eMuleBB over their REST/API
surfaces only for reads. All side effects are deferred to the controller.

## Policy

- Brand string + website are operator config, never hardcoded.
- User data path for libraries; never build output, never committed.
- No private data, no real media titles — synthetic placeholders only.
- Tracked text is LF; run `helpers/source-normalizer.py` on new files.

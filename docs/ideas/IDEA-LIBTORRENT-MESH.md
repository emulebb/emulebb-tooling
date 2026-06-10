# IDEA: libtorrent As Transport + eD2K↔BitTorrent Content Mesh

> **Exploratory proposal only.** Analysis and design exploration, not approved
> scope or a current branch direction. Nothing here is committed until a future
> active item promotes a specific slice. Captured 2026-06-10.

## Why this exists

Alternative to hand-porting NAT-T/µTP (see
[IDEA-NAT-TRAVERSAL-UTP](IDEA-NAT-TRAVERSAL-UTP.md)): instead of building the
connectivity stack, **reuse libtorrent-rasterbar** (uTP, Mainline DHT, NAT-PMP/
UPnP, hole-punching, IPv6, PEX, LSD, encryption) and bridge it to eD2K. The
ambition: real interoperability with the existing BitTorrent ecosystem, not an
eMuleBB-only island.

## The core obstacle (and the unlock)

- BitTorrent finds peers by **infohash** = `SHA1(info-dict)` (v1) or
  `SHA-256(info-dict)` (v2). The info-dict contains the **piece hashes**, so the
  infohash is bound to content via hashes that require the **bytes**.
- An eD2K downloader has the **ed2k MD4** but not the bytes, and there is no
  relation `BT-hash(content) ← MD4(content)`. So it **cannot derive** a file's
  public infohash. This is why naive "generate a torrent per file" stays an
  island.

**The unlock — verify, don't derive.** Stop trying to compute the public
infohash. Instead **discover** candidate public infohashes (torrent search /
DHT crawl by name+size, or a user-pasted magnet) and **verify** by hashing the
bytes you already have against the candidate's piece hashes. A match
cryptographically proves `ed2k_hash ↔ btih`, and you **join the real public
swarm** — interoperating with qBittorrent/Transmission/etc. directly. BT v2's
per-file merkle root makes this exact even inside multi-file torrents.

## Building blocks

1. **Dual-network client** — embed libtorrent as a first-class engine. eMuleBB
   joins the real mainline DHT and real swarms; magnets/`.torrent` work natively;
   instant interop with all BT clients; free uTP/NAT/IPv6/hole-punching. A
   download has two source networks.
2. **Content-equivalence bridge** — a verified `ed2k ↔ btih ↔ v2-file-root`
   graph, populated by (a) **search + content-verify** (the unlock above) and
   (b) **crowd-publish + import** (clients holding both identities publish the
   *verified* equivalence; seed from public hash databases).
3. **Gateway / republisher** — auto-generate **canonical** torrents for eD2K
   shares (lazy + cached hashing) and seed them on the public DHT, registering
   the magnet. Creates new public swarms so any BT client can fetch eD2K-origin
   content. Opt-in (legal/exposure).
4. **Surrogate overlay** — `surrogate = H(ed2k_hash)` used as an additive
   `get_peers` **discovery key** (not a transfer infohash), as an eMuleBB-only
   acceleration layer and a LowID↔LowID win. Robust because `get_peers` is a set
   (peers can be added, not erased).

## Discovery via Kad (the cleanest bridge)

Publish the BT infohash as a **Kad metadata tag** under the file's ed2k hash
(e.g. `TAG_BT_INFOHASH`, optionally a piece-length tag and a "verified-public"
flag):

- **Keyed by exactly what the downloader has** (the ed2k hash) — learned in the
  *same* Kad source/note lookup, no derivation, no new infra, serverless.
- **Additive tag → compatibility-preserving.** Kad tag lists are already
  extensible and stock eMule/aMule ignore unknown tags, so this is *not* a Kad
  protocol fork (far friendlier than eMuleAI's opcode approach).
- **Scope honesty:** only eMuleBB clients read Kad; real torrent clients never
  touch it. The Kad tag is the eMuleBB-internal *map*; actual cross-client
  interop happens **in the BT swarm** once eMuleBB joins it. It is the discovery
  half — real interop requires the published btih to be a **verified public**
  infohash (block ② or ③), not an eMuleBB-canonical one.

## Surrogate hash and mutable items (why they only get you so far)

- **Surrogate `H(ed2k)`** works as a **DHT discovery key** (Kademlia is just
  key→peers) but **cannot be the transfer infohash** — BEP 9 metadata exchange
  verifies `SHA1(metadata) == infohash` and pieces verify against the real
  hashes, so a surrogate is rejected for transfer.
- **Mutable items (BEP 44/46)** can bridge a *computable* key (well-known
  eMuleBB pubkey + ed2k-derived salt) → the real infohash, over the public DHT.
  But any key derivable from a **public** value (the ed2k hash) implies the
  **write** capability is public too → the single-valued mutable item is
  **poisonable** (DoS/overwrite), so treat it as cache, layered over the additive
  surrogate `get_peers`, never as authority.
- **Ground truth = final MD4 (+ piece) verification.** Every cross-network link
  is best-effort; a wrong mapping wastes a connection, never corrupts.

## v1 vs v2

- **v2 (BEP 52):** per-file SHA-256 merkle roots = clean content-addressed
  per-file identity → exact content-matching even inside multi-file torrents. But
  the **swarm key is still the infohash**, still not ed2k-derivable.
- **v1:** transport/DHT/republish/surrogate all work the same, and v1 matches the
  *current* ecosystem (most public swarms are v1). The one loss: content-matching
  works cleanly only for **single-file** torrents; v1 multi-file packs have no
  per-file hash and pieces span file boundaries, so a single file inside a pack
  cannot be per-file verified/joined.
- **Hybrid v1+v2** is the best middle path: universal v1 compatibility **and** v2
  per-file matching; libtorrent generates hybrids natively.

## v1 out-of-hash metadata

Only the `info` dict is hashed. Outside it (`comment`, `created by`,
`creation date`, `announce`/`announce-list`, `url-list` web seeds, `nodes`) is
freely settable without changing the infohash — **but** magnet/DHT peers fetch
only the `info` dict (BEP 9), so those fields **do not propagate** across a swarm;
they exist only in the `.torrent` *file*. And you cannot move metadata *into*
`info` (e.g. an `ed2k` key) without changing the infohash and breaking
matching/determinism. So `comment` is useful only for **distributed `.torrent`
files / an index** (e.g. embed `ed2k:<md4>` + original name there), not for
swarm-wide publishing — for which a side channel (Kad tag / equivalence index)
is required.

## Determinism + cost control

- Canonical torrent generation (fixed piece length, `name = ed2k-hex`,
  single-file, fixed meta) → all seeders derive the **same** infohash, so the
  mapping/bridge is coherent.
- **Lazy hashing + cache:** never BT-hash all 50k shared files up front; hash a
  file once on first transfer/boost and cache `{ed2k → infohash, piece layout}`
  beside `known.met`. (Aside: eMule's AICH is an SHA-1 file tree, but different
  chunking, not reusable for BT piece/merkle hashes.)

## The "go big" combination

Stack **① + ② + ③** (phased **①→④→②→③**): eMuleBB becomes a **dual-network,
content-addressed mesh** where ed2k-hash, btih and v2-root are interchangeable,
verification-linked handles to the same bytes. Popular content fuses with the
massive public BT swarms (real interop); eD2K-exclusive content is republished
into BT or accelerated among eMuleBB peers via the surrogate overlay.

## Honest ceilings

- **Island unless verified/republished.** Discovery getting easier does not move
  *who is on the other end*; real interop needs content that exists/maps on both
  networks. The bridge's **coverage** is the real limiter (long-tail
  eD2K-exclusive files have no BT twin) — ② and ③ are the engines that grow it.
- **Seeder hashes once** (lazy + cache).
- **Legal/exposure** from republishing → opt-in, clearly surfaced.
- **Product identity / weight:** build in **`emulebb-rust`** (can host libtorrent
  or a Rust BT stack cleanly and speaks `/api/v1`); the MFC app just sees "more
  sources." Do not put a Boost/libtorrent beast in `srchybrid`.

## Relationship to other items

- Connectivity alternative to [IDEA-NAT-TRAVERSAL-UTP](IDEA-NAT-TRAVERSAL-UTP.md).
- Belongs to the emulebb-rust modernization line; controller/REST bridge to the
  desktop app.

# IDEA: Cooperative DHT — creative protocol-level cooperation between qBittorrentBB clients

> **Exploratory candidate set.** Captured 2026-06-14 from an operator design
> session. Nothing here is committed. This is the **menu** of mechanisms for
> notes 11–12 of the [Suite Joint Roadmap](../active/SUITE-JOINT-ROADMAP.md); a
> specific slice is chosen at promotion time. Theory base and packaging:
> [IDEA-QBITTORRENTBB-MESH](IDEA-QBITTORRENTBB-MESH.md) and
> [IDEA-LIBTORRENT-MESH](IDEA-LIBTORRENT-MESH.md).

## Framing

Cooperating clients are **instances of our own client** (qBittorrentBB, and by
extension the rust eD2K indexer where analogous), not adversarial strangers. They
can trust each other via a minted publisher key (note 11). The question: how do a
network of cooperating clients **collectively search and index** better than each
crawling the DHT blind — pooling work instead of duplicating it.

The baseline today: each harvester passively observes `get_peers`/`announce` +
actively BEP-51 samples + ephemeral BEP-9 metadata fetches → local SQLite. Every
node redundantly crawls the same DHT and fetches the same popular metadata.
Cooperation's job is to stop duplicating and start pooling.

## Boundary decision (operator, 2026-06-14)

**A libtorrent fork is on the table**, with a preference for **protocol-compliant**
extensions that degrade gracefully against non-cooperating clients, but openness
to more invasive ideas. Guiding principle: prefer mechanisms that are
**invisible/harmless to non-cooperating peers** (compliant extensions, gated by
the community key) so a fork never degrades participation in the public
DHT/swarm. This is broader than the "vanilla libtorrent + plugin" line assumed in
IDEA-QBITTORRENTBB-MESH; it supersedes that constraint for this idea.

## Note 11 — Publishing the whole library (the thing cooperation discovers)

BitTorrent's DHT finds peers for an infohash you already know; it has no native
"list everything this peer publishes." Bridge it with:

- **BEP-46 mutable DHT entry** under the operator's **minted publisher keypair**
  (ed25519). A `get` on the public key always returns the operator's *latest*
  library pointer, updatable without changing identity. DHT items are size-capped
  (~1 KB), so the entry is a **pointer**, not the catalog.
- The pointer resolves to a **catalog torrent** (v2/hybrid, so files are
  individually addressable and verifiable) enumerating the public library with
  `bb:` metadata. Regenerated deterministically (note-1 idempotence); re-`put`
  with an incremented sequence number.
- **Decisions:** mint a new publisher keypair (suite-wide identity, also backs
  note-6 provenance and optional collection signing; stored under the user data
  path, never committed). Public key is distributed **out-of-band** (the website
  the `bb:` comment already points to). Catalog granularity TBD — likely multiple
  options (whole-library for small operators; paged/sharded with the pointer
  resolving to an index-of-catalogs for large ones).
- libtorrent supports BEP-44/46 (`dht_put_item`/`dht_get_item`) and v2/hybrid
  creation stock — no fork needed for note 11 itself.

## Note 12 — Cooperation candidate set

The enabler for the deep wire-level plays: **custom BEP-10 extension messages**
(via libtorrent's plugin API, or a fork) let cooperating clients exchange
arbitrary messages over existing peer connections.

### A. DHT as a shared substrate (not just peer-finding)

1. **Rendezvous swarm = bulletin board.** All cooperating clients `announce` to a
   well-known derived infohash (`SHA1(community-key ‖ date)`, rotating). It maps
   to no real file — `get_peers` on it returns live cooperative membership.
2. **PEX solves trust-set discovery for free.** Once in the rendezvous swarm,
   PEX (BEP-11) gossips the entire membership — join one peer, learn all the
   others. Answers "how do nodes find each other" without a directory.
3. **DHT as a gossip key-value bus.** BEP-44 mutable items with `salt` as a
   multi-slot signed store under the community key: rotating "what's new" feeds,
   digests, etc. The DHT itself becomes shared storage.

### B. Peer-wire extension tricks (the deep layer)

4. **`bb_search` — federated keyword search over peer connections.** A query goes
   down the BT connection; each peer answers from its local SQLite. Real-time
   fan-out search at the wire layer, riding rendezvous-swarm connections — no
   HTTP/Prowlarr hop.
5. **Bloom-filter exchange of known infohashes.** Each node advertises a Bloom
   filter of every infohash it has metadata for. Before an expensive BEP-9 swarm
   fetch for H, check peers' filters; if a peer has H, pull the metadata blob
   directly from it. (v2: filter file-roots too.)
6. **Metadata-cache relay (BEP-9 generalized).** A custom extension lets peers
   serve metadata for **anything they have indexed**, seeding or not — the
   cooperative becomes a distributed magnetico cache; query a peer for H without
   touching the swarm. Likely the single biggest efficiency multiplier.
7. **Sample pooling (BEP-51 gossip).** Beyond directed `sample_infohashes` to
   swarm peers, gossip accumulated samples so each node sees a far wider slice of
   the DHT than its own vantage allows.

### C. Coordinator-free coordination

8. **Node-ID-locality keyspace partitioning.** Each node's random DHT node ID
   already places it in a keyspace region the DHT naturally routes to it. So each
   node deep-crawls / BEP-51-samples the region **near its own ID** (where it is
   the natural authority) and gossips results (A/B). The partition is *implicit in
   node-ID placement* — full DHT coverage with zero coordination, resolving the
   "partitioned crawl without a coordinator" problem. Best paired with a fork that
   exposes DHT internals (idea 11 below).

### D. v2-specific cooperation

9. **File-level cross-seeding.** v2 file-roots identify a *file* independent of
   its torrent. Cooperating nodes detect that a file in node-1's torrent A is
   byte-identical (same `file_root`) to a file in node-2's torrent B and serve
   pieces to each other's swarms at the file level — a shared CDN for any file any
   member holds, regardless of packaging.
10. **Dedup + verification of the gossip.** `file_root` lets a node verify content
    identity and dedupe the same file across many torrents — turning "a list of
    torrents" into a deduplicated, verifiable *file-level* index across the whole
    cooperative.

### E. Trust / anti-poisoning

11. **Reputation gossip.** Cooperating nodes share quality signals — which
    infohashes resolved to real, healthy, sane-metadata content (live swarm
    counts, file-list sanity) — so the pooled index is trustworthy in a way no
    single crawler can achieve.

### Fork-enabled additions

12. **Surface the peer's real BEP-5 DHT port** from the PORT message (libtorrent
    hides it today; directed BEP-51 sampling currently guesses the BT listen
    port). Higher-yield directed sampling. Already flagged in the harvester notes
    as the higher-yield vector.
13. **Direct DHT-internals infohash mining** — hook the routing table / incoming
    `get_peers` stream to harvest every infohash the node *observes being routed*,
    not just BEP-51 samples. Makes idea 8 (node-ID locality) fully real.
14. **Trusted-peer larger/full BEP-51 sample** — serve a larger or complete
    infohash list to authenticated cooperative peers (gated by the community key)
    while staying standard toward strangers. Protocol-compliant degradation.
15. **Custom DHT "list-near-K" query** (stretch) — a BEP-44-flavored extension on
    the DHT UDP socket, answered only by cooperating nodes. More invasive.

## Recommended creative core

1. Rendezvous swarm + PEX (membership/trust discovery) — #1, #2.
2. Metadata-cache relay + Bloom-filter exchange (eliminate redundant crawling) —
   #5, #6.
3. `bb_search` extension (real-time distributed search) — #4.
4. Node-ID-locality partitioning + sample pooling (coordinator-free coverage) —
   #7, #8, with fork ideas #12, #13.
5. v2 file-root dedup/verify + file-level cross-seed — #9, #10.

Anti-poisoning (#11) and the trusted-peer fork extensions (#14, #15) layer on
once the core proves out.

## App-layer complement (already mostly built)

Independently of the wire-level plays, cooperating operators can register **each
other's Torznab endpoints** in a shared Prowlarr for federated search — the
application-layer form of cooperation, available today via note-15 surfaces. The
wire-level set above is the *deeper* capability beyond that.

## Open questions at promotion

- Catalog granularity (whole-library vs paged/sharded index-of-catalogs).
- Which fork-enabled ideas justify the fork delta vs staying plugin-only.
- Trust-set bootstrap: manual key exchange vs emergent brand-discovery vs the
  rendezvous-swarm/PEX path (#2).

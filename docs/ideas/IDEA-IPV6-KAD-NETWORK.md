# Idea: IPv6-Native Kad Network

Exploratory idea material. This is not an active implementation plan, release
scope, or current product claim unless a future `docs/active/` item explicitly
promotes a specific slice.

## Summary

This note captures the future design space for a distinct IPv6 Kad network. It
is intentionally separate from
[FEAT-035](../active/items/FEAT-035.md), which covers dual-stack compatibility
for the current eD2K/Kad network.

The strongest external inspiration is qBittorrent's backend architecture:
qBittorrent uses libtorrent, and libtorrent follows the BitTorrent dual-stack
DHT model where IPv4 and IPv6 DHTs are distinct. BEP 32 describes separate IPv4
and IPv6 routing tables, generally with the same node ID, while libtorrent
persists separate DHT bootstrap state as `nodes` and `nodes6`.

References:

- [p2p-overlord KV6_001 Kad2 IPv6-compatible overlay design](https://github.com/p2p-overlord/p2p-overlord-agents/blob/develop/docs/kad/KV6_001_KAD2_IPV6_DESIGN.md)
- [BEP 32: IPv6 extension for DHT](https://www.bittorrent.org/beps/bep_0032.html)
- [libtorrent DHT reference](https://libtorrent.org/reference-DHT.html)
- [libtorrent DHT security extension](https://www.libtorrent.org/dht_sec.html)
- [libtorrent DHT extension surfaces](https://www.libtorrent.org/dht_extensions.html)
- [libtorrent settings reference](https://libtorrent.org/reference-Settings.html)

## Design Direction

If eMuleBB ever pursues an IPv6-native Kad network, the design should start
from explicit state separation. The p2p-overlord `KV6_001` design is the
strongest current external reference for this shape: keep legacy IPv4 Kad2 as a
separate overlay, add an IPv6-capable Kad2-derived overlay, and merge behavior
only above transport and routing.

| Concept | IPv4 Kad | IPv6 Kad |
|---|---|---|
| Logical role | `kad4`, the current public Kad network | `kad6`, a future IPv6-capable overlay |
| Routing table | current IPv4 contact space | separate IPv6 contact space |
| Bootstrap state | current `nodes.dat` family | separate `nodes6`-style state |
| Socket binding | IPv4 UDP endpoint | IPv6 UDP endpoint |
| Endpoint validation | IPv4 address and port | IPv6 address and port |
| Diagnostics | current Kad counters | separate IPv6 Kad counters |

The client may share one Kad node ID across address families unless a later
design proves that separate identities are safer for eMule Kad. That mirrors
the qBittorrent/libtorrent/BEP 32 pattern without copying BitTorrent DHT wire
semantics into eMule.

The important architectural distinction is one logical Kad service backed by
two family-local overlays:

- `kad4` remains byte-compatible with existing Kad2 peers and current eMule
  behavior
- `kad6` gets a family-correct IPv6 contact and packet model instead of
  overloading IPv4 fields
- search, publish, and result aggregation may be merged above the overlays,
  but routing, liveness, scoring, bootstrap, and reachability stay per-family

This is an idea boundary, not a current implementation commitment. Any
`kad6` wire shape must become a separate active item before code changes start.

## Compatibility Boundaries

This idea must not be implemented as a partial tag import.

Do not:

- bolt eMuleAI IPv6 publish/result tags onto the current IPv4-only Kad path and
  call the feature complete
- make new Kad tags mandatory for current public-network peers
- change current Kad opcode meanings, packet shapes, or publish/search
  semantics as part of ordinary compatibility work
- replace the existing IPv4 Kad network or make IPv4 peers second-class
- mix IPv4 and IPv6 bootstrap persistence in one opaque file format
- reinterpret classic Kad `uint32` contact fields as IPv6
- force legacy Kad2 peers to parse IPv6 contacts, capability flags, or
  family-mixed result lists
- merge IPv4 and IPv6 contacts into one routing table
- treat eMuleAI or NeoMule IPv6 peer/client tags as if they define a complete
  IPv6 Kad protocol

Do:

- keep IPv4 Kad fully usable
- keep IPv6 Kad state separately observable and separately recoverable
- use cross-family bootstrap hints only as hints
- keep steady-state lookups mostly same-family once the IPv6 table is healthy
- design migration, rollback, and diagnostics before implementation starts

## KV6_001 Reference Model

The p2p-overlord `KV6_001` design gives eMuleBB useful vocabulary for a future
native IPv6 Kad track:

- `kad4`: the existing Kad2 IPv4 overlay, unchanged on the wire
- `kad6`: a new IPv6-capable Kad2-derived overlay with explicit IPv6 contact
  encoding
- merged service layer: search, publish, and result presentation combine
  semantically equivalent data without mixing transport state

For eMuleBB, this means `kad6` should preserve Kad intent and state-machine
concepts where possible: bootstrap, hello, lookup, keyword search, source
search, notes search, publish, firewall checks, and callbacks. It should not
reuse legacy packet bodies when those bodies are structurally IPv4-shaped.

A future active design should choose an explicit packet family, such as
`KADEMLIA6_*` or a version-negotiated `KADEMLIA2_V6_*` family. The exact names
are placeholders here. The required property is that old `kad4` peers never
receive packet bodies that they could misparse as classic Kad2 packets.

## Future Contact And Identity Model

A plausible `kad6` contact model should carry at least:

- Kad node ID
- address family
- IPv6 address
- UDP and TCP ports
- Kad protocol or contact version
- UDP key or equivalent obfuscation metadata
- verification and reachability flags
- feature bits for optional `kad6` behavior

Use one logical Kad identity across both overlays by default:

- one user-visible Kad identity
- one search and publish key derivation model
- separate `kad4` and `kad6` endpoint presence
- separate routing tables, replacement caches, liveness, and firewall status

Separate node IDs remain an open question only if later eMule-specific evidence
shows that shared identity creates worse routing, privacy, or abuse behavior.

## Routing, Search, And Publish Guidance

Routing should remain XOR-based. The future change is routing ownership, not
the distance model:

- one routing table for `kad4`
- one routing table for `kad6`
- family-local contact scoring, replacement caches, and stale-contact handling
- endpoint-family validation before a contact can enter the matching table

Search should run as one logical operation above both overlays when both are
enabled:

- keep separate `kad4` and `kad6` frontier queues
- merge keyword results by file identity and useful metadata
- merge source results by file hash and endpoint
- preserve source-family provenance so diagnostics and UI can explain where a
  result came from
- avoid blind cross-family flooding once either routing table is healthy

Publish should also be per-overlay:

- publish IPv4-reachable sources through `kad4`
- publish IPv6-reachable sources through `kad6`
- keep acceptance, retry, and failure telemetry per family
- never project one family's public reachability onto the other

## Reachability And Admission

IPv4 and IPv6 reachability must be independent:

- IPv4 UDP reachable
- IPv4 TCP reachable
- IPv6 UDP reachable
- IPv6 TCP reachable

`kad6` should advertise a public IPv6 source or contact only when local policy
allows public participation and the address is suitable for public routing.
Global-scope IPv6 addresses should be preferred for public DHT participation;
temporary, tunnel, or ambiguous multi-homed addresses need explicit selection
and diagnostics before they become public Kad identity inputs.

Primary-table admission should stay conservative:

- validate that an endpoint matches the overlay family
- prefer verified contacts before promotion into the primary table
- suppress duplicate or family-confused contact intake
- detect prefix clustering and suspiciously convenient near-target placement
- keep reputation local; do not introduce shared global reputation

## qBittorrent/libtorrent Lessons

Use the qBittorrent/libtorrent model as architecture guidance, not as a wire
protocol template:

- separate routing tables avoid contaminating IPv4 reachability with IPv6
  assumptions
- separate persisted bootstrap pools let an IPv6 DHT recover independently
- cross-family bootstrap can help a new table start, but it should not erase
  family boundaries
- per-family diversity matters; libtorrent-style thinking around IPv4 `/24`
  and IPv6 `/64` diversity is a useful local-policy reference
- verified node-ID policy and strict routing-table admission are useful only
  when adapted to eMule Kad compatibility constraints

The BEP 32 idea that dual-stack nodes may use one ID while keeping two routing
tables is a useful default. Its `nodes`/`nodes6` split is also useful as a
conceptual guardrail: family-specific data can be exchanged deliberately, but
steady-state behavior should not erase the boundary between IPv4 and IPv6.

## Observability And Evidence

Promotion from idea to active implementation should require reusable evidence
before any public release claim:

- `kad4` parity evidence against stock/community Kad behavior
- internal `kad6` conformance scenarios for contact encoding, bootstrap,
  lookup, search, publish, and reachability
- packet-level captures or JSONL-style evidence for both overlays
- routing-table snapshots with family, bucket, score, and verification state
- search-frontier traces that show per-family fanout and stop conditions
- publish-acceptance traces that show per-family success and rejection patterns
- merged-result provenance so UI, logs, and support diagnostics can distinguish
  `kad4`, `kad6`, and dual-family results

Evidence must prove that `kad4` still behaves like classic Kad before any
`kad6` optimization is considered successful.

## Staged Promotion Path

A future active implementation should be split into narrow, reviewable slices:

1. Address and endpoint abstraction in the current app, with no wire change.
2. Family-aware reachability and diagnostics for sockets and bind selection.
3. Dual routing-table ownership, initially internal-only for `kad6`.
4. A written `kad6` wire/contact specification with fixtures before runtime
   interoperability work.
5. `kad6` bootstrap and hello on controlled peers.
6. `kad6` lookup, keyword/source/notes search, and merged result provenance.
7. `kad6` publish with family-aware acceptance and retry telemetry.
8. Protocol-safe quality improvements such as adaptive fanout, disjoint lookup
   scheduling, local scoring, duplicate suppression, and better stop
   conditions.
9. Live dual-stack evidence before release documentation can describe IPv6 Kad
   as available.

## Open Questions Before Promotion

Before this idea becomes an active item, answer these questions:

- Should eMuleBB share one Kad node ID across IPv4 and IPv6, or use separate
  IDs per address family?
- What is the on-disk format for IPv6 bootstrap state, and how is it rolled
  back independently from current `nodes.dat`?
- How are IPv6 Kad contacts discovered before the IPv6 table is healthy?
- Should cross-family bootstrap ever exchange contact hints, and if so how are
  those hints kept from becoming steady-state family mixing?
- What exact `kad6` packet family or version-negotiation shape keeps legacy
  peers safe from misparse?
- Which fields are mandatory in the `kad6` contact model, and which are
  feature-bit gated?
- Which eMuleAI IPv6 tags are useful only after end-to-end address consumers
  exist?
- Which diagnostics prove the IPv6 table is healthy without overclaiming
  compatibility with current IPv4 Kad?
- What parity evidence is required against the current public Kad network?
- What evidence is required before quality improvements, such as adaptive
  fanout or local scoring, can be applied to `kad4` without compatibility drift?

## Promotion Criteria

Promote this idea only after:

- [FEAT-035](../active/items/FEAT-035.md) has produced a stable address
  abstraction and dual-stack endpoint handling
- the current app can display, persist, copy, filter, and diagnose IPv6
  endpoints consistently
- a separate active item defines the IPv6 Kad state model, persistence, and
  validation plan
- a packet/contact specification exists for `kad6`, including fixtures and
  legacy-misparse safety rules
- parity evidence proves `kad4` remains stock-compatible after any shared
  routing/search/publish planner changes
- release docs explicitly classify the feature as experimental, opt-in, or
  release-bound with matching evidence

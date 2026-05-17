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

- [BEP 32: IPv6 extension for DHT](https://www.bittorrent.org/beps/bep_0032.html)
- [libtorrent DHT reference](https://libtorrent.org/reference-DHT.html)
- [libtorrent settings reference](https://libtorrent.org/reference-Settings.html)

## Design Direction

If eMule BB ever pursues an IPv6-native Kad network, the design should start
from explicit state separation:

| Concept | IPv4 Kad | IPv6 Kad |
|---|---|---|
| Routing table | current IPv4 contact space | separate IPv6 contact space |
| Bootstrap state | current `nodes.dat` family | separate `nodes6`-style state |
| Socket binding | IPv4 UDP endpoint | IPv6 UDP endpoint |
| Endpoint validation | IPv4 address and port | IPv6 address and port |
| Diagnostics | current Kad counters | separate IPv6 Kad counters |

The client may share one Kad node ID across address families unless a later
design proves that separate identities are safer for eMule Kad. That mirrors
the qBittorrent/libtorrent/BEP 32 pattern without copying BitTorrent DHT wire
semantics into eMule.

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

Do:

- keep IPv4 Kad fully usable
- keep IPv6 Kad state separately observable and separately recoverable
- use cross-family bootstrap hints only as hints
- keep steady-state lookups mostly same-family once the IPv6 table is healthy
- design migration, rollback, and diagnostics before implementation starts

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

## Open Questions Before Promotion

Before this idea becomes an active item, answer these questions:

- Should eMule BB share one Kad node ID across IPv4 and IPv6, or use separate
  IDs per address family?
- What is the on-disk format for IPv6 bootstrap state, and how is it rolled
  back independently from current `nodes.dat`?
- How are IPv6 Kad contacts discovered before the IPv6 table is healthy?
- Which eMuleAI IPv6 tags are useful only after end-to-end address consumers
  exist?
- Which diagnostics prove the IPv6 table is healthy without overclaiming
  compatibility with current IPv4 Kad?
- What parity evidence is required against the current public Kad network?

## Promotion Criteria

Promote this idea only after:

- [FEAT-035](../active/items/FEAT-035.md) has produced a stable address
  abstraction and dual-stack endpoint handling
- the current app can display, persist, copy, filter, and diagnose IPv6
  endpoints consistently
- a separate active item defines the IPv6 Kad state model, persistence, and
  validation plan
- release docs explicitly classify the feature as experimental, opt-in, or
  release-bound with matching evidence

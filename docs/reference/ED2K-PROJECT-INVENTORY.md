# eD2K Project Inventory

Last full verification: 2026-09-30

This inventory tracks active, stale, obscure, and historical projects around
eD2K, eDonkey2000, eMule, Kad, server software, controller tooling, protocol
libraries, and eMule mods.

It is a research index, not an endorsement list. Projects marked historical or
archive-only may still be valuable protocol and product references, but they
should not be treated as maintained dependencies without a fresh review.

The 2026-09-30 refresh rechecked every linked GitHub repository, canonical
workspace product status, current releases, repository redirects and archives,
eMule-Security live server-list metadata, and public searches for new eD2K/Kad
servers, clients, protocol libraries, bootstrap tools, and controllers. GitHub
counts are dated snapshots; release and commit dates are stronger maintenance
signals than stars alone.

The 2026-10-02 incremental update added `ModderMule/eNode-go`; it did not repeat
the full inventory audit.

The 2026-10-13 incremental update added `aria2-next`, `rmule`, `njMule`,
`macMule`, `p2pwatch`, and `hispamula-indexer`. It also rechecked repositories
with visible post-September activity and refreshed the materially changed
server, client, and controller entries below; it did not repeat the full
non-GitHub or archive audit.

The 2026-10-23 update refreshed `emulebb-rust`, `Ember-P2P`, `rucio`, the active
server implementations, and fast-moving controller entries. It added
`laurentgeynet-ux/eMule-Rust` plus a second discovery wave covering Gopeed,
FluxDown, Kelpie, AmuleD, Mulee, aMule Android, new aMule controllers, and new
protocol utilities. The review used date-bounded GitHub repository and code
searches, broader web searches, current default branches, releases, source
trees, and GitHub checks. It found no additional credible ED2K server daemon
beyond the server lines already listed below; it did not repeat every historical
archive or dead non-GitHub link. Every project status now follows the linked ranking methodology.

## Dashboard

The inventory contains **130 detailed entries** across nine categories. Each category link opens a ranked detail section; [methodology](ed2k-inventory/methodology.md) defines every status, adoption band, warning, and sort rule.

| Category | Entries | Status mix | Adoption mix | Brief snapshot |
|---|---:|---|---|---|
| [ED2K Server Software](ed2k-inventory/servers-and-bootstrap.md#ed2k-server-software) | 11 | 🟢 4 · 🟡 1 · 🟣 2 · ⚫ 4 | 🟢 0 · 🟡 1 · ⚪ 8 · ❔ 2 | Server implementations from experimental code to historical source. |
| [Server Lists And Bootstrap Infrastructure](ed2k-inventory/servers-and-bootstrap.md#server-lists-and-bootstrap-infrastructure) | 8 | 🟢 4 · 🟡 1 · 🟣 0 · ⚫ 3 | 🟢 2 · 🟡 2 · ⚪ 2 · ❔ 2 | Server-list services, harvesters, nodes.dat, and bootstrap guidance. |
| [Protocol References](ed2k-inventory/protocols-and-adjacent.md#protocol-references) | 4 | 🟢 0 · 🟡 1 · 🟣 0 · ⚫ 3 | 🟢 0 · 🟡 0 · ⚪ 0 · ❔ 4 | Historical protocol documentation and implementation references. |
| [Modern Clients, Forks, And Front Ends](ed2k-inventory/clients.md#modern-clients-forks-and-front-ends) | 34 | 🟢 16 · 🟡 11 · 🟣 1 · ⚫ 6 | 🟢 5 · 🟡 5 · ⚪ 19 · ❔ 5 | Current clients, rewrites, forks, wrappers, and front ends. |
| [Controllers, Indexers, And Automation](ed2k-inventory/controllers-and-indexers.md#controllers-indexers-and-automation) | 21 | 🟢 11 · 🟡 9 · 🟣 0 · ⚫ 1 | 🟢 0 · 🟡 4 · ⚪ 16 · ❔ 1 | Automation, Arr adapters, WebUIs, remotes, containers, and indexers. |
| [Protocol Libraries And Utilities](ed2k-inventory/libraries-and-utilities.md#protocol-libraries-and-utilities) | 18 | 🟢 4 · 🟡 10 · 🟣 1 · ⚫ 3 | 🟢 0 · 🟡 2 · ⚪ 13 · ❔ 3 | Reusable protocol libraries, diagnostics, hashing tools, and experiments. |
| [Adjacent Agent-Built P2P Watchlist](ed2k-inventory/protocols-and-adjacent.md#adjacent-agent-built-p2p-watchlist) | 4 | 🟢 0 · 🟡 3 · 🟣 0 · ⚫ 1 | 🟢 0 · 🟡 0 · ⚪ 4 · ❔ 0 | Clean-slate and adjacent P2P work outside confirmed stock behavior. |
| [Historical eMule Mods And Source Archives](ed2k-inventory/historical-and-archives.md#historical-emule-mods-and-source-archives) | 23 | 🟢 0 · 🟡 2 · 🟣 21 · ⚫ 0 | 🟢 0 · 🟡 0 · ⚪ 2 · ❔ 21 | Mod families, source mirrors, and incomplete historical evidence. |
| [Public Archive Collections](ed2k-inventory/historical-and-archives.md#public-archive-collections) | 7 | 🟢 2 · 🟡 1 · 🟣 4 · ⚫ 0 | 🟢 0 · 🟡 3 · ⚪ 2 · ❔ 2 | Public and local preservation collections. |

## Competitive Snapshot

| Project | Activity | Public adoption | Product maturity | Stock eD2K/Kad position | eMuleBB assessment |
|---|---|---|---|---|---|
| **emulebb-rust** | 🟢 Current; 2026-10-23 reviewed head | ⚪ 7 stars | Public beta with passing reviewed checks | Explicit stock-compatible forward client | Strongest fit with workspace policy and licensing; adoption and stable-release maturity remain behind established products. |
| **eMuleRust** | 🟢 Current; RC3 released 2026-10-17 | ⚪ 5 stars | Released candidate with broad project-authored tests | Targets eMule 0.72a behavior | Serious independent implementation and interoperability lead; still needs external traces, broader security automation, and gap closure. |
| **Ember P2P** | 🟢 Current; v1.7.4 released 2026-10-18 | ⚪ 31 stars | Packaged Rust/Tauri product | Mixes eD2K/Kad with an Ember-only DHT and peer-exchange opcode | Ahead in visible adoption and product polish, but its private extensions and remaining gaps make it a poor stock-default oracle. |
| **Rucio** | 🟢 Current; 0.49.0 released 2026-10-23 | 🟡 53 stars | Mature daemon/CLI/WebUI packaging | Separate libp2p network with a partial eMule bridge | Strong product and architecture reference, not a full eMule replacement; the bridge lacks major stock surfaces and uses GPL-3.0. |
| **FluxDown** | 🟢 Current; v0.6.1 released 2026-10-23 | 🟢 4,927 stars | Polished multi-platform downloader | Native eD2K download engine without upload/share contribution | Strategically important adoption threat, but 🔴 excluded from healthy-peer ranking because it is explicitly download-only. |

### How good are we?

**emulebb-rust** is competitive on policy alignment, stock-wire intent, reproducible multi-platform delivery, and reviewed CI health. It is not yet the adoption or release-maturity leader. Ember, Rucio, Gopeed, and FluxDown have stronger visible reach or packaging momentum; independent eMuleRust has a broader current release claim. Our strongest defensible position is disciplined stock compatibility and evidence quality. The largest gaps are public adoption, stable-release maturity, independently retained live interoperability evidence, and closure of the broader Client gate.

## Category Index

## ED2K Server Software

Server implementations from experimental code to historical source. **11 entries**; status mix 🟢 4 · 🟡 1 · 🟣 2 · ⚫ 4. [Open the ranked details →](ed2k-inventory/servers-and-bootstrap.md#ed2k-server-software)

## Server Lists And Bootstrap Infrastructure

Server-list services, harvesters, nodes.dat, and bootstrap guidance. **8 entries**; status mix 🟢 4 · 🟡 1 · 🟣 0 · ⚫ 3. [Open the ranked details →](ed2k-inventory/servers-and-bootstrap.md#server-lists-and-bootstrap-infrastructure)

## Protocol References

Historical protocol documentation and implementation references. **4 entries**; status mix 🟢 0 · 🟡 1 · 🟣 0 · ⚫ 3. [Open the ranked details →](ed2k-inventory/protocols-and-adjacent.md#protocol-references)

## Modern Clients, Forks, And Front Ends

Current clients, rewrites, forks, wrappers, and front ends. **34 entries**; status mix 🟢 16 · 🟡 11 · 🟣 1 · ⚫ 6. [Open the ranked details →](ed2k-inventory/clients.md#modern-clients-forks-and-front-ends)

## Controllers, Indexers, And Automation

Automation, Arr adapters, WebUIs, remotes, containers, and indexers. **21 entries**; status mix 🟢 11 · 🟡 9 · 🟣 0 · ⚫ 1. [Open the ranked details →](ed2k-inventory/controllers-and-indexers.md#controllers-indexers-and-automation)

## Protocol Libraries And Utilities

Reusable protocol libraries, diagnostics, hashing tools, and experiments. **18 entries**; status mix 🟢 4 · 🟡 10 · 🟣 1 · ⚫ 3. [Open the ranked details →](ed2k-inventory/libraries-and-utilities.md#protocol-libraries-and-utilities)

## Adjacent Agent-Built P2P Watchlist

Clean-slate and adjacent P2P work outside confirmed stock behavior. **4 entries**; status mix 🟢 0 · 🟡 3 · 🟣 0 · ⚫ 1. [Open the ranked details →](ed2k-inventory/protocols-and-adjacent.md#adjacent-agent-built-p2p-watchlist)

## Historical eMule Mods And Source Archives

Mod families, source mirrors, and incomplete historical evidence. **23 entries**; status mix 🟢 0 · 🟡 2 · 🟣 21 · ⚫ 0. [Open the ranked details →](ed2k-inventory/historical-and-archives.md#historical-emule-mods-and-source-archives)

## Public Archive Collections

Public and local preservation collections. **7 entries**; status mix 🟢 2 · 🟡 1 · 🟣 4 · ⚫ 0. [Open the ranked details →](ed2k-inventory/historical-and-archives.md#public-archive-collections)

## Research And Maintenance

- [Ranking, status, adoption, warning, and refresh methodology](ed2k-inventory/methodology.md)
- [Negotiated fast server publishing snapshot](ed2k-inventory/protocols-and-adjacent.md#negotiated-fast-server-publishing-snapshot)
- [Historical preservation ranking](ed2k-inventory/historical-and-archives.md)

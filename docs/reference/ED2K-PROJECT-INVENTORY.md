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

The inventory contains **130 detailed entries** across nine categories. Each category link opens a ranked detail section; [methodology](ed2k-inventory/METHODOLOGY.md) defines every status, adoption band, warning, and sort rule.

| Category | Entries | Status | Adoption |
|---|---:|---|---|
| [Servers](ed2k-inventory/SERVERS-AND-BOOTSTRAP.md#ed2k-server-software) | 11 | 🟢4 🟡1 🟣2 ⚫4 | 🟢0 🟡1 ⚪8 ❔2 |
| [Bootstrap](ed2k-inventory/SERVERS-AND-BOOTSTRAP.md#server-lists-and-bootstrap-infrastructure) | 8 | 🟢4 🟡1 🟣0 ⚫3 | 🟢2 🟡2 ⚪2 ❔2 |
| [References](ed2k-inventory/PROTOCOLS-AND-ADJACENT.md#protocol-references) | 4 | 🟢0 🟡1 🟣0 ⚫3 | 🟢0 🟡0 ⚪0 ❔4 |
| [Clients](ed2k-inventory/CLIENTS.md#modern-clients-forks-and-front-ends) | 34 | 🟢16 🟡11 🟣1 ⚫6 | 🟢5 🟡5 ⚪19 ❔5 |
| [Automation](ed2k-inventory/CONTROLLERS-AND-INDEXERS.md#controllers-indexers-and-automation) | 21 | 🟢11 🟡9 🟣0 ⚫1 | 🟢0 🟡4 ⚪16 ❔1 |
| [Libraries](ed2k-inventory/LIBRARIES-AND-UTILITIES.md#protocol-libraries-and-utilities) | 18 | 🟢4 🟡10 🟣1 ⚫3 | 🟢0 🟡2 ⚪13 ❔3 |
| [Adjacent P2P](ed2k-inventory/PROTOCOLS-AND-ADJACENT.md#adjacent-agent-built-p2p-watchlist) | 4 | 🟢0 🟡3 🟣0 ⚫1 | 🟢0 🟡0 ⚪4 ❔0 |
| [Historical Mods](ed2k-inventory/HISTORICAL-AND-ARCHIVES.md#historical-emule-mods-and-source-archives) | 23 | 🟢0 🟡2 🟣21 ⚫0 | 🟢0 🟡0 ⚪2 ❔21 |
| [Archives](ed2k-inventory/HISTORICAL-AND-ARCHIVES.md#public-archive-collections) | 7 | 🟢2 🟡1 🟣4 ⚫0 | 🟢0 🟡3 ⚪2 ❔2 |

## Competitive Snapshot

| Project | Activity | Adoption | Maturity | Compatibility |
|---|---|---|---|---|
| **emulebb-rust** | 🟢 2026-10-23 | ⚪ 7★ | Public beta | Stock target |
| **eMuleRust** | 🟢 RC3 | ⚪ 5★ | Release candidate | 0.72a target |
| **Ember P2P** | 🟢 v1.7.4 | ⚪ 31★ | Released | Private extensions |
| **Rucio** | 🟢 0.49.0 | 🟡 53★ | Released | Partial bridge |
| **FluxDown** | 🟢 v0.6.1 | 🟢 4,927★ | Released | 🔴 Download-only |

- **emulebb-rust:** strongest policy and licensing fit, but still behind on
  adoption and stable-release maturity.
- **eMuleRust:** serious interoperability lead whose broad claims still need
  independent traces and security hardening.
- **Ember P2P:** ahead in visible polish, but private extensions and remaining
  gaps make it a poor stock-default oracle.
- **Rucio:** strong product reference, not a full eMule replacement; its bridge
  omits major stock surfaces and uses GPL-3.0.
- **FluxDown:** major adoption threat, but excluded from healthy-peer rankings
  because it is explicitly download-only.

### How good are we?

**emulebb-rust** is competitive on policy alignment, stock-wire intent, reproducible multi-platform delivery, and reviewed CI health. It is not yet the adoption or release-maturity leader. Ember, Rucio, Gopeed, and FluxDown have stronger visible reach or packaging momentum; independent eMuleRust has a broader current release claim. Our strongest defensible position is disciplined stock compatibility and evidence quality. The largest gaps are public adoption, stable-release maturity, independently retained live interoperability evidence, and closure of the broader Client gate.

## Category Index

## ED2K Server Software

Server implementations from experimental code to historical source. **11 entries**; status mix 🟢 4 · 🟡 1 · 🟣 2 · ⚫ 4. [Open the ranked details →](ed2k-inventory/SERVERS-AND-BOOTSTRAP.md#ed2k-server-software)

## Server Lists And Bootstrap Infrastructure

Server-list services, harvesters, nodes.dat, and bootstrap guidance. **8 entries**; status mix 🟢 4 · 🟡 1 · 🟣 0 · ⚫ 3. [Open the ranked details →](ed2k-inventory/SERVERS-AND-BOOTSTRAP.md#server-lists-and-bootstrap-infrastructure)

## Protocol References

Historical protocol documentation and implementation references. **4 entries**; status mix 🟢 0 · 🟡 1 · 🟣 0 · ⚫ 3. [Open the ranked details →](ed2k-inventory/PROTOCOLS-AND-ADJACENT.md#protocol-references)

## Modern Clients, Forks, And Front Ends

Current clients, rewrites, forks, wrappers, and front ends. **34 entries**; status mix 🟢 16 · 🟡 11 · 🟣 1 · ⚫ 6. [Open the ranked details →](ed2k-inventory/CLIENTS.md#modern-clients-forks-and-front-ends)

## Controllers, Indexers, And Automation

Automation, Arr adapters, WebUIs, remotes, containers, and indexers. **21 entries**; status mix 🟢 11 · 🟡 9 · 🟣 0 · ⚫ 1. [Open the ranked details →](ed2k-inventory/CONTROLLERS-AND-INDEXERS.md#controllers-indexers-and-automation)

## Protocol Libraries And Utilities

Reusable protocol libraries, diagnostics, hashing tools, and experiments. **18 entries**; status mix 🟢 4 · 🟡 10 · 🟣 1 · ⚫ 3. [Open the ranked details →](ed2k-inventory/LIBRARIES-AND-UTILITIES.md#protocol-libraries-and-utilities)

## Adjacent Agent-Built P2P Watchlist

Clean-slate and adjacent P2P work outside confirmed stock behavior. **4 entries**; status mix 🟢 0 · 🟡 3 · 🟣 0 · ⚫ 1. [Open the ranked details →](ed2k-inventory/PROTOCOLS-AND-ADJACENT.md#adjacent-agent-built-p2p-watchlist)

## Historical eMule Mods And Source Archives

Mod families, source mirrors, and incomplete historical evidence. **23 entries**; status mix 🟢 0 · 🟡 2 · 🟣 21 · ⚫ 0. [Open the ranked details →](ed2k-inventory/HISTORICAL-AND-ARCHIVES.md#historical-emule-mods-and-source-archives)

## Public Archive Collections

Public and local preservation collections. **7 entries**; status mix 🟢 2 · 🟡 1 · 🟣 4 · ⚫ 0. [Open the ranked details →](ed2k-inventory/HISTORICAL-AND-ARCHIVES.md#public-archive-collections)

## Research And Maintenance

- [Ranking, status, adoption, warning, and refresh methodology](ed2k-inventory/METHODOLOGY.md)
- [Negotiated fast server publishing snapshot](ed2k-inventory/PROTOCOLS-AND-ADJACENT.md#negotiated-fast-server-publishing-snapshot)
- [Historical preservation ranking](ed2k-inventory/HISTORICAL-AND-ARCHIVES.md)

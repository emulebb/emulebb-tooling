# eD2K Servers and Bootstrap

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

Current and historical server implementations are separated from server-list and bootstrap infrastructure so protocol software is not confused with discovery data.

Ranking badges and thresholds are defined in [Methodology](METHODOLOGY.md). Statistics are dated snapshots, not live user counts.

## ED2K Server Software

Server software is listed separately from server lists. A server implementation
accepts eD2K/eMule client connections, handles login/search/source operations,
and may expose UDP status or admin APIs.

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| JEmuleServer | 🟢 Active/current | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-23 |
| eNode-go | 🟢 Active/current | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-23 |
| ed2k-server (Rust; formerly the unidentified `ed2k-rust` lead) | 🟢 Active/current | ⚪ Niche | Production-used MVP | Ecosystem dependency | 2026-10-20 |
| goed2k-server | 🟢 Active/current | ⚪ Niche | Active development | Ecosystem dependency | 2026-08-20 |
| satan-edonkey-server | 🟡 Verification needed | ❔ Unknown | Reference-only | Ecosystem dependency | Unknown |
| p2p-overlord ED2K server | 🟣 Archive/reference | ⚪ Niche | Reference-only | Historical reference | 2026-05-10 |
| ed2kd | ⚫ Stale/historical | ⚪ Niche | Stale | Historical reference | 2019-10-24 |
| gomule | ⚫ Stale/historical | ⚪ Niche | Stale | Historical reference | 2013-12-05 |
| eNode | ⚫ Stale/historical | 🟡 Visible | Stale | Historical reference | 2013-03-29 |
| ed2j | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2012-07-08 |
| Lugdunum eserver | 🟣 Archive/reference | ❔ Unknown | Reference-only | Historical reference | Unknown |

### Tier 2 — Active or maintained, niche adoption

#### JEmuleServer

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Server role**
- Status: 🟢 Active, experimental
- Language: Java
- Source or archive: https://github.com/dagga/JEmuleServer
- Repo stats (GitHub, 2026-10-23):
  - `dagga/JEmuleServer`: 5 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-23 `a74ebe3`; latest release `v1.2.23` on
    2026-10-23; GPL-3.0; all eight checks on the reviewed commit passed.
- Notes: Modern open-source eMule/eD2K server project. The README describes a
         Java 21 server with protocol obfuscation, compression, advanced search,
         large-file support, Lugdunum extensions, embedded H2 storage, LowID
         callbacks, fake-file filtering, admin CLI, and IPv6 support. Treat as
         a fresh research lead until protocol coverage and license fit are
         reviewed in code. Source review on 2026-10-13 found generic unknown
         login-tag handling and a flexible `OP_SERVERIDENT` tag list, but no
         `OP_OFFERFILES` batch/rate enforcement in `PublishHandler`; it must
         add matching enforcement before advertising faster pacing.

#### eNode-go

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Server role**
- Status: 🟢 Active, experimental
- Language: Go
- Source or archive: https://github.com/ModderMule/eNode-go
- Repo stats (GitHub, 2026-10-23):
  - `ModderMule/eNode-go`: 4 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-23 `a2ec654`; latest release `v0.5.0` on
    2026-10-23; MIT license; all three checks on the reviewed commit passed.
- Lineage: Fork of `zt8989/eNode-go` and a Go port of the original Node.js
  `eNode` server listed below.
- Notes: Implements TCP/UDP eD2K operations, protocol obfuscation, LowID
         callbacks, Lugdunum extensions, server gossip, optional IPv6 and NAT
         traversal, memory/MySQL/MongoDB storage, access filters, and a
         loopback-default admin dashboard. The repository has unit and
         Docker-backed database integration tests. Its current source already
         enforces per-session soft/hard offer limits and stores later batches
         cumulatively, but does not negotiate an `offerfiles_v` pace. It is
         maintained under the same `ModderMule` GitHub owner as eMule Qt, which
         its default server configuration also promotes. Treat the cross-server
         and IPv6/NAT extensions as research claims until independently tested
         against stock-compatible clients and servers.

#### ed2k-server (Rust; formerly the unidentified `ed2k-rust` lead)

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Production-used MVP** · **Ecosystem dependency** · **Server role**
- Status: 🟢 Active, production-used MVP
- Language: Rust
- Source or archive: https://github.com/andrey23127/ed2k-server
- Repo stats (GitHub, 2026-10-23):
  - `andrey23127/ed2k-server`: 31 stars, 5 forks, 2 open issues; default
    `master`; default-branch commit 2026-10-20 `d6cf5fb`; latest release
    `v0.9.83` on 2026-10-18; MIT license.
- Public network evidence: eMule-Security listed `ed2k-rust main server` in
  its 2026-09-29 snapshot. The repository's current VPS example seeds that
  endpoint, while a source comment records the earlier test-server address
  captured by this inventory in June. That evidence resolves the prior
  source-verification gap without assuming that GitHub ownership and public
  server operation are the same identity.
- Notes: Clean-room Linux server implementation with TCP and UDP search/source
         operations, server gossip, obfuscation, NAT traversal, opt-in IPv6,
         admin UI, IP filtering, and mandatory operator-supplied content
         filters. The reviewed `0.9.x` source implements the opt-in
         `offerfiles_v=1`
         login/`OP_SERVERIDENT` pacing negotiation, per-client enforcement,
         and global record-rate backpressure while leaving legacy clients
         unchanged. Its README calls the `0.9.x` line a production-used
         test/MVP; verify protocol behavior and operational claims
         independently before adopting it as an interoperability reference.

#### goed2k-server

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Server role**
- Status: 🟢 Active
- Language: Go
- Source or archive: https://github.com/chenjia404/goed2k-server
- Repo stats (GitHub, 2026-09-30):
  - `chenjia404/goed2k-server`: 6 stars, 3 forks, 1 open issue; default
    `master`; default-branch commit 2026-08-20 `a6dc0d6`.
- Notes: Go ED2K/eMule server built around `github.com/monkeyWie/goed2k`; implements
         login, status, message, ID assignment, offer files, search, search-more,
         source lookup, callbacks, JSON/MySQL/PostgreSQL catalog storage, and admin
         UI/API. Its current offer handler replaces the client's complete indexed
         set on every packet; negotiated
         multi-batch publishing would therefore discard earlier batches until
         cumulative per-session offer semantics are implemented.

### Tier 3 — Experimental or verification required

#### satan-edonkey-server

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Reference-only** · **Ecosystem dependency** · **Server role**
- Status: 🟡 Historical, needs verification
- Language: Unknown
- Source or archive: Historical references only
- Notes: Announced in 2007 as an alternative eDonkey server after major server
         shutdowns. Keep as a research lead until source or a trustworthy archive is
         found.

### Tier 4 — Stale or historical

#### p2p-overlord ED2K server

- Assessment: **🟣 Archive/reference** · **⚪ Niche** · **Reference-only** · **Historical reference** · **Server role**
- Status: 🟣 Historical, archive-only
- Language: Go
- Source or archive: https://github.com/p2p-overlord/p2p-overlord-ed2k-server
- Repo stats (GitHub, 2026-05-29):
  - `p2p-overlord/p2p-overlord-ed2k-server`: 0 stars, 0 forks, 0 open issues; default `master`; default-branch commit 2026-05-10 `7ca18a2`; archived.
- Notes: Archived fork lineage retained only as historical reference. The
         eMuleBB workspace no longer tracks a Go ED2K server; `ed2k-server`
         is the sole local deterministic server.

#### ed2kd

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Stale** · **Historical reference** · **Server role**
- Status: ⚫ Stale
- Language: C
- Source or archive: https://github.com/gureedo/ed2kd
- Repo stats (GitHub, 2026-05-29):
  - `gureedo/ed2kd`: 14 stars, 11 forks, 0 open issues; default `master`; default-branch commit 2019-10-24 `f6c330d`.
- Notes: eDonkey2000 server implementation using libevent, zlib, libconfig, and SQLite
         support. Local research checkout exists in archived server material.

#### gomule

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Stale** · **Historical reference** · **Server role**
- Status: ⚫ Stale
- Language: Go
- Source or archive: https://github.com/HackLinux/gomule
- Repo stats (GitHub, 2026-05-29):
  - `HackLinux/gomule`: 3 stars, 6 forks, 0 open issues; default `master`; default-branch commit 2013-12-05 `e8565a0`.
- Notes: Go "Goroutines eMule Server" project. Treat as a small historical
         implementation reference until protocol coverage is revalidated.

#### eNode

- Assessment: **⚫ Stale/historical** · **🟡 Visible** · **Stale** · **Historical reference** · **Server role**
- Status: ⚫ Stale
- Language: Node.js
- Source or archive: https://github.com/petermrg/eNode
- Repo stats (GitHub, 2026-09-30):
  - `petermrg/eNode`: 76 stars, 28 forks, 5 open issues; default `master`;
    default-branch commit 2013-03-29 `59b81f7`.
- Notes: Experimental eD2K/eMule server. README describes TCP/UDP opcodes,
         obfuscation, Lugdunum/eMule extended protocol, LowID callbacks, files over 4
         GiB, and pluggable storage through MySQL or MongoDB. The previously
         listed `zt8989/eNode` is a smaller duplicate/mirror of the same commit;
         `petermrg/eNode` is the older and substantially more referenced public
         repository.

#### ed2j

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **Server role**
- Status: ⚫ Historical
- Language: Java
- Source or archive: https://github.com/vavavr00m/ed2j
- Repo stats (GitHub, 2026-05-29):
  - `vavavr00m/ed2j`: 7 stars, 1 fork, 0 open issues; default `master`; default-branch commit 2012-07-08 `c782d7a`.
- Notes: Java repository automatically exported from Google Code. Contains an
         `ed2k/server` tree and is useful as an obscure server-side protocol
         reference.

#### Lugdunum eserver

- Assessment: **🟣 Archive/reference** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Server role**
- Status: 🟣 Historical, archive-only
- Language: Native binary
- Source or archive: https://lugdunum.shortypower.org/kiten.html
- Notes: Dominant historical eDonkey/eD2K server family. Gratis but not open source;
         local binary/decompile research archive exists. Use for protocol behavior
         notes only, not as a source dependency.

## Server Lists And Bootstrap Infrastructure

These projects and services are not ED2K server implementations. They publish
server addresses, `server.met` files, or bootstrap guidance.

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| eMule Security server.met | 🟢 Active/current | 🟢 Established | Maintained | Ecosystem dependency | Unknown |
| nodes.dat | 🟢 Active/current | 🟢 Established | Maintained | Ecosystem dependency | Unknown |
| server-met.net | 🟢 Active/current | 🟡 Visible | Maintained | Ecosystem dependency | Unknown |
| shortypower eD2K ServerList | 🟢 Active/current | 🟡 Visible | Maintained | Ecosystem dependency | Unknown |
| Telemacore ed2k-server-list | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem dependency | 2026-10-23 |
| Bunny-Head ed2k-servers | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | Unknown |
| aMule safe server list guidance | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |
| MLDonkey ServerList guide | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |

### Tier 1 — Active with visible adoption

#### eMule Security server.met

- Assessment: **🟢 Active/current** · **🟢 Established** · **Maintained** · **Ecosystem dependency** · **Bootstrap/list role**
- Status: 🟢 Maintained
- Type: Server-list service
- Link: http://upd.emule-security.org/server.met and
        https://www.emule-security.org/serverlist
- Notes: Common `server.met` bootstrap URL used by clients and examples. Validate
         availability before relying on it in tests. The live page was updated
         2026-09-29 and now identifies the Rust implementation lead as
         `ed2k-rust main server`.

#### nodes.dat

- Assessment: **🟢 Active/current** · **🟢 Established** · **Maintained** · **Ecosystem dependency** · **Bootstrap/list role**
- Status: 🟢 Maintained
- Type: Kad bootstrap and server-list portal
- Link: https://www.nodes-dat.com/
- Notes: Publishes live Kad `nodes.dat` links and related eMule/eDonkey server-list
         references, including eMule-Security and Kademlia.Ru node sources. Treat as
         runtime bootstrap infrastructure, not source code.

#### server-met.net

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Maintained** · **Ecosystem dependency** · **Bootstrap/list role**
- Status: 🟢 Maintained
- Type: Server-list service
- Link: https://www.server-met.net/
- Notes: Public server list site. Treat as runtime bootstrap infrastructure, not
         source code.

#### shortypower eD2K ServerList

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Maintained** · **Ecosystem dependency** · **Bootstrap/list role**
- Status: 🟢 Maintained
- Type: Server-list service
- Link: https://emule.shortypower.org/
- Notes: Public eD2K server-list mirror with active server capability, user, file,
         and port metadata. Useful for cross-checking eMule-Security and other
         public server-list snapshots.

### Tier 3 — Experimental or verification required

#### Telemacore ed2k-server-list

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Bootstrap/list role**
- Status: 🟡 Active, needs trust and license review
- Type: Automated server-list harvester and generated portal
- Link: https://github.com/Telemacore/ed2k-server-list
- Repo stats (GitHub, 2026-10-23):
  - `Telemacore/ed2k-server-list`: 3 stars, 2 forks, 0 open issues; default
    `main`; default-branch commit 2026-10-23 `4d8d67c`; no recognized license
    reported by GitHub.
- Notes: New August 2026 project that probes and discovers servers, then
         publishes `server.met`, JSON, text, and a GitHub Pages directory on a
         six-hour schedule. Useful as a secondary data-source and implementation
         lead; do not promote it to a trusted default without code, provenance,
         and output-quality review.

### Tier 4 — Stale or historical

#### Bunny-Head ed2k-servers

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **Bootstrap/list role**
- Status: ⚫ Historical, repository unavailable
- Type: Server-list repository
- Link: https://github.com/Bunny-Head/ed2k-servers
- Last known stats (GitHub, 2026-05-29):
  - `Bunny-Head/ed2k-servers`: 4 stars, 0 forks; last known default-branch
    commit 2023-05-25 `c643060`.
- Notes: The repository returned `404` during the 2026-09-30 audit. Preserve
         the slug as provenance only; do not use it for bootstrap or examples.

#### aMule safe server list guidance

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Bootstrap/list role**
- Status: ⚫ Historical
- Type: Safety guidance
- Link: https://wiki.amule.org/t/index.php?title=Keep_a_safe_list_of_servers
- Notes: Explains fake-server risk and safe-list practice. Useful context for product
         guidance.

#### MLDonkey ServerList guide

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Bootstrap/list role**
- Status: ⚫ Historical
- Type: Usage guidance
- Link: https://bugfreeblog.duckdns.org/wp-content/uploads/mldonkey-website/ServerList.html
- Notes: Documents `ed2k://|server|...|/` server links and server-list management
         for MLDonkey.

# eD2K Project Inventory

Last verified: 2026-06-07

This inventory tracks active, stale, obscure, and historical projects around
eD2K, eDonkey2000, eMule, Kad, server software, controller tooling, protocol
libraries, and eMule mods.

It is a research index, not an endorsement list. Projects marked historical or
archive-only may still be valuable protocol and product references, but they
should not be treated as maintained dependencies without a fresh review.

The 2026-06-07 refresh checked the canonical workspace `repos` and
`workspaces` directories, the generated workspace manifests, local analysis
archives, current public GitHub metadata, eMule-Security live server-list
metadata, and current public forum/site leads for the projects changed below.

## Status Labels

| Status | Meaning |
|---|---|
| Active | Recent or ongoing development is visible, or the project is owned by this workspace. |
| Maintained | Usable and periodically maintained, but not necessarily fast-moving. |
| Stale | Source exists, but no current development was apparent during review. |
| Historical | Important for provenance or protocol behavior, but no longer a current project. |
| Archive-only | Local or public archive evidence exists; upstream may be gone or binary-only. |
| Needs verification | Name or lead is useful, but source, license, or project identity still needs confirmation. |

## Status Markers

| Marker | Meaning |
|---|---|
| 🟢 | Active, maintained, or visibly current. |
| 🟡 | Needs verification before use as evidence or dependency. |
| 🟣 | Archive/reference material. |
| ⚫ | Historical or stale lead. |

## ED2K Server Software

Server software is listed separately from server lists. A server implementation
accepts eD2K/eMule client connections, handles login/search/source operations,
and may expose UDP status or admin APIs.

- **JEmuleServer**
  - Status: Active, experimental
  - Language: Java
  - Source or archive: https://github.com/dagga/JEmuleServer
  - Repo stats (GitHub, 2026-05-29):
    - `dagga/JEmuleServer`: 2 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2026-05-29 `8092fd2`.
  - Notes: Modern open-source eMule/eD2K server project. The README describes a
           Java 21 server with protocol obfuscation, compression, advanced search,
           large-file support, Lugdunum extensions, embedded H2 storage, LowID
           callbacks, fake-file filtering, admin CLI, and IPv6 support. Treat as
           a fresh research lead until protocol coverage and license fit are
           reviewed in code.

- **goed2k-server**
  - Status: Active
  - Language: Go
  - Source or archive: https://github.com/chenjia404/goed2k-server
  - Repo stats (GitHub, 2026-05-29):
    - `chenjia404/goed2k-server`: 4 stars, 2 forks, 0 open issues; default `master`; default-branch commit 2026-04-10 `0bfe17c`.
  - Notes: Go ED2K/eMule server built around `github.com/monkeyWie/goed2k`; implements
           login, status, message, ID assignment, offer files, search, search-more,
           source lookup, callbacks, JSON/MySQL/PostgreSQL catalog storage, and admin
           UI/API. The eMuleBB managed fork lives at
           `https://github.com/emulebb/goed2k-server`.

- **ed2k-rust test server**
  - Status: 🟡 Active test server, needs source verification
  - Language: Rust, inferred from server name
  - Source or archive: Public source not confirmed
  - Public network evidence: `ed2k-rust test server`, `45.87.41.16:6262`, listed
    on https://www.emule-security.org/serverlist on 2026-06-07.
  - Notes: eMule-Security's live server list reports this as a reachable ED2K
           server with active users and indexed files. Track as a current
           ecosystem lead until the implementation repository, maintainer,
           protocol coverage, and license are found.

- **p2p-overlord ED2K server**
  - Status: Historical, archive-only
  - Language: Go
  - Source or archive: https://github.com/p2p-overlord/p2p-overlord-ed2k-server
  - Repo stats (GitHub, 2026-05-29):
    - `p2p-overlord/p2p-overlord-ed2k-server`: 0 stars, 0 forks, 0 open issues; default `master`; default-branch commit 2026-05-10 `7ca18a2`; archived.
  - Notes: Archived fork lineage retained only as historical reference; active
           eMuleBB workspace topology tracks `goed2k-server` directly. The
           obsolete `emulebb-ed2k-server` fork slug has no current public
           repository and should not be used.

- **ed2kd**
  - Status: Stale
  - Language: C
  - Source or archive: https://github.com/gureedo/ed2kd
  - Repo stats (GitHub, 2026-05-29):
    - `gureedo/ed2kd`: 14 stars, 11 forks, 0 open issues; default `master`; default-branch commit 2019-10-24 `f6c330d`.
  - Notes: eDonkey2000 server implementation using libevent, zlib, libconfig, and SQLite
           support. Local research checkout exists in archived server material.

- **eNode**
  - Status: Stale
  - Language: Node.js
  - Source or archive: https://github.com/zt8989/eNode
  - Repo stats (GitHub, 2026-05-29):
    - `zt8989/eNode`: 8 stars, 3 forks, 0 open issues; default `master`; default-branch commit 2013-03-29 `59b81f7`.
  - Notes: Experimental eD2K/eMule server. README describes TCP/UDP opcodes,
           obfuscation, Lugdunum/eMule extended protocol, LowID callbacks, files over 4
           GiB, and pluggable storage through MySQL or MongoDB.

- **gomule**
  - Status: Stale
  - Language: Go
  - Source or archive: https://github.com/HackLinux/gomule
  - Repo stats (GitHub, 2026-05-29):
    - `HackLinux/gomule`: 3 stars, 6 forks, 0 open issues; default `master`; default-branch commit 2013-12-05 `e8565a0`.
  - Notes: Go "Goroutines eMule Server" project. Treat as a small historical
           implementation reference until protocol coverage is revalidated.

- **ed2j**
  - Status: Historical
  - Language: Java
  - Source or archive: https://github.com/vavavr00m/ed2j
  - Repo stats (GitHub, 2026-05-29):
    - `vavavr00m/ed2j`: 7 stars, 1 fork, 0 open issues; default `master`; default-branch commit 2012-07-08 `c782d7a`.
  - Notes: Java repository automatically exported from Google Code. Contains an
           `ed2k/server` tree and is useful as an obscure server-side protocol
           reference.

- **Lugdunum eserver**
  - Status: Historical, archive-only
  - Language: Native binary
  - Source or archive: https://lugdunum.shortypower.org/kiten.html
  - Notes: Dominant historical eDonkey/eD2K server family. Gratis but not open source;
           local binary/decompile research archive exists. Use for protocol behavior
           notes only, not as a source dependency.

- **satan-edonkey-server**
  - Status: Historical, needs verification
  - Language: Unknown
  - Source or archive: Historical references only
  - Notes: Announced in 2007 as an alternative eDonkey server after major server
           shutdowns. Keep as a research lead until source or a trustworthy archive is
           found.

## Server Lists And Bootstrap Infrastructure

These projects and services are not ED2K server implementations. They publish
server addresses, `server.met` files, or bootstrap guidance.

- **Bunny-Head ed2k-servers**
  - Status: Stale
  - Type: Server-list repository
  - Link: https://github.com/Bunny-Head/ed2k-servers
  - Repo stats (GitHub, 2026-05-29):
    - `Bunny-Head/ed2k-servers`: 4 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2023-05-25 `c643060`.
  - Notes: GitHub-hosted list of working ED2K servers. Useful for bootstrap and
           link-check examples, not a server implementation.

- **eMule Security server.met**
  - Status: 🟢 Maintained
  - Type: Server-list service
  - Link: http://upd.emule-security.org/server.met and
          https://www.emule-security.org/serverlist
  - Notes: Common `server.met` bootstrap URL used by clients and examples. Validate
           availability before relying on it in tests. The 2026-06-07 server-list
           page also exposed the `ed2k-rust test server` lead.

- **nodes.dat**
  - Status: 🟢 Maintained
  - Type: Kad bootstrap and server-list portal
  - Link: https://www.nodes-dat.com/
  - Notes: Publishes live Kad `nodes.dat` links and related eMule/eDonkey server-list
           references, including eMule-Security and Kademlia.Ru node sources. Treat as
           runtime bootstrap infrastructure, not source code.

- **server-met.net**
  - Status: Maintained
  - Type: Server-list service
  - Link: https://www.server-met.net/
  - Notes: Public server list site. Treat as runtime bootstrap infrastructure, not
           source code.

- **shortypower eD2K ServerList**
  - Status: 🟢 Maintained
  - Type: Server-list service
  - Link: https://emule.shortypower.org/
  - Notes: Public eD2K server-list mirror with active server capability, user, file,
           and port metadata. Useful for cross-checking eMule-Security and other
           public server-list snapshots.

- **aMule safe server list guidance**
  - Status: Historical
  - Type: Safety guidance
  - Link: https://wiki.amule.org/t/index.php?title=Keep_a_safe_list_of_servers
  - Notes: Explains fake-server risk and safe-list practice. Useful context for product
           guidance.

- **MLDonkey ServerList guide**
  - Status: Historical
  - Type: Usage guidance
  - Link: https://bugfreeblog.duckdns.org/wp-content/uploads/mldonkey-website/ServerList.html
  - Notes: Documents `ed2k://|server|...|/` server links and server-list management
           for MLDonkey.

## Protocol References

- **aMule ED2K protocol wiki**
  - Status: Historical
  - Link: https://wiki.amule.org/wiki/Ed2k_protocol
  - Notes: Protocol notes for eD2K client/server behavior. Revalidate against current
           code before treating as normative.

- **eMule server FAQ**
  - Status: Historical
  - Link: https://emule-project.net/faq/faq_server.htm
  - Notes: User-facing server behavior and connectivity background.

- **eDonkey network server software history**
  - Status: Historical
  - Link: https://en.wikipedia.org/wiki/EDonkey_network
  - Notes: Summarizes Lugdunum/eserver and satan-edonkey-server history. Use only as
           secondary context.

- **eMule/aMule server opcode code**
  - Status: Maintained/historical
  - Link: eMuleBB source, aMule source
  - Notes: The current client code remains the most practical protocol reference for
           `OP_LOGINREQUEST`, `OP_SEARCHREQUEST`, `OP_SERVERLIST`, source lookup, and
           server tags.

## Modern Clients, Forks, And Front Ends

- **eMuleBB**
  - Status: Active
  - Language/platform: Windows, C++/MFC
  - Link: https://github.com/emulebb/emulebb
  - Repo stats (GitHub, 2026-05-29):
    - `emulebb/emulebb`: 39 stars, 1 fork, 24 open issues; default `main`; default-branch commit 2026-05-29 `68ef812`.
  - Notes: Workspace product line; modernized eMule broadband edition with compatibility
           and release hardening.

- **eMule Community**
  - Status: Maintained
  - Language/platform: Windows, C++/MFC
  - Link: https://github.com/irwir/eMule
  - Repo stats (GitHub, 2026-06-07):
    - `irwir/eMule`: 1239 stars, 112 forks, 0 open issues; default `master`; repository pushed 2026-01-10.
  - Notes: Community continuation of classic eMule. Important compatibility and
           user-expectation reference. Local analysis checkouts track `v0.60d`
           and `v0.72a`, while managed app worktrees carry the community
           baseline and tracing harness branches. The `eMule_v0.72a-community`
           prerelease was updated on 2026-05-31 to beta 8 with Windows ARM64
           binaries, Visual Studio 2026 builds, `mbedTLS 4.1.0`, and updated
           MediaInfo allowance.

- **eMuleAI**
  - Status: Active
  - Language/platform: Windows, C++/MFC
  - Link: https://github.com/eMuleAI/eMuleAI
  - Repo stats (GitHub, 2026-05-29):
    - `eMuleAI/eMuleAI`: 35 stars, 4 forks, 11 open issues; default `master`; default-branch commit 2026-04-21 `8e34bde`.
  - Notes: Modern eMule fork with UI, performance, and feature ideas already used as
           comparative reference in tooling docs.

- **eMule Qt**
  - Status: Active
  - Language/platform: Qt 6/C++23
  - Link: https://github.com/ModderMule/emule-qt
  - Repo stats (GitHub, 2026-05-29):
    - `ModderMule/emule-qt`: 20 stars, 1 fork, 1 open issue; default `main`; default-branch commit 2026-04-08 `5a30f16`.
  - Notes: Qt port intended to modernize the eMule client and improve platform
           independence. Local analysis checkout exists under
           `EMULEBB_WORKSPACE_ROOT\analysis\emule-qt`. Homepage:
           https://emule-qt.org/. The public repository was still active in the
           2026-06-07 GitHub refresh.

- **rucio**
  - Status: 🟢 Active, early
  - Language/platform: Rust
  - Link: https://github.com/ogarcia/rucio
  - Repo stats (GitHub, 2026-06-07):
    - `ogarcia/rucio`: 18 stars, 0 forks, 2 open issues; default `master`; latest
      release `0.14.0` on 2026-06-05.
  - Notes: New Rust P2P file-sharing daemon inspired by eMule and MLDonkey. It
           uses its own Kademlia/Gossipsub/libp2p-style stack and optionally
           builds eMule/Kad2 compatibility for Kad search and `ed2k://` download
           workflows. Treat as a fresh monitoring lead until Kad2 and ED2K
           compatibility are reviewed in code and network traces.

- **HydraP2P**
  - Status: 🟡 Needs verification
  - Language/platform: Unknown
  - Link: Public discussion lead only
  - Notes: Mentioned in 2026 I2P/eMule discussion as a beta project associated
           with Sharing-Devils and possible I2P-oriented evolution. No canonical
           source, binary, website, protocol scope, or license was confirmed in
           the 2026-06-07 search pass.

- **eMule eSE LiveTV**
  - Status: Active
  - Language/platform: Windows, C++/Node.js
  - Link: https://github.com/diad87/eMule-eSE-LiveTV
  - Repo stats (GitHub, 2026-05-29):
    - `diad87/eMule-eSE-LiveTV`: 14 stars, 4 forks, 1 open issue; default `main`; default-branch commit 2026-05-19 `4147c51`.
  - Notes: eMule mod exploring P2P live TV over Kad/eD2K with HLS and Node.js web UI.
           No local checkout was present in the canonical workspace during the
           2026-05-29 refresh.

- **aMule**
  - Status: Active
  - Language/platform: Cross-platform C++/wxWidgets
  - Link: https://github.com/amule-project/amule
  - Repo stats (GitHub, 2026-05-29):
    - `amule-project/amule`: 1187 stars, 256 forks, 40 open issues; default `master`; default-branch commit 2026-05-29 `229e268`.
  - Notes: Cross-platform eMule-like client and protocol reference. The
           canonical workspace has an eMuleBB fork at `repos\amule` with
           upstream remote `https://github.com/amule-project/amule.git`.

- **p2p-overlord**
  - Status: Active
  - Language/platform: Rust/Node
  - Link: https://github.com/emulebb/p2p-overlord-agents and
          https://github.com/emulebb/p2p-overlord-be
  - Repo stats (GitHub, 2026-05-29):
    - `emulebb/p2p-overlord-agents`: 0 stars, 0 forks, 0 open issues; default `develop`; default-branch commit 2026-05-23 `045c4be`.
    - `emulebb/p2p-overlord-be`: 0 stars, 0 forks, 0 open issues; default `develop`; default-branch commit 2026-05-24 `1b85e78`.
  - Notes: Separate headless/server-oriented product in the eMuleBB product family.
           Relevant future integration repos are `p2p-overlord-agents` and
           `p2p-overlord-be`; the ED2K server lineage is not active because eMuleBB uses
           `goed2k-server`.

- **MLDonkey**
  - Status: Maintained/stale
  - Language/platform: OCaml daemon
  - Link: https://github.com/ygrek/mldonkey
  - Repo stats (GitHub, 2026-05-29):
    - `ygrek/mldonkey`: 339 stars, 53 forks, 54 open issues; default `master`; default-branch commit 2025-01-28 `0d44635`.
  - Notes: Multi-network P2P daemon with eDonkey/eMule support; useful for headless
           daemon and controller ideas.

- **Shareaza**
  - Status: Stale
  - Language/platform: Windows C++
  - Link: https://github.com/ivan386/Shareaza
  - Repo stats (GitHub, 2026-05-29):
    - `ivan386/Shareaza`: 123 stars, 50 forks, 9 open issues; default `ipv6`; default-branch commit 2019-08-07 `0c2f2f5`.
  - Notes: Multi-network P2P client with eD2K support. Historical UX and protocol
           reference.

- **Envy**
  - Status: Stale
  - Language/platform: Windows C++
  - Link: https://github.com/GetEnvy/Envy
  - Repo stats (GitHub, 2026-05-29):
    - `GetEnvy/Envy`: 52 stars, 12 forks, 11 open issues; default `master`; default-branch commit 2020-03-18 `43787f3`.
  - Notes: Shareaza-derived multi-network client.

- **Lphant**
  - Status: Historical
  - Language/platform: C#/.NET
  - Link: https://github.com/knocte/lphant
  - Repo stats (GitHub, 2026-05-29):
    - `knocte/lphant`: 25 stars, 6 forks, 0 open issues; default `master`; default-branch commit 2012-05-19 `c16be38`.
  - Notes: GPL-era lphant source mirror; useful for old client behavior comparisons.

- **Hathi**
  - Status: Historical
  - Language/platform: C#/.NET
  - Link: https://github.com/lle0x/hathi
  - Repo stats (GitHub, 2026-05-29):
    - `lle0x/hathi`: 1 star, 0 forks, 1 open issue; default `main`; default-branch commit 2022-04-18 `b87ce11`.
  - Notes: Fork of lphant 1.0, described as an eDonkey2000 filesharing client.

- **JMule**
  - Status: Historical
  - Language/platform: Java
  - Link: https://github.com/zhoushineyoung/jmule-mod
  - Repo stats (GitHub, 2026-05-29):
    - `zhoushineyoung/jmule-mod`: 2 stars, 3 forks, 0 open issues; default `master`; default-branch commit 2015-02-22 `b6dac44`.
  - Notes: Java implementation lineage for eMule/eD2K protocol behavior.

- **eMule Plus**
  - Status: Historical, archive-only
  - Language/platform: Windows C++
  - Link: Local archive evidence
  - Notes: Independent eMule-derived client line. Keep source provenance notes in
           historical sections when used.

- **xMule/lMule**
  - Status: Historical, needs verification
  - Language/platform: Linux C++
  - Link: SourceForge and mirrors
  - Notes: Pre-aMule Linux lineage; keep as research leads until canonical
           source/archive links are verified.

- **iMule**
  - Status: Historical, needs verification
  - Language/platform: C++/I2P
  - Link: Public mirrors
  - Notes: Anonymous/I2P-oriented eMule lineage; verify canonical source before using as
           reference.

## Controllers, Indexers, And Automation

- **aMuTorrent**
  - Status: Active
  - Language/platform: Node.js/React/Docker
  - Link: https://github.com/emulebb/amutorrent
  - Repo stats (GitHub, 2026-05-29):
    - `emulebb/amutorrent`: 0 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2026-05-28 `a79eae0`.
  - Notes: Unified download manager for aMule, eMuleBB, and BitTorrent clients;
           current workspace-owned controller product. It exposes ED2K workflows
           through Torznab and qBittorrent-compatible APIs for Sonarr/Radarr. The
           upstream `got3nks/amule-web-controller` slug redirects to
           `got3nks/amutorrent`.

- **eMulerr**
  - Status: Active
  - Language/platform: .NET/Docker
  - Link: https://github.com/isc30/eMulerr
  - Repo stats (GitHub, 2026-05-29):
    - `isc30/eMulerr`: 89 stars, 4 forks, 12 open issues; default `main`; default-branch commit 2026-04-17 `a6119dd`.
  - Notes: Radarr/Sonarr bridge for eD2K/Kad. Emulates a qBittorrent API and exposes a
           web UI/Torznab surface. No local checkout was present in the canonical
           workspace during the 2026-05-29 refresh.

- **amarr**
  - Status: Active
  - Language/platform: Java
  - Link: https://github.com/vexdev/amarr
  - Repo stats (GitHub, 2026-05-29):
    - `vexdev/amarr`: 59 stars, 5 forks, 25 open issues; default `main`; default-branch commit 2026-05-06 `0876bfd`.
  - Notes: aMule connector for Sonarr/Radarr that emulates a torrent client and can
           integrate Torznab-style indexers. No local checkout was present in the
           canonical workspace during the 2026-05-29 refresh.

- **ed2k-indexer**
  - Status: Active/stale
  - Language/platform: Python
  - Link: https://github.com/tronarite/ed2k-indexer
  - Repo stats (GitHub, 2026-05-29):
    - `tronarite/ed2k-indexer`: 0 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2026-03-17 `a3e8ccc`.
  - Notes: Self-hosted Torznab-compatible indexer for Radarr/Sonarr and eMule workflows.

- **docker-amule**
  - Status: Maintained
  - Language/platform: Docker
  - Link: https://github.com/ngosang/docker-amule
  - Repo stats (GitHub, 2026-05-29):
    - `ngosang/docker-amule`: 225 stars, 20 forks, 4 open issues; default `master`; default-branch commit 2026-05-15 `085d0e3`.
  - Notes: Containerized aMule deployment; useful for repeatable controller and headless
           scenarios.

- **GM_EmuleLinker**
  - Status: Active/stale
  - Language/platform: JavaScript/userscript
  - Link: https://github.com/alo0/GM_EmuleLinker
  - Repo stats (GitHub, 2026-05-29):
    - `alo0/GM_EmuleLinker`: 5 stars, 1 fork, 0 open issues; default `master`; default-branch commit 2026-03-17 `7e4223d`.
  - Notes: Browser helper for sending ED2K links to remote eMule/aMule/MLDonkey/system
           handlers.

- **TransMule**
  - Status: Active
  - Language/platform: Vue/Node.js/Docker
  - Link: https://github.com/Jo3l/transmule
  - Repo stats (GitHub, 2026-05-29):
    - `Jo3l/transmule`: 16 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2026-05-28 `a12de3b`.
  - Notes: Self-hosted download manager that unifies aMule ED2K/Kademlia,
           Transmission, and pyLoad. Useful as a modern aMule-control UI and
           file-management reference; verify ED2K search/indexer behavior before
           using it as a Servarr bridge reference.

- **Mularr**
  - Status: Active
  - Language/platform: Web/Docker
  - Link: https://github.com/joecarl/mularr
  - Repo stats (GitHub, 2026-05-29):
    - `joecarl/mularr`: 20 stars, 0 forks, 1 open issue; default `main`; default-branch commit 2026-05-03 `554a5a5`.
  - Notes: New aMule-focused web UI and automation project with *Arr, Gluetun,
           Telegram, qBittorrent-compatible, and Torznab-compatible surfaces.
           Treat as a fresh controller lead until source and runtime behavior are
           reviewed.

- **aMule web controllers**
  - Status: Needs verification
  - Language/platform: Web/API tooling
  - Link: Public search lead
  - Notes: Generic bucket for web/API control projects not yet split out above.
           Current named examples include aMuTorrent, TransMule, Mularr, eMulerr,
           and amarr.

- **aMule M26**
  - Status: 🟢 Active, needs runtime review
  - Language/platform: Web template / Docker
  - Link: https://github.com/jjling2011/amule-m26
  - Repo stats (GitHub, 2026-06-07):
    - `jjling2011/amule-m26`: 0 stars, 0 forks; latest release `v0.1.3` on
      2026-06-07.
  - Notes: Modern aMule WebUI template packaged around the `ngosang/docker-amule`
           configuration model. Useful UI/packaging lead; not a protocol
           implementation by itself.

## Protocol Libraries And Utilities

- **goed2k**
  - Status: Active
  - Language/platform: Go
  - Link: https://github.com/monkeyWie/goed2k
  - Repo stats (GitHub, 2026-05-29):
    - `monkeyWie/goed2k`: 5 stars, 1 fork, 1 open issue; default `main`; default-branch commit 2026-04-03 `a8f73de`.
  - Notes: Go ED2K client/library with `server.met`, server connection, Kad
           bootstrap/source lookup, search, downloads, upload, UPnP, and terminal UI
           support.

- **libed2k/qmule**
  - Status: Stale
  - Language/platform: C++
  - Link: https://github.com/qmule/libed2k
  - Repo stats (GitHub, 2026-05-29):
    - `qmule/libed2k`: 82 stars, 27 forks, 4 open issues; default `master`; default-branch commit 2016-06-02 `5408c65`.
  - Notes: Cross-platform eDonkey protocol library inspired by libtorrent-rasterbar.

- **ed2k-ruby**
  - Status: Maintained/stale
  - Language/platform: Ruby
  - Link: https://github.com/edelkas/ed2k-ruby
  - Repo stats (GitHub, 2026-05-29):
    - `edelkas/ed2k-ruby`: 0 stars, 0 forks, 0 open issues; default `master`; default-branch commit 2025-11-17 `2afc76f`.
  - Notes: Ruby implementation of eD2K/eDonkey2000 and extended eMule protocol concepts.

- **ed2k Rust crate**
  - Status: Stale
  - Language/platform: Rust
  - Link: https://github.com/Kimundi/ed2k
  - Repo stats (GitHub, 2026-05-29):
    - `Kimundi/ed2k`: 1 star, 0 forks, 0 open issues; default `main`; default-branch commit 2023-05-20 `73fb463`.
  - Notes: ED2K hash implementation, not a full network protocol library. Useful
           for hash-behavior comparison around chunk-boundary variants.

- **kadkad**
  - Status: Needs verification
  - Language/platform: Rust
  - Link: Public/local source not confirmed
  - Notes: Rust Kad2 library/daemon research lead. No canonical checkout was found
           in `repos`, `workspaces`, or the listed local analysis directories
           during the 2026-05-29 refresh.

- **rust2k**
  - Status: Needs verification
  - Language/platform: Rust
  - Link: Public/local source not confirmed
  - Notes: Rust ED2K/Kad research lead. No canonical checkout was found in
           `repos`, `workspaces`, or the listed local analysis directories during
           the 2026-05-29 refresh.

- **jaMule**
  - Status: Needs verification
  - Language/platform: Java
  - Link: Referenced by amarr
  - Notes: Java aMule/ED2K helper library referenced by amarr; confirm canonical source
           before promoting.

- **goe2k**
  - Status: Archive-only
  - Language/platform: Go
  - Link: Local archive evidence
  - Notes: Archived Go ED2K material observed under local research archives. Confirm
           canonical source before linking.

- **jed2k**
  - Status: Archive-only
  - Language/platform: Java/C++ lineage
  - Link: Local archive evidence
  - Notes: Archived ED2K implementation material observed in local research archives.
           Confirm canonical source before linking.

- **KadGlobe**
  - Status: 🟡 Active, needs protocol review
  - Language/platform: Python/JavaScript
  - Link: https://github.com/floatingbit23/KadGlobe
  - Repo stats (GitHub, 2026-06-07):
    - `floatingbit23/KadGlobe`: 0 stars, 0 forks; repository pushed 2026-05-19; no
      releases.
  - Notes: Kademlia visualization and telemetry tool that claims live UDP/Kad probes
           and eMule metrics. Track as a diagnostics idea lead until packet behavior,
           data sources, and compatibility are reviewed.

## Historical eMule Mods And Source Archives

The workspace has archive evidence under `EMULEBB_WORKSPACE_ROOT\analysis\mods-archive`.
These projects are historical reference material for UX, upload policy,
anti-leecher logic, server handling, large-share behavior, and compatibility
hardening. Do not import behavior wholesale.

- **MorphXT**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-MorphXT_v12.3_src_and_libs`,
                             `eMule-0.50a-MorphXT_v12.7_src_and_libs`;
                             https://sourceforge.net/projects/emulemorph/files/MorphXT/
  - Notes: Major mod lineage and frequent reference for PowerShare, UX, IP-to-country,
           FakeAlyzer, and upload features.

- **Xtreme**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-Xtreme-8.1-src`
  - Notes: Major mod lineage with known-file, AICH, IP-filter, and performance ideas.

- **ScarAngel**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-ScarAngel-v4.2-src`;
                             https://scarangel.sourceforge.net/eng_download.html
  - Notes: Stulle/Morph-related mod lineage with anti-leecher and sharing policy ideas.

- **StulleMule**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-StulleMule_v7.0-src`
  - Notes: Important source for threaded save, transfer window, and upload/share policy
           ideas.

- **Mephisto**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-Mephisto-v3.0-src`;
                             https://sourceforge.net/projects/mephisto/files/Mephisto/
  - Notes: Important source for trickle slot and multi-chunk upload policy references.

- **UltiMatiX**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-UltiMatiX_v5.0_31.08.2016_by_engo3k`
  - Notes: Late mod line referenced for upload policy and advanced preferences ideas.

- **NeoMule / NeoMule Reloaded**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-NeoMule-v4.55a`,
                             `eMule-0.50a-neomuleneomule_reloaded-fa3debb`
  - Notes: IPv6, NAT, and broader protocol-adjacent idea reference.

- **AcKroNiC**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-AcKroNiC_v6.0-src`
  - Notes: Historical mod with PowerShare and anti-leecher relevance.

- **beba**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-beba_2.72_src`
  - Notes: Historical mod and ResizableLib-related dependency provenance.

- **MagicAngel**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-MagicAngel-v4.0-src`
  - Notes: Historical mod with server, sharing, and UI code references.

- **ZZUL TRA**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-ZZUL-TRA_2.6_Src`
  - Notes: Historical mod lineage useful for upload/queue behavior comparison.

- **Adunanza**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-Adunanza`;
                             https://sourceforge.net/p/amule-adunanza/code/HEAD/tree/
  - Notes: Italian network/community lineage; compare carefully because topology and
           behavior goals differ.

- **DreaMule**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-DreaMule_2.12_sources`,
                             `eMule-0.50a-DreaMule_3.0_final`
  - Notes: Historical mod/client line.

- **AA Community**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-AA_Community_Sources`
  - Notes: Historical community mod archive.

- **Euro-Com MoD**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-Euro-Com_MoD_v1.6`
  - Notes: Historical mod archive.

- **LPE / lightweight**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-lightweight_src_15.04.12`,
                             `eMule-0.50a-LPE-src_04.06.12`
  - Notes: Lightweight/LPE branch with X-Mod and Stulle references in changelogs.

- **MorphCA**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-MorphCA_v1.0_src-Libs_Vs08Pile_Ready_Incl_Win7Sdk_hotfix`,
                             `eMule-0.50a-MorphCA_v2.2_src_libs-vs08-vs10.compile.ready.incl.win7sdk`
  - Notes: Morph-derived archive line.

- **XCA**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-0.50a-XCA_1.3-src_VS2010-16.12.11`
  - Notes: Historical mod archive with server-list and protocol code references.

- **eMule BitComet plugin**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMule-bitcomet-plugin`
  - Notes: Historical integration/plugin line.

- **eMule Plus**
  - Status: Historical, archive-only
  - Archive/source evidence: `eMulePlus-1.2e.Source`
  - Notes: Independent eMule-derived client source archive.

- **VeryCD / easyMule**
  - Status: Needs verification
  - Archive/source evidence: Public search lead
  - Notes: Important Chinese eMule/easyMule lineage, but canonical source/archive needs
           verification before adding as a sourced row.

- **EastShare, Sivka, iONiX, Phoenix, TK4**
  - Status: Needs verification
  - Archive/source evidence: Public search leads
  - Notes: Historically important mod names. Promote only when source archive URLs are
           verified.

## Public Archive Collections

- **eMule Mods / emule-mods.de**
  - Status: 🟣 Archive/reference
  - Link: http://www.emule-mods.de/
  - Notes: Historically important German eMule mod index repeatedly referenced by
           mod docs, forums, and academic papers. Verify live availability and mirrors
           before relying on it as a download/source archive.

- **eMule Mods Italia**
  - Status: 🟢 Maintained reference/forum
  - Link: https://emulemods.altervista.org/
  - Notes: Italian eMule mods forum and guide site with current activity around
           Community releases, eMuleAI, nodes.dat, and mod guides.

- **Leechermods**
  - Status: 🟢 Maintained mod/news archive
  - Link: https://www.leechermods.com/
  - Notes: Long-running file-sharing and mod news blog with current 2026 activity
           and deep historical archives. Include neutrally as research evidence, not
           as an endorsement of any specific mod behavior.

- **eMule Fans**
  - Status: 🟢 Maintained reference/archive
  - Link: https://www.emulefans.com/
  - Notes: Chinese eMule/eD2K site covering official/community releases, mods,
           server lists, Kad nodes, IP filters, DLP libraries, language packs, and
           historical software references.

- **emulefans ed2k-software**
  - Status: Archive-only
  - Link: https://github.com/emulefanscom/ed2k-software
  - Repo stats (GitHub, 2026-05-29):
    - `emulefanscom/ed2k-software`: 8 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2024-04-23 `d0d2b09`.
  - Notes: Public archive of eD2K software packages and eMule mods. Confirm license and
           source completeness before reusing material.

- **emulefans misc**
  - Status: Archive-only
  - Link: https://github.com/emulefanscom/misc
  - Repo stats (GitHub, 2026-05-29):
    - `emulefanscom/misc`: 5 stars, 1 fork, 0 open issues; default `master`; default-branch commit 2024-04-24 `0a18d57`.
  - Notes: Miscellaneous eMule/eD2K archive material.

- **local compressed archive set**
  - Status: Archive-only
  - Link: External research archive
  - Notes: Includes `eMule-mods-archive.rar`, `jed2k.rar`, `goe2k.rar`, `libed2k.rar`,
           `mldonkey.rar`, `qmule.rar`, and ED2K server research archives. Do not
           reference machine-specific absolute paths in committed docs.

## Maintenance Procedure

Refresh this file when a new eD2K/eMule-related repo is discovered or before
using any project as implementation evidence.

1. Search both public sources and local research archives.
2. Classify server implementations separately from server lists, bootstrap
   services, protocol libraries, clients, controllers, and mods.
3. Prefer canonical upstream URLs. If only a local checkout exists, keep the
   entry as needs verification until an upstream, archive, or provenance link
   is found.
4. Record closed-source historical servers as protocol/history evidence only.
5. Validate whether source, binary archive, license, and protocol coverage are
   actually present before changing status from needs verification.
6. Keep rows concise and factual. Do not add marketing claims or endorsement
   language.

Recommended recurring searches:

```text
ed2k server github
eDonkey server source code
Lugdunum eserver archive
satan-edonkey-server source
node ed2k server github
go ed2k server github
java ed2k server github
emule mod source archive
MorphXT Xtreme ScarAngel StulleMule Mephisto source
VeryCD easyMule source
eMule EastShare Sivka iONiX Phoenix TK4 source
Torznab ed2k eMule
aMule Sonarr Radarr ed2k
aMuTorrent TransMule Mularr eMulerr amarr
JEmuleServer goed2k-server ED2K server
ed2k hash library Rust Ruby Go
site:github.com ed2k pushed after current year
site:github.com eMule Kad pushed after current year
site:github.com "Kad2" "eMule" "Rust"
eMule Security ed2k-rust test server
rucio eMule Kad2 Rust
eMule 0.72a community beta
emule-qt GitHub
KadGlobe eMule Kademlia
aMule WebUI template ed2k
HydraP2P Sharing-Devils eD2K I2P
shortypower eD2K ServerList
```

After editing, run:

```powershell
git diff --check
rg -n "ED2K-PROJECT-INVENTORY" EMULEBB_WORKSPACE_ROOT\repos\emulebb-tooling\docs
```

Run `python -m emule_workspace validate` when the workspace lock is free.

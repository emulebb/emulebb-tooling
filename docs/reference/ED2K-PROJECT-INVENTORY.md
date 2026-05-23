# eD2K Project Inventory

Last verified: 2026-05-23

This inventory tracks active, stale, obscure, and historical projects around
eD2K, eDonkey2000, eMule, Kad, server software, controller tooling, protocol
libraries, and eMule mods.

It is a research index, not an endorsement list. Projects marked historical or
archive-only may still be valuable protocol and product references, but they
should not be treated as maintained dependencies without a fresh review.

## Status Labels

| Status | Meaning |
|---|---|
| Active | Recent or ongoing development is visible, or the project is owned by this workspace. |
| Maintained | Usable and periodically maintained, but not necessarily fast-moving. |
| Stale | Source exists, but no current development was apparent during review. |
| Historical | Important for provenance or protocol behavior, but no longer a current project. |
| Archive-only | Local or public archive evidence exists; upstream may be gone or binary-only. |
| Needs verification | Name or lead is useful, but source, license, or project identity still needs confirmation. |

## ED2K Server Software

Server software is listed separately from server lists. A server implementation
accepts eD2K/eMule client connections, handles login/search/source operations,
and may expose UDP status or admin APIs.

| Project | Status | Language | Source or archive | Notes |
|---|---|---|---|---|
| goed2k-server | Active | Go | https://github.com/chenjia404/goed2k-server | Go ED2K/eMule server built around `github.com/monkeyWie/goed2k`; implements login, status, message, ID assignment, offer files, search, search-more, source lookup, callbacks, JSON/MySQL/PostgreSQL catalog storage, and admin UI/API. The eMuleBB managed fork lives at `https://github.com/emulebb/goed2k-server`. |
| p2p-overlord ED2K server | Historical reference | Go | https://github.com/p2p-overlord/p2p-overlord-ed2k-server | Renamed fork lineage retained only as historical reference; active eMuleBB workspace topology tracks `goed2k-server` directly. The obsolete `https://github.com/emulebb/emulebb-ed2k-server` fork should not be used. |
| ed2kd | Stale | C | https://github.com/gureedo/ed2kd | eDonkey2000 server implementation using libevent, zlib, libconfig, and SQLite support. Local research checkout exists in archived server material. |
| eNode | Stale | Node.js | https://github.com/zt8989/eNode | Experimental eD2K/eMule server. README describes TCP/UDP opcodes, obfuscation, Lugdunum/eMule extended protocol, LowID callbacks, files over 4 GiB, and pluggable storage through MySQL or MongoDB. |
| gomule | Stale | Go | https://github.com/HackLinux/gomule | Go "Goroutines eMule Server" project. Treat as a small historical implementation reference until protocol coverage is revalidated. |
| ed2j | Historical | Java | https://github.com/vavavr00m/ed2j | Java repository automatically exported from Google Code. Contains an `ed2k/server` tree and is useful as an obscure server-side protocol reference. |
| Lugdunum eserver | Historical, archive-only | Native binary | https://lugdunum.shortypower.org/kiten.html | Dominant historical eDonkey/eD2K server family. Gratis but not open source; local binary/decompile research archive exists. Use for protocol behavior notes only, not as a source dependency. |
| satan-edonkey-server | Historical, needs verification | Unknown | Historical references only | Announced in 2007 as an alternative eDonkey server after major server shutdowns. Keep as a research lead until source or a trustworthy archive is found. |

## Server Lists And Bootstrap Infrastructure

These projects and services are not ED2K server implementations. They publish
server addresses, `server.met` files, or bootstrap guidance.

| Project or service | Status | Type | Link | Notes |
|---|---|---|---|---|
| Bunny-Head ed2k-servers | Active/stale | Server-list repository | https://github.com/Bunny-Head/ed2k-servers | GitHub-hosted list of working ED2K servers. Useful for bootstrap and link-check examples, not a server implementation. |
| eMule Security server.met | Maintained | Server-list service | http://upd.emule-security.org/server.met | Common `server.met` bootstrap URL used by clients and examples. Validate availability before relying on it in tests. |
| server-met.net | Maintained | Server-list service | https://www.server-met.net/ | Public server list site. Treat as runtime bootstrap infrastructure, not source code. |
| aMule safe server list guidance | Historical | Safety guidance | https://wiki.amule.org/t/index.php?title=Keep_a_safe_list_of_servers | Explains fake-server risk and safe-list practice. Useful context for product guidance. |
| MLDonkey ServerList guide | Historical | Usage guidance | https://bugfreeblog.duckdns.org/wp-content/uploads/mldonkey-website/ServerList.html | Documents `ed2k://|server|...|/` server links and server-list management for MLDonkey. |

## Protocol References

| Reference | Status | Link | Notes |
|---|---|---|---|
| aMule ED2K protocol wiki | Historical | https://wiki.amule.org/wiki/Ed2k_protocol | Protocol notes for eD2K client/server behavior. Revalidate against current code before treating as normative. |
| eMule server FAQ | Historical | https://emule-project.net/faq/faq_server.htm | User-facing server behavior and connectivity background. |
| eDonkey network server software history | Historical | https://en.wikipedia.org/wiki/EDonkey_network | Summarizes Lugdunum/eserver and satan-edonkey-server history. Use only as secondary context. |
| eMule/aMule server opcode code | Maintained/historical | eMuleBB source, aMule source | The current client code remains the most practical protocol reference for `OP_LOGINREQUEST`, `OP_SEARCHREQUEST`, `OP_SERVERLIST`, source lookup, and server tags. |

## Modern Clients, Forks, And Front Ends

| Project | Status | Language/platform | Link | Notes |
|---|---|---|---|---|
| eMuleBB | Active | Windows, C++/MFC | https://github.com/emulebb/emulebb | Workspace product line; modernized eMule broadband edition with compatibility and release hardening. |
| eMule Community | Maintained | Windows, C++/MFC | https://github.com/irwir/eMule | Community continuation of classic eMule. Important compatibility and user-expectation reference. |
| eMuleAI | Active | Windows, C++/MFC | https://github.com/eMuleAI/eMuleAI | Modern eMule fork with UI, performance, and feature ideas already used as comparative reference in tooling docs. |
| eMule Qt | Active | Qt/C++ | https://github.com/ModderMule/emule-qt | Qt port intended to modernize the eMule client and improve platform independence. Homepage: https://emule-qt.org/ |
| eMule eSE LiveTV | Active/stale | Windows, C++/Node.js | https://github.com/diad87/eMule-eSE-LiveTV | eMule mod exploring P2P live TV over Kad/eD2K with HLS and Node.js web UI. Local sibling checkout was observed during research. |
| aMule | Maintained | Cross-platform C++/wxWidgets | https://github.com/amule-project/amule | Cross-platform eMule-like client and protocol reference. |
| p2p-overlord | Active | Rust/Node | https://github.com/emulebb/p2p-overlord-agents and https://github.com/emulebb/p2p-overlord-be | Separate headless/server-oriented product in the eMuleBB product family. Relevant future integration repos are `p2p-overlord-agents` and `p2p-overlord-be`; the ED2K server lineage is not active because eMuleBB uses `goed2k-server`. |
| MLDonkey | Maintained/stale | OCaml daemon | https://github.com/ygrek/mldonkey | Multi-network P2P daemon with eDonkey/eMule support; useful for headless daemon and controller ideas. |
| Shareaza | Stale | Windows C++ | https://github.com/ivan386/Shareaza | Multi-network P2P client with eD2K support. Historical UX and protocol reference. |
| Envy | Stale | Windows C++ | https://github.com/GetEnvy/Envy | Shareaza-derived multi-network client. |
| Lphant | Historical | C#/.NET | https://github.com/knocte/lphant | GPL-era lphant source mirror; useful for old client behavior comparisons. |
| Hathi | Historical | C#/.NET | https://github.com/lle0x/hathi | Fork of lphant 1.0, described as an eDonkey2000 filesharing client. |
| JMule | Historical | Java | https://github.com/zhoushineyoung/jmule-mod | Java implementation lineage for eMule/eD2K protocol behavior. |
| eMule Plus | Historical, archive-only | Windows C++ | Local archive evidence | Independent eMule-derived client line. Keep source provenance notes in historical sections when used. |
| xMule/lMule | Historical, needs verification | Linux C++ | SourceForge and mirrors | Pre-aMule Linux lineage; keep as research leads until canonical source/archive links are verified. |
| iMule | Historical, needs verification | C++/I2P | Public mirrors | Anonymous/I2P-oriented eMule lineage; verify canonical source before using as reference. |

## Controllers, Indexers, And Automation

| Project | Status | Language/platform | Link | Notes |
|---|---|---|---|---|
| aMuTorrent | Active | Python/Qt | https://github.com/emulebb/amutorrent | Unified download manager for aMule and BitTorrent clients; current workspace-owned controller product. |
| eMulerr | Active | .NET/Docker | https://github.com/isc30/eMulerr | Radarr/Sonarr bridge for eD2K/Kad. Emulates a qBittorrent API and exposes a web UI/Torznab surface. Local sibling checkout was observed during research. |
| amarr | Active/stale | Java | https://github.com/vexdev/amarr | aMule connector for Sonarr/Radarr that emulates a torrent client and can integrate Torznab-style indexers. Local sibling checkout was observed during research. |
| ed2k-indexer | Stale | Python | https://github.com/tronarite/ed2k-indexer | Self-hosted Torznab-compatible indexer for Radarr/Sonarr and eMule workflows. |
| docker-amule | Maintained | Docker | https://github.com/ngosang/docker-amule | Containerized aMule deployment; useful for repeatable controller and headless scenarios. |
| GM_EmuleLinker | Stale | JavaScript/userscript | https://github.com/alo0/GM_EmuleLinker | Browser helper for sending ED2K links to remote eMule/aMule/MLDonkey/system handlers. |
| TransMule | Needs verification | Controller/bridge | Public search lead | Keep as a controller search term until canonical source is confirmed. |
| aMule web controllers | Needs verification | Web/API tooling | Public search lead | Track individual projects only after source, license, and target aMule version are confirmed. |

## Protocol Libraries And Utilities

| Project | Status | Language/platform | Link | Notes |
|---|---|---|---|---|
| goed2k | Active | Go | https://github.com/monkeyWie/goed2k | Go ED2K client/library with `server.met`, server connection, Kad bootstrap/source lookup, search, downloads, upload, UPnP, and terminal UI support. |
| libed2k/qmule | Stale | C++ | https://github.com/qmule/libed2k | Cross-platform eDonkey protocol library inspired by libtorrent-rasterbar. |
| ed2k-ruby | Stale | Ruby | https://github.com/edelkas/ed2k-ruby | Ruby implementation of eD2K/eDonkey2000 and extended eMule protocol concepts. |
| kadkad | Active/stale | Rust | Local sibling checkout | Rust Kad2 library/daemon research project. Canonical upstream URL still needs verification before linking. |
| rust2k | Active/stale | Rust | Local sibling checkout | Rust ED2K/Kad research project. Canonical upstream URL still needs verification before linking. |
| jaMule | Needs verification | Java | Referenced by amarr | Java aMule/ED2K helper library referenced by amarr; confirm canonical source before promoting. |
| goe2k | Archive-only | Go | Local archive evidence | Archived Go ED2K material observed under local research archives. Confirm canonical source before linking. |
| jed2k | Archive-only | Java/C++ lineage | Local archive evidence | Archived ED2K implementation material observed in local research archives. Confirm canonical source before linking. |

## Historical eMule Mods And Source Archives

The workspace has archive evidence under `EMULE_WORKSPACE_ROOT\analysis\mods-archive`.
These projects are historical reference material for UX, upload policy,
anti-leecher logic, server handling, large-share behavior, and compatibility
hardening. Do not import behavior wholesale.

| Mod or client line | Status | Archive/source evidence | Notes |
|---|---|---|---|
| MorphXT | Historical, archive-only | `eMule-0.50a-MorphXT_v12.3_src_and_libs`, `eMule-0.50a-MorphXT_v12.7_src_and_libs`; https://sourceforge.net/projects/emulemorph/files/MorphXT/ | Major mod lineage and frequent reference for PowerShare, UX, IP-to-country, FakeAlyzer, and upload features. |
| Xtreme | Historical, archive-only | `eMule-0.50a-Xtreme-8.1-src` | Major mod lineage with known-file, AICH, IP-filter, and performance ideas. |
| ScarAngel | Historical, archive-only | `eMule-0.50a-ScarAngel-v4.2-src`; https://scarangel.sourceforge.net/eng_download.html | Stulle/Morph-related mod lineage with anti-leecher and sharing policy ideas. |
| StulleMule | Historical, archive-only | `eMule-0.50a-StulleMule_v7.0-src` | Important source for threaded save, transfer window, and upload/share policy ideas. |
| Mephisto | Historical, archive-only | `eMule-0.50a-Mephisto-v3.0-src`; https://sourceforge.net/projects/mephisto/files/Mephisto/ | Important source for trickle slot and multi-chunk upload policy references. |
| UltiMatiX | Historical, archive-only | `eMule-0.50a-UltiMatiX_v5.0_31.08.2016_by_engo3k` | Late mod line referenced for upload policy and advanced preferences ideas. |
| NeoMule / NeoMule Reloaded | Historical, archive-only | `eMule-0.50a-NeoMule-v4.55a`, `eMule-0.50a-neomuleneomule_reloaded-fa3debb` | IPv6, NAT, and broader protocol-adjacent idea reference. |
| AcKroNiC | Historical, archive-only | `eMule-0.50a-AcKroNiC_v6.0-src` | Historical mod with PowerShare and anti-leecher relevance. |
| beba | Historical, archive-only | `eMule-0.50a-beba_2.72_src` | Historical mod and ResizableLib-related dependency provenance. |
| MagicAngel | Historical, archive-only | `eMule-0.50a-MagicAngel-v4.0-src` | Historical mod with server, sharing, and UI code references. |
| ZZUL TRA | Historical, archive-only | `eMule-0.50a-ZZUL-TRA_2.6_Src` | Historical mod lineage useful for upload/queue behavior comparison. |
| Adunanza | Historical, archive-only | `eMule-0.50a-Adunanza`; https://sourceforge.net/p/amule-adunanza/code/HEAD/tree/ | Italian network/community lineage; compare carefully because topology and behavior goals differ. |
| DreaMule | Historical, archive-only | `eMule-0.50a-DreaMule_2.12_sources`, `eMule-0.50a-DreaMule_3.0_final` | Historical mod/client line. |
| AA Community | Historical, archive-only | `eMule-0.50a-AA_Community_Sources` | Historical community mod archive. |
| Euro-Com MoD | Historical, archive-only | `eMule-0.50a-Euro-Com_MoD_v1.6` | Historical mod archive. |
| LPE / lightweight | Historical, archive-only | `eMule-0.50a-lightweight_src_15.04.12`, `eMule-0.50a-LPE-src_04.06.12` | Lightweight/LPE branch with X-Mod and Stulle references in changelogs. |
| MorphCA | Historical, archive-only | `eMule-0.50a-MorphCA_v1.0_src-Libs_Vs08Pile_Ready_Incl_Win7Sdk_hotfix`, `eMule-0.50a-MorphCA_v2.2_src_libs-vs08-vs10.compile.ready.incl.win7sdk` | Morph-derived archive line. |
| XCA | Historical, archive-only | `eMule-0.50a-XCA_1.3-src_VS2010-16.12.11` | Historical mod archive with server-list and protocol code references. |
| eMule BitComet plugin | Historical, archive-only | `eMule-bitcomet-plugin` | Historical integration/plugin line. |
| eMule Plus | Historical, archive-only | `eMulePlus-1.2e.Source` | Independent eMule-derived client source archive. |
| VeryCD / easyMule | Needs verification | Public search lead | Important Chinese eMule/easyMule lineage, but canonical source/archive needs verification before adding as a sourced row. |
| EastShare, Sivka, iONiX, Phoenix, TK4 | Needs verification | Public search leads | Historically important mod names. Promote only when source archive URLs are verified. |

## Public Archive Collections

| Collection | Status | Link | Notes |
|---|---|---|---|
| emulefans ed2k-software | Archive-only | https://github.com/emulefanscom/ed2k-software | Public archive of eD2K software packages and eMule mods. Confirm license and source completeness before reusing material. |
| emulefans misc | Archive-only | https://github.com/emulefanscom/misc | Miscellaneous eMule/eD2K archive material. |
| local compressed archive set | Archive-only | External research archive | Includes `eMule-mods-archive.rar`, `jed2k.rar`, `goe2k.rar`, `libed2k.rar`, `mldonkey.rar`, `qmule.rar`, and ED2K server research archives. Do not reference machine-specific absolute paths in committed docs. |

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
```

After editing, run:

```powershell
git diff --check
rg -n "ED2K-PROJECT-INVENTORY" EMULE_WORKSPACE_ROOT\repos\emulebb-tooling\docs
```

Run `python -m emule_workspace validate` when the workspace lock is free.

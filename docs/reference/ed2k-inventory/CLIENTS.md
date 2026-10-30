# Modern eD2K Clients, Forks, and Front Ends

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

Current clients are ranked by activity and public adoption. Download-only implementations remain visible for threat and ecosystem tracking but are excluded from healthy-peer rankings.

Ranking badges and thresholds are defined in [Methodology](METHODOLOGY.md). Statistics are dated snapshots, not live user counts.

## Modern Clients, Forks, And Front Ends

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| Gopeed | 🟢 Active/current | 🟢 Established | Active development | Direct competitor/watchlist | 2026-10-23 |
| rucio | 🟢 Active/current | 🟡 Visible | Released | Direct competitor/watchlist | 2026-10-23 |
| aria2-next | 🟢 Active/current | 🟢 Established | Released | Direct competitor/watchlist | 2026-10-13 |
| aMule | 🟢 Active/current | 🟢 Established | Active development | Direct competitor/watchlist | 2026-10-13 |
| eMule Community | 🟢 Active/current | 🟢 Established | Maintained | Direct competitor/watchlist | 2026-08-20 |
| eMuleAI | 🟢 Active/current | 🟡 Visible | Active development | Direct competitor/watchlist | 2026-07-25 |
| emulebb-rust | 🟢 Active/current | ⚪ Niche | Public beta | Direct competitor/watchlist | 2026-10-29 |
| Ember | 🟢 Active/current | ⚪ Niche | Active development | Direct competitor/watchlist | 2026-10-21 |
| eMuleRust (`laurentgeynet-ux/eMule-Rust`) | 🟢 Active/current | ⚪ Niche | Experimental | Direct competitor/watchlist | 2026-10-18 |
| Mulee | 🟢 Active/current | ⚪ Niche | Experimental | Ecosystem watchlist | 2026-10-17 |
| eMule Qt | 🟢 Active/current | ⚪ Niche | Active development | Direct competitor/watchlist | 2026-10-13 |
| eMule Next | 🟢 Active/current | ⚪ Niche | Experimental | Direct competitor/watchlist | 2026-10-11 |
| eMuleBB | 🟢 Active/current | ⚪ Niche | Stable | Workspace baseline | 2026-09-25 |
| eMule eSE LiveTV | 🟢 Active/current | ⚪ Niche | Active development | Ecosystem watchlist | 2026-08-02 |
| macMule | 🟢 Active/current | ⚪ Niche | Maintained | Ecosystem watchlist | 2026-02-14 |
| avwarez eMule build/fork | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem watchlist | 2026-10-23 |
| njMule | 🟡 Verification needed | ⚪ Niche | Experimental | Direct competitor/watchlist | 2026-10-13 |
| rmule | 🟡 Verification needed | ⚪ Niche | Experimental | Direct competitor/watchlist | 2026-10-12 |
| aMule Android Preview | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem watchlist | 2026-10-08 |
| Kelpie | 🟡 Verification needed | ⚪ Niche | Experimental | Ecosystem watchlist | 2026-10-02 |
| AmuleD v2 Python | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem watchlist | 2026-09-29 |
| padMule | 🟡 Verification needed | ⚪ Niche | Experimental | Direct competitor/watchlist | 2026-08-14 |
| MLDonkey | 🟡 Verification needed | 🟡 Visible | Stale | Direct competitor/watchlist | 2025-01-28 |
| HydraP2P | 🟡 Verification needed | ❔ Unknown | Experimental | Ecosystem watchlist | Unknown |
| iMule | 🟡 Verification needed | ❔ Unknown | Reference-only | Ecosystem watchlist | Unknown |
| xMule/lMule | 🟡 Verification needed | ❔ Unknown | Reference-only | Ecosystem watchlist | Unknown |
| Envy | ⚫ Stale/historical | 🟡 Visible | Stale | Historical reference | 2026-08-07 |
| Hathi | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2022-04-18 |
| Shareaza | ⚫ Stale/historical | 🟡 Visible | Stale | Historical reference | 2019-08-07 |
| JMule | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2015-02-22 |
| Lphant | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2012-05-19 |
| eMule Plus | 🟣 Archive/reference | ❔ Unknown | Reference-only | Historical reference | Unknown |
| p2p-overlord | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |
| FluxDown | 🟢 Active/current | 🟢 Established | Active development | Direct competitor/watchlist | 2026-10-23 |

### Tier 1 — Active with visible adoption

#### Gopeed

- Assessment: **🟢 Active/current** · **🟢 Established** · **Active development** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active, multi-protocol client with native eD2K integration
- Language/platform: Go core with Flutter desktop, mobile, and Web clients
- Link: https://github.com/GopeedLab/gopeed
- Repo stats (GitHub, 2026-10-23):
  - `GopeedLab/gopeed`: 27,111 stars, 1,763 forks, 343 open issues; default
    `main`; reviewed default-branch commit 2026-10-23 `4d65948`; latest stable
    release `v1.9.3` on 2026-03-18; GPL-3.0.
- Notes: eD2K support landed immediately before `v1.9.3` and the current
         fetcher integrates `monkeyWie/goed2k` for real transfers, resume
         state, peer statistics, configuration, and task lifecycle; it is not
         merely an `ed2k://` handler. Its very large user-facing footprint
         makes it the most visible newly identified eD2K-capable product in
         this sweep. Several reviewed head build jobs were failed or
         cancelled, and protocol behavior inherits `goed2k`; verify stock
         compatibility independently and do not use GPL-3.0 code in the
         GPL-2.0-only eMuleBB Rust tree.

#### rucio

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Released** · **Direct competitor/watchlist** · **🟢 Uploads verified chunks and seeds completed files**
- Status: 🟢 Active, released, partial eMule bridge
- Language/platform: Rust; daemon, CLI, embedded WebUI, containers, and
  optional Tauri desktop shell
- Link: https://github.com/ogarcia/rucio
- Repo stats (GitHub, 2026-10-23):
  - `ogarcia/rucio`: 53 stars, 2 forks, 2 open issues; default `master`;
    default-branch commit 2026-10-23 `b87f2f1` beginning `0.50.0`
    development; latest release `0.49.0` on 2026-10-23; GPL-3.0.
- Notes: New Rust P2P file-sharing product inspired by eMule and MLDonkey. Its
         primary network is a separate libp2p stack using Kademlia discovery,
         Gossipsub keyword search, BLAKE3 content identities, and `rucio:`
         links. The optional `rucio-emule` bridge can bootstrap Kad2, search
         keywords and sources, download `ed2k://` files, upload verified
         partial chunks, and continue seeding completed files. It is not a
         full eMule replacement: the audited scope has no eD2K server leg or
         AICH, intentionally omits RSA secure identification, and advertises
         no client-UDP reask, source exchange, or shared-directory browsing.
         The project has substantive Rust CI (`fmt`, Clippy with
         `-D warnings`, and all-feature tests); all checks on the reviewed
         default branch and `0.49.0` release commit passed, but its scripted
         E2E lane excludes the live eMule leg. The local HTTP API defaults to
         loopback but has no built-in authentication when exposed. Treat Rucio
         as a strong daemon/product-packaging and clean network-separation reference;
         require independent wire traces before using its eMule behavior as an
         oracle, and do not copy GPL-3.0-only implementation code into the
         GPL-2.0-only eMuleBB Rust tree.

#### aria2-next

- Assessment: **🟢 Active/current** · **🟢 Established** · **Released** · **Direct competitor/watchlist** · **🟢 Upload/share behavior documented**
- Status: 🟢 Active, released, needs protocol review
- Language/platform: C++20; Windows, macOS, Linux, and Android
- Link: https://github.com/AnInsomniacy/aria2-next
- Repo stats (GitHub, 2026-10-13):
  - `AnInsomniacy/aria2-next`: 666 stars, 28 forks, 2 open issues; default
    `main`; default-branch commit 2026-10-13 `612ffea`; latest release
    `v3.0.1` on 2026-10-13; GPL-2.0.
- Notes: New download engine preserving aria2 command-line, configuration,
         session, and JSON-RPC surfaces while adding a native eD2K/Kad
         implementation. Its README claims server and Kad source/search,
         verified transfers, upload queues, credits, obfuscation, persisted
         identity, sharing, and wire checks against aMule. Source review on
         2026-10-13 found that `ServerSession` offers at most the first 200
         shareable entries and repeats that selection every ten minutes; it
         has no continuation cursor or negotiated pace. Treat the broader
         claims as a strong interoperability lead, not an oracle, until code
         and live traces are independently reviewed. `FateLightX/AriaLite` is
         a current macOS front end that bundles this engine.

#### aMule

- Assessment: **🟢 Active/current** · **🟢 Established** · **Active development** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active
- Language/platform: Cross-platform C++/wxWidgets
- Current upstream: https://github.com/amule-org/amule (`master`; 3.1.0
  released 2026-09-21). The older `amule-project/amule` repository is the
  frozen predecessor, not the maintained upstream.
- Repo stats (GitHub, 2026-10-13):
  - `amule-org/amule`: 384 stars, 33 forks, 62 open issues; default `master`;
    default-branch commit 2026-10-13 `f9dba47`; latest release `3.1.0` on
    2026-09-21.
- Local reference (2026-10-19): managed `repos\amule` at
  `cfc357134e97561685a91c6822222493d39c7de2`; current source comparison,
  build, offline-fixture, and moving parity reference.
- Notes: The historical `emulebb/amule` Windows-build fork is retained as the
         `emulebb` remote in the same clone for provenance, not as a second
         checkout. Open PR `#1715` adds experimental, opt-in `offerfiles_v=1`
         client negotiation and reports isolated interoperability against
         `ed2k-server` source tag `v0.9.81`; production server-load validation
         and upstream review are still incomplete.

#### eMule Community

- Assessment: **🟢 Active/current** · **🟢 Established** · **Maintained** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Maintained
- Language/platform: Windows, C++/MFC
- Link: https://github.com/irwir/eMule
- Repo stats (GitHub, 2026-09-30):
  - `irwir/eMule`: 1287 stars, 114 forks, 0 open issues; default `master`;
    stable `eMule_v0.72a-community` release published 2026-08-20.
- Notes: Community continuation of classic eMule. Important compatibility and
         user-expectation reference. Local analysis checkouts track `v0.60d`
         and `v0.72a`, while managed app worktrees carry the community
         baseline and tracing harness branches. The `0.72a` train progressed
         from the June beta snapshots recorded previously to a stable GitHub
         release in August.

#### eMuleAI

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Active development** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active
- Language/platform: Windows, C++/MFC
- Link: https://github.com/eMuleAI/eMuleAI
- Repo stats (GitHub, 2026-09-30):
  - `eMuleAI/eMuleAI`: 70 stars, 7 forks, 29 open issues; default `master`;
    default-branch commit 2026-07-25 `a2f05dc`; latest release
    `eMuleAI_v1.6` on 2026-07-25.
- Notes: Modern eMule fork with UI, performance, and feature ideas already used as
         comparative reference in tooling docs.

### Tier 2 — Active or maintained, niche adoption

#### emulebb-rust

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Public beta** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active, public-beta forward client
- Language/platform: Rust; headless multiplatform daemon plus embedded SPA WebUI
- Link: https://github.com/emulebb/emulebb-rust
- Repo stats (GitHub, 2026-10-29):
  - `emulebb/emulebb-rust`: 9 stars, 0 forks, 32 open issues; default `main`;
    default-branch commit 2026-10-29 `17003d6`; public prerelease
    `rust-v0.1.0-beta.2` on 2026-10-02; nightly prereleases through
    2026-10-26; GPL-2.0.
- Notes: Workspace-owned forward eD2K/Kad client. It targets stock-compatible
         wire behavior while remaining a separate implementation from the MFC
         product. The public beta ships Windows, Linux, macOS, and container
         artifacts. CI, CodeQL, and Nightly workflows passed for the reviewed
         default-branch commit. The broader Client gate remains open, so do not infer stable
         release readiness from the beta or repository activity.

#### Ember

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active, protocol-extension caution
- Language/platform: Rust/Tauri/Svelte; Windows and Linux packages
- Link: https://github.com/untaimed18/Ember-P2P
- Repo stats (GitHub, 2026-10-23):
  - `untaimed18/Ember-P2P`: 31 stars, 0 forks, 6 open issues; default `main`;
    default-branch commit 2026-10-21 `9ebe026`; latest release `v1.7.4` on
    2026-10-18; GPL-3.0.
- Notes: Ground-up client that implements eD2K/Kad interoperation but also
         enables its own encrypted Ember DHT and an Ember-only peer-exchange
         opcode. Those additions make it a useful implementation and adoption
         lead, but not a stock-compatible default-behavior reference for
         eMuleBB. Its README documents remaining end-to-end gaps. All eight
         checks on the `v1.7.4` release commit passed, while two of seven checks
         on the reviewed default-branch commit were failing.

#### eMuleRust (`laurentgeynet-ux/eMule-Rust`)

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Direct competitor/watchlist** · **🟢 Upload/share behavior documented**
- Status: 🟢 Active, released candidate, independent verification required
- Language/platform: Rust/Flutter; Tokio daemon, JSON-RPC API, Windows and
  experimental Linux desktop bundles, CLI, and MCP server
- Link: https://github.com/laurentgeynet-ux/eMule-Rust
- Repo stats (GitHub, 2026-10-23):
  - `laurentgeynet-ux/eMule-Rust`: 5 stars, 0 forks, 15 open issues; default
    `master`; default-branch commit 2026-10-18 `fbbea83`; latest release
    `v0.2.0-RC3` on 2026-10-17; GPL-2.0-or-later.
- Notes: Young ground-up client targeting eMule 0.72a wire behavior. Source
         review found broad eD2K/Kad coverage including SX1/SX2, AICH, secure
         identification, client UDP, upload/download paths, and legacy import
         formats. All four checks on the reviewed default branch and all six
         release checks passed. The release reports pinned loopback
         interoperability with eMule 0.50a, eMule 0.72a, and aMule 3.1.0 plus
         a supervised public-network bench, but that evidence remains
         project-authored and needs independent traces before oracle use.
         Current docs retain gaps around peer chat/shared-file browsing,
         preview, outbound direct callback, and parts of port-test and Kad
         firewall behavior; the release also observed LowID despite UPnP.
         There is no fuzz or CodeQL workflow, and `cargo deny` is non-blocking.
         The protocol crate forbids unsafe code, but the daemon contains small
         Windows/ICMP unsafe FFI surfaces, so the README's tree-wide memory-
         safety wording is broader than the source.

#### Mulee

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active, new native macOS front end over aMule
- Language/platform: Swift/macOS application bundling `amuled`
- Link: https://github.com/cqagc/mulee
- Repo stats (GitHub, 2026-10-23):
  - `cqagc/mulee`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-17 `94556a0`; latest release `v0.1.11` on
    2026-10-17; GPL-3.0; no check runs on the reviewed commit.
- Notes: Polished Apple-Silicon download manager for HTTP, BitTorrent, eD2K,
         and video. It bundles a pinned aMule daemon as the eD2K engine and
         adds signed/notarized packaging, link handlers, browser extensions,
         native status surfaces, previews, sleep/disk handling, and port-
         forwarding guidance. Treat it as a product/UX and packaging
         reference, not an independent eD2K/Kad implementation.

#### eMule Qt

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active
- Language/platform: Qt 6/C++23
- Link: https://github.com/ModderMule/emule-qt
- Repo stats (GitHub, 2026-10-13):
  - `ModderMule/emule-qt`: 34 stars, 4 forks, 4 open issues; default `main`;
    default-branch commit 2026-10-13 `c502f60`; latest release `v0.6.12` on
    2026-10-13; GPL-2.0.
- Notes: Qt port intended to modernize the eMule client and improve platform
         independence. It remains an external research reference and is not
         materialized by the canonical workspace. Homepage:
         https://emule-qt.org/. The September release cadence makes it one of
         the most visibly active independent client implementations. Its
         current core keeps the stock-derived 200-file batch and 60-second
         spacing, making it a direct negotiated-pacing adoption candidate.

#### eMule Next

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active, beta
- Language/platform: Windows C++/MFC
- Link: https://github.com/favoritejonny/Emule-Next
- Repo stats (GitHub, 2026-10-13):
  - `favoritejonny/Emule-Next`: 8 stars, 0 forks, 0 open issues; default
    `main`; default-branch commit 2026-10-11 `5d69617`; `v1.0.0-beta.1`
    prerelease published 2026-09-27; GPL-2.0.
- Notes: Independent eMule Community fork with Win32/x64 portable packages,
         refreshed UI assets, 43 languages, CI, checksums, and SBOM release
         evidence. Treat it as a young fork and validate substantive runtime
         changes separately from packaging and presentation work.

#### eMuleBB

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Stable** · **Workspace baseline** · **❔ Contribution mode not independently classified**
- Status: 🟢 Maintained, stable `0.7.x` line
- Language/platform: Windows, C++/MFC
- Link: https://github.com/emulebb/emulebb
- Repo stats (GitHub, 2026-09-30):
  - `emulebb/emulebb`: 41 stars, 1 fork, 1 open issue; default `main`;
    default-branch commit 2026-09-25 `9466ece`; stable `0.7.3` released
    2026-07-05.
- Notes: Shipped Windows eMuleBB client with compatibility and release
         hardening. The MFC surface is frozen on the `0.7.x` maintenance line;
         active forward client work is in `emulebb-rust`.

#### eMule eSE LiveTV

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Active
- Language/platform: Windows, C++/Node.js
- Link: https://github.com/diad87/eMule-eSE-LiveTV
- Repo stats (GitHub, 2026-09-30):
  - `diad87/eMule-eSE-LiveTV`: 17 stars, 4 forks, 0 open issues; default
    `main`; default-branch commit 2026-08-02 `d08f8b0`.
- Notes: eMule mod exploring P2P live TV over Kad/eD2K with HLS and Node.js web UI.
         No local checkout was present in the canonical workspace during the
         2026-05-29 refresh.

#### macMule

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Maintained** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟢 Maintained, packaging-only
- Language/platform: macOS application bundle around eMule Community and Wine
- Link: https://github.com/mderouet/macMule
- Repo stats (GitHub, 2026-10-13):
  - `mderouet/macMule`: 23 stars, 2 forks, 0 open issues; default `master`;
    default-branch commit 2026-02-14 `511f3fe`; latest release `v0.70b` on
    2026-02-14; GPL-2.0.
- Notes: Build and packaging wrapper for running the current eMule Community
         x64 client through Wine on Apple Silicon and Intel macOS. It does not
         implement eD2K/Kad itself; protocol behavior remains the bundled
         eMule build's behavior.

### Tier 3 — Experimental or verification required

#### avwarez eMule build/fork

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Active, substantial patch stack needing provenance review
- Language/platform: Windows C++/MFC with a CMake build and dependency patch
  orchestration
- Link: https://github.com/avwarez/eMule-build and
        https://github.com/avwarez/eMule
- Repo stats (GitHub, 2026-10-23):
  - `avwarez/eMule-build`: 2 stars, 0 forks, 0 open issues; default `v0.72a`;
    default-branch commit 2026-10-23 `21adff6`; latest release
    `v0.72a-20260930-160400` on 2026-09-30; no GitHub-detected license; all
    seven checks on the reviewed commit passed.
- Notes: Builds a public eMule fork and pinned dependencies through CMake and
         carries a large ordered patch series for modern C++, legacy Windows
         removal, libplum port mapping, firewall diagnostics, PowerShare,
         warnings, robustness fixes, language corrections, and temporary
         diagnostics. The submodule URL uses SSH and the build repository
         lacks a root README/license declaration, so verify reproducibility,
         source/license provenance, and runtime behavior before treating the
         release as another maintained eMule distribution.

#### njMule

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Direct competitor/watchlist** · **🟢 Upload/share behavior documented**
- Status: 🟡 Active, pre-alpha
- Language/platform: Java 25; JavaFX desktop, web UI, and headless core
- Link: https://github.com/njMule/njMule
- Repo stats (GitHub, 2026-10-13):
  - `njMule/njMule`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-13 `aac6e33`; no public release; GPL-3.0.
- Notes: New eD2K/Kad client that claims server and Kad connectivity/search,
         verified downloads, upload queues, credits, secure identification,
         source exchange, shared files, and read-only eMule profile import.
         `FilePublisher` currently uses the stock-derived 200-file batch and
         60-second interval. The public repository was created on 2026-10-12
         and labels itself pre-alpha, so the broad surface needs independent
         code and runtime review before use as protocol evidence.

#### rmule

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Direct competitor/watchlist** · **🟢 Upload/share behavior documented**
- Status: 🟡 Active, early release
- Language/platform: Rust; terminal UI and headless CLI
- Link: https://github.com/Lazark0x/rmule
- Repo stats (GitHub, 2026-10-13):
  - `Lazark0x/rmule`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-12 `63ee533`; latest release `v0.2.0` on
    2026-10-12; GPL-3.0.
- Notes: New library-first eD2K/Kad client with server login/search, Kad,
         peer transfer, shared-file registration, upload handling, persisted
         state, and a parity matrix tied to aMule source and captured bytes.
         Its current session follower sends the complete share set in one
         `OP_OFFERFILES` command rather than applying a stock or negotiated
         batch/pacing policy. Its README still records missing or intentionally
         omitted surfaces, including Kad notes and shared-directory browsing.
         Review actual publication scheduling and live behavior before
         treating it as a compatibility reference.

#### aMule Android Preview

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Active, native preview requiring runtime and provenance review
- Language/platform: Kotlin/Jetpack Compose Android shell with ARM64 aMule
  daemon and WebUI binaries
- Link: https://github.com/XG-DL/amule-android-preview
- Repo stats (GitHub, 2026-10-23):
  - `XG-DL/amule-android-preview`: 1 star, 0 forks, 0 open issues; default
    `main`; reviewed default-branch commit 2026-10-08 `b856d04`; latest
    release `v0.1.9-native-preview` on 2026-10-15; all four checks on the
    reviewed commit passed; GitHub reports no recognized repository license.
- Notes: Packages patched, pinned `amule-org/amule` `amuled` and `amuleapi`
         builds for Android API 33/ARM64 and documents reproducible dependency
         downloads with hashes. IPv6, geolocation, uTP, QUIC, and native
         translation catalogs are disabled in the packaged core. It is a
         useful mobile lifecycle and packaging lead, but not an independent
         protocol implementation; verify binary/source correspondence and
         repository licensing before reuse.

#### Kelpie

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Active, new engine requiring independent live verification
- Language/platform: Go engine process with a standard-library Python asyncio
  client
- Link: https://github.com/XiaoYouChR/Kelpie
- Repo stats (GitHub, 2026-10-23):
  - `XiaoYouChR/Kelpie`: 6 stars, 1 fork, 0 open issues; default `main`;
    default-branch commit 2026-10-02 `c3c475a`; latest release `v0.2.0` on
    2026-10-02; MIT license; all nine checks on the reviewed commit passed.
- Notes: New download/upload engine descended from ideas in `goed2k` and the
         earlier `Python-eD2k` process boundary. Its source tree contains
         distinct server, Kad, peer, upload, obfuscation, AICH, secure-ident,
         NAT, disk, and fake-server components plus extensive Go/Python tests.
         The README claims LowID callbacks, SX2, UDP reask, secure
         identification, global server search, uploads, IPv6 peer exchange,
         and benchmarks against aMule and `goed2kd`. Development visible in
         the reviewed repository is concentrated on 2026-10-01/02, so those
         compatibility and performance claims remain project-authored until
         reproduced with independent traces.

#### AmuleD v2 Python

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Active, broad claims without independent evidence
- Language/platform: Python 3.12 console client and daemon
- Link: https://github.com/Methelina/AmuleD_v2_KAD-eD2k_Python
- Repo stats (GitHub, 2026-10-23):
  - `Methelina/AmuleD_v2_KAD-eD2k_Python`: 0 stars, 0 forks, 0 open issues;
    default `main`; default-branch commit 2026-09-29 `041b5cd`; no GitHub
    release or check runs; Apache-2.0.
- Notes: Independent clean-room claim with a substantial source and test tree
         covering server sessions, Kad search/publish, downloads, uploads,
         AICH, source exchange, secure identification, obfuscation, buddies,
         callbacks, NAT traversal, IP filtering, and persistent state. The
         README reports live KAD operations and a 46.7 MB multi-part download
         from eMuleAI, but the repository provides no CI result, signed
         release, or independently captured interoperability record. Treat
         its unusually broad `0.6.0` feature matrix as a verification target,
         not as protocol authority.

#### padMule

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Direct competitor/watchlist** · **🟡 Full peer with optional policy-incompatible Leech Mode**

> 🟡 **Policy warning:** The documented optional Leech Mode conflicts with eMuleBB contribution policy.
- Status: 🟡 Active, experimental, agent-assisted
- Language/platform: Rust engine with native SwiftUI iPad app
- Link: https://github.com/ajbufort/padMule
- Repo stats (GitHub, 2026-09-30):
  - `ajbufort/padMule`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-08-14 `ce2d91b`; GPL-2.0; no releases.
- Notes: From-scratch iPad client with Rust protocol, file-format, Kad, engine,
         CLI, and UniFFI crates behind a native SwiftUI app. The repository
         explicitly documents coordinated Claude-agent development, treats
         eMule 0.50a as wire authority, vendors aMule 3.0.1 as a read-only
         runnable oracle, and carries differential-transfer scripts, fuzz
         targets, supply-chain checks, and claimed on-device evidence. It is a
         high-value clean-room interoperability and mobile-lifecycle reference,
         not yet an independently verified authority. Its optional Leech Mode
         and padMule-to-padMule enhancement channel conflict with eMuleBB policy;
         review those boundaries before borrowing behavior. The source license
         is described as GPL-2.0-or-later, while its own notice says some linked
         binary configurations convey under GPL-3.0-or-later.

#### MLDonkey

- Assessment: **🟡 Verification needed** · **🟡 Visible** · **Stale** · **Direct competitor/watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Maintained/stale
- Language/platform: OCaml daemon
- Link: https://github.com/ygrek/mldonkey
- Repo stats (GitHub, 2026-05-29):
  - `ygrek/mldonkey`: 339 stars, 53 forks, 54 open issues; default `master`; default-branch commit 2025-01-28 `0d44635`.
- Notes: Multi-network P2P daemon with eDonkey/eMule support; useful for headless
         daemon and controller ideas.

#### HydraP2P

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Experimental** · **Ecosystem watchlist** · **🟢 Upload/share behavior documented**
- Status: 🟡 Needs verification
- Language/platform: Unknown
- Link: Public discussion lead only
- Notes: Mentioned in 2026 I2P/eMule discussion as a beta project associated
         with Sharing-Devils and possible I2P-oriented evolution. No canonical
         source, binary, website, protocol scope, or license was confirmed in
         the 2026-09-30 search pass.

#### iMule

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Reference-only** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Historical, needs verification
- Language/platform: C++/I2P
- Link: Public mirrors
- Notes: Anonymous/I2P-oriented eMule lineage; verify canonical source before using as
         reference.

#### xMule/lMule

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Reference-only** · **Ecosystem watchlist** · **❔ Contribution mode not independently classified**
- Status: 🟡 Historical, needs verification
- Language/platform: Linux C++
- Link: SourceForge and mirrors
- Notes: Pre-aMule Linux lineage; keep as research leads until canonical
         source/archive links are verified.

### Tier 4 — Stale or historical

#### Envy

- Assessment: **⚫ Stale/historical** · **🟡 Visible** · **Stale** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: ⚫ Stale, isolated 2026 build refresh
- Language/platform: Windows C++
- Link: https://github.com/GetEnvy/Envy
- Repo stats (GitHub, 2026-09-30):
  - `GetEnvy/Envy`: 51 stars, 12 forks, 11 open issues; default `master`;
    default-branch commit 2026-08-07 `7737356` (`VS2026`).
- Notes: Shareaza-derived multi-network client. One build-oriented commit after
         a six-year gap is not enough evidence to classify the project as
         maintained.

#### Hathi

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **🟢 Upload/share behavior documented**
- Status: ⚫ Historical
- Language/platform: C#/.NET
- Link: https://github.com/lle0x/hathi
- Repo stats (GitHub, 2026-05-29):
  - `lle0x/hathi`: 1 star, 0 forks, 1 open issue; default `main`; default-branch commit 2022-04-18 `b87ce11`.
- Notes: Fork of lphant 1.0, described as an eDonkey2000 filesharing client.

#### Shareaza

- Assessment: **⚫ Stale/historical** · **🟡 Visible** · **Stale** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: ⚫ Stale
- Language/platform: Windows C++
- Link: https://github.com/ivan386/Shareaza
- Repo stats (GitHub, 2026-05-29):
  - `ivan386/Shareaza`: 123 stars, 50 forks, 9 open issues; default `ipv6`; default-branch commit 2019-08-07 `0c2f2f5`.
- Notes: Multi-network P2P client with eD2K support. Historical UX and protocol
         reference.

#### JMule

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: ⚫ Historical
- Language/platform: Java
- Link: https://github.com/zhoushineyoung/jmule-mod
- Repo stats (GitHub, 2026-05-29):
  - `zhoushineyoung/jmule-mod`: 2 stars, 3 forks, 0 open issues; default `master`; default-branch commit 2015-02-22 `b6dac44`.
- Notes: Java implementation lineage for eMule/eD2K protocol behavior.

#### Lphant

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: ⚫ Historical
- Language/platform: C#/.NET
- Link: https://github.com/knocte/lphant
- Repo stats (GitHub, 2026-05-29):
  - `knocte/lphant`: 25 stars, 6 forks, 0 open issues; default `master`; default-branch commit 2012-05-19 `c16be38`.
- Notes: GPL-era lphant source mirror; useful for old client behavior comparisons.

#### eMule Plus

- Assessment: **🟣 Archive/reference** · **❔ Unknown** · **Reference-only** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: 🟣 Historical, archive-only
- Language/platform: Windows C++
- Link: Local archive evidence
- Notes: Independent eMule-derived client line. Keep source provenance notes in
         historical sections when used.

#### p2p-overlord

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **❔ Contribution mode not independently classified**
- Status: ⚫ Historical, archived
- Language/platform: Rust/Node
- Link: https://github.com/emulebb/p2p-overlord-agents and
        https://github.com/emulebb/p2p-overlord-be
- Repo stats (GitHub, 2026-09-30):
  - `emulebb/p2p-overlord-agents` and `emulebb/p2p-overlord-be` are both
    archived; their last default-branch commits are from 2026-06-11.
- Notes: Retired separate headless/server-oriented product lineage. It is not
         part of the current eMuleBB portfolio; retain only for historical contract
         and architecture research.

### Capability warning — Download-only clients

#### FluxDown

- Assessment: **🟢 Active/current** · **🟢 Established** · **Active development** · **Direct competitor/watchlist** · **🔴 Download-only; no upload contribution**

> 🔴 **Capability warning:** This implementation is explicitly download-only and does not upload or share. It is excluded from healthy-peer rankings.
- Status: 🟢 Active, popular download-only implementation
- Language/platform: Rust engine with desktop, Web, Android, and iOS clients
- Link: https://github.com/zerx-lab/FluxDown
- Repo stats (GitHub, 2026-10-23):
  - `zerx-lab/FluxDown`: 4,927 stars, 290 forks, 369 open issues; default
    `main`; default-branch commit 2026-10-23 `9308448`; latest release
    `v0.6.1` on 2026-10-23; AGPL-3.0; all 16 checks on the reviewed commit
    passed.
- Notes: Contains a native Rust eD2K engine rather than link handoff, with
         server subscriptions, server and Kad source discovery, peer
         transfers, UPnP, per-part MD4 verification, resume, and cross-client
         settings surfaces. Its own documentation explicitly calls the engine
         download-only: it does not upload or share, ignores optional AICH
         link data, and therefore is not a full stock-client behavior oracle.
         The large audience and polished multi-platform product surface make
         it strategically important despite that protocol asymmetry.

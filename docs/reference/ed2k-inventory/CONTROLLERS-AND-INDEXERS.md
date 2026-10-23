# Controllers, Indexers, and Automation

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

Automation layers, Arr adapters, native remote applications, WebUIs, containers, and indexers around eMule and aMule.

Ranking badges and thresholds are defined in [Methodology](METHODOLOGY.md). Statistics are dated snapshots, not live user counts.

## Controllers, Indexers, And Automation

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| Mularr | 🟢 Active/current | 🟡 Visible | Active development | Ecosystem dependency | 2026-10-07 |
| docker-amule | 🟢 Active/current | 🟡 Visible | Maintained | Ecosystem dependency | 2026-09-22 |
| aMulerr (formerly eMulerr) | 🟢 Active/current | 🟡 Visible | Active development | Ecosystem dependency | 2026-07-15 |
| amarr | 🟢 Active/current | 🟡 Visible | Active development | Ecosystem dependency | 2026-05-06 |
| aMule Remote | 🟢 Active/current | ⚪ Niche | Released | Ecosystem dependency | 2026-10-21 |
| hispamula-indexer | 🟢 Active/current | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-12 |
| aMule Nuxt | 🟢 Active/current | ⚪ Niche | Active development | Ecosystem dependency | 2026-10-04 |
| TransMule | 🟢 Active/current | ⚪ Niche | Active development | Ecosystem dependency | 2026-09-29 |
| aMule React UI | 🟢 Active/current | ⚪ Niche | Released | Ecosystem dependency | 2026-09-27 |
| aMule M26 | 🟢 Active/current | ⚪ Niche | Active development | Ecosystem dependency | 2026-07-03 |
| goed2kd | 🟢 Active/current | ⚪ Niche | Maintained | Ecosystem dependency | 2026-04-09 |
| Mularr Home Assistant integration | 🟡 Verification needed | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-23 |
| aMulio | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem dependency | 2026-10-13 |
| p2pwatch | 🟡 Verification needed | ⚪ Niche | Active development | Ecosystem dependency | 2026-10-13 |
| TauriMule | 🟡 Verification needed | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-05 |
| aMule Modern | 🟡 Verification needed | ⚪ Niche | Experimental | Ecosystem dependency | 2026-10-02 |
| aMularr (`manuel-alcocer/amularr`) | 🟡 Verification needed | ⚪ Niche | Experimental | Ecosystem dependency | 2026-09-15 |
| GM_EmuleLinker | 🟡 Verification needed | ⚪ Niche | Stale | Ecosystem dependency | 2026-03-17 |
| ed2k-indexer | 🟡 Verification needed | ⚪ Niche | Stale | Ecosystem dependency | 2026-03-17 |
| aMule web controllers | 🟡 Verification needed | ❔ Unknown | Experimental | Ecosystem dependency | Unknown |
| aMuTorrent | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2026-07-05 |

### Tier 1 — Active with visible adoption

#### Mularr

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active
- Language/platform: Web/Docker
- Link: https://github.com/joecarl/mularr
- Repo stats (GitHub, 2026-10-23):
  - `joecarl/mularr`: 176 stars, 5 forks, 5 open issues; default `main`;
    default-branch commit 2026-10-07 `c6dceda`; latest release `v1.0.0` on
    2026-10-07; MIT license.
- Notes: New aMule-focused web UI and automation project with *Arr, Gluetun,
         Telegram, qBittorrent-compatible, and Torznab-compatible surfaces.
         Treat as a fresh controller lead until source and runtime behavior are
         reviewed.

#### docker-amule

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Maintained** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Maintained
- Language/platform: Docker
- Link: https://github.com/ngosang/docker-amule
- Repo stats (GitHub, 2026-09-30):
  - `ngosang/docker-amule`: 270 stars, 19 forks, 3 open issues; default
    `master`; default-branch commit 2026-09-22 `4946742`; latest release
    `3.1.0-1` on 2026-09-21.
- Notes: Containerized aMule deployment; useful for repeatable controller and headless
         scenarios.

#### aMulerr (formerly eMulerr)

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active
- Language/platform: JavaScript/Docker
- Link: https://github.com/isc30/aMulerr
- Repo stats (GitHub, 2026-09-30):
  - `isc30/aMulerr`: 93 stars, 6 forks, 5 open issues; default `main`;
    default-branch commit 2026-07-15 `cc93714`.
- Notes: Radarr/Sonarr bridge for eD2K/Kad. Emulates a qBittorrent API and
         exposes a Torznab surface. GitHub redirects the old `eMulerr` slug to
         `aMulerr`, and the current README explicitly calls aMulerr its
         successor; use the new name and URL in maintained references.

#### amarr

- Assessment: **🟢 Active/current** · **🟡 Visible** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active
- Language/platform: Kotlin/JVM
- Link: https://github.com/vexdev/amarr
- Repo stats (GitHub, 2026-09-30):
  - `vexdev/amarr`: 61 stars, 6 forks, 31 open issues; default `main`;
    default-branch commit 2026-05-06 `0876bfd`; latest release `v1.6.2` on
    2026-05-06; MIT license.
- Notes: aMule connector for Sonarr/Radarr that emulates a torrent client and can
         integrate Torznab-style indexers. No local checkout was present in the
         canonical workspace during the 2026-05-29 refresh.

### Tier 2 — Active or maintained, niche adoption

#### aMule Remote

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Released** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active, released native remote controller
- Language/platform: Swift for macOS, iOS/iPadOS, visionOS, tvOS, and watchOS
- Link: https://github.com/sidimam/AmuleRemote
- Repo stats (GitHub, 2026-10-23):
  - `sidimam/AmuleRemote`: 0 stars, 0 forks, 1 open issue; default `main`;
    default-branch commit 2026-10-21 `c646928`; latest release
    `v1.5-build26` on 2026-10-21; MIT license; all three checks on the
    reviewed commit passed.
- Notes: Native Apple-platform controller that speaks aMule's External
         Connections protocol and is distributed through the App Store, DMG,
         and Homebrew. It materially broadens remote-device UX but delegates
         all eD2K/Kad behavior to `amuled`; use as EC and product reference
         only.

#### hispamula-indexer

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active, new integration
- Language/platform: Python/FastAPI/Docker
- Link: https://github.com/ascalotoru/hispamula-indexer
- Repo stats (GitHub, 2026-10-13):
  - `ascalotoru/hispamula-indexer`: 0 stars, 0 forks, 0 open issues; default
    `master`; default-branch commit 2026-10-12 `4e8686b`; latest release
    `v1.0.4` on 2026-10-12; Apache-2.0.
- Notes: Authenticated Torznab/Newznab scraper for a public eD2K-link catalog.
         It emits real `ed2k://` identities through an aMulerr-compatible
         magnet wrapper for downstream aMule workflows; it does not itself
         query, serve, or publish on the eD2K/Kad networks.

#### aMule Nuxt

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active, needs security/runtime review
- Language/platform: TypeScript/Nuxt/Docker
- Link: https://github.com/JuanmanDev/amule-nuxt
- Repo stats (GitHub, 2026-10-13):
  - `JuanmanDev/amule-nuxt`: 3 stars, 0 forks, 2 open issues; default
    `master`; default-branch commit 2026-10-04 `a8aae22`; latest release
    `v1.20.0` on 2026-10-04; MIT license.
- Notes: Modern aMule WebUI that implements the EC protocol directly in
         TypeScript and adds HTTP/JSON, WebSocket updates, scheduled search,
         a browser demo, and an MCP control surface. The README warns that the
         MCP endpoint is unauthenticated; keep it on a trusted network or
         behind authentication. Useful EC/API/UI reference after code and live
         behavior review.

#### TransMule

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active
- Language/platform: Vue/Node.js/Docker
- Link: https://github.com/Jo3l/transmule
- Repo stats (GitHub, 2026-09-30):
  - `Jo3l/transmule`: 44 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-09-29 `2165a03`.
- Notes: Self-hosted download manager that unifies aMule ED2K/Kademlia,
         Transmission, and pyLoad. Useful as a modern aMule-control UI and
         file-management reference; verify ED2K search/indexer behavior before
         using it as a Servarr bridge reference.

#### aMule React UI

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Released** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active, released aMule 3.1 WebUI alternative
- Language/platform: React/TypeScript/Docker over `amuleapi`
- Link: https://github.com/alvarogl/amule-react-ui
- Repo stats (GitHub, 2026-10-23):
  - `alvarogl/amule-react-ui`: 1 star, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-09-27 `45c4886`; latest release `v1.1.2` on
    2026-09-24; MIT license; three reviewed checks passed and one was
    cancelled.
- Notes: Full browser controller for aMule 3.1's REST/SSE `amuleapi`, covering
         authentication, transfers, search, servers, Kad, shared files,
         peers, categories, preferences, logs, and statistics. The repository
         includes API tests, browser E2E coverage, container packaging, and
         deployment guidance. It is a UI/control reference and delegates all
         network behavior to aMule.

#### aMule M26

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Active, needs runtime review
- Language/platform: Web template / Docker
- Link: https://github.com/jjling2011/amule-m26
- Repo stats (GitHub, 2026-09-30):
  - `jjling2011/amule-m26`: 0 stars, 0 forks; default `main`;
    default-branch commit 2026-07-03 `5b54091`; latest release `v0.1.3` on
    2026-06-07.
- Notes: Modern aMule WebUI template packaged around the `ngosang/docker-amule`
         configuration model. Useful UI/packaging lead; not a protocol
         implementation by itself.

#### goed2kd

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Maintained** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟢 Maintained/early
- Language/platform: Go daemon/API
- Link: https://github.com/chenjia404/goed2kd
- Repo stats (GitHub, 2026-09-30):
  - `chenjia404/goed2kd`: 2 stars, 1 fork, 0 open issues; default `master`;
    default-branch commit 2026-04-09 `14d7139`; no recognized license
    reported by GitHub.
- Notes: Headless daemon over `goed2k` with HTTP/JSON RPC and WebSocket events
         for server/Kad control, downloads, search, shared files, state, and
         future WebUI integration. Distinct from `goed2k-server`, which is a
         network index server rather than a client daemon.

### Tier 3 — Experimental or verification required

#### Mularr Home Assistant integration

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, new derivative integration
- Language/platform: Python Home Assistant custom component/HACS package
- Link: https://github.com/evlas/Mularr
- Repo stats (GitHub, 2026-10-23):
  - `evlas/Mularr`: 1 star, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-23 `c3606d7`; latest release `v0.0.3` on
    2026-10-23; GPL-3.0; all five checks on the reviewed commit passed.
- Notes: Home Assistant integration for monitoring and automating a Mularr
         instance through sensors, switches, buttons, and a coordinator/API
         layer. It is two controller layers removed from the wire and should
         be evaluated for home-automation UX only.

#### aMulio

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, incomplete end-to-end media integration
- Language/platform: Python/FastAPI Stremio bridge over aMule 3.1 `amuleapi`
- Link: https://github.com/alexruperez/amulio
- Repo stats (GitHub, 2026-10-23):
  - `alexruperez/amulio`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-13 `3c05beb`; no public release;
    Apache-2.0; all 13 checks on the reviewed commit passed.
- Notes: Exposes a self-hosted aMule library as a private Stremio catalog,
         uses signed stream URLs, enqueues selected eD2K links, and streams
         completed files from allowlisted paths. Its README says live
         discovery, queueing, progress, and cancellation are validated while
         controlled completion/playback remains pending. It is a controller
         and media UX reference, not an eD2K/Kad implementation.

#### p2pwatch

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, needs privacy/runtime review
- Language/platform: Python
- Link: https://github.com/mission-titar/p2pwatch
- Repo stats (GitHub, 2026-10-13):
  - `mission-titar/p2pwatch`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-13 `ba32bc0`; latest release `v4.1.0` on
    2026-10-05; AGPL-3.0.
- Notes: Continuous eD2K/Kad crawler and indexer for recovery-oriented
         searches. The project states that it records file observations and
         protocol-provided pseudonymous source identifiers but not peer IPs,
         ports, or countries. Review protocol completeness, retention,
         consent, and deployment behavior independently before reuse.

#### TauriMule

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, new alpha
- Language/platform: Rust/Tauri/TypeScript Windows front end over `amuled`
- Link: https://github.com/alexwing/Taurimule
- Repo stats (GitHub, 2026-10-13):
  - `alexwing/Taurimule`: 2 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-05 `31998d7`; release `v0.3.0` on
    2026-10-05; GPL-3.0.
- Notes: New lightweight Windows UI/orchestration layer that bundles or drives
         the existing aMule daemon through the External Connections protocol;
         it does not implement the eD2K/Kad wire. The initial repository was
         produced in seven commits on one day and already included a broad UI,
         four translations, manuals, screenshots, and release packaging. That
         is evidence of rapid or agent-accelerated construction, not by itself
         evidence of runtime maturity; the author does not explicitly label it
         vibe-coded. Track its multi-tab search, import, filename-cleanup,
         Tauri/EC, and desktop-packaging ideas. Verify the bundled `amuled`
         binary's provenance, redistribution terms, EC coverage, and live
         behavior before treating the package as a compatibility reference.

#### aMule Modern

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, new desktop shell needing runtime review
- Language/platform: C#/Avalonia desktop front end for aMule 3.0.1
- Link: https://github.com/eduardoddddddd/amule-modern
- Repo stats (GitHub, 2026-10-23):
  - `eduardoddddddd/amule-modern`: 0 stars, 0 forks, 0 open issues; default
    `main`; default-branch commit 2026-10-02 `40fc1b9`; no release or check
    runs; GPL-2.0.
- Notes: Windows/macOS shell that controls a local aMule daemon over EC. The
         source includes tests and launch/build scripts but no reviewed CI or
         release artifacts. Treat its desktop composition and EC mapping as a
         fresh lead, not as proof of complete aMule behavior.

#### aMularr (`manuel-alcocer/amularr`)

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active, new and independently unverified
- Language/platform: Python/FastAPI/Docker
- Link: https://github.com/manuel-alcocer/amularr
- Repo stats (GitHub, 2026-10-23):
  - `manuel-alcocer/amularr`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-09-15 `779af38`; no public release or
    GitHub-detected license; all four checks on the reviewed commit passed.
- Notes: Separate from both `aMulerr` and `amarr`. It implements a Torznab
         indexer and qBittorrent-compatible download-client bridge while
         speaking aMule's External Connections protocol directly. The source
         includes unit/integration tests and container deployment, but its EC
         coverage, authentication boundaries, queue semantics, and license
         need review before reuse.

#### GM_EmuleLinker

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Stale** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active/stale
- Language/platform: JavaScript/userscript
- Link: https://github.com/alo0/GM_EmuleLinker
- Repo stats (GitHub, 2026-05-29):
  - `alo0/GM_EmuleLinker`: 5 stars, 1 fork, 0 open issues; default `master`; default-branch commit 2026-03-17 `7e4223d`.
- Notes: Browser helper for sending ED2K links to remote eMule/aMule/MLDonkey/system
         handlers.

#### ed2k-indexer

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Stale** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Active/stale
- Language/platform: Python
- Link: https://github.com/tronarite/ed2k-indexer
- Repo stats (GitHub, 2026-05-29):
  - `tronarite/ed2k-indexer`: 0 stars, 0 forks, 0 open issues; default `main`; default-branch commit 2026-03-17 `a3e8ccc`.
- Notes: Self-hosted Torznab-compatible indexer for Radarr/Sonarr and eMule workflows.

#### aMule web controllers

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Experimental** · **Ecosystem dependency** · **Controller/indexer role**
- Status: 🟡 Needs verification
- Language/platform: Web/API tooling
- Link: Public search lead
- Notes: Generic bucket for web/API control projects not yet split out above.
         Current named examples include aMuTorrent, TransMule, Mularr, aMulerr,
         amarr, aMularr, aMulio, aMule Nuxt, TauriMule, aMule Remote, aMule
         Modern, and goed2kd.

### Tier 4 — Stale or historical

#### aMuTorrent

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **Controller/indexer role**
- Status: ⚫ Historical, frozen `0.7.3` release companion
- Language/platform: Node.js/React/Docker
- Link: https://github.com/emulebb/amutorrent
- Repo stats (GitHub, 2026-09-30):
  - `emulebb/amutorrent`: 2 stars, 0 forks, 17 open issues; default `main`;
    default-branch commit 2026-07-05 `9e5de44`; MIT license.
- Notes: Unified download manager for aMule, eMuleBB, and BitTorrent clients;
         the eMuleBB fork is the frozen browser controller shipped with the
         `0.7.3` line, not the forward controller product. It exposes ED2K
         workflows through Torznab and qBittorrent-compatible APIs for
         Sonarr/Radarr. The upstream `got3nks/amule-web-controller` slug
         redirects to `got3nks/amutorrent`.

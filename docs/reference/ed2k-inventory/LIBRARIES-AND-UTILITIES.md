# Protocol Libraries and Utilities

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

Reusable eD2K/Kad libraries, hashing and AICH tools, diagnostics, EC utilities, and protocol experiments.

Ranking badges and thresholds are defined in [Methodology](METHODOLOGY.md). Statistics are dated snapshots, not live user counts.

## Protocol Libraries And Utilities

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| Python-eD2k | 🟢 Active/current | ⚪ Niche | Experimental | Component candidate | 2026-09-27 |
| ed2k-ruby | 🟢 Active/current | ⚪ Niche | Maintained | Component candidate | 2026-08-03 |
| goed2k | 🟢 Active/current | ⚪ Niche | Active development | Component candidate | 2026-06-02 |
| jaMule | 🟢 Active/current | ⚪ Niche | Maintained | Component candidate | 2026-05-06 |
| ed2k-vault | 🟡 Verification needed | ⚪ Niche | Experimental | Component candidate | 2026-10-23 |
| nodemule | 🟡 Verification needed | ⚪ Niche | Experimental | Component candidate | 2026-10-22 |
| eNodeMeta | 🟡 Verification needed | ⚪ Niche | Active development | Component candidate | 2026-10-21 |
| eMule Kad extraction (`avwarez/eMule-kad`) | 🟡 Verification needed | ⚪ Niche | Active development | Component candidate | 2026-10-19 |
| eMule HTTP Cache | 🟡 Verification needed | ⚪ Niche | Active development | Component candidate | 2026-10-06 |
| aMule EC Profiler | 🟡 Verification needed | ⚪ Niche | Experimental | Component candidate | 2026-07-30 |
| KadGlobe | 🟡 Verification needed | ⚪ Niche | Active development | Component candidate | 2026-05-19 |
| jed2k | 🟡 Verification needed | 🟡 Visible | Stale | Component candidate | 2023-09-03 |
| kadkad | 🟡 Verification needed | ❔ Unknown | Experimental | Component candidate | Unknown |
| rust2k | 🟡 Verification needed | ❔ Unknown | Experimental | Component candidate | Unknown |
| ed2k Rust crate | ⚫ Stale/historical | ⚪ Niche | Stale | Historical reference | 2023-05-20 |
| ged2k | ⚫ Stale/historical | ⚪ Niche | Stale | Historical reference | 2023-04-13 |
| libed2k/qmule | ⚫ Stale/historical | 🟡 Visible | Stale | Historical reference | 2016-06-02 |
| goe2k | 🟣 Archive/reference | ❔ Unknown | Reference-only | Historical reference | Unknown |

### Tier 2 — Active or maintained, niche adoption

#### Python-eD2k

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟢 Active, early
- Language/platform: Python asyncio client with Go sidecar
- Link: https://github.com/XiaoYouChR/Python-eD2k
- Repo stats (GitHub, 2026-09-30):
  - `XiaoYouChR/Python-eD2k`: 5 stars, 1 fork, 0 open issues; default `main`;
    default-branch commit 2026-09-27 `3546c46`; MIT license.
- Notes: Typed Python integration layer that keeps `goed2k` networking and
         durable state in a Go sidecar and uses NDJSON over stdio. Useful as a
         process-boundary and Python-controller reference, not an independent
         wire-protocol implementation.

#### ed2k-ruby

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Maintained** · **Component candidate** · **Library/tool role**
- Status: 🟢 Maintained
- Language/platform: Ruby
- Link: https://github.com/edelkas/ed2k-ruby
- Repo stats (GitHub, 2026-09-30):
  - `edelkas/ed2k-ruby`: 0 stars, 0 forks, 0 open issues; default `master`;
    default-branch commit 2026-08-03 `3309d75`.
- Notes: Ruby implementation of eD2K/eDonkey2000 and extended eMule protocol concepts.

#### goed2k

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Active development** · **Component candidate** · **Library/tool role**
- Status: 🟢 Active
- Language/platform: Go
- Link: https://github.com/monkeyWie/goed2k
- Repo stats (GitHub, 2026-09-30):
  - `monkeyWie/goed2k`: 9 stars, 3 forks, 2 open issues; default `main`;
    default-branch commit 2026-06-02 `f2a71d5`; MIT license.
- Notes: Go ED2K client/library with `server.met`, server connection, Kad
         bootstrap/source lookup, search, downloads, upload, UPnP, and terminal UI
         support.

#### jaMule

- Assessment: **🟢 Active/current** · **⚪ Niche** · **Maintained** · **Component candidate** · **Library/tool role**
- Status: 🟢 Maintained
- Language/platform: Java
- Link: https://github.com/vexdev/jamule
- Repo stats (GitHub, 2026-09-30):
  - `vexdev/jamule`: 6 stars, 0 forks, 1 open issue; default `main`;
    default-branch commit 2026-05-06 `7aa8ff4`; MIT license.
- Notes: Java aMule External Connections protocol client used by amarr. The
         canonical source is now confirmed; this is controller protocol code,
         not an eD2K/Kad wire library.

### Tier 3 — Experimental or verification required

#### ed2k-vault

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, new hashing utility with edge cases still open
- Language/platform: Rust CLI and Slint GUI
- Link: https://github.com/L-at-nnes/ed2k-vault
- Repo stats (GitHub, 2026-10-23):
  - `L-at-nnes/ed2k-vault`: 4 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-23 `f7cc20d`; latest release `v0.1.1` on
    2026-10-23; MIT license; all ten checks on the reviewed commit passed.
- Notes: Generates eD2K links, part hashsets, AICH roots, HTML/CSV output, and
         `.emulecollection` files for large directory trees with incremental
         caching and parallel hashing. The author explicitly requests eMule
         fixtures for exact-part-size MD4 behavior and filename percent-
         encoding, so keep it out of compatibility fixtures until those
         boundaries are cross-checked against stock output.

#### nodemule

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, new search-only protocol library
- Language/platform: Node.js ESM/TypeScript declarations
- Link: https://github.com/seancheung/nodemule
- Repo stats (GitHub, 2026-10-23):
  - `seancheung/nodemule`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-22 `2e845ac`; no GitHub release;
    GPL-2.0; all four checks on the reviewed commit passed.
- Notes: Zero-runtime-dependency search client for eD2K server TCP/UDP and
         Kad2 UDP, with `server.met`/`nodes.dat` loaders, concurrent server
         pools, streamed merged results, filters, tests, and typed exports.
         It explicitly does not download, upload, or share files, and labels
         `0.1.0` experimental despite exercised public searches. Useful as a
         compact search-codec/API reference after independent packet review.

#### eNodeMeta

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, extension library with no recognized license
- Language/platform: Go/gRPC metadata library
- Link: https://github.com/ModderMule/enodemeta
- Repo stats (GitHub, 2026-10-23):
  - `ModderMule/enodemeta`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-21 `7b143c6`; no public release or
    GitHub-detected license; the single reviewed check passed.
- Notes: Metadata/link/container model for eMule Qt spanning torrent, Usenet,
         Kademlia, eD2K, magnet, NZB, and Web links. It is an application-
         internal gRPC data contract, not a stock eD2K/Kad wire library.
         Review license and generated-code provenance before any reuse.

#### eMule Kad extraction (`avwarez/eMule-kad`)

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, extracted source needing build and provenance review
- Language/platform: C++/CMake library and CLI
- Link: https://github.com/avwarez/eMule-kad
- Repo stats (GitHub, 2026-10-23):
  - `avwarez/eMule-kad`: 0 stars, 0 forks, 0 open issues; default `master`;
    default-branch commit 2026-10-19 `56d2126`; no public release or check
    runs; GPL-2.0.
- Notes: Extracts the Kad implementation from eMule Community 0.72a into a
         standalone CMake-shaped tree with a CLI. The repository has no
         README, CI, or visible compatibility record; treat it as a source-
         organization experiment and GPL reference, not an independently
         maintained Kad library.

#### eMule HTTP Cache

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, non-stock eMule Qt extension
- Language/platform: Go server with a parallel PHP reference implementation
- Link: https://github.com/ModderMule/emule-http-cache-go
- Repo stats (GitHub, 2026-10-23):
  - `ModderMule/emule-http-cache-go`: 0 stars, 0 forks, 0 open issues; default
    `main`; default-branch commit 2026-10-06 `5064de5`; latest release
    `v0.1.5` on 2026-10-06; no check runs or GitHub-detected license.
- Notes: Implements encrypted, expiring HTTP chunk storage addressed through
         custom eD2K-link data for eMule Qt. It documents quotas, capability
         URLs, AES-encrypted payloads, conformance tests, and the client's
         cleartext-HTTP constraint. This is a negotiated/application extension
         outside stock eMule behavior; use only as an architecture lead after
         security and licensing review.

#### aMule EC Profiler

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, early diagnostics utility
- Language/platform: Python standard-library TCP proxy and dashboard
- Link: https://github.com/got3nks/amule-ec-profiler
- Repo stats (GitHub, 2026-10-23):
  - `got3nks/amule-ec-profiler`: 2 stars, 1 fork, 0 open issues; default
    `main`; default-branch commit 2026-07-30 `7976cd8`; no public release or
    check runs; GPL-2.0.
- Notes: Verbatim pass-through proxy between EC clients and `amuled` that
         attributes bytes, calls, latency, flags, and tag costs by opcode and
         caller, with JSON/text session reports. Useful for measuring API
         amplification and controller behavior; it observes EC and does not
         implement or modify the eD2K/Kad wire.

#### KadGlobe

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Component candidate** · **Library/tool role**
- Status: 🟡 Active, needs protocol review
- Language/platform: Python/JavaScript
- Link: https://github.com/floatingbit23/KadGlobe
- Repo stats (GitHub, 2026-09-30):
  - `floatingbit23/KadGlobe`: 2 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-05-19 `4d1fd94`; no releases.
- Notes: Kademlia visualization and telemetry tool that claims live UDP/Kad probes
         and eMule metrics. Track as a diagnostics idea lead until packet behavior,
         data sources, and compatibility are reviewed.

#### jed2k

- Assessment: **🟡 Verification needed** · **🟡 Visible** · **Stale** · **Component candidate** · **Library/tool role**
- Status: 🟡 Maintained/stale
- Language/platform: Java/Android
- Link: https://github.com/a-pavlov/jed2k
- Repo stats (GitHub, 2026-09-30):
  - `a-pavlov/jed2k`: 171 stars, 43 forks, 40 open issues; default `master`;
    default-branch commit 2023-09-03 `bc10ef8`; repository pushed
    2024-04-06; no recognized license reported by GitHub.
- Notes: Public Java library for eD2K networks and Android. This resolves the
         previous archive-only source gap; still review licensing and current
         protocol coverage before reuse.

#### kadkad

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟡 Needs verification
- Language/platform: Rust
- Link: Public/local source not confirmed
- Notes: Rust Kad2 library/daemon research lead. No canonical checkout was found
         in `repos`, `workspaces`, or the listed local analysis directories
         during the 2026-09-30 refresh, and the public GitHub search found no
         credible exact-name project.

#### rust2k

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Experimental** · **Component candidate** · **Library/tool role**
- Status: 🟡 Needs verification
- Language/platform: Rust
- Link: Public/local source not confirmed
- Notes: Rust ED2K/Kad research lead. No canonical checkout was found in
         `repos`, `workspaces`, or the listed local analysis directories during
         the 2026-09-30 refresh, and the public GitHub search found no credible
         exact-name project.

### Tier 4 — Stale or historical

#### ed2k Rust crate

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Stale** · **Historical reference** · **Library/tool role**
- Status: ⚫ Stale
- Language/platform: Rust
- Link: https://github.com/Kimundi/ed2k
- Repo stats (GitHub, 2026-05-29):
  - `Kimundi/ed2k`: 1 star, 0 forks, 0 open issues; default `main`; default-branch commit 2023-05-20 `73fb463`.
- Notes: ED2K hash implementation, not a full network protocol library. Useful
         for hash-behavior comparison around chunk-boundary variants.

#### ged2k

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Stale** · **Historical reference** · **Library/tool role**
- Status: ⚫ Stale
- Language/platform: Go
- Link: https://github.com/a-pavlov/ged2k
- Repo stats (GitHub, 2026-09-30):
  - `a-pavlov/ged2k`: 3 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2023-04-13 `5a3fdb9`; Apache-2.0.
- Notes: Small Go port/lineage of `a-pavlov/jed2k`. Do not confuse it with the
         unverified local `goe2k` archive name below.

#### libed2k/qmule

- Assessment: **⚫ Stale/historical** · **🟡 Visible** · **Stale** · **Historical reference** · **Library/tool role**
- Status: ⚫ Stale
- Language/platform: C++
- Link: https://github.com/qmule/libed2k
- Repo stats (GitHub, 2026-05-29):
  - `qmule/libed2k`: 82 stars, 27 forks, 4 open issues; default `master`; default-branch commit 2016-06-02 `5408c65`.
- Notes: Cross-platform eDonkey protocol library inspired by libtorrent-rasterbar.

#### goe2k

- Assessment: **🟣 Archive/reference** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Library/tool role**
- Status: 🟣 Archive-only
- Language/platform: Go
- Link: Local archive evidence
- Notes: Archived Go ED2K material observed under local research archives. Confirm
         canonical source before linking.

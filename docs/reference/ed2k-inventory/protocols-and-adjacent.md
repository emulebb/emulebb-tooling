# Protocol References and Adjacent P2P

[← Back to the eD2K inventory dashboard](../ED2K-PROJECT-INVENTORY.md)

Stock protocol references, the negotiated fast-publishing research snapshot, and clean-slate or adjacent P2P projects that are not confirmed stock eD2K/Kad implementations.

Ranking badges and thresholds are defined in [Methodology](methodology.md). Statistics are dated snapshots, not live user counts.

## Protocol References

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| eMule/aMule server opcode code | 🟡 Verification needed | ❔ Unknown | Reference-only | Protocol reference | Unknown |
| aMule ED2K protocol wiki | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |
| eDonkey network server software history | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |
| eMule server FAQ | ⚫ Stale/historical | ❔ Unknown | Reference-only | Historical reference | Unknown |

### Tier 3 — Experimental or verification required

#### eMule/aMule server opcode code

- Assessment: **🟡 Verification needed** · **❔ Unknown** · **Reference-only** · **Protocol reference** · **Reference role**
- Status: 🟡 Maintained/historical
- Link: eMuleBB source, aMule source
- Notes: The current client code remains the most practical protocol reference for
         `OP_LOGINREQUEST`, `OP_SEARCHREQUEST`, `OP_SERVERLIST`, source lookup, and
         server tags.

### Tier 4 — Stale or historical

#### aMule ED2K protocol wiki

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Reference role**
- Status: ⚫ Historical
- Link: https://wiki.amule.org/wiki/Ed2k_protocol
- Notes: Protocol notes for eD2K client/server behavior. Revalidate against current
         code before treating as normative.

#### eDonkey network server software history

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Reference role**
- Status: ⚫ Historical
- Link: https://en.wikipedia.org/wiki/EDonkey_network
- Notes: Summarizes Lugdunum/eserver and satan-edonkey-server history. Use only as
         secondary context.

#### eMule server FAQ

- Assessment: **⚫ Stale/historical** · **❔ Unknown** · **Reference-only** · **Historical reference** · **Reference role**
- Status: ⚫ Historical
- Link: https://emule-project.net/faq/faq_server.htm
- Notes: User-facing server behavior and connectivity background.

## Negotiated Fast Server Publishing Snapshot

This 2026-10-13 snapshot is specific to the experimental `offerfiles_v=1`
extension: a publishing client requests version 1 in `OP_LOGINREQUEST`, and a
supporting server returns a complete batch/interval policy in the first
`OP_SERVERIDENT`. It accelerates incremental `OP_OFFERFILES` visibility on the
connected eD2K server only; it does not change Kad publication. The eMuleBB
policy and outstanding proof boundary are recorded in
[RUST-REF-015](../../products/emulebb-rust/history/items/RUST-REF-015.md) and
[RUST-CI-005](../../products/emulebb-rust/history/items/RUST-CI-005.md).

Current implementation state:

- `emulebb-rust` implements the negotiating client with legacy fallback.
- `andrey23127/ed2k-server` current `0.9.x` source implements the opt-in server
  advertisement, matching enforcement, and global backpressure; aMule's
  published isolated result remains pinned to source tag `v0.9.81`.
- aMule PR `#1715` implements an experimental, disabled-by-default client and
  reports isolated 60,000-file publication against that server source in 179.4
  seconds. The PR remains open and production server-load proof remains
  incomplete.

High-value next adoption candidates:

- **eMule Qt plus eNode-go**: the active client still uses a 200-file,
  60-second scheduler, while the same owner's server already stores later
  batches cumulatively and enforces soft/hard limits. This is the clearest
  independent paired implementation after aMule/`ed2k-server`.
- **njMule**: its pre-alpha `FilePublisher` explicitly uses 200 files every 60
  seconds. The architecture is new enough to add connection-scoped negotiation
  before the first public release.
- **aria2-next**: its server session currently selects at most the first 200
  shareable entries and repeats that prefix every ten minutes. Negotiated
  continuation would improve both large-library coverage and time to visibility.
- **eMule Community, eMule Next, and eMuleAI**: the inspected stock-derived
  paths retain the 200-file cap and one-minute gate. They have broad user reach,
  but need conservative opt-in UX and independent interoperability evidence.
- **JEmuleServer**: its parser already tolerates unknown named login tags and
  its server-ident path is extensible. It needs per-client batch/pacing and
  server-wide backpressure before it can advertise the capability safely.

Projects needing prerequisite work rather than simple acceleration:

- **rmule** currently sends the complete share set in one `OP_OFFERFILES`.
  It first needs bounded legacy fallback and multi-batch state; negotiation
  would then provide the safe faster path.
- **goed2k-server** currently replaces the client's indexed set on each offer
  packet. It must preserve cumulative session offers before accepting a paced
  multi-batch client.
- Controllers and packaging layers such as aMuTorrent, Mularr, aMule Nuxt,
  TauriMule, docker-amule, macMule, and AriaLite do not implement this wire path.
  They benefit indirectly when their underlying aMule, eMule, or aria2-next
  engine adopts it.
- The stable eMuleBB MFC line is frozen for maintenance; forward adoption and
  proof remain owned by `emulebb-rust`.

## Adjacent Agent-Built P2P Watchlist

These projects do not implement stock eD2K/Kad and are not compatibility
references. They are retained because their explicitly AI-assisted development
or clean-slate protocol scope, test claims, and security disclaimers provide
useful comparisons for evaluating the current wave of rapidly produced P2P
software. Do not move code or protocol assumptions from this section into
eMuleBB without an independent design, license, security, and interoperability
review.

### Ranking summary

| Project | Activity | Adoption | Maturity | Relevance | Latest activity |
|---|---|---|---|---|---|
| ED3K specification | 🟡 Verification needed | ⚪ Niche | Active development | Adjacent watchlist | 2026-10-20 |
| NomadPortal-Android | 🟡 Verification needed | ⚪ Niche | Experimental | Adjacent watchlist | 2026-08-27 |
| Rekindle | 🟡 Verification needed | ⚪ Niche | Experimental | Adjacent watchlist | 2026-02-19 |
| WebTorrent Rust (`webtorrent_rs`) | ⚫ Stale/historical | ⚪ Niche | Reference-only | Historical reference | 2025-12-25 |

### Tier 3 — Experimental or verification required

#### ED3K specification

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Active development** · **Adjacent watchlist** · **Non-stock or adjacent protocol**
- Status: 🟡 Active, clean-slate and intentionally incompatible
- Language/platform: Protobuf protocol specification, conformance contracts,
  and test vectors
- Link: https://github.com/ed3k-protocol/ed3k-spec
- Repo stats (GitHub, 2026-10-23):
  - `ed3k-protocol/ed3k-spec`: 0 stars, 0 forks, 0 open issues; default `main`;
    default-branch commit 2026-10-20 `94bc567`; no release or check runs;
    GitHub reports no recognized license.
- Notes: New protocol design inspired by eD2K but replacing the wire with
         Protobuf contracts and adding NAT traversal and IPv6. Its repository
         contains specifications, schemas, extension documents, and vectors,
         but it is not an eMule network implementation. Track only as an
         adjacent design experiment; do not mix ED3K messages or assumptions
         into stock-compatible eMuleBB behavior.

#### NomadPortal-Android

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Adjacent watchlist** · **Non-stock or adjacent protocol**
- Status: 🟡 Active, early beta, explicitly vibe-coded
- Language/platform: Kotlin/Jetpack Compose with embedded Python Reticulum/LXMF
- Link: https://github.com/JamesM92/NomadPortal-Android
- Repo stats (GitHub, 2026-09-30):
  - `JamesM92/NomadPortal-Android`: 1 star, 0 forks, 5 open issues; default
    `dev`; default-branch commit 2026-08-27 `3880b4d`; latest prerelease
    `v0.0.3` on 2026-08-26; GitHub reports no recognized license.
- Notes: Android client for Reticulum/LXMF messaging, NomadNet page hosting,
         voice, Bluetooth/LoRa/TCP transports, and remote-shell access. The
         author explicitly describes it as built with an AI assistant, states
         that they are not a security expert, and warns that no professional
         audit has covered its cryptographic identity, permissions, or
         untrusted-input paths. Its repository describes a PolyForm
         Noncommercial license, which is also unsuitable as a source donor for
         eMuleBB. Useful as an example of unusually clear AI-development and
         security-risk disclosure.

#### Rekindle

- Assessment: **🟡 Verification needed** · **⚪ Niche** · **Experimental** · **Adjacent watchlist** · **Non-stock or adjacent protocol**
- Status: 🟡 Active/early, explicitly AI-assisted
- Language/platform: Rust/Tauri/SolidJS over the Veilid P2P network
- Link: https://github.com/ScopeCreep-zip/Rekindle
- Repo stats (GitHub, 2026-09-30):
  - `ScopeCreep-zip/Rekindle`: 10 stars, 0 forks, 0 open issues; default
    `main`; default-branch commit 2026-02-19 `365971a`; latest prerelease
    `v0.0.2-alpha` on 2026-02-19; MIT license.
- Notes: Decentralized gaming-chat client with Rust protocol, crypto, voice,
         and community crates behind a Tauri UI. The README explicitly says AI
         is used and that the project may appear vibe-coded. It identifies
         one-to-one messaging as the primary tested workflow while voice,
         communities, and game detection are not yet confirmed end to end.
         Track its separation of reusable Rust crates from the desktop shell
         and its candid implemented-versus-verified labeling; do not accept
         its multi-layer cryptography claims without a dedicated audit.

### Tier 4 — Stale or historical

#### WebTorrent Rust (`webtorrent_rs`)

- Assessment: **⚫ Stale/historical** · **⚪ Niche** · **Reference-only** · **Historical reference** · **Non-stock or adjacent protocol**
- Status: ⚫ Archived, explicitly vibe-coded experiment
- Language/platform: Rust; WebTorrent/BitTorrent library
- Link: https://github.com/DIG-Network/webtorrent_rs
- Repo stats (GitHub, 2026-09-30):
  - `DIG-Network/webtorrent_rs`: 0 stars, 0 forks, 0 open issues; default
    `master`; default-branch commit 2025-12-25 `cc8dea5`; archived; no
    releases or GitHub-detected license. The README states MIT.
- Notes: Unofficial Rust port claiming tracker, DHT, TCP/uTP/WebRTC, metadata,
         peer exchange, NAT traversal, throttling, and more than 80 tests. The
         maintainer explicitly calls it vibe-coded, experimental, unmaintained,
         and unsuitable for production. Useful primarily as a cautionary case:
         a broad implemented-feature list is not evidence of live swarm
         compatibility, maintenance, or production safety.

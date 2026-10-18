# emulebb-rust Release Scope

This document is the canonical human-facing product boundary for
`emulebb-rust`. It defines the client that exists today, the ordered suite
phases that may follow it, the compatibility authority for each kind of
behavior, and the gate that prevents later phases from diluting unfinished
client work.

`emulebb-rust` is an **automation-first, headless IPv4 eD2K/Kad client** for
reliable search, download, upload, and sharing. It is operated through a
Rust-native REST API and embedded browser operations console. The product is
optimized for broadband operation and large libraries through Rust-native
asynchronous architecture without changing supported stock wire semantics.

The integrated suite is delivered in three hard-gated phases:

1. **Client** - finish and prove the eD2K/Kad client, API, WebUI, persistence,
   packaging, and supported routing modes.
2. **Indexer** - add an autonomous persistent eD2K/Kad observation index only
   after the Client gate closes.
3. **Arr** - add Torznab and the Arr-required qBittorrent compatibility subset
   only after the Indexer gate closes.

Production implementation of a later phase must not begin while the preceding
gate is open. Forward design and deterministic fixtures may be prepared only
when they do not add dormant production paths or distract from the active gate.

## Behavior authority

Use this precedence instead of a general promise to reproduce another client:

1. **Stock/community eMule** owns eD2K and Kad wire formats, advertised
   capabilities, network identity, interoperability state machines, and other
   externally observable stock protocol behavior.
2. **Maintained eMuleBB MFC** owns only explicitly identified non-wire
   operational defaults and ceilings plus disk and network I/O outcomes. It
   does not own Rust API, UI, settings, controller, persistence, or thread
   structure.
3. **Rust-native design** owns concurrency, memory use, batching, observability,
   internal algorithms, and async I/O where those choices preserve the first
   two authorities' required outcomes.
4. **Current aMule** is interoperability evidence and a source of optimization
   candidates. It is not an implicit behavior authority.

Stock wire behavior wins whenever authorities conflict. A new wire extension
requires an explicit registry entry, negotiation and downgrade rules, and a
tracked evidence disposition. The currently default-on `offerfiles-v1`
extension remains part of the Client gate until its full RUST-CI-005 evidence
matrix passes.

## Current phase: Client

### Supported surface

- **eD2K (IPv4):** server login/ident (HighID and LowID), search, source
  discovery, download and upload through the block/part protocol, hashset and
  AICH request/answer, ICH salvage, secure identification, credits, upload
  queues, UDP source reask, and server-mediated LowID callback.
- **Kad (IPv4):** bootstrap, routing-table maintenance, lookup, keyword/source/
  notes search and publish, firewall checks, LowID buddy operation, relayed
  callbacks, and the protocol-required local keyword/source/notes index.
- **Transfers and delivery:** durable piece storage, verification, resume,
  completion rehash, continued seeding, and materialization by name into the
  selected category path or configured `incomingDir`.
- **Sharing:** recursively monitored shared-folder roots. Single-file sharing
  and non-recursive roots are not supported product surfaces.
- **Control plane:** the Rust-forward `/api/v1` contract, authenticated HTTP
  operation, and the embedded SPA operations console. The MFC REST contract is
  not a compatibility constraint.
- **Persistence:** one SQLite database for identity, peers, credits, servers,
  categories, settings, searches, transfers, known/shared files, and the local
  Kad protocol index.
- **Safety:** IP and user-hash bans, IP filtering, admission controls, Kad flood
  limits, packet validation, transfer attribution, VPN diagnostics, and
  fail-visible durable-state checks.
- **Routing:** explicit direct mode and the proven Docker-over-Gluetun network-
  namespace deployment. Direct mode makes no anonymity promise. Native VPN
  binding remains experimental until its own fail-closed leak evidence exists.

The embedded WebUI is an operations console, not a recreation of the MFC GUI.
It covers health, configuration, network state, searches, transfers, sharing,
logs, diagnostics, and—when their phases ship—index and adapter state.

### Beta contract policy

The first-party API, configuration, and database schema are deliberately
unstable through the Client, Indexer, and Arr phases. Breaking changes are
allowed when they improve the long-term model, but each change must update all
owned consumers, OpenAPI, examples, validators, and tests together.

- `/api/v1` remains the versioned beta namespace; its compatibility promise
  begins only at the explicit post-Arr contract freeze.
- Retired fields and routes are hard errors. Do not alias, remap, ignore, or
  bridge obsolete beta shapes.
- Product code accepts only the exact current SQLite schema. Any incompatible
  schema change fails startup and requires a completely fresh profile. There
  is no end-user migration, reset, repair, or partial index rebuild path.
- One profile contains one database. An index-only schema break therefore also
  invalidates identity, credits, transfers, settings, and all other profile
  state; this is an accepted beta tradeoff.

### Frozen intentional differences

The omission and extension registries in `repos/emulebb-rust/policy` are the
machine-readable authority. The rows below are the declared intentional
differences; RUST-CI-006 remains responsible for proving that the current-head
set is complete.

| Registry ID | Disposition | Compatibility contract |
|---|---|---|
| `sx1-live-source-exchange` | Permanent omission | SX2 only; SX1 is unadvertised and live SX1 packets are ignored. |
| `ipv6-ed2k-kad` | Permanent omission | eD2K, Kad, peer transfer, NAT, and bootstrap remain IPv4-only. |
| `peer-chat-messaging` | Permanent omission | No peer chat/captcha surface; captcha is unadvertised and bounded unsolicited packets are tolerated. |
| `ed2k-preview` | Permanent omission | Preview is unadvertised; Rust neither requests nor answers peer media previews. |
| `kad-flood-lan-exemption` | Permanent omission | LAN/loopback stays flood-exempt; public peers retain stock flood controls. |
| `conn-rate-rolling-five-second-window` | Deferred behavior | The conservative rolling grant window is local and has no wire effect. |
| `offerfiles-v1` | Negotiated extension | Stock-shaped offers and stock fallback are mandatory when negotiation is absent, invalid, or rejected. |

The permanent omissions are product decisions, not client-gate gaps. Reopening
one requires an explicit scope decision and matching registry update. The
connection-rate row remains a reported defer. The extension remains default-on
but cannot close RUST-CI-005 without its deterministic, stock eMule,
current-aMule, reconnect, downgrade, malformed-input, and scale evidence.

### Client gate

The Indexer phase cannot begin until all of the following are true:

- every active non-suite Rust item is closed or explicitly removed from the
  product; any newly opened client item joins this gate;
- current-head stock eMule/current-aMule/Rust parity evidence is reconciled with
  the registries and current documentation;
- there are no unresolved critical safety, data-integrity, privacy, or stock-
  wire findings;
- `offerfiles-v1` satisfies the complete RUST-CI-005 evidence contract;
- the canonical API and WebUI complete status, settings, network, search,
  transfer, upload, sharing, log, and diagnostic workflows;
- Docker-over-Gluetun tunnel-down testing proves zero off-tunnel P2P egress;
- packages compile, test, install/start, serve the WebUI, perform a local
  transfer, and shut down cleanly on Windows, Linux, and macOS x64/ARM64; and
- deep bounded public-network campaigns pass on Windows x64 and Linux x64.

Because every newly accepted client item joins the gate, issue triage must
reject speculative or low-value work rather than using priority alone to defer
it silently.

## Future phase: Indexer

The autonomous indexer is an integrated product domain, not the
protocol-required local Kad index described above. Its production work begins
only after the Client gate closes.

- Run in the same daemon and database behind an explicit internal domain
  boundary.
- Enable passive collection and bounded active replay/discovery by default.
- Persist remotely observed records until the operator deletes them; do not
  impose a product TTL or configured record/disk ceiling.
- Retain origin, observation provenance, and last-seen metadata.
- Expose `live`, `index`, and `hybrid` execution through one canonical search
  and result model.
- On low disk or SQLite write failure, pause index writes and active discovery,
  preserve normal client networking and transfers, and expose a persistent
  operator-visible fault.

The Indexer gate requires bounded network behavior, deterministic persistence
and restart coverage, search-result provenance, disk-pressure isolation, and
cross-platform packaged operation.

## Future phase: Arr

Arr integration begins only after the Indexer gate closes.

- Serve Torznab and native qBittorrent-compatible paths from the same HTTP
  listener as the first-party API.
- Keep authentication and rate controls explicit for each route family.
- Implement only the qBittorrent Web API behavior required by the supported
  Prowlarr/Sonarr/Radarr workflows; reject unsupported operations clearly.
- Translate adapter requests into the canonical search and transfer services.
  Compatibility adapters must not own parallel transfer, category, or index
  state.
- Keep selection rules, schedules, media management, and post-processing in
  external controllers.

API, configuration, and schema compatibility freeze together only after the
Arr gate passes.

## Cross-phase non-goals

- Native desktop UI or a recreation of the MFC GUI.
- Internal category-rule, scheduling, media-selection, or post-processing
  engines.
- Coordinator or federation behavior before an explicit later product phase.
- Proxy transports, IPv6 eD2K/Kad, uTP peer transport, collection-file import/
  export, peer chat/captcha, peer preview, SX1, single-file sharing, or
  non-recursive shared roots.
- Compatibility layers for retired beta API, configuration, or schema shapes.
- Treating aMule behavior, qBittorrent behavior, or MFC implementation structure
  as an authority outside the explicitly defined adapter or outcome boundary.

## Platform contract

Windows, Linux, and macOS on x64 and ARM64 remain supported release targets.
Every target requires compile/test viability and packaged runtime smoke. Deep
public-network and VPN evidence remains concentrated on Windows x64 and Linux
x64; this difference is evidence depth, not permission to ship an untested
package on another supported target.

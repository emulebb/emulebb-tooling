# emulebb-rust Release Scope

This document is the canonical human-facing product boundary for
`emulebb-rust`. It defines the client that exists today, the ordered suite
phases that may follow it, the compatibility authority for each kind of
behavior, and the gate that prevents later phases from diluting unfinished
client work.

`emulebb-rust` is one **universal, automation-first, headless IPv4 eD2K/Kad daemon** for
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

## Current Operator Hold And Work Priority (2026-11-13)

**Beta 3 promotion remains on hold.** The operator separately authorized the
lean Android APK, JNI, continuous foreground service and signing work under
[RUST-FEAT-056](active/items/RUST-FEAT-056.md), including additive APK publication
through existing nightlies. Initial APKs remain experimental pending actual
device qualification; Play Store publication is outside scope.
The client-fix and delivery
batch in [PR #329](https://github.com/emulebb/emulebb-rust/pull/329) is published
as the accepted [nightly from source `6429b952`](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261113.g6429b952).
Its complete public-byte, provenance and OCI inventory passed verification.
The later README-only [PR #330](https://github.com/emulebb/emulebb-rust/pull/330)
also proved trusted documentation-only CI on both its real PR and actual main
push `bc0f319d`; it did not produce new binaries. Balanced reliability leads
the next product implementation wave, including
the shared bounded-persistence contract under [#155](active/items/RUST-REF-016.md).
Existing configuration, schema and client-correctness owners retain their
responsibilities; the checkpoint is evidence, not a recurring precondition for
every new branch.

[Scoop (#324)](active/items/RUST-FEAT-147.md) is the first accepted new
distribution lane. [Linux services (#325)](active/items/RUST-CI-049.md) are
deferred to a bounded design review; there is no authorization to implement or
enable a service. The [PM policy](../../reference/PM-COORDINATION-POLICY.md)
owns the standing routine: reserve independent branch outcomes, integrate
compatible authored commits into small batches, qualify the actual combined
tip, merge in dependency order and retire finished delivery state. A selected
publication checkpoint receives complete source-bound nightly/public-byte
proof. Batching changes neither required checks nor the operator holds, and
does not require publication after every contribution. Storage and Scoop
implementation still require their accepted contracts and parent allocation.

The hold prohibits Beta 3 candidate selection/certification and promotion;
[#142](active/items/RUST-CI-009.md) remains held. Separately authorized
unpublished packaging candidates and CI-gated nightly prereleases may proceed
through their actual gates. Intake does not authorize a new release tag,
external package channel, community submission, signing, hosting or spending.
GitHub issues and Project #3 own status, priority and phase placement.

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
tracked evidence disposition. The default-on `offerfiles-v1` extension is
governed by the completed RUST-CI-005 evidence matrix; any negotiation,
downgrade, stock-compatibility, or scale-evidence regression reopens the Client
gate.

## Current phase: Client

eMuleBB Rust is an active beta led by CI-gated nightly builds from `main`.
Choose the newest dated nightly prerelease from GitHub Releases. Repeatedly
tested on live eD2K/Kad networks. Beta3 release remains under the operator
hold above while multiarchitecture/multiplatform and workspace work take
priority. Retained evidence includes the persisted
live-profile campaign recorded by
[RUST-FEAT-033](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-FEAT-033.md) and exact-candidate Windows and
Linux campaigns from the same work. Current-head reconciliation remains tracked
by [RUST-CI-006](active/items/RUST-CI-006.md), and immutable Beta 3 candidate
selection remains tracked by [RUST-CI-009](active/items/RUST-CI-009.md). This
supports beta operation; it is not a stable-release certification.

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
  Stock/MFC profile imports preserve and trust known eD2K/AICH hashes;
  unambiguous file metadata matches are reused without an initial rehash.
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

### Universal deployment and distribution

Native and OCI delivery consume one daemon, adjacent WebUI, authenticated
control contract and profile-ownership model. Keep writable profiles, payloads
and secrets outside versioned application installations. A package manager or
service wrapper must not become another settings authority or API bridge.
[#297](active/items/RUST-CI-043.md) owns that shared deployment/configuration
contract; [#298](active/items/RUST-CI-044.md) owns database boundaries.

Ubuntu 24.04 and Debian 13, each on x64 and ARM64, are the initial declared
Linux qualification targets. These are targets, not completed four-way install
or minimum-OS evidence. Derive actual ELF/libc and native-library requirements
from the selected package bytes, then qualify installation and lifecycle on
each claimed release. Existing inconsistent libc declarations do not establish
an older supported baseline; do not infer Debian 12 or Ubuntu 22.04 support.

Scoop is the first new package-manager lane under
[#324](active/items/RUST-FEAT-147.md), consuming immutable verified Windows ZIPs.
Use explicitly selected beta versions, preserve complete WebUI payloads and
leave profile/data ownership unchanged. Package updates must not migrate or
reset a database, erase state, promise cross-schema resume, or silently follow
a moving nightly. Preserve matching old binary/profile pairs for explicit
rollback. Uninstall preserves operator state. Semantic continuity stays with
[#234](active/items/RUST-FEAT-063.md); unfinished continuity is not permission
to add a package-script conversion path.

Linux-service implementation is deferred. The bounded
[#325 review](active/items/RUST-CI-049.md) must recommend user versus system
service, identity, profile/key/data ownership, listeners, logs, clean shutdown,
profile-lock reuse and explicit enablement before implementation is considered.
It does not block later Scoop delivery and authorizes no unit installation or automatic start.

APT, RPM and Homebrew remain candidate outcomes rather than active delivery
issues. APT needs an accepted ownership/signing/update proposal; RPM needs its
own selected distro matrix; Homebrew needs an accepted package and launchd
model. AUR and Nix are unactivated pending demand and maintenance capacity.
None authorizes hosting, paid infrastructure, signing or community submission.
NAS qualification reuses existing OCI images under
[#228](active/items/RUST-FEAT-058.md), not a new generic Docker implementation.
BSD, Android/Fire OS and ChromeOS retain their existing owners and require
environment-specific evidence before support claims. Android developer daemon
bundles remain distinct from an APK or device-runtime qualification.
The operator's Termux launch exposed a JVM-dependent HTTPS verifier panic.
The [native CLI repair and evidence](https://github.com/emulebb/emulebb-tooling/blob/main/docs/products/emulebb-rust/history/items/RUST-BUG-186.md)
now include accepted source-built API 37/x86_64/16 KiB emulator TLS and
authenticated first-launch proof. Separately,
[RUST-FEAT-056](active/items/RUST-FEAT-056.md#current-state) records bounded
API 36/ARM64 physical execution of the source `54a5f220` signed APK: rendered
WebUI, local transfer/collision/restart and system day/night theme checks. That
candidate failed the full APK runtime matrix and was not published. The later
manual-start source `42bffd97` passed source checks and bounded physical tests
but failed full nightly qualification. The operator subsequently expanded the
APK target to Android 12+ with safe shared-storage collision delivery, while
retaining both native Android archives. That expanded candidate still requires
fresh-source APK/device and publication proof; automatic boot resume is deferred. Android/Fire OS support,
the full API matrix, particular untested hardware, Termux UID/runtime,
unavailable/degraded-network execution, VPN behavior and the 24-hour soak remain
open under that owner. Optional environment expansion does not independently
hold the core Client gate.

### Beta contract policy

The first-party API and database schema are deliberately unstable through the
Client, Indexer, and Arr phases. Breaking changes are
allowed when they improve the long-term model, but each change must update all
owned consumers, OpenAPI, examples, validators, and tests together.

- Minimal TOML bootstrap configuration has a separate stability goal. Preserve
  its keys and semantics by default; mutable settings belong in SQLite.
  [Persistence Policy](reference/PERSISTENCE-POLICY.md) owns the contract,
  including read-only `server.met` and `nodes.dat` imports. Configuration/API
  coherence and schema review are high-priority Beta3 work under
  [RUST-CI-043](active/items/RUST-CI-043.md) and
  [RUST-CI-044](active/items/RUST-CI-044.md). Release remains held; these reviews
  do not authorize migrations or silently change profile compatibility.
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
under completed deterministic, stock eMule, current-aMule, reconnect,
downgrade, malformed-input, and 100,000-file scale evidence.

### Client gate

The Indexer phase cannot begin until all of the following are true:

- every active mandatory core Client item is closed or explicitly removed from
  the product; newly accepted core Client work joins this gate;
- current-head stock eMule/current-aMule/Rust parity evidence is reconciled with
  the registries and current documentation;
- there are no unresolved critical safety, data-integrity, privacy, or stock-
  wire findings;
- `offerfiles-v1` continues to satisfy the complete RUST-CI-005 evidence contract;
- the canonical API and WebUI complete status, settings, network, search,
  transfer, upload, sharing, log, and diagnostic workflows;
- Docker-over-Gluetun tunnel-down testing proves zero off-tunnel P2P egress;
- packages compile, test, install/start, serve the WebUI, perform a local
  transfer, and shut down cleanly on Windows, Linux, and macOS x64/ARM64; and
- deep bounded public-network campaigns pass on Windows x64 and Linux x64.

Optional distribution channels and additional environment qualification are
explicit expansion scope outside this phase-advancement gate. Their existing
Client phase ownership is retained; an owning issue and the
`distribution-expansion` classification record the boundary. The current
expansion owners are NAS, FreeBSD/other Unix, Android/Fire OS, ChromeOS, Scoop
and the Linux-service design review. APT, RPM and Homebrew are candidates,
not activated implementation issues; AUR and Nix remain unactivated ideas.

This classification cannot exempt a core safety, integrity, privacy or wire
defect, remove a currently required CI check, or skip a platform selected by a
release workflow. Full nightly qualification continues to require its complete
current platform inventory, including macOS and experimental Android compile/
ELF evidence. Issue priority alone never changes either gate.

Reject speculative or low-value work rather than creating ownerless expansion
items or silently deferring mandatory core work.

### Beta increment gate

An incremental beta may be prepared while the broader Client gate remains open;
it does not authorize Indexer work or imply that every later Client item is
complete. RUST-CI-009 owns the current Beta 3 candidate certification and
depends on RUST-CI-006 current-head parity evidence, required hosted CI, complete
dry-run release assembly, packaged lifecycle checks, and a retained manifest of
exact revisions and artifact digests.

For Beta 3, only Windows/Linux native x64 and ARM64 packages and the required
Linux OCI variants are mandatory platform deliverables. macOS, Android/Fire
OS, ChromeOS, NAS-specific certification, and additional Unix targets continue
in parallel without blocking this beta increment. Shared safety, integrity,
privacy, policy, dependency, CodeQL, provenance, and Windows/Linux correctness
checks remain mandatory. RUST-CI-035 delivered the workflow aggregation,
release-assembly and manifest profile split; the selected workflow's actual
enforcement remains in force. Full nightly still selects its complete inventory.
Optional artifacts ship only with their own successful qualification and
explicit manifest entries.

This beta platform selection does not close the broader Client gate or
authorize Indexer/Arr implementation. The required candidate uses immutable
source revisions and retained artifact digests; separate operator approval
is still required to publish.

Candidate selection is explicit and restartable. Normal review and breaking
beta improvements continue until an immutable candidate revision is selected.
Any product or contract change after selection invalidates that candidate and
requires a new certification pass. Candidate certification does not bump a
version, create or move a tag, publish a GitHub Release or image, close a
milestone, or replace the separate operator decision to ship.

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

API and database schema compatibility freeze together only after the Arr gate
passes; minimal bootstrap configuration follows the separate stability review
above.

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

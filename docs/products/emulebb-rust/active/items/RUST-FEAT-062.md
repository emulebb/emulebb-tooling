---
id: RUST-FEAT-062
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/233
title: Persist Kad routing state in SQLite and keep met files import-only
status: OPEN
priority: Major
category: feature
labels: [rust, kad, sqlite, persistence, nodes-dat, server-met]
milestone: post-beta-polish
created: 2026-11-05
source: operator-approved profile continuity design 2026-11-05
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/233. This local document owns the durable engineering contract.

# RUST-FEAT-062 - Persist Kad routing state in SQLite and keep met files import-only

## Runtime coupling local-suite checkpoint (2026-11-16)

The final coupled **uncommitted working material** is green in the supported
local Rust suite. This is accepted local-suite evidence, not an exact committed
source or newly staged runtime qualification. `test rust-unit --workstream
public-foundation-round-1` exited zero; retained log:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/kad-sqlite-rust-acceptance-round-4/rust-unit.log`.
The aggregate was 2,871 passed, zero failures and one ignored subprocess helper.
Selected owners included Core 537 with all integrations; REST 158 plus 3
integrations; metadata 113 plus 3 integrations; daemon 108 unit plus 8 hosted,
1 logging and 6 ownership checks; DHT 146, Kad-net 92 and routing 63. All workspace
consumers were included, including 11 host-run Android consumer checks; this is
not Android device or cross-platform qualification.

Eight existing Python owners passed 250 checks with one POSIX-only skip:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/kad-sqlite-harness-cut-round-2/junit.xml`.
The WebUI gate also passed 52 unit checks and 32 Playwright checks across Chromium
and mobile WebKit, plus TypeScript typecheck and production build. These are
selected local consumer checks, not proof that the entire round-one public
surface or 59-field settings redesign is implemented.

Earlier Rust rounds 1 and 3 failed fixture/lifetime defects and remain retained
under `reports/kad-sqlite-rust-acceptance-round-1` and
`reports/kad-sqlite-rust-acceptance-round-3`. Round 2 was safely interrupted during
compilation after a hosted fixture's file-backed discovery assumption was found;
it has no completed test verdict. Repairs include:

- the direct-route startup fixture no longer retains a blocking VPN guard;
- ingress leases span the worker allocation peak and fixed-buffer transient
  capacity is accounted, with structural regressions;
- startup attachment releases its temporary permit before replying, while an
  explicit handoff fence protects queued commands;
- a real SQLite-failure regression through the shared daemon finalizer verifies
  network cleanup and owner drain, typed failure, unchanged Kad revision and
  reopen after removing the owned fault trigger. Code inspection confirms
  post-owner exit paths use that finalizer, and the existing eight hosted tests
  pass; separate SQL-fault injection in every early hosted branch is not proved;
- hosted fixtures initialize both SQLite discovery domains instead of relying
  on a profile cache-file sentinel; Rust does not write source-input cache files.

The [#155 accounting scope](RUST-REF-016.md#admission-and-resource-accounting)
is retained product-payload capacity, not measured total RSS. The existing REST
CI campaign and test owner have been extended for real Kad HTTP 500 fault/retry,
clean reopen and loopback restart, including the corrected protocol-versus-REST
node-ID comparison. **That registered runtime phase remains unrun.** The staged
`b509524f` friend campaign below remains older evidence. Exact clean committed
sources, a matching runtime receipt and the new campaign are still required.
No 100k runtime campaign, combined 100k jobs, full platform matrix or 365-day
qualification is claimed.

The actual database-backed POST frontdoors in this cut are import, stop, server
connection (automatic and server-specific), and server creation with connect=true.
Kad start only changes running intent/status; bootstrap uses an existing DHT and
network bootstrap. Neither currently creates a runtime or invokes SQLite. Keep
shared error translation consistent without claiming unreachable SQL-fault proof
for those two routes. Review the existing start-without-runtime/Kad-only
lifecycle concern in the later native-controller cut; do not add production SQL
or artificial runtime work merely to make a fault fixture reachable.

## Schema 72 and typed owner checkpoint (2026-11-15)

Rust `b08709a1` adds bounded typed Kad load/initialize commands and a leased
snapshot payload through the shared owner. Rust `ca5e6993` persists the generated
Kad node identity in SQLite and selects fresh schema 72. Identity is durable
state, not a mutable application setting. The earlier schema 71 repository
checkpoint below is dated evidence, not the current fresh-schema declaration.

Parent-recorded focused proof: 112 metadata unit plus 3 integration checks and
517 Core checks plus selected integrations passed; the selected Python suite
passed 72 with one POSIX-only skip against the actual fresh selected schema 72.
This is storage/owner proof. Production DHT identity binding and runtime
restore/import/checkpoint wiring are in progress and not qualified by it.
The passing local peer campaign at `b509524f` exercised the earlier staged
runtime; it is not proof for the new schema 72 lifecycle. Keep runtime wiring on
the same owner and retain admission-before-copy, generation and drain contracts.

## Typed DHT boundary and shared-owner proof (2026-11-15)

Rust `45ca468b` adds typed DHT routing capture/restore and learned-key boundary
handling. The selected typed-boundary test sets passed 90, 59 and 141 checks.
This commit does not change SQL or wire the runtime persistence lifecycle.
The [#155 local peer/current-contract campaign](RUST-REF-016.md#registered-conformance-and-local-peer-checkpoint-2026-11-15)
records the subsequent ordinary-request/drain repair and passing rerun at
`b509524f`. Actual upload-byte progress under SQL contention and runtime Kad
checkpoint delivery are still pending; retain the same shared owner.

## Shared friend-owner dependency checkpoint (2026-11-15)

The [#155 scoped friend-owner checkpoint](RUST-REF-016.md#scoped-friend-owner-checkpoint-2026-11-15)
records implementation at Rust `ea0f9653`, focused Core/REST/integration proof
and selected-artifact OpenAPI validation. Historical discovery notes below
predate that worker implementation. This does not claim runtime Kad persistence,
the canonical settings/CLI redesign, all-SQL async conversion, actual upload
contention behavior or combined-scale qualification. Continue through the same
owner rather than add another persistence lane.

## Typed metadata checkpoint (2026-11-15)

Rust `c14433d5` adds typed Kad routing snapshot persistence; `82181294` makes
SQL column ownership explicit. That checkpoint used fresh schema 71. These commits
are pushed on the round-one branch, not merged delivery. Snapshot replacement,
validation and initialization status use coordinated metadata transactions;
no opaque source-file or serialized contact blob is the stored authority.

Focused metadata proof: 108 unit plus 3 integration checks passed. The existing
Python selection against an actual fresh schema 71 from the selected Rust
sources passed 80 with one POSIX-only skip; retained XML is
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/public-foundation-round-1/schema71-python.xml`.
The selected companion heads are Rust `82181294`, tests `d14d5871` and tooling
`9a2d3deb`. This adds metadata repository capability only. Runtime Kad snapshot
admission/checkpointing, source-file removal, settings/REST work and full-scope
qualification remain pending. Runtime wiring waits for the shared
[#155-A owner](RUST-REF-016.md#allocated-foundation-owner-155-a-2026-11-15);
no competing actor or per-request blocking-task lane is authorized.

## Historical foundation discovery checkpoint (2026-11-15)

Round-one branch evidence: Rust `70e595a2`, build-tests `d14d5871` and
specification/policy baseline tooling `77b30a82`. These are pushed checkpoints,
not merged delivery; no PR is authorized before the operator returns.

The first scoped implementation adds independent durable discovery-initialization
state and atomic server-list initialization. Automatic server import accepts the
first validated nonempty fallback, preserves explicit empty/disabled operator
state, and does not overwrite a list changed while a fetch was in flight. The
existing Python harness uses selected-workstream fixtures and transactional
explicit server inputs, preserving deterministic public-bootstrap isolation.

Focused evidence recorded by the parent: metadata 104 unit plus 3 integration
checks; daemon 108 unit plus 15 integration checks with one ignored helper;
Python 80 passed with one POSIX-only skip. Two review rounds resulted in
operator-race and explicit-fixture repairs. Normal push checks passed with
output-root-relative receipts:

- `reports/local-check/emulebb-rust/20261115T185408Z-f63dbe33`
- `reports/local-check/emulebb-build-tests/20261115T185216Z-90fd5f42`

This does not qualify the full public foundation. Kad file persistence removal,
the coordinated settings/REST redesign, library/download/search changes and
combined-scale proof remain pending. The accepted #155-A bounded persistence
worker is still unimplemented and is a prerequisite for runtime Kad checkpoint
wiring; reuse that owner rather than introduce a competing actor. Bootstrap
state alone is not a claim that runtime Kad persistence is complete.

## Summary

Make SQLite the durable authority for accepted Kad routing contacts while the
bounded live routing table remains in memory. Treat `nodes.dat` and
`server.met` strictly as compatibility import formats: parse and validate the
payload, merge its logical records, and discard the source bytes. Neither file
is profile state and the daemon must never create, refresh, or restore it.

This replaces the current `nodes.dat` startup, explicit-import, and graceful-
shutdown persistence paths. It also formalizes the existing `server.met`
behavior, which already imports server rows into SQLite without retaining the
payload.

## Historical review baseline (2026-11-12)

Reviewed against product revision
`080a5dea70186da31dab958757b5b8c0fd883f82`, whose exact current schema is 68.
Verified library content is independent of downloads; Kad snapshot persistence
remains open work in this item. The earlier review at `7b295bda` and schema 54
is historical provenance, not the current schema contract.

- `server.met` URL import parses servers and merges them into the SQLite server
  repository. There is no canonical profile-local `server.met`.
- `nodes.dat` is currently both an interchange format and durable state. The
  daemon loads it at startup, explicit import writes it to the profile, and
  graceful shutdown replaces it with a bounded routing sample.
- The Kad routing table is bounded and memory-resident. Its contacts contain
  substantially more useful state than a basic endpoint, including verified
  status and UDP anti-spoofing key material.
- The beta persistence policy requires one exact current schema and explicitly
  forbids migrations, legacy reads, repair branches, and silent profile reset.
- The daemon's `discovery_bootstrap` path still seeds and loads a profile-local
  `nodes.dat`; core network control still writes it after import and shutdown.
  These are the remaining persistence paths to replace. Preserve the current
  accepted-contact count returned by a live import.

## Required Design

### Runtime and durable authorities

- The live Kad routing table remains the runtime authority while Kad is
  running. SQLite is its restart snapshot, not an unbounded observation log.
- Persist the routing table's accepted bounded contact set. A checkpoint must
  delete rows no longer represented by the accepted snapshot so stale contacts
  do not accumulate indefinitely.
- Keep open sockets, pending RPCs, searches, lookup queues, timers, retry
  scheduling, publish state, and other transient work in memory only.
- Restore usable, non-expired contacts from SQLite before Kad bootstrap begins.
  An initialized-empty collection must suppress hidden built-in/public fallback
  seeds and automatic repopulation. Explicit operator-configured bootstrap
  endpoints remain usable as distinct operator input. An unfinished fresh
  provider initialization follows the master's next-launch retry rule.
- Represent a bootstrap endpoint whose node identity is not yet learned as
  logical bootstrap data rather than fabricating a routing-table identity.

### SQLite contact semantics

The current schema must represent every field needed to restore the accepted
routing semantics without serializing a Rust struct or copying `nodes.dat`:

- Kad node ID when known;
- normalized IPv4 address and UDP/TCP ports;
- advertised Kad protocol version;
- UDP anti-spoofing key and the public IPv4 address to which it is bound;
- verified status;
- HELLO source UDP port, received-HELLO state, and requested-response-ACK state;
- observed UDP and TCP firewall flags;
- routing contact type and active probe type;
- bootstrap/import provenance where it affects bootstrap behavior;
- expiry, creation, last-seen, and last-type-change timestamps needed by the
  current routing policy.

The implementation may normalize this into more than one table, but it must
use typed columns and explicit constraints. It must not store an opaque
`nodes.dat` blob or a serialized in-memory contact as the durable model.

### Checkpoint lifecycle

- Mark the durable snapshot dirty when accepted routing contacts or their
  persistence-relevant metadata change.
- Coalesce dirty changes into periodic checkpoints every 15 minutes. A clean
  interval does no SQLite write. Explicit import and graceful shutdown are
  immediate checkpoints outside that periodic cadence.
- Capture and admit the final snapshot before cancellation or the network
  teardown timeout can discard its source runtime. Then complete accepted
  persistence/finalization and drain/join before connection/profile-lease release.
  Never rely on a snapshot request made after teardown has already canceled Kad.
- A successful explicit `nodes.dat` import commits its normalized logical
  contacts immediately, even if Kad is stopped. If Kad is running, merge the
  same normalized records into the live routing table.
- Use one transaction per checkpoint/import so readers see the previous or the
  complete new snapshot, never a partial contact set.
- A periodic write failure is visible in diagnostics and leaves the snapshot
  dirty for a bounded retry. A shutdown write failure is reported but must not
  resurrect a met-file fallback.

### Generation and compact key projection

This accepted integration contract remains pending implementation. Keep routing
mutation generation, coarse learned-key generation and the database CAS revision
as separate concepts. A database revision is not the dirty signal, and a coarse
key-cache change alone is not proof that persisted routing evidence changed.

At the 15-minute checkpoint boundary, derive an exact, stably ordered compact
projection of durable key/binding evidence for the accepted routing contacts.
Compare relevant identities, endpoint/key and bound-address values, not a digest,
count or unrelated peer-cache activity. A non-routing key-cache change whose
projection is unchanged must not create a database checkpoint. Route changes or
changed relevant key evidence require a coherent bounded full snapshot.

Fence capture against routing/key-generation and binding changes; never publish
or acknowledge a stale mixture. Only acknowledge the captured generation and
projection after successful persistence for that runtime generation. Concurrent
new mutations remain dirty. A delayed snapshot must not overwrite a newer
explicit import or replacement runtime; retain database revision CAS as the
independent durability guard. Generation exhaustion must not silently wrap.

Reserve and measure projection, snapshot and conversion costs under the shared
bounded-owner contract before cloning. Use the actual routing table as membership
authority; do not introduce a second long-lived shadow-membership registry or
another persistence worker. The comparison projection is a bounded derived
checkpoint aid, not a competing routing authority.

Required proof includes no-write clean intervals and irrelevant-key changes,
relevant learned-key/binding changes, route membership changes, mutation during
capture, delayed old-runtime completion and revision conflicts. Preserve final
snapshot admission before cancellation/teardown and final drain before lease
release. These are acceptance requirements, not current-runtime claims.

### Import and merge rules

- Keep the existing authenticated URL-import routes:
  `POST /api/v1/kad/operations/import-nodes-url` and
  `POST /api/v1/servers/operations/import-met-url`.
- Do not add unauthenticated, local-path, multipart-upload, or arbitrary raw-
  byte REST surfaces in this item.
- Apply existing payload-size, URL, parser, and contact/server validation before
  any durable mutation.
- Deduplicate Kad contacts by stable node identity and resolve endpoint
  collisions deterministically. Invalid or unusable records do not enter the
  durable snapshot.
- Merge without downgrading a stronger existing record. In particular, an
  import must not erase verified status, a usable learned UDP key and its bound
  address, a newer supported protocol version, or fresher runtime observations.
- Imported metadata may fill missing fields. Conflicting weaker imported state
  does not overwrite stronger live or durable state.
- `server.met` continues to merge normalized server rows through the existing
  server repository rules. The source bytes are discarded after parsing.

### No met-file persistence

- Remove profile-local `nodes.dat` reads and writes from daemon startup,
  explicit import, trusted discovery seeding, and shutdown.
- Trusted first-run discovery may download and parse a `nodes.dat` or
  `server.met` source, but it must commit only normalized logical rows and
  discard the bytes.
- Do not write `nodes.dat` or `server.met` as a cache, backup, export, recovery
  artifact, or compatibility fallback.
- Existing operator-owned met files are not deleted automatically. The daemon
  simply stops treating them as live profile state.

## Compatibility and Scope Constraints

- Evolve the checked-in current SQLite schema directly. This item provides no
  migration for profiles created by an older schema.
- The target process opens only the exact schema it was built for. Do not add
  legacy table probes, fallback reads, repair, or automatic profile reset.
- Keep verified library content, local-file identity, root membership, and
  download ownership established by RUST-REF-017 unchanged. This item owns only
  the Kad persistence boundary and met-file imports.
- Do not change Kad wire behavior, contact-admission policy, routing-table
  capacity, REST authentication, or server-selection policy except where the
  persistence boundary requires it.
- Do not turn the SQLite snapshot into the future autonomous observation index.
  RUST-FEAT-002 owns that separate logical domain.
- Do not add met-file export. If a diagnostic representation is later needed,
  it must be explicitly designed as a diagnostic artifact rather than profile
  authority.

## Acceptance Criteria

- [ ] A fresh current-schema profile can bootstrap, learn Kad contacts, stop,
      and restore its accepted routing snapshot from SQLite with no
      profile-local `nodes.dat`.
- [ ] The durable model retains the verification, UDP-key, endpoint, version,
      firewall/HELLO, routing classification, provenance, and freshness fields
      required to restore current routing behavior.
- [ ] Dirty state checkpoints after 15 minutes, clean state performs no write,
      and graceful shutdown checkpoints before discarding the runtime.
- [ ] Explicit `nodes.dat` URL import is durable immediately whether Kad is
      running or stopped.
- [ ] Import tests prove identity/endpoint deduplication and prove that weaker
      imported data cannot downgrade verified, UDP-key, version, or freshness
      state.
- [ ] Server and Kad imports retain their authenticated URL surfaces and parser
      limits while discarding the source payload.
- [ ] Startup, trusted seeding, explicit import, periodic checkpoint, and
      shutdown tests prove that neither `nodes.dat` nor `server.met` is written.
- [ ] An incompatible database still fails visibly under the exact-schema
      policy; no migration or met-file fallback is introduced.
- [ ] Existing Kad/server deterministic integration and WebUI smoke tests remain
      green with messages updated to describe import rather than file saving.

## Validation

- Focused metadata-store tests for the current schema, constraints, bounded
  snapshot replacement, and transaction rollback.
- Kad routing tests covering snapshot extraction/restoration, dirty tracking,
  expiry, and complete persistence-relevant field round trips.
- Import tests for every accepted `nodes.dat` layout, duplicate identities,
  endpoint conflicts, invalid records, and stronger-record preservation.
- Daemon lifecycle tests with a temporary profile proving SQLite-only startup,
  periodic checkpoint, graceful shutdown, and empty-profile trusted seeding.
- REST and WebUI tests for both authenticated URL imports and updated user-
  visible success text.
- A repository search and filesystem assertion proving no product path writes
  `nodes.dat` or `server.met`.

## Dependencies

This item is a prerequisite for RUST-FEAT-063. Semantic profile carry-forward
must transport logical Kad contacts and server rows rather than met files.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_kad-routing-maint.md` section 4.2 (existing): The built-in fallback still exists. The existing SQLite routing/bootstrap item explicitly preserves built-in seeds and owns bootstrap provenance; scope reconciliation should record this headless operational choice.

### Scoped Follow-up Acceptance

- [ ] Document fallback ordering and seed review/refresh responsibility.
- [ ] Do not fabricate verified identities or retain import met bytes as durable state.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

Make SQLite the durable authority for accepted Kad routing contacts while keeping the live routing table in memory. Treat both `nodes.dat` and `server.met` strictly as compatibility import formats: parse, validate, merge into logical database rows, and discard the source bytes. Never create, update, or restore either met file as profile state.

Reviewed against product `7b295bda` (schema 54). Kad SQLite snapshot persistence remains open after RUST-REF-017; its library/download boundaries remain intact.

- Add a current-schema SQLite representation for the bounded Kad routing snapshot, including the contact identity, IPv4 endpoint, UDP/TCP ports, Kad version, UDP key and bound public IPv4, verification and HELLO state, firewall observations, routing/probe classification, bootstrap provenance, expiry, and relevant freshness timestamps.
- Restore accepted contacts from SQLite into the in-memory routing table at startup. Keep sockets, pending RPCs, timers, search state, and other transient work memory-only.
- Coalesce dirty runtime changes into periodic checkpoints every 15 minutes. Clean intervals write nothing; explicit import and graceful shutdown checkpoint immediately outside the periodic cadence.
- Merge `nodes.dat` contacts deterministically and deduplicate them. Preserve a stronger existing contact rather than downgrading verification, learned UDP-key state, protocol version, or fresher observations.
- Keep the authenticated REST/WebUI URL-import surfaces. Do not add a local-file or upload surface in this item.
- Preserve the existing logical `server.met` behavior: imported servers become SQLite server rows and the payload is discarded.
- Remove daemon startup/shutdown reliance on profile-local `nodes.dat`, including trusted bootstrap seeding that writes the file. Empty durable state may use parsed trusted or built-in seeds without retaining met bytes.
- Follow the beta persistence policy: evolve the checked-in current schema directly; do not add migrations, legacy fallback reads, repair, or automatic profile conversion.

- Restart restores the bounded Kad contact snapshot from SQLite without a `nodes.dat` file.
- Dirty, periodic, shutdown, and immediate-import checkpoint behavior is deterministic and tested.
- Merge tests prove deduplication and non-downgrade rules for verified and UDP-key metadata.
- Startup, import, and shutdown tests prove neither `nodes.dat` nor `server.met` is written.
- Existing authenticated URL imports and Kad/server bootstrap behavior remain functional.

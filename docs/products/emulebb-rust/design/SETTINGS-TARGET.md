# Configuration And Settings Target

**Review target; not implemented or accepted as a runtime change.**
[RUST-CI-043 / #297](../active/items/RUST-CI-043.md) owns this specification.
The [target inventory](SETTINGS-INVENTORY.json) defines every proposed public
setting and bootstrap value, including owner, storage, type, units, defaults,
validation, sensitivity, visibility and application mode. Parent review must
accept the remaining target before implementation. The operator accepted the
clean bootstrap naming and target default ports below on 2026-11-12; this does
not accept the complete proposed leaf, storage or REST redesign.
Current user guides and OpenAPI remain
the authority for the implemented client.

## Ownership And Names

TOML contains process/profile/control-service bootstrap only. SQLite owns
mutable product settings and durable product state. Runtime sockets, timers,
queues and active work stay in memory; payloads, logs and diagnostics stay in
files. Requiring a restart does not make a product setting bootstrap material.

The operator-facing settings domains are `network`, `transfers`, `storage`,
`sharing` and `security`. Each value has one typed definition, persistence
owner and runtime consumer. JSON uses camelCase; TOML, SQL columns and Rust use
snake_case; URL segments use kebab-case. Apply these conventions directly.
There are no aliases, compatibility shims, fallback keys, semantic remapping or
silently ignored obsolete fields. Retired shapes are hard errors. The target
defines one spelling and meaning for each value.

`emulebb-settings` owns typed field definitions, defaults, bounds and cross-field
validation. `emulebb-metadata` owns settings transactions. Core coordinates
publication to the runtime owners identified in the inventory. HTTP behavior
belongs to the REST/OpenAPI contract; the SPA consumes that same schema and
build-generated field metadata. Implementation must generate/check leaf schema
and UI metadata from the typed definitions rather than maintain independent
lists of defaults or bounds. The review inventory becomes a checked generated
snapshot when those definitions are implemented; it is not another runtime
configuration reader.

## Bootstrap

The profile locator selects one profile before its private bootstrap is read.
An explicit `--profile` wins over the platform-default profile location. The
bootstrap file is `emulebb-rust-settings.toml`; the database filename is the
fixed profile-local `emulebb-rust-metadata.db`, not a product setting.

The only TOML table is `[rest]`, with these keys:

| Key | Target default | Responsibility |
| --- | --- | --- |
| `bind_addr` | `127.0.0.1:20017` | Authenticated REST/WebUI listener |
| `api_key` | Privately generated for a fresh bootstrap | Control authentication |
| `web_root_dir` | Unset | Optional static-asset location; default is `webui` beside the executable |

The process may receive `--rest-bind-addr` for an explicit run-scoped control
listener selection. Its precedence is CLI, then bootstrap, then fresh-bootstrap
defaults. This does not write the bootstrap or product settings. Product
settings have no parallel CLI or environment value authority. Workspace
`EMULEBB_` variables remain tooling inputs, outside the product settings API.

Both the top-level bootstrap and nested table reject unknown keys and invalid
types. Paths resolve once against the profile when relative; validation is
non-mutating. The key uses exact printable non-whitespace ASCII bytes, length
32..1024, and rejects the inventory's case-insensitive placeholder list. Fresh
generation uses 32 bytes from the OS CSPRNG encoded as hexadecimal. There is no secret-bearing CLI flag
or secret-bearing URL parameter.

The bootstrap is owner-only: Unix profile/file modes `0700`/`0600`, with the
corresponding owner-restricted Windows access. Reject unsafe existing access
with actionable diagnostics. Never print an existing key or include it in
settings, status, error values, ordinary structured logs or public examples.
Fresh-key provisioning may hand the newly generated key to the operator once;
this explicit provisioning handoff is separate from ordinary structured logs.
Changing that handoff requires a separately accepted bootstrap UX decision.
Rotation edits private bootstrap and takes effect on process restart.

The authenticated private diagnostic bundle has its own full-fidelity contract
under [#280](../active/items/RUST-BUG-178.md), including the exact API key and
sensitive values. Its warning, private labeling and acknowledgement remain with
that owner. The settings resource's secret exclusion does not change that
private export contract or assign backend redaction, a shareable export or a
logger rewrite to this review.

The operator explicitly chose this clean Beta3 bootstrap contract and target
REST `20017`, P2P TCP `20019` and UDP `20020` defaults. Use only canonical keys;
reject obsolete spellings without aliases, shims, fallback reads, remapping or
silent ignoring. Other proposed bootstrap validation, address-family or
key-generation changes are not accepted by this naming/default decision.
Preserve existing `--incoming-dir` and `--p2p-bind-interface` run
overrides in initial hardening; removing them needs a separate scope decision.
This review changes no reader or startup behavior and includes no profile
evolution work.

## Product Settings And Public Surface

The inventory specifies 68 proposed product controls. `normal` controls form
the primary console; `advanced` controls remain supported but secondary. Both
use the same contract and validation. Restart-bound network/NAT, binding and
security controls remain SQLite settings. Limits, live upload policy and server
connection policy have explicitly named runtime owners.

All numeric units are explicit in names and inventory. Rates are bytes per
second; storage floors are bytes; durations use their named units. Server
keepalive is whole minutes, with zero disabling it, under the contract owned
by [#223](../active/items/RUST-BUG-156.md). A zero value has meaning only where
the inventory states it. JSON integers remain exactly representable by the
first-party client and checked by the Rust type/validator.

Generated client identity and private keys belong to dedicated durable state,
not editable settings. Protocol TTLs/capacities, scheduler cadence, negotiated
capabilities and diagnostic probes remain implementation policies. Their
inventory entries describe ownership, not public controls. Autonomous Indexer
state and its retention model are outside this Client review.

Server entries, bootstrap endpoints, shared roots/ignore rules, categories,
friends and filter rules remain dedicated SQLite-backed collections. Do not
embed them in the settings snapshot. Bounded scalar arrays such as DNS resolver
endpoints and NAT backend preference are single leaf values. Imported filter
rules are durable product data; a mutable side file is not their authority.

`server.met` and `nodes.dat` are read-only compatibility inputs. Import actions
never create, refresh, replace or write them back. Their SQLite-state work stays
with [#233](../active/items/RUST-FEAT-062.md).

## Settings Representation

Use **validated structured domain documents**, one row per domain, in the one
profile SQLite database. Do not create a generic untyped scalar key store or a
parallel file. The target repository boundary is conceptually:

```sql
CREATE TABLE settings_documents (
    domain TEXT PRIMARY KEY CHECK (domain IN
        ('network', 'transfers', 'storage', 'sharing', 'security')),
    document_json TEXT NOT NULL
        CHECK (json_valid(document_json) AND json_type(document_json) = 'object')
) STRICT;

CREATE TABLE settings_revision (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    revision INTEGER NOT NULL CHECK (revision >= 1)
) STRICT;
```

This is a proposed settings representation, not executable schema work or a
product schema-version allocation. JSON object keys follow the JSON casing
rule; SQL identifiers stay snake_case. All rows decode into closed typed Rust
domains, with recursive unknown-field rejection and whole-candidate validation.
Startup rejects malformed, incomplete or invalid current-schema settings;
defaults are materialized only by the fresh-profile transaction. There is no
silent per-field substitution for invalid durable data.

Settings are bounded whole-snapshot reads and small conditional writes. No
runtime query needs to search a particular setting across profiles or join its
leaf against a large catalog. Domain documents therefore avoid duplicated
per-leaf SQL/Rust constraints and keep additions reviewable. Typed SQL columns
would be justified by relational query requirements that these settings do not
have. This choice makes no claim about catalog query performance and changes no
transfer/library indexes. [#298](../active/items/RUST-CI-044.md) owns that wider
schema review.

One read transaction captures all domain rows and the revision. One
`BEGIN IMMEDIATE` write transaction checks the expected revision and writes
every changed domain plus the next revision. Serialization and validation finish
before the first write. No update API may commit a domain independently. Use
checked revision arithmetic; exhaustion fails without changing state.

## One Settings Resource

The target resource is **`/api/v1/settings`**, with GET and PATCH only. It is
authenticated with `X-API-Key`, bounded to 256 KiB for a PATCH body and requires
`application/json` (an optional UTF-8 charset is accepted); request content
encoding must be absent or `identity`. Bootstrap credentials and generated identity are absent.
Existing dedicated collections, network/NAT status, logs and operations remain
separate resources. This review does not alter `/api/v1`, `apiVersion` or the
contract-version policy.

GET returns the full typed shape defined by the inventory:

```typescript
type SettingsSnapshot = {
  network: NetworkSettings;
  transfers: TransferSettings;
  storage: StorageSettings;
  sharing: SharingSettings;
  security: SecuritySettings;
};
type SettingsApplication = {
  state: "applied" | "restartRequired" | "applyFailed";
  pendingRestart: string[]; // canonical JSON pointers to restart-bound leaves
  pendingApply: string[];   // canonical JSON pointers whose publication failed
};
type SettingsRead = {
  data: {
    saved: SettingsSnapshot;
    effective: SettingsSnapshot;
    application: SettingsApplication;
  };
  meta: {
    apiVersion: "v1";
    settingsRevision: string;
  };
};
```

Each domain's exact fields, types, nullability and bounds are the inventory's
paths under that domain. No other domain or leaf is accepted. The revision is
an opaque decimal string on the wire, avoiding loss of integer precision. This
representation contains no generated timestamp or other per-request field.
Native responses retain `X-Contract-Version` and use
`Cache-Control: no-store, no-transform`.

GET and successful PATCH emit the complete `SettingsRead` as RFC 8785 canonical
JSON, UTF-8 without a BOM, extra whitespace or trailing newline. Hash those
exact response bytes with SHA-256. The strong ETag is the quoted ASCII value
`"settings-<saved-revision>-<digest>"`, with a 64-character lowercase hexadecimal
digest. The saved revision in the tag equals `meta.settingsRevision`; it is not
the full representation validator by itself. Responses use identity encoding
with no `Content-Encoding`; compression middleware must exclude this resource.
An additional representation encoding would require its own correct strong
validator and explicit contract review.

`If-Match` must contain exactly one tag in that format. Reject weak tags,
wildcards, lists and malformed revision/digest strings as invalid requests.
Saved revisions use canonical positive decimal digits, no leading zero, up to
SQLite's signed 64-bit maximum. The stored serialized complete snapshot is
bounded to 128 KiB before commit. The larger request bound accommodates escaping
of accepted long paths; string bounds apply to decoded values, not escaped
request bytes.

`saved` is the complete committed snapshot. `effective` is the runtime's admitted
settings snapshot: startup-bound leaves retain the captured startup values until
restart, while live policy leaves publish together. This is not a promise that
a socket is bound or a peer connected; those outcomes belong to network/status
resources. Application lists are sorted and contain canonical pointers only.
GET observes a settings publication barrier so it cannot combine half an update
with another revision. Capture saved rows/revision, effective values and
application state under the same ordered publication boundary, then derive
immutable response bytes and their validator from that capture. Every event
that changes effective/application data uses that boundary too. The resource
does not expose an ambiguous effective-revision scalar when the process has a
mix of live and startup-bound values.

An unchanged representation has identical bytes and ETag on repeated GETs.
Admission of saved values after restart or an application-state change changes
the ETag when it changes the representation, even if the saved revision stays
the same. A restart that changes none of the represented data keeps the ETag.

PATCH uses a closed, recursively partial `SettingsSnapshot` in the body, without
the response envelope. It requires `If-Match` from a successful GET. For example:

```http
PATCH /api/v1/settings
Content-Type: application/json
X-API-Key: <private-key>
If-Match: "settings-42-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

{"network":{"p2p":{"tcpPort":20029,"udpPort":20030}},"sharing":{"scanOnStartup":true}}
```

This is a schematic authenticated target request, not a current-client command.
It returns `SettingsRead` with the committed revision and explicit application
state. Listener settings in this example are saved and reported as pending
restart until a successful process restart admits them.

- Omitted leaves stay unchanged. Supplied objects merge their known leaves.
- `null` clears only a nullable override; its fallback is stated in the
  inventory. Null for a required leaf is rejected.
- A supplied array replaces that complete bounded leaf array. Validate item
  types, order, uniqueness and cross-field prerequisites before writing.
- Resetting a value means explicitly PATCHing its inventory default. There is
  no magic reset token or settings reset action.
- Empty bodies, empty supplied objects, duplicate JSON keys and unknown fields
  are rejected at every nesting level.
  A nonempty, valid patch producing the saved snapshot is a successful no-op
  only after its full current validator matches: no revision increment, write
  or runtime notification; unchanged represented state keeps the same ETag.
- Concurrent writers serialize. Compare the complete current strong validator
  under the publication/order boundary before any write; check the captured
  saved revision again inside the write transaction. Either a changed full
  representation or a failed revision compare-and-set returns 412 without a
  write. A saved revision alone is insufficient authorization to overwrite.

## Commit And Application Semantics

Authenticate and parse first; validate shape, field bounds and the complete
candidate, including cross-domain rules. Use the existing bounded persistence
execution boundary. Filesystem validation does not create directories or hold
the global core/DB mutex over async work.

Validate both the saved candidate and its projected effective snapshot before
writing. A live change cannot violate an invariant against startup-bound values
that remain active until restart. Such a request fails with
`SETTINGS_VALIDATION_FAILED` and the relevant canonical paths. For example,
lowering the live connection cap must remain valid against the effective
half-open limit even when the same request saves a smaller restart-bound limit.
The caller can save the startup-bound prerequisite, restart, then change the
live cap. Missing interfaces, changed filesystem access or failed binds after
commit are operational outcomes, not permission to silently alter durable data.

An owned settings coordinator orders mutations through commit and runtime
publication. Cancellation while queued writes nothing. Once accepted for
completion, dropping the HTTP caller cannot abandon a committed update. Capture
the current full representation and compare `If-Match` before accepting its
candidate for a write or a no-op. Keep mutation and effective/application events
ordered through candidate validation, commit and publication. The transaction
compares the captured saved revision before any write. No DB/global-state mutex
is held over awaited validation/driver work. A validation, precondition or
persistence failure changes neither saved state nor runtime behavior.

A changed effective/application state may cause 412 while the saved revision
is unchanged. After any 412, GET the complete resource again, reassess the patch
against its saved/effective/application data and submit its exact returned ETag.
Do not reconstruct a tag from a revision or blindly retry using a fresh token.

After commit, publish the precomputed live policy as one logical snapshot. Do
not expose mixed upload, download and connection budgets by independently
updating public owners. Release DB/global-state guards before awaited driver
notifications; those callbacks must not re-enter the update coordinator.
Restart-bound values remain pending rather than being described as active.

A post-commit publication failure cannot claim rollback. Return
`SETTINGS_APPLY_FAILED` with `details.committed: true`, the saved revision and
bounded `pendingApply`/`pendingRestart` pointer lists. GET remains the recovery
read for saved/effective state. Do not return the submitted values or secrets in
an error. Repeating an obsolete conditional request does not create another
revision. No implicit retry or profile repair is part of this contract.

## Errors

Errors use the native `error.code`, `error.message`, `error.details` envelope.
Details contain bounded canonical field paths and state/revision metadata,
never raw submitted values or credentials.

The exact error shape is:

```typescript
type SettingsError = {
  error: { code: string; message: string; details: SettingsErrorDetails };
};
type SettingsRule =
  | "syntax" | "shape" | "unknown-field" | "duplicate-key" | "null" | "empty"
  | "if-match" | "minimum" | "maximum" | "length" | "format" | "enum"
  | "array-size" | "duplicate-item" | "cross-field" | "effective-prerequisite"
  | "snapshot-size" | "path";
type SettingsErrorDetails =
  | Record<string, never>
  | { issues: { path: string; rule: SettingsRule }[]; truncated: boolean }
  | { settingsRevision: string }
  | { maximumBytes: 262144 }
  | {
      committed: true;
      settingsRevision: string;
      pendingApply: string[];
      pendingRestart: string[];
    };
```

`SETTINGS_REQUEST_INVALID` and `SETTINGS_VALIDATION_FAILED` use `issues`, capped
at 64 entries sorted by path/rule, with `truncated` reporting the cap. Paths are
canonical JSON pointers, or the empty root pointer for an unparseable document;
an unknown key is reported against its known containing object without echoing
the supplied name. Rules contain no submitted values.
`SETTINGS_PRECONDITION_FAILED` returns the current saved `settingsRevision`.
That value can equal the caller's saved revision because the full represented
effective/application data participates in the condition. The error contains no
replacement validator; a fresh GET supplies the representation and its ETag.
`PAYLOAD_TOO_LARGE` reports the request `maximumBytes`.
`SETTINGS_APPLY_FAILED` uses the committed-outcome shape. All remaining codes
use empty details. Messages are sanitized human text, at most 512 UTF-8 bytes;
clients branch on code/rules, not message wording.

| HTTP | Code | Outcome |
| --- | --- | --- |
| 400 | `SETTINGS_REQUEST_INVALID` | Invalid JSON, unknown key, wrong shape, empty patch, null misuse or malformed conditional validator; no change |
| 401 | `UNAUTHORIZED` | Missing/incorrect authentication; no state disclosure |
| 412 | `SETTINGS_PRECONDITION_FAILED` | Full representation validator or saved-revision compare-and-set failed; no change |
| 413 | `PAYLOAD_TOO_LARGE` | Request exceeds the bound; no change |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Unsupported body encoding; no change |
| 422 | `SETTINGS_VALIDATION_FAILED` | Field or complete-candidate constraint failed; no change |
| 428 | `SETTINGS_PRECONDITION_REQUIRED` | Required full `If-Match` validator absent; no change |
| 500 | `SETTINGS_PERSISTENCE_FAILED` | Transaction failed/rolled back; runtime unchanged |
| 500 | `SETTINGS_APPLY_FAILED` | Explicit committed outcome; application state available through GET |
| 503 | `SETTINGS_UNAVAILABLE` | Bounded executor/order admission unavailable; no write accepted |

These codes/statuses are proposed target definitions, not implemented OpenAPI.
Operational network errors do not turn an invalid request into a successful
settings change. Internal error causes remain sanitized private diagnostics.

## One P2P UDP Owner

The accepted target default is P2P TCP `20019` and **one P2P UDP endpoint `20020`**.
They are SQLite controls, not TOML keys. The network listener owner initializes
the shared UDP transport once; Kad RPC and eD2K client UDP use its receive/send
handles. Disabling Kad routing must not disable eD2K client UDP. With no enabled
P2P protocol there is no advertised active P2P endpoint.

Protocol classification, obfuscation key spaces, source filtering, request
correlation and malformed-input bounds remain protocol-specific. A Kad-specific
policy must not consume unrelated eD2K traffic. Reserved marker and encrypted
packet cases need their protocol goldens; this review does not redefine wire
formats or propose a second public socket.

NAT derives its local address and TCP/UDP mappings from the one P2P binding.
Only verified gateway/peer observations may change advertised external ports.
Every enabled, eligible UDP advertisement uses the same effective mapping in
eD2K HELLO UDP fields, eMule info and Kad/source advertisements; client
reask/callback sends use that transport. Disabled capabilities keep their
protocol-defined zero/omission behavior, verified against wire goldens. TCP
server login uses the same
effective TCP mapping owner. Mapping loss/remap updates advertisements and
reachability coherently; never advertise a query/probe socket's source port.

Server queries, DNS and STUN may use bounded request-scoped ephemeral sockets
for correlation, reply processing and egress pinning. They are internal
transports, not independently configured public listeners or advertised P2P
ports. A separate advertised listener requires demonstrated protocol evidence
and parent review. Higher default port numbers provide no security benefit.

## Implementation Queue

No slice is authorized by this review. Existing owners retain their work; the
parent allocates code only after accepting the target and reserving files.

| Slice | Existing owner | Dependency | Acceptance |
| --- | --- | --- | --- |
| S1: typed target definitions and closed bootstrap | #297 | Parent target acceptance | Complete defaults/units/validation, unknown-key rejection and secret exclusion |
| S2: settings repository and ordered atomic publication | Extend delivered #299; coordinate #155/#298 | S1 and shared persistence owner | One conditional transaction, rollback and cancellation guarantees, saved/effective state |
| S3: server behavior authority | #223 | S1; coordinate S2 core ownership | One connection-plan owner, whole-minute keepalive, correct live/restart state |
| S4: listener/default and shared UDP integration | #297 | S1/S2; S3 advertisements | Configured binds and advertisements agree on Windows/Linux; no extra public UDP listener |
| S5: REST/OpenAPI/SPA target | #297 | S1/S2; S3/S4 contract frozen for the slice | One resource, exact errors/ETags, generated schemas/controls and settings-resource secret exclusion |
| S6: durable collections and import boundaries | #233 for Kad, #298 settings/state coordination | S1; independent of S5 UI styling | Read-only compatibility inputs; collection state in SQLite; no mutable settings side file |
| S7: cross-platform qualification and current-doc update | #297 | Accepted implementation slices | Synthetic failure/restart/bind/conformance proof and qualified current instructions |

File reservations are bounded by slice:

- **S1:** `emulebb-settings/src/lib.rs` and `surface.rs`; daemon bootstrap/CLI
  types, fresh-bootstrap output and their tests. Keep runtime consumers
  untouched until their owner is assigned. Preserve the accepted bootstrap
  spelling/defaults; other reader changes require their own acceptance.
- **S2:** metadata settings repository/schema objects, `core/profile_state.rs`,
  settings methods in `core/app_api.rs`, and atomicity/router tests. Reuse the
  delivered #299 transaction and owned ordered completion; do not create
  parallel DB/HTTP atomicity fixes or a competing persistence actor.
- **S3:** server settings consumption and connection-plan functions, coordinated
  portions of `network_api.rs` and their focused tests. Core budget and listener
  reservations remain separate.
- **S4:** daemon network assembly/binding; core listener, reachability and NAT
  mapping paths; Kad RPC receive and eD2K UDP/HELLO adapters only where required.
  Parent serializes shared `network_api.rs` integration with S3.
- **S5:** REST settings handler/validator/routes, the canonical OpenAPI settings
  schemas, SPA types/forms/client error handling and conformance tests. Preserve
  the separate #280 authenticated raw private-bundle contract and owner. Derive
  leaf metadata from S1; no independent field/default registry.
- **S6:** existing Kad persistence/import owner. A filter-rule import/DB slice
  needs an explicit implementation assignment under #297/#298 before code;
  this specification allocates no unrelated table/index redesign.
- **S7:** persisted harness fixtures/checks, current product guides and examples
  only after the implementation is qualified. Review docs stay target-only.

Atomic settings #299 is delivered on current main `080a5dea`; preserve its
ordered completion, transaction, rollback and cancellation guarantees. It is
not evidence that the target representation, resource, revision or validator
is implemented. Six proposed live server controls still need the actual runtime
owner under #223; incoming-directory application remains startup-bound.

## Required Verification

Use synthetic disposable profiles and persisted supported runners. This review
opens no operator profile, creates no network runtime and executes no tests.

- **Definitions/defaults:** exact fresh bootstrap and DB defaults; all inventory
  leaves round-trip through typed definitions; mechanical casing; every unknown
  key rejected recursively; no hidden state/constants in the public payload.
- **Bounds:** integer overflow/precision, nullability, array replacement,
  duplicate keys/invalid enum values, request/snapshot size, IPv4/interface
  membership, NAT renewal/lease
  ordering, resolver prerequisites, path validation without pre-commit writes.
- **Atomicity:** accepted routed cross-domain PATCH with injected later SQLite
  failure; independent connection observes no partial update; restart loads the
  complete saved snapshot; failed persistence leaves runtime unchanged.
- **Concurrency/cancellation:** two conditional writers; stale full validator
  after waiting; DB revision compare-and-set failure; queued cancellation;
  cancellation after commit; read barrier; precondition checks before a no-op;
  no DB/global lock over awaited validation/driver work.
- **Representation validators:** stable canonical bytes/digest for unchanged
  GETs and no-ops; exact SHA-256/strong-tag syntax; no generated timestamp;
  effective/application change and restart admission alter the tag without a
  settings write; unchanged restart retains it; stale tags return 412 even with
  the same saved revision; recovery refetches and reassesses the whole resource.
  Identity encoding and no-transform survive response middleware. Reject weak,
  wildcard, multiple and malformed tags before any mutation.
- **Application:** live policy snapshot is coherent; restart fields stay pending;
  saved/effective cross-field prerequisites hold before commit;
  post-commit failure reports committed state and exact pending paths; restart
  admits the saved snapshot or exposes a bounded operational startup failure.
- **Secrets:** API key/private identity excluded from the settings/status
  resources, their errors, generated public schemas/examples and normal
  structured logging. Once-only
  fresh-key provisioning follows the accepted bootstrap handoff. Retain the
  separate #280 authenticated private-bundle full-fidelity tests and its
  warning/acknowledgement ownership. Authentication is mandatory on
  the settings resource; no URL/query credential transport.
- **Windows/Linux sockets:** fresh default-model assertions; actual TCP/UDP
  binds; nondefault configured ports; occupied/invalid bind handling; shared
  UDP Kad/eD2K plaintext/encrypted/malformed dispatch; Kad stopped/eD2K active;
  NAT remap/loss and every advertised port field. Keep request sockets distinct
  from advertised listeners. Do not substitute random ports for a default-bind
  acceptance check or silently skip an occupied-runner result.
- **Surface conformance:** exact GET/PATCH fields, errors, strong ETags,
  conditional writes, current OpenAPI and SPA controls move in the same accepted
  implementation; all schemas/default metadata agree with S1. No synthetic
  success count replaces a real persistence-failure route.

Binding tests disable external discovery in the fixture and use local peers.
Default-model verification is separate from isolated network execution. Heavy
validation is parent-serialized; optional platform work does not silently
change Windows/Linux requirements. Beta3 publication and long soak stay held.

## Source Evidence

Read-only source baseline: Rust
`15020b7663a6771bc2d6e8282416ea36a7d7c163`. The inventory records the reviewed
files. Key trace boundaries are daemon `DaemonBootstrapSettings` and
`DaemonProfile`, settings `CoreSettings`/`AppSettings` and surface registry,
metadata `load_setting_json`/`replace_settings_section`, core
`update_app_settings`/budget derivation/connection plan, REST request validators,
OpenAPI and SPA form serialization.

Shared UDP evidence is in `core/network_api.rs` listener assembly,
`kad-net/rpc/receive_loop.rs` foreign datagram dispatch, DHT raw datagram send,
`ed2k_client_udp/dispatch.rs` and `service.rs`, `ed2k_tcp/hello.rs`, and
`core/ed2k_net_drivers.rs` mapping/advertisement synchronization. Request-scoped
server UDP transport is in `ed2k_server/udp_runtime.rs`; DNS uses its bound
request transport in `core/hostname_lookup.rs`.

Source inspection establishes design dependencies and ownership, not executed
portability, performance, protocol parity or implementation completion.

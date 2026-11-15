# Configuration and settings target

**Accepted round-one target: 59 leaves; implementation and qualification pending.**
The operator accepted the [Public Foundation](PUBLIC-FOUNDATION.md) on
2026-11-15. That is the master scope and behavior specification under
[RUST-CI-043 / #297](../active/items/RUST-CI-043.md). This document owns the
settings-specific detail. The PM accepted the source-reviewed 59-leaf engineering catalog in
[SETTINGS-INVENTORY.json](SETTINGS-INVENTORY.json). This does not claim
implementation. Regenerate/check the final inventory from typed
settings definitions once implemented; do not create another runtime reader.

## Ownership and supported surface

TOML owns only process/profile/control-service bootstrap. SQLite exclusively
owns mutable product settings and durable product state. A restart requirement
does not make a setting bootstrap material. Runtime sockets, timers and active
work stay in memory; payloads, logs and diagnostics remain files.

Application groups are `network`, `transfers`, `storage`, `sharing`, `security`.
Each key has one typed definition, persistence owner and runtime consumer.
`emulebb-settings` owns types, defaults, bounds, units and whole-candidate
validation; `emulebb-metadata` owns coordinated transactions. Core coordinates
runtime application. REST/OpenAPI and SPA consume generated metadata rather
than independent default or validation lists.

JSON uses camelCase; SQL/Rust/TOML use snake_case; URL segments use kebab-case.
Names specify units such as BytesPerSecond and Seconds. Closed current types
receive normal validation, without shims, aliases, remapping, retired-input
lists or tests preserving removed names. Curate actual operator controls;
implementation tuning, generated identities and private keys are not settings.
Download priority and category priority defaults are absent.

## Bootstrap and profile

The sole TOML table is `[rest]`:

| Key | Default | Responsibility |
| --- | --- | --- |
| `bind_addr` | `0.0.0.0:20017` | Authenticated REST/WebUI listener |
| `api_key` | `change_me_123change_me_123change_me_123` | Accepted ready-package/fresh-profile starter secret |
| `web_root_dir` | Unset | Explicit assets directory; omitted default is `webui` beside executable |

Preserve existing bootstrap semantics, accepted key policy and minimum length.
Do not add secret generation, key-renaming or additional validation proposals
under this foundation. Keep secrets out of normal settings/status/log surfaces;
the separately owned authenticated private diagnostic contract remains intact.

Normal startup has only `--profile` as runtime configuration. Omission uses
`current_exe().parent()` on every platform; explicit relative paths use caller
CWD. Missing selected profiles can be created; read-only paths fail visibly.
Installed launchers may supply explicit writable profiles. Keep the fixed
profile-local bootstrap and database filenames. Do not add product environment
overrides or duplicate authorities.

## Accepted settings representation

This is the accepted engineering target for the next implementation slice, not
a claim that current schema 71, REST or CLI already implements it. Store one
complete typed `SavedSettings` document and its revision in a singleton row:

```sql
CREATE TABLE app_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    revision INTEGER NOT NULL CHECK (revision >= 1),
    document_json TEXT NOT NULL CHECK (
        json_valid(document_json)
        AND json_type(document_json) = 'object'
        AND length(CAST(document_json AS BLOB)) <= 131072
    )
) STRICT;
```

All five groups and all 59 leaves are present. Each leaf has the same typed
`{mode, value}` representation:

```typescript
type SavedValue<T> = { mode: "default" | "custom"; value: T };
```

The value type comes from that leaf's one authoritative definition. This is a
bounded typed settings document, not an untyped key/value/EAV store. Generate
value, saved and partial-update types plus field metadata/validation from the
same definitions; do not hand-maintain three independent 59-field catalogs.
Reuse existing nullable-update helpers where they express presence correctly.

### Default resolution

At startup, replace default-marked values in memory from the running typed
defaults before validating the resolved whole candidate. The stored value of a
default-marked leaf is not authoritative. There is no previous-default comparison,
intent tracking, per-field repair or caller revision check. Startup resolution
alone does not write the row or advance its revision.

A custom leaf retains its saved value, even when a later release's default now
happens to equal it. Equality classification happens only during an explicit
set: a set equal to the current default becomes default; otherwise it becomes
custom. Reset always selects default. Untouched leaves keep their modes.
A custom null is allowed only for a nullable leaf and, under the equality rule,
only while the current default differs from null. Required leaves reject null.

Future changes to compiled defaults must review valid custom/default cross-field
combinations. Never silently clamp a custom value or discard it to make a new
default fit. The compiled default document itself must meet whole-candidate and
serialized-representation limits.

### Coherent read and typed PATCH

GET returns one coherent capture of resolved saved settings/default markers,
admitted effective values, revision and application status. Use this data shape
inside the normal native envelope:

```typescript
type SettingsReadData = {
  saved: SavedSettings;       // five complete groups, all 59 tagged leaves
  effective: SettingsValues; // five complete groups, plain typed values
  application: {
    pendingRestart: SettingKey[];
    failed: SettingApplyFailure[];
  };
};
type SettingApplyFailure = {
  key: SettingKey;
  code: string;
  message: string;
  truncated: boolean;
};
type SettingsPatch = {
  expectedRevision: string;
  set?: SettingsPartial;
  reset?: SettingKey[];
};
```

`meta.settingsRevision` and `expectedRevision` are exact positive decimal
strings, no leading zero, within SQLite's signed 64-bit range. They are opaque
CAS tokens, not timestamps or counters clients should increment. The normal
native `meta` fields remain present. There is no full-representation ETag/digest
CAS requirement: runtime-only application changes do not create a second saved
settings validator.

`SettingsPartial` is a recursively partial version of the same five typed value
groups. It must distinguish an omitted nullable leaf from an explicit null.
`SettingKey` uses canonical dotted keys from the compiled 59-field catalog.
Reject unknown current keys, duplicate reset keys, an overlap between set/reset,
and a syntactically empty operation. Empty nested objects do not count as an
operation. Replacing a supplied bounded array replaces that whole leaf.

This is an exact target PATCH example, not a current-runtime command:

```http
PATCH /api/v1/settings
Content-Type: application/json
X-API-Key: <private-key>

{
  "expectedRevision": "42",
  "set": {
    "security": {
      "ipFilter": {
        "enabled": true,
        "filePath": "filters/ipfilter.dat"
      }
    },
    "transfers": { "maxConcurrentDownloads": 8 }
  },
  "reset": ["storage.incomingDirectory"]
}
```

The explicit 8 becomes default because it equals the current job-cap default.
Reset selects the current incoming default. Validate the entire resolved
candidate, including cross-field rules, before committing any of these edits.
Offline syntactic validation must not require the target interface or filesystem
to exist on the preparation machine; runtime availability is checked on apply.

### Revision, persistence and publication

One write transaction checks the expected saved revision and updates the document
and its checked next revision together. Use the shared bounded persistence owner
for runtime commands and retain required commit/publication work after caller
cancellation. Do not add another atomicity actor or per-request blocking lane.

Every successful explicit nonempty REST write and offline set/reset advances the
checked revision, even when the resulting value/mode is unchanged. A set equal
to an already-selected default is still a valid explicit operation. Startup
resolution alone never advances. Failed CAS, validation or database commit leaves
the document/revision unchanged. Exhaustion fails explicitly without wrapping.
Missing/malformed expected revision is invalid input; stale revision is a conflict.
An uncertain worker/commit outcome remains explicitly unknown until recovered;
do not translate uncertainty into a claim that the write rolled back.

After a valid commit, saved desired values remain authoritative even if live
application fails. Return coherent saved/effective/application status; report
failed fields rather than pretending the save rolled back. Restart-bound leaves
stay pending until restart. Capture the read under the same ordered publication
boundary so it cannot combine revisions or half-published live settings. Broad
service hot-reconfiguration is outside scope.

### Size and application-status bounds

- Request body: 256 KiB (262,144 bytes).
- Serialized resolved saved document: 128 KiB (131,072 UTF-8 bytes), checked
  before SQL. This is a whole-candidate constraint, not a promise that every
  individually valid leaf combination fits.
- Coherent read representation: 512 KiB (524,288 bytes), including compiled
  defaults/effective values and bounded application status.
- At most one failure entry per supported leaf; each message is bounded to 512
  UTF-8 bytes without splitting a code point, with explicit `truncated` state.
  Keys/codes use the bounded current catalog. Do not echo unbounded exceptions.

The typed `DocumentTooLarge` outcome maps to HTTP 413. Prove exact serialized
UTF-8 boundaries including JSON escaping, not just decoded character counts.
Do not silently truncate setting values or add arbitrary per-path limits that
regress accepted long-path support. Serialization and validation complete before
the first SQL write. The 59-leaf catalog below is an accepted target; current
code does not yet centrally enforce every target bound or application mode.

## REST, CLI and collections

Native settings live at `/api/v1/settings` and `/api/v1/settings/surface`, using
the common native data/meta and structured error conventions. Preserve current
native authentication; future adapters use their protocol's authentication with
the same secret. Typed bounds include request and response size limits.

Offline commands require explicit `--profile`:

```text
emulebb-rust --profile PATH settings get KEY
emulebb-rust --profile PATH settings set KEY VALUE
emulebb-rust --profile PATH settings reset KEY
```

They manage SQLite settings only, require the daemon stopped and use the existing
exclusive profile lease. Get prints only the resolved value; diagnostics go to
stderr. Each set/reset loads and validates the whole candidate, commits one key
atomically and advances revision without caller-supplied CAS. No JSON input
file or staged transaction. REST supports atomic multi-field changes.

Server entries, shared roots, categories, tags, friends and observations remain
dedicated collections, not settings blobs. IP-filter contents stay file-backed
with a configured source and explicit reload. Read-only network discovery
imports feed SQLite directly without retained met/dat files. Import scope
remains the implemented limited MFC scope; no Rust profile migration.

## Paths, numbers and deployment

Relative product paths resolve against the profile; absolute and supported UNC
paths are direct. No shell/environment/tilde expansion. Relative CLI profile and
import paths resolve against caller CWD. Explicit relative web assets are
profile-relative; omitted assets remain beside the executable. Expose resolved
paths where useful. Paths refer to the daemon/container filesystem.

Rates use bytes per second, storage sizes bytes, durations their explicit units.
Calendar timestamps use Unix seconds. JSON counters are numbers with documented
integer bounds and JavaScript precision limits; do not promise all 64-bit
integers are exactly representable in JavaScript or silently clamp them.

Docker uses `/config/emulebb-rust`, `/data/incoming`, `/data/temp`. Canonical
offline operations provision storage only on genuinely fresh first-run setup;
recover interrupted provisioning and preserve initialized profiles. Subsequent
launches pass only `--profile`. Saved settings own P2P interfaces and health
checks follow the configured listener. Existing Python harness owners prepare
new fixtures; no ad-hoc setup or parallel testing framework.

## Accepted leaf catalog

The machine-readable inventory owns exact types, bounds, defaults, application
modes and source evidence for these 59 leaves. Source review is at Rust
`70e595a2`; field consumers are inspected in the existing settings, daemon, core
and ED2K modules. Source defaults do not prove every current runtime wire is
correct. In particular, the existing connection coordinator cap is not an
active-job cap, and configured half-open limits must reach the admitted runtime.

The new job cap defaults to 8 with a built-in discovery-only exploration buffer 2.
The connection cap stays 500. Lowering the job cap drains admissions without
silently stopping current jobs. `storage.incomingDirectory` defaults to
profile-relative `incoming`; `storage.tempDirectory` to profile-relative `temp`.
They are selected for jobs under the master first-start/delivery rules.

`live` means the identified parameter owner admits it without restart;
`restart` means saved desired changes stay pending until restart. Do not label
server-plan or listener settings live without wiring and tests. Disk floors and
hostname enabled/resolvers already have rereading consumers. IP-filter explicit
reload rereads its admitted source file; changing its configured source remains
restart-bound in this round.

Bounds marked engineering target in the inventory must become central validation;
several current source fields have only integer types/runtime clamps. Defaults
and existing enforced floor/core/keepalive/flood bounds are source-backed. This
catalog is not a claim that current code implements all bounds or application
modes. Native counters remain JSON numbers; the settings catalog does not adopt
a blanket JavaScript-safe-integer limit.

| Key | Rust type | Default | Bounds/shape | Apply |
| --- | --- | --- | --- | --- |
| `network.ed2kEnabled` | `bool` | `true` | boolean | restart |
| `network.kadEnabled` | `bool` | `true` | boolean | restart |
| `network.autoConnect` | `bool` | `true` | boolean | restart |
| `network.p2p.bindIp` | `Option<Ipv4Addr>` | `null` | unicast IPv4; nullable | restart |
| `network.p2p.bindInterface` | `Option<String>` | `null` | nonempty UTF-8;256 bytes max; nullable | restart |
| `network.p2p.tcpPort` | `u16` | `20019` | 1..65535 | restart |
| `network.p2p.udpPort` | `u16` | `20020` | 1..65535 | restart |
| `network.nickname` | `String` | `"eMule"` | nonempty UTF-8;128 bytes max | restart |
| `network.connections.maxConnections` | `u32` | `500` | 1..2147483647 | live |
| `network.connections.maxNewConnectionsPerFiveSeconds` | `u32` | `50` | 1..2147483647 | live |
| `network.connections.maxHalfOpenConnections` | `u32` | `50` | 1..2147483647 | restart |
| `network.connections.connectTimeoutSeconds` | `u64` | `30` | 1..86400 | restart |
| `network.connections.callbackTimeoutSeconds` | `u64` | `45` | 1..86400 | restart |
| `network.servers.autoReconnect` | `bool` | `true` | boolean | restart |
| `network.servers.safeConnect` | `bool` | `false` | boolean | restart |
| `network.servers.usePriorities` | `bool` | `true` | boolean | restart |
| `network.servers.staticOnly` | `bool` | `false` | boolean | restart |
| `network.servers.acceptServerListUpdates` | `bool` | `false` | boolean | restart |
| `network.servers.connectTimeoutSeconds` | `u64` | `25` | 1..86400 | restart |
| `network.servers.reconnectIntervalSeconds` | `u64` | `30` | 1..86400 | restart |
| `network.servers.keepaliveMinutes` | `u64` | `0` | 0..1440 | restart |
| `network.servers.sessionRotationSeconds` | `u64` | `0` | 0..86400 | restart |
| `network.servers.deadServerRetries` | `u64` | `1` | 1..10 | restart |
| `network.hostnameLookup.enabled` | `bool` | `false` | boolean | live |
| `network.hostnameLookup.dnsServers` | `Vec<typed item>` | `[]` | bounded typed array;8 max | live |
| `network.nat.enabled` | `bool` | `true` | boolean | restart |
| `network.nat.requireInitialMapping` | `bool` | `false` | boolean | restart |
| `network.nat.backendOrder` | `Vec<NatBackend>` | `["pcp-natpmp","upnp"]` | bounded typed array;2 max | restart |
| `network.nat.pcpServerIp` | `Option<Ipv4Addr>` | `null` | unicast IPv4; nullable | restart |
| `network.nat.igdIp` | `Option<Ipv4Addr>` | `null` | unicast IPv4; nullable | restart |
| `network.nat.externalIpOverride` | `Option<Ipv4Addr>` | `null` | unicast IPv4; nullable | restart |
| `transfers.uploadLimitBytesPerSecond` | `u64` | `6348800` | 1..4398046509056 | live |
| `transfers.downloadLimitBytesPerSecond` | `u64` | `12499968` | 1..4398046509056 | live |
| `transfers.maxConcurrentDownloads` | `u32` | `8` | 1..2147483647 | live |
| `transfers.maxSourcesPerFile` | `u32` | `600` | 1..2147483647 | live |
| `transfers.maxParallelDownloadPeers` | `u32` | `2` | 1..2147483647 | restart |
| `transfers.upload.targetClientRateBytesPerSecond` | `u64` | `32768` | 1..4398046510080 | live |
| `transfers.upload.baseSlots` | `u32` | `12` | 1..64 | live |
| `transfers.upload.elasticPercent` | `u32` | `80` | 0..100 | live |
| `transfers.upload.queueCapacity` | `u32` | `10000` | 2000..10000 | live |
| `transfers.upload.sessionTransferPercent` | `u32` | `90` | 0..100 | restart |
| `transfers.upload.sessionTimeLimitSeconds` | `u64` | `7200` | 0..86400 | restart |
| `transfers.upload.creditSystemEnabled` | `bool` | `true` | boolean | live |
| `storage.incomingDirectory` | `PathBuf` | `"incoming"` | profile-relative or absolute; no expansion | restart |
| `storage.tempDirectory` | `PathBuf` | `"temp"` | profile-relative or absolute; no expansion | restart |
| `storage.minFreeProfileBytes` | `u64` | `1073741824` | 1073741824..5497558138880 | live |
| `storage.minFreeTempBytes` | `u64` | `5368709120` | 5368709120..5497558138880 | live |
| `storage.minFreeIncomingBytes` | `u64` | `5368709120` | 5368709120..5497558138880 | live |
| `sharing.scanOnStartup` | `bool` | `true` | boolean | restart |
| `sharing.kadPublishingEnabled` | `bool` | `true` | boolean | restart |
| `security.obfuscationEnabled` | `bool` | `true` | boolean | restart |
| `security.vpnGuard.mode` | `closed enum` | `"off"` | off / block | restart |
| `security.vpnGuard.allowedPublicIpCidrs` | `Vec<Ipv4Net>` | `[]` | bounded typed array;256 max | restart |
| `security.ipFilter.enabled` | `bool` | `false` | boolean | restart |
| `security.ipFilter.filePath` | `Option<PathBuf>` | `null` | profile-relative or absolute; no expansion; nullable | restart |
| `security.ipFilter.level` | `u32` | `127` | 0..4294967295 | restart |
| `security.tcpErrorFloodDetection.enabled` | `bool` | `true` | boolean | restart |
| `security.tcpErrorFloodDetection.intervalSeconds` | `u32` | `3600` | 60..86400 step60 | restart |
| `security.tcpErrorFloodDetection.threshold` | `u32` | `10` | 1..1000 | restart |

## Qualification boundary

Use the master specification's settings, revision, lease, restart/apply-failure,
Docker and combined-scale acceptance cases. Run normal checks and two review
rounds, retaining exact source evidence. This round ends at a tested pushed
checkpoint, with no PR/merge/publication until operator review. Future automatic
upgrades remain a design objective, not implemented machinery.

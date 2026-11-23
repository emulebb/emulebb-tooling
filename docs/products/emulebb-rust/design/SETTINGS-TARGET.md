# Configuration and settings target

The 59-leaf settings contract landed in [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349). The
[Public Foundation](PUBLIC-FOUNDATION.md) defines the shared behavior, and
[SETTINGS-INVENTORY.json](SETTINGS-INVENTORY.json) records the accepted leaf catalog.
The typed Rust definitions own the current field metadata.

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
Unknown keys/fields use ordinary current-schema errors, with no removed-name
recognition. Document the accepted settings surface only; remove superseded
shapes/examples instead of preserving comparison or historical guidance.
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

Store one complete typed `SavedSettings` document and its revision in a
singleton row. Offline settings commands, Core, REST and daemon startup use this
representation. Client adoption and qualification follow the foundation checkpoints:

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
An explicit set of null is valid only for a nullable leaf: it selects default
when the current default is null, otherwise custom. An already-custom null
remains custom if a future release default becomes null, like every other
untouched custom value. Required leaves reject null.

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
  code: "applyFailed";
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

The explicit 8 is custom because the current concurrency default is `null`
(automatic). Reset selects the current incoming default. Validate the entire resolved
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
service hot-reconfiguration is outside scope. Keep live application only where
straightforward; daemon restart is an acceptable way to apply configuration.
Do not add hidden configuration-application retry loops. An explicit settings
update or daemon restart retries application, with failures reported until then.
Ordinary protocol reconnection and download cleanup retry rules remain separate.

For a valid desired save that mixes live and restart-bound changes, validate the
proposed live values together with the effective restart-bound values. If that
candidate violates a whole-settings dependency, save the desired document but
defer the entire update until restart. Keep the complete effective capture
unchanged, including otherwise independent live edits, and report every desired
value differing from that capture in `pendingRestart`. Do not reject this valid
save, clamp values, or apply a subset of the incompatible update. This operator
decision was accepted on 2026-11-19. The pure declaration-driven application
planner implements the decision; runtime owner/consumer integration remains
part of the direct canonical settings cut.

The planner is implemented on Rust `2dad26c9`; all 55 settings tests pass in
`reports/settings-request-round-1/settings-application-plan.log`. Coverage
includes simultaneous dependent live fields, retained restart values, deferral
of independent live edits with an incompatible mixed update, and invalid input
without repair. The helper plans values only; it does not publish them as
admitted effective state. The existing runtime transfer policies already use
bytes per second, so this integration requires no new rate-conversion layer.

Return a bounded collection of independently detectable validation issues in
one response, each with a canonical setting path, stable code and readable
message; dependent checks require valid inputs. Any validation failure saves
nothing. Do not force repeated requests merely to discover the next independent
invalid field.

### Size and application-status bounds

- Request body: 256 KiB (262,144 bytes).
- Serialized resolved saved document: 128 KiB (131,072 UTF-8 bytes), checked
  before SQL. This is a whole-candidate constraint, not a promise that every
  individually valid leaf combination fits.
- Coherent read representation: 512 KiB (524,288 bytes), including resolved
  default-marked saved values, admitted effective values and bounded application
  status. Default metadata exposed by the settings surface is separate.
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

For a list-valued key, `VALUE` is one inline JSON array, for example
`settings set network.nat.backendOrder '["pcp-natpmp","upnp"]'`.
Ordinary values use plain text and the canonical key's type. Shell quoting
delivers the whole list as one argument. This remains a one-key operation;
reuse the standard JSON parser for list values. The literal `null` selects null
for nullable keys; string values otherwise remain literal plain text. Successful
set/reset commands print nothing to stdout.

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

`transfers.maxConcurrentDownloads` defaults to `null` for adaptive automatic
concurrency. A positive integer sets the ordinary ceiling with a fixed,
non-configurable 25% rare-opportunity burst allowance rounded up, always subject
to resource budgets. Sixteen active plus two preparation slots is an initial
qualification baseline, not a permanent count ceiling. The
[foundation scheduling contract](PUBLIC-FOUNDATION.md#resource-admission-and-discovery)
owns admission, scarcity and endgame behavior; no extra memory/burst setting is
introduced. The connection cap stays 500. Lowering the ordinary ceiling drains admissions without
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
| `transfers.maxConcurrentDownloads` | `Option<u32>` | `null` | null=auto; 1..2147483647 | live |
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

## Delivered implementation

The Rust typed declaration owns the saved document and generated schemas.
The singleton store enforces revision checks. The profile owner orders
durable writes with runtime publication, and the CLI owns offline edits.
See [Rust PR #349](https://github.com/emulebb/emulebb-rust/pull/349) for current source and validation. The
[development checkpoints](https://github.com/emulebb/emulebb-tooling/blob/07c034bbe59462244015a00204b68df4213ad75f/docs/products/emulebb-rust/design/SETTINGS-TARGET.md#typed-settings-implementation-boundary)
remain available in Git.

## Qualification boundary

Use the master specification for settings revisions, offline leases,
restart reporting, and scoped qualification. The live owners in this round
update in-memory state. A future fallible owner must report a committed save
whose runtime application fails.


### Harness settings fixtures

The existing Python metadata initializer seeds `app_settings` revision 1 with a
complete current saved document. Its defaults snapshot is generated from the
compiled Rust field metadata and lives at
`crates/emulebb-settings/tests/fixtures/default-settings.json` in the Rust repo.
The native defaults/catalog test checks exact equality with `SavedSettings`.
Product runtime code does not read this test fixture or gain another config input.

The stopped-profile fixture editor accepts canonical dotted keys and explicit
resets, preserves omitted leaves, classifies default/custom modes and advances
one revision per atomic edit. It checks the serialized document budget before
writing. Native startup remains the authority for product value validation.
Unknown keys, overlapping resets, oversized documents and SQL failures do not
partially update the document or revision.

Rust `f2f01d7d` passes all 32 settings tests, with retained output at
`reports/settings-request-round-1/settings-fixture-f2f01d7d.log`. Harness
`a849396a` passes all 41 tests in the existing `test_rust_metadata.py` owner via
Builder. Harness `0cbe8481` adopts this editor in the shared profile writer and
its launch/import, Android peer, library qualification and upload-soak callers.
The writer accepts canonical dotted keys and resets, validates supplied values
against `SettingsPartial` in the selected OpenAPI contract, and keeps server and
Kad bootstrap resources separate. Optional fixture inputs are omitted when not
supplied; nullable product values remain explicit. Section/row writers are gone.

Builder evidence under `reports/settings-request-round-1/` records 46 profile
writer passes and one POSIX-only skip in `profile-writer-second.log`; the broader
caller run records 382 passes and one remaining cross-client assertion failure
in `profile-callers-second.log`. After repairing that assertion, all 61 tests in
its existing owner pass in `profile-cross-client-final.log`. These are Python
fixture/caller checks, not live daemon or container qualification.

Harness `dd469f71`, `a0694400` and `a59a0018` adopt revisioned settings in the
native package smoke, Rust upload-cap callers and online P2P controls. The
package smoke restores a temporary download limit with its original default or
custom mode. Rust rate writes use bytes per second and submit once against the
observed exact revision. P2P controls stop before connecting when settings
conflict, application fails or a restart is pending. Direct smoke profiles seed
network choices before startup; the section-shaped network body adapter is gone.
The MFC rate caller continues using its own product API.

Existing Python owners pass 80 package tests, 106 upload/soak/cross-client tests,
and 188 client/P2P/direct-smoke tests with one POSIX-only skip. Logs are
`package-settings-second.log`, `upload-settings-first.log` and
`network-settings-first.log` under `reports/settings-request-round-1/`.
Tests exercise full-width revisions, original mode restoration, restart data
loss and conflict/apply-failure admission. They use controlled HTTP outcomes;
they do not qualify live networks or complete the packaged transfer campaign.
Harness `81570df5` adopts canonical settings in the NAT matrix and its direct,
OpenVPN and Gluetun callers. The default case resets the backend order; explicit
cases use the public backend choices. Every case verifies saved values and the
effective configuration after restart before evaluating NAT status. Conflicts,
lost effective values and unapplied settings stop the case. Existing Python
owners pass 45 tests, including generated-OpenAPI validation, recorded in
`nat-settings-first.log`. These are controlled outcomes, not live gateway proof.

Harness `dd27c771` verifies the local seeder's effective upload policy through
the canonical settings API. Harness `01ed0014` prepares the generic settings
write with a live observed revision, keeps HTTP 200 as its success criterion,
and selects the matching worktree's OpenAPI document by default. The generic
probe leaves full-library scan I/O to explicitly controlled library phases.
Unit validation exposed and replaced obsolete schema/root fixtures; the final
three focused regressions pass in `conformance-settings-focused-final.log`.

The existing native REST/OpenAPI campaign passes against Rust `f2f01d7d` and
Harness `01ed0014`, with graceful teardown. Its authoritative report is
`reports/rust-rest-openapi-ci/20261119T175332Z/report.json`. All 115 routes are
registered: 90 are exercised (38 successes and 52 expected errors), and 25
disruptive routes are intentionally skipped. Offline single-key settings,
profile ownership, local friend/upload controls, Kad persistence and category
persistence phases pass. Retained-job pagination traverses 100,000 jobs across
500 pages, including 99,000 completed and 1,000 unfinished jobs, and its restart
checks pass. The report explicitly leaves physical-library and memory-limit
qualification false. This is Windows/local evidence, not live VPN, Linux
container, WebUI or combined memory-tier qualification.

Harness `24cf800d` adopts canonical settings in Android storage configuration,
startup verification and fixture cleanup. Configuration uses the observed
revision, checks persistence, restarts through the existing service owner and
verifies saved/effective paths before accepting the result. Cleanup protects
both the active incoming path and a saved incoming path awaiting restart, and
compares the complete settings snapshot including revision. Existing owners
pass 320 tests in `android-storage-settings-first.log`.

Harness `7003293b` adopts the same contract in the synthetic Android delivery
and listener proofs. Temporary settings capture only the six current owned
leaves; restoration preserves their default/custom modes and unrelated fields.
Default leaves reset against installed defaults. Compensation requires the
confirmed fixture-write revision: lost responses or intervening settings saves
retain owned evidence for explicit recovery rather than issuing another write.
Existing delivery/listener tests pass all 84 cases, including those admission
faults, in `android-peer-settings-final.log`. These are controlled HTTP/ADB
outcomes; no phone or emulator was contacted and no APK qualification is claimed.

Harness `8c6c700b` adopts canonical revisioned settings in Android public-sharing
preparation and observation. Preparation checks saved values and defers network
start when a restart is required; observation requires effective values and no
pending application. The unfinished-download guard uses the current bounded
download resource. Its existing controlled HTTP/ADB suite passes 145 tests in
`reports/settings-request-round-1/android-public-settings-final.log`.

Harness `fcb669b0` shares strict cursor traversal between library roots, downloads,
Android lifecycle verification and retained-job conformance. Lifecycle checks
stream immutable job identities across every page without retaining the full
history. Existing owners pass 362 tests in `android-shared-pages-final.log`;
the final metadata-presence validation passes 18 focused tests in
`shared-pages-metadata-final.log`, both under the same report directory.

The native REST/OpenAPI campaign passes again with graceful teardown in
`reports/rust-rest-openapi-ci/20261119T182755Z/report.json`. The shared iterator
traverses all 100,000 retained jobs in 500 pages, 99,000 completed jobs in 495
pages and 1,000 unfinished jobs in five pages; restart counts are preserved.
Physical-library and memory-limit qualification remain explicitly false.
Android tests above use controlled outcomes, not an actual APK/device campaign.
The provisioning and WebUI checkpoints below supersede those integration gaps;
shared harness cleanup and complete platform qualification remain pending.

Rust `d8e7f657` shares synced temporary-file publication between hosted bootstrap
writes and fresh daemon startup. Initial creation never replaces an existing
bootstrap; failed publication leaves no partial final file and can be retried.
The accepted bootstrap template and keys remain unchanged. The Builder daemon
package suite passes 112 test executions with one isolated ownership fixture
intentionally ignored, including the two new publication regressions. Evidence
is retained in `reports/settings-request-round-1/bootstrap-atomic-daemon.log`.
This is Windows evidence for bootstrap-file publication, not qualification of
the still-planned Docker directory journal, recovery or atomic stage publication.

The feature checkpoints are pushed for Rust (`d8e7f657`), Harness (`f6819c12`)
and Tooling. Harness push validation passes 1,967 tests, with 16 platform skips
and five deselected cases; its exact evidence is
`reports/local-check/emulebb-build-tests/20261119T185438Z-0c3447f1/`.
The two initially failing source-wiring assertions now check canonical settings
while preserving the bilateral server-metadata and explicit P2P-binding gates.
Rust branch checks and the strict documentation build pass. This is a feature
checkpoint, with no PR, merge, main write or publication; the remaining scope
and platform qualification above are still open.

Rust `89c807a5` implements package-private container provisioning with an owned
same-filesystem stage, a durable bounded journal and a parent OS lock. Staging
uses the same prepared per-key operations as offline CLI settings under one
profile lease, then closes SQLite, syncs owned files and publishes with Linux
atomic no-replace rename. Default-marked storage receives package paths;
custom values and existing final profiles are preserved. A retained journal
after final publication deliberately authorizes no replay or cleanup. The
package supplies the existing durable parent; the initializer creates no parent
hierarchy. Static atomicity review identified this parent precondition, which
the source and regression now enforce. All 13 provisioning regressions now pass
on native Linux GNU/AMD64 and musl/AMD64, including actual no-replace rename and
restart at the journal/stage/final boundaries. The exact logs are
`reports/rust-linux/gnu-amd64/c50ed2869d2241088ad31c0b985c9a5b/container-profile-tests.log`
and `reports/rust-linux/musl-amd64/7c34c1642a364d9db8604805b8552ce7/container-profile-tests.log`.

Builder `29fdb42` and `6c0aec6` build, stage, audit and attest the private Linux
companion in GNU/musl packages. The scoped package/build/staging suites pass
318 tests in `reports/builder-unit/3937f7e087a3/` (one existing collection warning).
Harness `c72fde2e` prepares explicit image/VPN fixture settings through the
packaged offline CLI before starting the daemon and checks effective binding.
Its existing focused owners pass 94 tests with one Windows platform skip.
The Windows daemon package suite passes 112 tests in
`reports/settings-request-round-1/container-init-windows-daemon.log`; Linux-only
provisioning tests are not included in that count.

The GNU/AMD64 and musl/AMD64 package builds and their selected Linux library,
tracker, durability and provisioning suites pass, producing source-verified
archives and the GNU DEB. Ubuntu/AMD64 and Alpine/AMD64 images build from those
bytes and pass the shared native
image smoke, including non-root ownership of config/incoming/temp, authenticated
REST/WebUI, health receipt validation and graceful shutdown. Evidence is
`reports/rust-image-smoke/50b492a5a63341b780b4f0ff07354858/`,
`reports/rust-image-smoke/a162a4899e854b7aa5a279f7ee23b9e1/` and
`reports/settings-request-round-1/container-init-gnu-package.log` /
`container-init-musl-package.log`.
Each image proof explicitly prepares a saved `eth0` fixture before s6; it does
not claim an unmodified default-entrypoint fresh start. Builder `5a6ef26`
requires both storage owners and that fixture declaration in the proof, with
169 image/security/candidate regressions passing in
`reports/builder-unit/4b4ed101b8c8/`. ARM64, actual VPN and memory-tier
qualification remain outside this checkpoint. No PR, merge,
main write or publication was performed.

Rust `02a5bdb5` replaces the WebUI settings form with canonical surface-driven
editors. Each emitted field carries an explicit default/custom choice; nullable
values have an explicit unset choice. Saves contain only changed nested values
and dotted resets, with the exact opaque revision. Saved and running values,
pending restart and application failures are visible. A conflict or uncertain
write outcome retains edits and requires an explicit discard/reload before
another save; the UI never retries the write automatically. Bootstrap descriptors
remain read-only and resource links retain their existing sections.

Builder WebUI validation passes 87 unit tests, 32 Chromium/mobile-WebKit browser
tests, TypeScript checking and the production build in
`reports/settings-request-round-1/webui-settings-final.log`. The browser fixtures
exercise representative field types, navigation, edits, reset, conflict and
application state; they do not prove that every real daemon field renders.
The settings-crate suite passes all 32 tests in
`reports/settings-request-round-1/webui-settings-rust-fixture.log`, including
the frontend default snapshot against all 59 canonical typed leaves.

Harness `cdb4f2fc` extends the existing native package/browser owner rather than
adding a runner. The source-verified Windows/x64 package at Rust `02a5bdb5`
builds with zero warnings and passes
`reports/rust-release-package/0141dc839a82/report.json`, with clean source
provenance in the adjacent `sources.json`. Its retained `webuiSettings` proof
checks all 59 emitted fields against actual saved modes and values (49 default
leaves in this explicit fixture), then confirms exactly two revisioned UI writes
to change and restore a live upload limit, including effective application.
No response uncertainty authorizes a compensating write. The same campaign
passes authenticated panel navigation, stale-key recovery, local 12 MiB delivery,
verified partial-download restart, offline-writer exclusion and graceful
shutdown. An initial run exposed the ownership probe's object-only unwrapping
of a root page; its fixture now controls HTTP bytes and exercises the real
envelope and cursor checks. The two focused Python owners pass all 139 tests.
Build and final campaign logs are
`reports/settings-request-round-1/webui-native-package.log` and
`reports/settings-request-round-1/webui-native-smoke-final.log`.

This is native Windows qualification with fresh local-only profiles; remaining
shared harness adoption, other platform/browser campaigns and memory-tier
qualification remain open. The feature checkpoints are pushed; no PR, merge,
main write or publication was performed.

Harness `321763e7` adopts canonical field editors in the fresh-default and NAT
browser helpers. Unchanged values retain their modes without a write. Changed
values use one revisioned save; application failures are errors, and a pending
restart stops a combined consumer-network workflow before it starts. The two
focused browser/package Python owners pass 156 tests. Harness `851d1b12` aligns
the default-tab polling check with the current exact 12-download preview while
continuing to reject broader download pages and unrelated secondary polling.
The native package campaign passes again in
`reports/rust-release-package/ecb0db6fcded/report.json`, including all 59 settings
and their live save/restoration; the log is
`reports/settings-request-round-1/webui-native-current-polling.log`. The NAT
configuration action itself has controlled-test coverage, not a new public
network or VPN execution claim. Harness `042fc180` removes dead Rust settings
branches from the shared REST smoke owner and corrects stale unsupported-feature
reporting; the frozen MFC settings path remains intact. All 145 tests in that
existing owner pass, including push validation retained in
`reports/local-check/emulebb-build-tests/20261119T210211Z-d0c009b5/`.

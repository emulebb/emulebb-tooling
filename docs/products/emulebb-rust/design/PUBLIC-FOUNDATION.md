# Public foundation: round one

Status: accepted implementation specification, 2026-11-15. This document records
the operator's consolidated decisions. It defines the round-one target, not a
claim that the current product implements or qualifies it. The PM coordinates
implementation under [RUST-CI-043](../active/items/RUST-CI-043.md) / #297 and
[RUST-CI-044](../active/items/RUST-CI-044.md) / #298, reusing the existing
persistence, Kad and harness owners. Progress and evidence belong in those
owning items, not a second branch-wide backlog.

## Outcome and delivery boundary

Deliver a coherent database, application-settings, CLI, REST/OpenAPI and WebUI
foundation for one universal, lightweight eD2K/Kad daemon. Design for year-long
sessions, 100,000+ library contents and download jobs, and future Arr,
Qui/qBittorrent and autonomous-indexer capabilities.

Start with fresh profiles. Do not implement migrations, compatibility shims,
aliases, old-schema readers, remapping, retired-name lists, special rejection
paths or tests preserving removed inputs. Remove superseded active code,
configuration, fixtures and documentation. Validate the current contract normally.
The future objective is adoption of new versions without breaking settings,
library data or public contracts; automatic-upgrade machinery and its enforcement
are not implemented in this round. This foundation replaces the earlier proposal
to postpone coherent contract design until after Arr implementation.

The authorized stopping point is a tested, pushed review checkpoint. **No draft
PR, PR, merge, main-branch write, release or publication until the operator returns
and reviews the result.** A pushed checkpoint is not merged delivery. Retain the
same branches for iterative review and corrections. Eventual delivery through
reviewed PRs and main remains the long-term objective.

The PM owns scope, contracts, sequencing, source selection, shared Git operations,
agent assignments and acceptance. Use one managed workstream named
`public-foundation-round-1`, with one persistent
`feature/public-foundation-round-1` branch per involved repository. Required
repositories are emulebb-rust, emulebb-tooling and emulebb-build-tests. Add
emulebb-build only when actual orchestration changes require it. Canonical main
checkouts remain intact. Each checkout has one writer; work and integration are
sequential on its existing branch. Shared schema, lockfile and validation work
is serialized. Read-only reviews may run in parallel. Use stronger reasoning
for ownership/concurrency/recovery and economical assignments for bounded wiring.

Make granular, coherent commits with normal hooks and focused validation; push
clean checkpoints. Do not create replacement branches or worker PRs. Current
baseline source identities are Rust `0840e900`, tooling `40f1a544`, build-tests
`17438846`; refresh and record actual selected revisions before validation.

## Contract authority and representation

This is the master behavioral specification. The detailed typed settings
catalog, schema and route inventories, OpenAPI, validators and SPA models must
agree with it. Reconcile conflicting proposals rather than maintaining parallel
accepted targets. [SETTINGS-TARGET](SETTINGS-TARGET.md) and its inventory retain
their detailed settings ownership role under this specification. Architecture
documentation describes only implemented structure.

- One daemon, one SQLite database and coordinated persistence ownership. Reuse
  existing repository, profile-lease and storage infrastructure; no competing
  persistence actor or adapter-owned shadow state.
- Use compact internal keys, explicit foreign keys, constraints, transactions
  and indexed access paths. All startup, recovery and shutdown paths also need
  bounded work; list pagination alone is insufficient.
- Application-allocated public IDs, including jobs, categories, roots, servers,
  searches and results, are immutable never-reused decimal strings. Content is
  publicly addressed by its eD2K hash; immutable tag names are tag IDs. Natural
  protocol identities remain distinct fields. SQLite may use internal keys.
  Upload/queue resource IDs identify live instances only: their catalog must
  define the process-epoch/lifetime boundary, expiry and restart behavior without
  reusing a prior ID or requiring durable per-connection history.
- Persisted and public calendar timestamps are Unix seconds. Runtime scheduling
  uses monotonic clocks and whatever finer precision it requires. Revisions,
  not timestamps, order changes and detect conflicts.
- Native JSON uses camelCase; SQL/Rust/TOML use snake_case; URL segments use
  kebab-case. Use explicit unit names such as BytesPerSecond and Seconds and
  lowercase string enums. Protocol adapters use their prescribed names/units.
- Byte totals and cumulative counters are JSON numbers. Document supported
  integer ranges and JavaScript precision limitations; preserve exact backend
  arithmetic within those ranges and never silently clamp values.
- Progress is a fraction from 0 to 1, or null when unknown. Unknown size is
  null, not a fabricated zero. Verified bytes, verification, delivery and
  completion are distinct facts.

## Settings, paths and CLI

### Authorities and defaults

Preserve the current TOML surface: one `[rest]` table with `bind_addr`, `api_key`
and optional `web_root_dir`. Preserve accepted listener `0.0.0.0:20017`, P2P TCP
`20019`, UDP `20020` and starter-key policies. This round introduces no bootstrap
key rename, extra live authority or replacement runtime environment overrides.

SQLite exclusively owns mutable application settings, organized by purpose:
network, transfers, storage, sharing and security. Curate supported controls;
remove duplicate controls and unsupported implementation tuning. Every supported
key needs one typed definition of its units, bounds, cross-field constraints,
default, owner, platform applicability and application mode. Derive consumers
and metadata from that owner instead of maintaining independent defaults.

Each saved setting has default/custom state. At startup a default-marked value
resolves directly to the running release's default. A custom value stays saved.
Writing a value equal to today's default marks it default. Reset marks default.
There is no previous-default comparison, intent tracking or startup CAS check.
Record a complete settings structure, including the default markers, rather
than ambiguous sparse overrides.

REST writes require the current settings revision and validate the whole
candidate atomically. Conflict or validation failure saves nothing. Keep saved
desired values if live application subsequently fails; expose effective values,
failed fields and restart-pending fields. Do not claim a failed change applied.
Keep established live application; broad service hot-reconfiguration is outside
scope. Successful saved changes advance the revision.

### Path rules

Relative application storage paths, category temp/destination paths, shared
roots and IP-filter paths resolve against the selected profile. Absolute paths
and supported Windows UNC paths are used directly. No `~`, shell-variable or
environment-variable expansion. Expose resolved paths where callers need them.
Paths refer to the daemon filesystem, including container namespaces.

CLI profile/import-source arguments remain relative to the caller's working
directory. Explicit relative TOML `web_root_dir` is profile-relative; its omitted
packaged default remains `webui` beside the executable. Unset category temp and
destination inherit global temp and incoming respectively; do not infer special
meaning from an empty path.

### Commands

Normal startup accepts only `--profile` as runtime configuration, with ordinary
help/version behavior. Omission selects `current_exe().parent()` on every
platform; an explicit profile can create a fresh selected directory. Installed
launchers may supply an explicit writable profile.

Preserve the implemented MFC-only offline operations and their limited scope:
`import-emule-profile` (including hashes-only), `import-shared-directories` and
`reconcile-shared-files`. Do not expand into Rust-version profile migration,
full settings/identity import or download restoration.

Add:

```text
emulebb-rust --profile PATH settings get KEY
emulebb-rust --profile PATH settings set KEY VALUE
emulebb-rust --profile PATH settings reset KEY
```

Offline settings/import operations require explicit `--profile`. Settings
commands manage SQLite application keys only, not TOML. Require the daemon
stopped and acquire the existing exclusive profile lease. A single-key write
loads, validates the whole candidate and commits atomically, advancing its
revision without caller-supplied CAS. `get` prints only the resolved value;
diagnostics go to stderr. No JSON input file or staged CLI transaction. REST
handles atomic multi-field edits. Use canonical typed settings services, never
direct package-specific SQL or a second parser/validation implementation.

## Library, sharing and upload accounting

### Knowledge and locations

Keep content knowledge, verified hashes, names, location caches, tags, sharing
state, upload priority and lifetime statistics when a root or every copy
disappears. Separate content, local instances and root membership. Distinguish
known, present, unavailable and eligible-for-sharing facts. A failed scan is not
proof of deletion. Withdraw unavailable copies and reconcile on return.

Reuse cached verification only when trustworthy filesystem identity and change
evidence permits; otherwise hash. A same-filesystem move or hard link can often
reuse native identity; a copy on another filesystem generally needs hashing.
Name, size and timestamps alone do not universally prove byte identity. A newly
verified copy joins the existing hash record and inherits its policies/tags.
Remote search claims never constitute verified local identity.

Global incoming and category destination roots are automatically shared
recursively. Do not follow nested symbolic links/junctions; external targets
require their own roots. Overlapping roots do not duplicate content. Removing a
root removes eligibility through it, not knowledge. After a category destination
changes, the old path stays shared only if another current root covers it.
Moving a file outside configured roots does not authorize searching arbitrary
folders for it.

Library rows represent one content hash, with local locations exposed separately
and paginated. Default to present content; provide Shared, Unavailable and All
Known visibility filters. Use flat lists, not folder browsing/tree navigation.
Filename search is case-insensitive substring matching, minimum three
characters, without query language, regex or additional word-search modes.

### Sharing policy and tags

The persistent sharing enabled/disabled flag is **hash-level**, affecting all
completed local copies. It is independent of download start/stop and upload
priority. Disabled completed content is not advertised, actively uploaded or
served to direct requests. Retain upload priority for re-enable. Remote cached
advertisements may outlive disable, but requests must still be refused. Do not
bypass the policy by serving another completed copy/path.

Verified partial-piece exchange while downloading remains separate and enabled;
the flag controls complete library content. Previously unseen content starts
enabled. Persist the flag even with no copies. REST sets true/false explicitly,
never toggle, with bounded per-hash bulk outcomes. External schedulers own
rotation; no built-in scheduling/rule engine.

Add flat many-to-many hash-level tags, independent of download categories.
Tag names are their immutable public IDs, case-insensitively unique, 1-64 ASCII
letters/digits/hyphens, starting with a letter or digit. No whitespace, dots,
underscores or rewriting. No rename operation: create a new tag and explicitly
change assignments. Deleting a tag removes its assignments, not content. Root,
filename, availability, sharing-state and tag filters support external subsets.

### Statistics

Per hash expose real current-process and lifetime uploaded bytes, upload requests
and accepted upload-session counts, plus last-request and last-actual-upload
timestamps. All copies contribute to one hash's counters. Session counters reset
on process start. Lifetime totals persist across root/file/policy changes.
Application totals are consistent with the documented accounting scope.

Checkpoint accumulating lifetime counters in batches and flush on clean shutdown.
A crash may lose the uncheckpointed statistics window. Do not require permanent
per-peer connection-history rows. Support server-side sorting by every displayed
library statistic, including session/lifetime values and activity timestamps,
with deterministic tie-breakers and measured bounded-resource implementations.

IP filtering stays file-backed with one configured source and explicit reload.

## Downloads and categories

Downloads have independent durable job IDs and only one active job per hash.
Keep compact completed jobs until explicit removal, separate piece/source cleanup
from terminal history, and retain prior-download knowledge independently of job
removal. No download-priority control, including category defaults.

Use only start/stop. Stop preserves the job and partial data; sharing remains
independent. Preserve intent across restart and resume eligible work gradually.
New jobs start by default with an explicit stopped-on-add option. Bound active
work using `maxConcurrentDownloads` with a built-in bounded exploration buffer.
Connection and source caps have separate meanings. Queued/history rows do not
each require live workers, timers or source machinery.

An active duplicate add returns its existing job unchanged, including category,
destination and intent. Size is optional; conflicting known sizes remain errors.
Local content that still exists requires explicit re-download. Confirmed absent
content can download normally while exposing past-download information. Recorded
copies on unavailable storage require explicit choice. Re-download gets a new
job ID and preserves prior history. Explicitly renamed unfinished jobs retain
their chosen filename; keep observed alternatives separately. Future majority
naming is outside scope and must respect explicit names.

Categories have stable immutable allocated IDs, renameable case-insensitive
unique names and nullable uncategorized assignment. All is a filter, not a stored
category. Deleting a category clears job assignments without moving/deleting
files. Category changes do not implicitly change tags.

At first start, choose optional category temp storage or global fallback and
retain that location for the job. At delivery start resolve the current category
destination or global incoming, then persist the selected attempt destination
for recovery/retries. Completed files stay put. Preserve the existing `_01`,
`_02`, ... collision rule and report the actual delivered path; never overwrite an
unrelated collision. Preserve the existing durable delivery recovery boundaries.

Removal requests explicitly state whether data is deleted. Keep-data removal is
supported only for completed delivered jobs. An incomplete job can remain
stopped or be removed with partial data; do not create orphan-partial ownership
and recovery features in this round.

## Search and knowledge foundation

One canonical search model distinguishes live/index/hybrid execution, with live
as the stable default and separate network-backend selection. Design all modes
now, advertise only implemented capabilities; autonomous index/hybrid execution
and index projections/APIs are later implementation.

Separate search metadata, paginated result summaries and provenance. Give
results stable claim identities based on hash plus size; preserve different
known size claims rather than collapsing them by hash. Unknown size is a separate
unresolved null-size claim, never a fabricated zero or automatic merge of
contradictory sizes. Remote claims never overwrite local verified
facts. Provenance includes meaningful origin, source/method, freshness and
validation evidence. A complete-source observation does not prove local bytes.

Implement reusable identities and independent claim/observation storage needed
by current searches. Permanent knowledge is independent of client session
membership and bounded protocol-cache expiry. Aggregate identical repetitions
using source identity, first/last seen and count; retain distinct claims and
meaningful metadata changes instead of every duplicate packet.

Retain search history and knowledge without automatic expiry. No required
search-delete endpoint. Stop ends collection while preserving results. Terminal
stopped/completed sessions freeze membership; late responses may enrich the
independent corpus. Mark running sessions interrupted after restart; callers
explicitly issue a new linked search instead of silently replaying it.

## Native REST, OpenAPI and WebUI

Use `/api/v1` with these domain resources:

```text
/settings
/settings/surface
/downloads
/uploads
/upload-queue
/categories
/library/files/{hash}
/library/roots
/library/tags
/searches
```

Keep other supported meaningful network/system resources; finish an exact route
inventory before the cut. Evolve daemon routes, typed DTOs, validators, OpenAPI,
SPA and harness callers together; do not expose transitional dual contracts.

Use correct HTTP status codes with `data`/`meta` success wrappers and structured
`error.code`, `message`, `details`. Never hide an error under HTTP 200. Specify
creation/acceptance/no-content and error status/body combinations exactly in
OpenAPI. Keep error codes stable and details typed where useful.

Use one bounded action endpoint per download operation:

```text
POST /downloads/start
POST /downloads/stop
POST /downloads/verify
POST /downloads/remove
```

Explicit ID lists, including one-element lists for single jobs, return per-job
outcomes. One failure does not roll back unrelated successes. Ordinary resource
attributes use updates, reads use GET. Native bulk operations initially accept
bounded explicit selections; no all-matching asynchronous selection framework.

Use live indexed keyset cursors, stable tie-breakers and optional exact totals.
Document weak traversal consistency under concurrent changes; do not retain
per-client collection snapshots. Never clone/filter/sort a full durable
collection before slicing a response. Runtime queues need bounded query/index
structures too. Separate thin list summaries from expensive details/evidence.

The WebUI is an operations console using bounded pages, not continuous scrolling
or unbounded accumulated row caches. Use server-side search/filter/sort, default
download view unfinished with explicit Completed/All. Fetch for the active view.
Keep lightweight native SSE change/reset notifications, coalesce refreshes and
use polling as fallback rather than redundant broad snapshot polling. Snapshot
is a bounded dashboard summary; its underlying work must also be bounded.

Design shared bounded in-memory canonical change tracking for future qBittorrent
incremental polling: changed identities, removals, revisions and restart/reset
boundaries. No per-client snapshots or durable event journal. Initial, stale or
reset polling gets a full snapshot, constructed without an extra full collection
clone. Native callers keep paginated browsing. Scope invalidation and baseline
capture must handle subscription/reconnect races and overflow explicitly.

## Future consumers and bootstrap

### Adapter design, not adapter delivery

Future qBittorrent and Torznab routes use their native paths on the same listener,
calling canonical services without loopback HTTP, duplicate credentials, shadow
jobs/categories, a second database or transfer engine. Design for official
unmodified Qui and Prowlarr, Sonarr, Radarr and Lidarr. Qualify exact official
API-key-capable releases before claiming interoperability; development-branch
support is not release proof. Future Qui/Arr qBittorrent routes use the existing
`api_key` via `Authorization: Bearer`; native routes keep their own specified
authentication transport with the same secret. No cookie-login system for older
consumers.

Qui/qBittorrent sync uses incremental `rid` polling with bounded shared history;
full updates are only for initial/reset/stale state. Project one latest retained
job per content hash; removal must not resurrect an older historical attempt.
Older jobs remain native history. Preserve padded eD2K-hash input/projection and
the accepted bounded Qui workflow in its future adapter specification, using
current canonical completion/category/removal behavior.

Arr/Qui/qBittorrent/Torznab implementations, autonomous indexing, broad protocol
emulation, new import scope and automatic database upgrades are outside this
round. Their requirements shape the foundation now.

### Fresh-profile network discovery

Automatically fetch and validate `server.met` and `nodes.dat` on fresh-profile
initialization and import directly into SQLite. Do not retain or write back
downloaded source files. Kad runtime routing state also uses the coordinated
database owner.

Server source order is eMule Security, Emuling, then Gruk; use the first
parser-valid nonempty list. Kad uses eMule Security; no independent working
fallback has been confirmed. Reachability/header checks do not replace parsing.
If all sources fail, keep the daemon/REST operational and retry unfinished
initialization at the next launch, not in a background retry loop. Persist
initialization separately from list contents; deliberate empty/disabled lists
are not silently repopulated.

### Docker and deployment

Use separate `/config/emulebb-rust` profile, `/data/incoming` delivered files and
`/data/temp` partial storage. Automatically save storage paths through canonical
offline settings operations only when provisioning a genuinely fresh profile.
Make interrupted first-run provisioning recoverable and fail visibly if setup
cannot finish. Never overwrite an existing profile or reapply settings at every
restart. The running daemon receives only `--profile`.

Configure P2P interfaces through saved settings; remove product override
environment bridges. Health checks follow the actual configured listener, not
a hardcoded port. Update launchers, Compose/VPN examples, both container variants,
package smoke tests and harness callers. Keep legitimate harness scenario inputs
that choose routes/interfaces and apply them through canonical profile setup;
do not confuse them with daemon runtime overrides.

## Ordered implementation and acceptance

| Phase | Required outcome |
| --- | --- |
| 1. Contract baseline | Reconcile policy and this specification, typed settings catalog, exact route/schema inventories, error/lifecycle contracts and query/index designs. Refresh source ownership, fixtures and baseline measurements. |
| 2. Persistence/domain services | Coordinated fresh-schema cut, durable jobs/history, content/location/tag/policy/statistics, categories, recovery, independent search claims and Kad persistence. Replace unbounded startup/list/recovery collection paths. |
| 3. Settings/CLI/provisioning | Default/custom resolution, revisions and application status, offline get/set/reset, fresh-only Docker setup and canonical harness profile preparation. |
| 4. REST/OpenAPI/WebUI | Routes, DTOs, validators, OpenAPI and consumers together; bounded action/query paths, substring/statistic sorting, shared change tracking and paginated active-view UI. |
| 5. Integrated checkpoint | Package/harness repair, failure/recovery and combined-scale qualification, independent review/repairs, clean granular commits and pushes. Stop for operator review, no PR. |

Each slice includes its directly affected consumers and scoped checks. Avoid
temporary compatibility adapters. The parent resolves routine technical choices;
material product/scope changes return to the operator.

### Harness ownership

**Reuse and extend the existing Python test harness suite.** Before adding a
helper, search both existing scripts and implementation modules and prefer the
closest established owner. Reuse launch, monitoring, fixture, evidence and
cleanup infrastructure. No parallel framework, ad-hoc launcher or improvised
monitoring loop. When ownership/suitability remains unclear after inspection,
ask the operator. Use supported Builder/workstream orchestration, inherited
environment and serialized heavy validation. Keep deterministic fresh fixtures
isolated from public bootstrap; replacing source-file sentinels must not cause
accidental public traffic.

### Required proof

- Default/custom startup resolution with changed running defaults, equal-value
  and reset behavior, revision conflicts, atomic candidate failure, committed
  but failed application, restart-pending reporting and offline lease races.
- Creation/re-download races, nullable metadata, immutable IDs, no historical
  resurrection, start/stop intent, bounded active work and retained history.
- Crash/restart at delivery phases, fixed selected temp/attempt destination,
  collisions and safe retries without unrelated overwrite/deletion.
- Root overlap/removal/offline/reappearance, trustworthy cache reuse versus
  changed-identity rehash, symlink rules and all-copy sharing enforcement.
- Tags/filters/bulk outcomes; complete sharing disable versus partial exchange;
  real session/lifetime accounting, checkpoints/clean flush and every sort.
- Search claim conflicts, repeated aggregation, independent corpus lifetime,
  frozen terminal membership and interrupted restart.
- Runtime/OpenAPI success/error conformance, bounded first/late pages, current
  validation, notification overflow/restart/baseline races and UI cache limits.
- Docker fresh/existing/interrupted setup, configured listener health checks,
  package launches and offline command behavior.
- One profile with **100,000 library contents plus 100,000 retained download
  jobs**, mixed completed/queued/stopped and bounded active work. Measure startup,
  first/late pages, substring search, every statistic sort, mutations, shutdown,
  memory and CPU. Inspect query plans and transient allocations, not only output
  sizes. Physical reference devices/hard budgets are deferred qualification.

Perform two distinct inspection rounds: correctness/contracts/failure recovery,
then interactions, maintainability and resource use. Repair material findings and
refresh affected checks. Do not repeat unchanged heavy matrices just to count
rounds. Run applicable gates available without a PR; retain PR-only/physical
device evidence as explicitly pending. Overnight proof does not establish
365-day endurance.

The goal remains active until the agreed checkpoint is actually achieved or a
real blocker requires operator input. Preserve evidence, branch heads and exact
companion revisions for iterative review. Report completed phases, pending work,
failed/unavailable gates and risks honestly. Do not substitute elapsed overnight
time, a launched process or a pushed partial implementation for acceptance.

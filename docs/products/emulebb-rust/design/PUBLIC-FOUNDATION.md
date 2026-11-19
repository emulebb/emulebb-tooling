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
Year-long operation means sustained correctness and bounded resource growth.
Operator-initiated restarts are acceptable, including for configuration changes;
restartless reconfiguration is not a requirement.

Start with fresh profiles. Do not implement migrations, compatibility shims,
aliases, old-schema readers, remapping, retired-name lists, special rejection
paths or tests preserving removed inputs. Remove superseded active code,
configuration, fixtures and documentation. Validate the current contract normally.
Current parsers know only supported commands, fields and settings keys; unknown
input receives their ordinary validation error. Do not recognize removed names
to provide a tailored error or preserve removed-input test cases.
Maintained product documentation and specifications describe the current
foundation only. Remove obsolete examples, superseded inventories, comparison
tables and explanations of removed behavior rather than archiving or documenting
them again. Git is the history. Retain current acceptance/evidence references
without turning the specification into an implementation-history narrative.

SQLite is an internal implementation boundary, not a public SQL contract.
External integrations use REST; direct database access is unsupported. Internal
components, approved offline commands and the existing test harness use the
canonical database services under their established ownership/lease rules.

The future objective is adoption of new versions without breaking settings,
library data or public contracts; automatic-upgrade machinery and its enforcement
are not implemented in this round.

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
is serialized. Team size, delegation and model effort follow the
[PM Coordination Policy](../../../reference/PM-COORDINATION-POLICY.md); use
bounded independent review for concrete risks.

Make granular, coherent commits with normal hooks and focused validation; push
clean checkpoints. Do not create replacement branches or worker PRs. Record
actual selected revisions with validation evidence in the owning items.

## Contract authority and representation

This is the master behavioral specification. The detailed typed settings
catalog, schema and route inventories, OpenAPI, validators and SPA models must
agree with it. Reconcile conflicting proposals rather than maintaining parallel
accepted targets. [SETTINGS-TARGET](SETTINGS-TARGET.md) and its inventory retain
their detailed settings ownership role under this specification. Architecture
documentation describes only implemented structure.

- One daemon, one SQLite database and coordinated persistence ownership. Reuse
  existing repository, profile-lease and storage infrastructure; no competing
  persistence actor or adapter-owned shadow state. The allocated
  [155-A owner contract](../active/items/RUST-REF-016.md#allocated-foundation-owner-155-a-2026-11-15)
  owns bounded FIFO admission through commit/publication and explicit drain/join.
  Friend CRUD integrates first; runtime Kad/settings work reuses it later.
  The owning item's scoped friend checkpoint records implemented paths and
  evidence; neither allocation nor that slice claims all persistence is async.
- After admission, the operation owner retains SQL completion, cache publication
  and required follow-up handoff despite request disconnect/cancellation. Never
  report success before the required handoff is accepted; report known-committed
  handoff failures honestly and drain through that same owner at shutdown.
  Reuse existing finalizers/reservations, not per-endpoint actors or tasks.
  Apply and audit this rule as each mutation phase is implemented; request
  disconnect is distinct from explicit business cancellation. Unreviewed paths
  are neither certified safe nor presumed faulty.
- Use compact internal keys, explicit foreign keys, constraints, transactions
  and indexed access paths. All startup, recovery and shutdown paths also need
  bounded work; list pagination alone is insufficient.
- A serious database consistency fault, including an uncertain commit outcome
  or untrusted integrity, stops new work, attempts safe shutdown without claiming
  a clean checkpoint, and exits with a clear fatal error and nonzero status.
  Require operator intervention; do not build a restricted diagnostic operating
  mode or automatic database repair. Ordinary request/storage failures keep their
  scoped handling and are not automatically classified as fatal consistency faults.
- Durable application-allocated public IDs, including jobs, roots, servers,
  searches and results, are immutable never-reused decimal strings. Content is
  publicly addressed by its eD2K hash; immutable tag and category names are their
  public IDs. Natural
  protocol identities remain distinct fields. SQLite may use internal keys.
  Live upload and upload-queue entries expose opaque UUID strings as `id`,
  addressed by `/uploads/{id}` and `/upload-queue/{id}`. Use lowercase hyphenated
  UUIDs and retain protocol identities in separate fields. Retain an ID
  while its entry survives, including ordinary reasks and transitions between
  waiting/granted/uploading. Removal or process restart ends that lifetime;
  subsequent entries receive fresh IDs. IDs are independent of protocol peer
  identity, credit identity and changing queue rank. Maintain no durable
  per-connection history or database ID allocation for these ephemeral entries;
  credits and lifetime accounting retain their separate persistence rules.
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
default, owner, platform applicability and application mode. The accepted 59-leaf
engineering catalog is in SETTINGS-TARGET/SETTINGS-INVENTORY. Coordinated
consumer integration and qualification remain pending. Derive consumers
and metadata from that owner instead of maintaining independent defaults.

Each saved setting has default/custom state. At startup a default-marked value
resolves directly to the running release's default. A custom value stays saved.
Writing a value equal to today's default marks it default. Reset marks default.
There is no previous-default comparison, intent tracking or startup CAS check.
Record a complete settings structure, including the default markers, rather
than ambiguous sparse overrides.

REST writes require the current settings revision and validate the whole
candidate atomically. Conflict or validation failure saves nothing. Keep
validation responses bounded and report all independently detectable field
issues together, with canonical setting paths, stable codes and readable
messages. Run dependent checks only when their inputs are valid. Keep saved
desired values if live application subsequently fails; expose effective values,
failed fields and restart-pending fields. Do not claim a failed change applied.
Keep straightforward live application; classify changes requiring complex
reconfiguration as restart-bound. No hidden configuration-application retry
loop: failures remain explicit, and retry is through an explicit settings update
or daemon restart. Broad service hot-reconfiguration is outside scope.
Successful saved changes advance the revision.

### Path rules

Relative application storage paths, category temp/destination paths, shared
roots and IP-filter paths resolve against the selected profile. Absolute paths
and supported Windows UNC paths are used directly. No `~`, shell-variable or
environment-variable expansion. Expose resolved paths where callers need them.
Paths refer to the daemon filesystem, including container namespaces.
The active profile and SQLite database require local storage. Temporary payload
data, library roots and completed destinations may use non-local storage where
the required filesystem operations can be performed safely. Use existing
filesystem primitives and explicit failures, without distributed locking or a
universal filesystem-recovery subsystem.

The canonical storage keys are `storage.incomingDirectory` and
`storage.tempDirectory`, defaulting to profile-relative `incoming` and `temp`;
`security.ipFilter.filePath` retains the external filter source.

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

For list-valued settings, `VALUE` is one inline JSON array, for example
`settings set network.nat.backendOrder '["pcp-natpmp","upnp"]'`.
Ordinary values remain plain text parsed according to the key's canonical type.
Shell quoting must deliver the list as one argument. Each command still writes
one key; use the standard JSON parser for list values, not a separate list grammar.

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
Shared-directory GET returns cached configuration and last observed health,
updated by the existing two-second monitor or explicit scans. New unverified
roots are conservatively inaccessible; reads do not probe the filesystem or
promise instantaneous truth. Physical root mutations/health work uses retained
blocking I/O.

Library rows represent one content hash, with local locations exposed separately
and paginated. Default to present content; provide Shared, Unavailable and All
Known visibility filters. Use flat lists, not folder browsing/tree navigation.
Filename search is case-insensitive substring matching, minimum three
characters, without query language, regex or additional word-search modes.
Match the stored display name only; names of other copies remain visible in the
paginated locations resource. Support multiple locations for serving and
availability without adding duplicate discovery, naming reconciliation or
deduplication features. Users manage duplicates with external tools.

Two library-view boundaries await the operator before the canonical list/detail
surface is implemented:

- Present: verified copies under currently configured accessible roots, or also
  verified copies outside those roots. Current-root-only is the recommendation;
  removing a root still retains content knowledge.
- All Known and hash detail: all client-owned hashes (accepted downloads and
  verified/imported content), or only content ever verified complete. The first
  is the recommendation; remote-only observations remain outside the library.

These recommendations are pending decisions, not accepted public behavior.

### Sharing policy and tags

The persistent sharing enabled/disabled flag is **hash-level**, affecting all
completed local copies. It is independent of download start/stop and upload
priority. Disabling is a publication/request-admission policy: skip future
publications and reject new upload requests, including requests on existing
connections. Requests accepted before disable may finish, including multiple
blocks covered by an accepted payload request. Payload acceptance is the granted,
source-bound verified-reader admission under the current policy and mutation
fence. Receiving a packet or holding a queue slot alone conveys no entitlement
to another payload request. A waiting queue entry is not an accepted payload
request and conveys no entitlement to a later data grant.
Recheck eligibility during ordinary slot selection and new block-request
admission, skipping/removing ineligible waiters through normal queue processing
without an immediate queue sweep. Publish the committed flag through the
existing policy owner and check it at normal request
admission. Retain upload priority for re-enable. Remote cached advertisements
may outlive disable, but new requests must still be refused. Do not bypass the
policy by serving another completed copy/path.

Verified partial-piece exchange while downloading remains separate and enabled;
the flag controls complete library content. Previously unseen content starts
enabled. Persist the flag even with no copies. `POST /library/files/sharing`
accepts `{enabled, hashes}` with an explicit boolean and 1-100 distinct known
hashes. Return HTTP 207 with ordered per-hash outcomes; an unknown hash is a
per-item 404 and is never created implicitly. Shared refusal returns 503 before
mutation; committed publication failures retain `committed:true` in their item
error details. REST sets true/false explicitly, never toggle, with bounded
per-hash bulk outcomes. Last successfully ordered
write wins; there is no per-hash revision mechanism. External schedulers own
rotation; no built-in scheduling/rule engine.

Retain the MFC-style upload ranking/credits, base-slot and elasticity controls,
and session-rotation behavior. Foundation work covers their canonical settings
wiring, persistence, bounded REST/WebUI visibility, resource accounting and
sharing/statistics interactions. Do not expand this round into an automatic
upload-controller or queue-algorithm redesign. Preserve protocol interactions
and qualify directly affected behavior through the existing harness.

Add flat many-to-many hash-level tags, independent of download categories.
Tag names are their immutable public IDs, case-insensitively unique, 1-64 ASCII
letters/digits/hyphens, starting with a letter or digit. No whitespace, dots,
underscores or rewriting. No rename operation: create a new tag and explicitly
change assignments. Deleting a tag removes its assignments, not content. Root,
filename, availability, sharing-state and tag filters support external subsets.

Tag assignments use only bounded bulk actions: `POST /library/files/tags/add`
and `POST /library/files/tags/remove`, with `{tag, hashes}`. Each request names
one existing tag and 1-100 distinct explicit hashes; a single hash uses the same
path. Return ordered per-hash outcomes using the native bulk response pattern.
Do not add parallel per-file assignment routes or create tags/content implicitly.

### Statistics

Per hash expose real current-process and lifetime uploaded bytes, upload requests
and accepted upload-session counts, plus last-request and last-actual-upload
timestamps. Unobserved event timestamps are null; epoch zero is a valid observed
timestamp. All copies contribute to one hash's counters. Session counters reset
on process start. Lifetime totals persist across root/file/policy changes.
Application totals are consistent with the documented accounting scope.
Count upload requests for known hashes even when sharing policy refuses them,
so the counter measures observed demand. Accepted-session and sent-byte counters
measure admitted service and actual transmission separately. Count an accepted
upload stint when its first verified payload is ready for transmission. Repeated
request packets and sharing-policy toggles do not create another stint. Releasing
or recycling a slot, or switching its requested hash, ends the stint; a later
admitted payload starts another. Requests for unknown hashes do not create
library records.

Checkpoint accumulating lifetime counters in batches and flush on clean shutdown.
A crash may lose the uncheckpointed statistics window. Do not require permanent
per-peer connection-history rows. Support server-side sorting by every displayed
library statistic, including session/lifetime values and activity timestamps,
with deterministic tie-breakers and measured bounded-resource implementations.

IP filtering stays file-backed with one configured source and explicit reload.

## Downloads and categories

Downloads have independent durable job IDs and only one unremoved unfinished
job per hash.
Keep compact completed jobs until explicit removal, separate piece/source cleanup
from terminal history, and retain prior-download knowledge independently of job
removal. No download-priority control, including category defaults.

Use only start/stop. Stop preserves the job and partial data; sharing remains
independent. Preserve intent across restart and resume eligible work gradually.
An unfinished download's storage failure requires explicit `start`, including
full-disk and unavailable-temp-volume failures. Persist a bounded failure code,
message and failure timestamp, expose the reason in detail, and retain the
failed condition across restart. An admitted explicit start clears that failure
for a new fenced attempt; refusal before admission changes nothing. Normal
network/source retries remain automatic and are not whole-job storage failures.
An unavailable delivery destination follows the same explicit-start rule for
unfinished execution. Preserve usable verified payload and reuse it where
straightforward. An unrecoverable partial download may require explicit removal
and re-download; this round does not promise recovery of every filesystem
failure or introduce a complex repair framework. Never report invalid data as
complete or modify unrelated files to obtain recovery.
Internal cleanup after completion or removal retries automatically through its
durable journal. Cleanup failure never restarts downloading, recopies a completed
output or regresses historical completion.
After an abrupt crash, recovery may re-download a small recent uncheckpointed
payload tail. Preserve consistent saved settings and start/stop intent, validate
checkpointed progress before reuse, never report incomplete data as verified,
and preserve completed outputs without repeating delivery. Do not require a
durable filesystem sync for every received block.
New jobs start by default with an explicit stopped-on-add option. The normal
workload is **10 to 1,000 incomplete downloads with 100,000+ completed records**.
Mass additions and 100,000 retained jobs remain scale/qualification cases; they
must not force one live worker, timer or piece map per job. Completed history
does not participate in source discovery or payload admission.

### Resource admission and discovery

Default concurrency is **automatic and adaptive**. Derive admission from charged
working-state memory, available system memory/pressure, and bounded connection
and I/O capacity. Respect applicable container limits; available-memory estimates
alone do not authorize allocations. **16 active downloads plus 2 preparation
slots** is the initial engineering/qualification baseline, not a permanent
product count ceiling. Replace the implementation's fixed eighteen-resident
restriction when delivering this policy.

Keep the setting name `maxConcurrentDownloads`, nullable with default `null`
for automatic adaptive concurrency. In automatic mode the scheduler chooses
the ordinary concurrency target; a configured positive integer supplies
the user's ordinary ceiling, subject to resource admission. Document that an
explicit ceiling permits a fixed **25% rare-opportunity burst, rounded up**:
for N ordinary downloads, at most N + ceil(N / 4) may be active under this
setting. Burst tolerance is not configurable in this round. Bursts never
override resource budgets, and ordinary work waits while above its target.
The global connection cap remains separately meaningful, currently 500.
Lowering admission drains existing work rather than silently stopping jobs.

A started job need not be a live payload execution. Waiting jobs use bounded,
shared discovery through server/Kad requests and short peer preparation probes;
the initial preparation allowance serves known-size jobs as well as metadata
discovery. Read small SQLite batches, cap outstanding requests and request rate,
persist validated observations, release probe resources, and rotate through
waiting jobs with retry backoff. Do not hydrate full execution manifests merely
to discover sources or inspect useful part availability. Do not add per-waiting-
job tasks or timers. Discovery buffers and networking require separate bounded
accounting; the resident manifest ceiling is not their allowance.

A ready job has a reachable source reporting a part it still needs. A payload
execution with no useful sources checkpoints and releases its slot/resident
backing safely, returning to waiting. Use a grace period for connection setup
and slow peers to avoid switching churn; an elapsed clock alone must not cancel
in-flight storage work. Under memory pressure alone, stop new admission, evict
unused cache, and let existing executions drain at safe release points rather
than proactively stopping them. Recover admission gradually to avoid oscillation.
Insufficient free space detected by preflight before payload work is resource
waiting with automatic reconsideration, not an execution storage failure.
Actual execution storage failures still require explicit start. A preflight
check does not guarantee that a later storage operation will succeed.
Bulk library scanning/hashing uses spare capacity and throttles under contention
to protect payload transfers, especially rare-part acquisition and endgame,
while keeping networking and REST responsive.

The resident manifest cache retains a **64 MiB soft target and an initial
128 MiB hard ceiling**, with update/checkpoint headroom reserved before admitting
more payload work. This ceiling does not grow automatically on larger systems
in this round. It covers per-part state/bitmaps, MD4/AICH hash lists, manifest
metadata, reader-pinned older versions, and admitted replacement backing;
payload bytes remain on disk. The existing **8 MiB native transient-work
budget** remains separate. Charge resident backing until its last reader
releases it, including after eviction. These are internal subsystem budgets,
not new saved memory settings, a second worker pool or a total daemon RAM limit.
Maximum-geometry retained-backing validation selected 128 MiB: eighteen entries
plus four admitted replacement credits require 120,696,504 bytes on the measured
Windows target. This is component evidence, not full adaptive concurrency,
total RSS or end-to-end acceptance; the owning
[runtime item](../active/items/RUST-REF-016.md) records remaining qualification.

### Scarcity, completion and endgame

Prioritize opportunities for **missing parts available from only one currently
known reachable source**. This is observed part scarcity, not the file's total
source count; an unknown count does not prove rarity. Admit a rare opportunity
as a resource-safe burst where possible. Otherwise yield an ordinary download
at a safe checkpoint, choosing the one with least recent useful payload
progress while protecting endgame work. Do not treat pending cancellation or
eviction as memory already released. If every active job is acquiring rare
parts or in endgame, burst only if resources permit; otherwise wait.

After capturing a rare part, a progressing download keeps its slot until it
stalls or completes, subject to later rare-opportunity displacement of ordinary
work. Rare opportunities always take precedence: do not add an aging rule that
guarantees ordinary downloads a protected turn during sustained rare demand.
For ordinary admission choose **fewest remaining bytes first**, with rotating
creation order for ties. This ranking does not itself interrupt progressing
downloads and introduces no public download-priority control.

Within a file, prefer scarce missing parts. Among equally scarce candidates,
finish an already-started part so it can be verified and shared sooner. Permit
bounded duplicate requests to different peers for outstanding blocks delaying
endgame completion; accept the first valid response and cancel redundant
requests. Bound redundant request/byte work under the same resource controls.

Expose a closed, nullable `waitingReason` through REST and the WebUI, separate
from coarse lifecycle state. A queued job has exactly one of three fixed codes:
`network` when networking cannot operate, `sources` when networking can operate
but no reachable source is currently confirmed to offer useful missing data,
or `resources` when useful work awaits scheduler admission/capacity, including
preflight storage headroom. Network absence includes unusable interfaces,
VPN policy blocking connectivity, and disabled networking. Disconnected sources
and discovery/retry backoff fall under `sources`; queue ordering, memory,
connections, I/O capacity and rare-opportunity displacement fall under
`resources`. Outside queued state the reason is `null`; stopped, metadata
waiting, storage failure, verifying and delivering retain their own lifecycle
semantics. These codes are not an extensible string set. Adding/changing a code
requires an explicit public-contract decision. Enforce state/reason combinations
in OpenAPI, backend checks and client types; detail belongs in network/failure
information and the resource summary, not new scheduler-specific reason codes.
Include one lightweight resource summary: active/preparing/waiting counts,
configured concurrency mode/value, current adaptive target, burst activity,
and resident-memory usage/budget. Coalesce updates rather than emitting per-block
events or fetching all jobs. Do not expose internal scheduling scores.

An active duplicate add returns its existing job unchanged, including category,
destination and intent. Size is optional; conflicting known sizes remain errors.
Local content that still exists requires explicit re-download. Confirmed absent
content can download normally while exposing past-download information. Recorded
copies on unavailable storage require explicit choice. Re-download gets a new
job ID and preserves prior history. Explicitly renamed unfinished jobs retain
their chosen filename; keep observed alternatives separately. Future majority
naming is outside scope and must respect explicit names.

Historical completion never regresses or automatically downloads again when
output disappears. Execution, verification, delivery and terminal completion
remain separately observable. Public `sizeBytes` is the persisted job expected/
learned total: admission may initialize an absent claim from accepted canonical
content, while independent verification fills an unknown total or fences an
incompatible claim. Verified content keeps its authority; reads never silently
rewrite job claims. The [2b/2c storage allocation](../active/items/RUST-CI-044.md#allocated-download-job-storage-cut-phases-2b2c)
owns job children, callback generations and durable cleanup references.

Category names are their immutable public IDs. SQLite retains a positive
`AUTOINCREMENT` i64 key and nullable category foreign keys internally. The resource
is `{name, tempDir, destinationDir, comment}`: both paths are nullable strings
and comment is an editable string. Category names use the same rules as tag
names: 1-64 ASCII letters/digits/hyphens, starting with a letter or digit. Preserve
spelling; no whitespace, dots, underscores, trimming or rewriting. Names are
immutable: create a new category and reassign explicitly. Uniqueness is ASCII
case-insensitive through a SQLite `NOCASE` unique name constraint; cached matching uses
`eq_ignore_ascii_case`.
Duplicate case-insensitive names on creation return HTTP 409 with stable error
code `CATEGORY_NAME_CONFLICT`; invalid fields return 400 and missing IDs 404.

Creation requires a valid name; omitted paths default to null and
omitted comment to the empty string. PATCH omission retains a field, explicit
null clears only a path; PATCH edits paths and comment. All is a collection
filter, not a stored category; no synthetic category zero exists. Assignment is
nullable. Deleting a category clears only matching job references, without
renumbering categories or moving/deleting files. Category changes do not
implicitly change tags.
Recreating a deleted name creates a new internal category and does not relink
assignments cleared by the earlier deletion.
Address a category at `/categories/{categoryName}` using ASCII case-insensitive
lookup that returns the saved spelling. Download add/PATCH/search-download inputs
and download resources use one `category` field containing the canonical name
or null for uncategorized. An omitted add selector defaults to uncategorized;
an omitted PATCH selector retains the assignment. Transfer filtering uses
`category`, with omission selecting All.

Phase 2a also requires bounded category sharing publication: order SQL and
immediate authoritative caches, then retain the mutation receipt through a
tracked continuation in the existing sharing/health owner. A large filesystem
scan must not block unrelated friend/Kad persistence or hold locks across I/O.
Use indexed membership traversal, retain the eligibility safety fence until
publication succeeds, and report known-committed publication failures honestly
while preserving final Kad checkpoint/drain. Bounded eligibility reads use the
existing store outside ordinary persistence admission, with separately bounded
workspace/concurrency and tracked profile lifetime. For direct socket writes,
check the root epoch and admit an owned packet of at most the existing 200 server
items under a short lock, then release it before I/O. Earlier root changes
invalidate/retry; a later change may let that one in-flight packet finish, while
each subsequent batch rechecks. The [scoped category checkpoint](../active/items/RUST-REF-016.md#registered-category-checkpoint-2026-11-16)
records exact-source contract/lifecycle proof; remaining resource obligations
are not qualified by it. [#155-A](../active/items/RUST-REF-016.md#planned-category-publication-continuation-phase-2a)
owns bounded admission, leases and serving revalidation, alongside the
[#233 shutdown contract](../active/items/RUST-FEAT-062.md).

The local-eligibility finalizer registry tracks existing blocking
SQL/publication units through caller abort and shutdown. Its separate limit is
4 admitted units/8 MiB ordinary retained payload, reserved before clone/spawn,
in addition to the Core owner's 64 slots/8 MiB and bounded eligibility reads.
It introduces no persistence actor; seal/join its actual work after the final
Kad/network stage and before profile-lease release, as ordered below. This increases
the combined payload allowance; it is neither the Core's 8 MiB limit nor RSS.
One separately accounted prepared-ingest job preserves existing 256-GiB support.
Its 64-MiB representation lease includes a 4-MiB publication workspace and checked
path/text costs, follows actual hashing/results through SQL/publication after
caller abort, and takes one registry slot with zero ordinary bytes. The registry's
combined charged allowance is 72 MiB; Core's 8 MiB and read workspace are
additional.
Parser/SQL allocator costs and RSS are excluded. The category checkpoint provides
scoped monitor/root/reload lifecycle evidence; broader hash/scan and complete
parser/ingest allocation qualification remain open. Root SQL jobs
must settle before profile release. This does not complete phase 2a or round one;
these plans add no public limit or actor.
Reuse one retained coalesced reload worker: an admitted root command's token
preserves successful SQL/cache scan intent across caller cancellation. Scans
must not restart a stopped monitor.

At first start, choose optional category temp storage or global fallback and
retain that location for the job. At delivery start resolve the current category
destination or global incoming, then persist the selected attempt destination
for recovery/retries. Completed files stay put. Preserve the existing `_01`,
`_02`, ... collision rule and report the actual delivered path; never overwrite an
unrelated collision. Preserve the existing durable delivery recovery boundaries.

Delivery verification is distinct from destructive ownership. A stable freshly
hash-matching recorded output can remain Delivered + Unowned with a refreshed
verification fingerprint conditional on the same job/path. Bytes alone never
grant deletion/overwrite authority. Materialization, promotion, retry and
restart must agree; pending storage cleanup must not recopy successful delivery.
Publish committed retirement/journal state coherently so cleanup remains
retryable in the same process and after reopen.

Use common capability/authority-preserving cleanup through exact job storage
and journals when atomic directory rename is unsupported. Preserve foreign
replacements, markers, symlinks and collisions; if safety cannot be proved,
leave cleanup pending without unchecked rename or recursive deletion. This
delivery/job-storage repair belongs to phases 2b/2c; the owning
[#155 analysis and acceptance](../active/items/RUST-REF-016.md#allocated-deliveryjob-storage-repair-phases-2b2c)
records its evidence and unimplemented status.

Removal of an unfinished or completed job requires an explicit `deleteData`.
Both modes retire daemon-owned internal pieces. `deleteData:false` preserves
completed outputs; `deleteData:true` additionally requests deletion of the exact
output only with proven job ownership. Independent and unowned copies are
preserved. Stop retains the job and resumable internal pieces; removal does not
create orphan-partial ownership and recovery features in this round.
Removing a completed job with `deleteData:false` leaves its output in the library
under the existing hash-level sharing policy, preserves prior-download knowledge,
and does not implicitly disable sharing.

## Search and knowledge foundation

One canonical model distinguishes live/index/hybrid execution. Live is the
implemented default; automatic/server/global/Kad selects its network backend.
Design index/hybrid and future adapters now, advertise only implemented
capabilities. Live sessions start empty and collect network observations only.
Passive-index lookups cannot preload session results or manufacture occurrences.

### Identities and provenance

SQLite allocates immutable never-reused positive i64 session and claim IDs,
rendered as exact decimal strings. Claim identity is hash plus nullable unsigned
64-bit size. Unknown, zero and contradictory known sizes remain distinct claims.
Remote claims never create verified local library identity or prove local bytes.

Permanent `content_claims` and typed `content_claim_observations` are independent
of session membership and protocol-cache expiry. Fingerprints include origin,
reporter and exact metadata presence/values. Aggregate identical occurrences by
first/last-seen seconds and count; preserve meaningful variants. `reporterEndpoint`
identifies the captured canonical reporting endpoint, separately from advertised
peer identity. Unknown reporters are null. Kad retains the queried IPv4 contact,
including replies without AICH. Store wire AICH as a typed 20-byte root; preserve
reporter-IP/version corroboration and the distinction between server claims and
accepted integrity authority.

`search_results` keys membership by session and claim. Its observation relation
references the permanent observation through composite claim/observation keys
and stores independent session-local occurrence times/counts. Terminal sessions
freeze membership and summaries while late packets can enrich permanent facts.
Retain history and knowledge without automatic expiry. Stop ends collection and
preserves results; explicit deletion/clear discards session membership while
retaining permanent knowledge. Restart durably records collecting sessions as
interrupted errors; callers explicitly create a new linked search through
ordinary `POST /searches` with optional `parentSearchId` and their chosen
criteria. The WebUI prefills criteria for editing and sends exact string IDs.
Creation uses the declared file-type tokens. The parent supplies provenance;
each new ID owns independent network collection and results. The creation
transaction validates parent existence; a missing parent returns HTTP 404
without allocating an ID.

Deleting a parent clears its children's `parentSearchId` while preserving the
children and results. The relationship uses `ON DELETE SET NULL`, an indexed
parent key and a check that the parent ID precedes the child. Unlinking advances
the child metadata timestamp. Status transitions preserve a committed unlink
when execution still holds its immutable creation specification.

`POST /searches/{searchId}/stop` durably freezes queued/running collection before
removing queued execution and cancelling its worker. It preserves session/result
membership and returns HTTP 204 without a body. Existing terminal sessions are
idempotent successes with unchanged metadata; an absent ID returns HTTP 404.
Stopped sessions expose status `stopped`, null `completedAt` and no active
progress. Late packets can update permanent knowledge but not the frozen session.
The WebUI offers Stop for queued/running sessions and continues to browse results.

### Durable reducers and ownership

Filename consensus gives at most one vote per reporter and normalized filename.
Known endpoints share one vote across server/global origins; unknown reporters
count once per origin. Repeated packets and changing counts do not multiply
votes. Store reporter votes, materialized name totals and an indexed winner.
Compare whole quality tuples (useful name, sources, complete sources, rating),
then binary normalized name. Size knowledge is constant within a claim.

For sources and complete sources independently, sum eD2K reporter maxima with
u32 saturation and compare that subtotal with the strongest Kad estimate.
Unknown eD2K reporters use one bucket per server/global origin. Keep independent
eD2K and Kad components so eD2K can overtake an initially stronger Kad estimate.
Generated columns expose their maximum without observation-history scans.

Select populated presentation fields independently using whole quality tuples;
equal quality prefers the smaller binary/numeric value. Keep source ID/port as
one pair, rating as a maximum and completeness as any complete report. Missing
fields never erase winners. Values live in `search_results`; `search_field_quality`
retains only their winning tuples. Ingress supplies bounded fresh presentation
observations independently of exact raw facts and filename votes.

The profile owner commits raw facts, membership, votes, availability, field
winners and count/time updates atomically. Its receipt contains the complete
committed summary. Allocation and publication remain owned after caller
cancellation; SQL failure publishes no uncommitted state. Uncertain outcomes
fault ingress and are not replayed automatically. Header writes contain no
result snapshot and cannot replay observations. Network forwarding uses bounded
channels, propagates backpressure and drains decoded occurrences on cancellation.

Use the existing 64-slot/8 MiB temporary-work owner. Reads use its blocking SQL
worker and retain reply charges through projection/serialization or caller drop.
Header/provenance rows/pages cap charged backing at 128/256 KiB. Summary rows/pages
cap it at 512 KiB/1 MiB. Selected download seeds retain 512 KiB and use a slim
indexed identity/name/source lookup plus at most 100 byte-bounded provenance rows;
permanent provenance stays separately pageable. Preserve High-ID source-hint and
AICH trust rules. Admission, failed reads, closing and explicit retry reuse common
patterns; do not manufacture hidden retries or copy full runtime configurations.

### Indexed browsing and native contract

Schema 101 maintains result cardinality transactionally and indexes collecting
sessions for startup interruption. Header pages seek newest session ID first.
Keep all twelve global result sorts: displayName, sizeBytes, sources,
completeSources, rating, fileType, artist, album, title, lengthSeconds,
bitrateKbps and codec. Sources descending is the default. Text uses binary
ordering. Claim ID breaks ties in the same direction. Unknown size sorts before
known size ascending and after it descending.

Each sort has a session-local index. A derived non-null size key distinguishes
unknown from the full unsigned size range; a composite foreign key binds the
membership key to the permanent claim, preventing contradictory copied size.
Cursors carry an anchor claim ID scoped to session/sort/direction, not arbitrary
text keys. Resolve that bounded key by primary key, then bind the explicit tuple
into the indexed range. Reserve 128 KiB preparation separately from the 1 MiB
result reply. Limits are 1..200, default 100; byte budgets can shorten a page.
Follow `hasMore`/`nextCursor`. Traversal is weakly consistent during live summary
changes; rows can move across a boundary. No per-client snapshots are retained.
An absent anchor in a retained session yields an empty page.

Use these independent resources:

```text
POST /searches                                      -> 201 metadata + Location
GET  /searches                                      -> cursor-paged metadata
GET  /searches/{searchId}                            -> metadata
GET  /searches/{searchId}/results                    -> sorted summary page
GET  /searches/{searchId}/results/{resultId}          -> selected summary
GET  /searches/{searchId}/results/{resultId}/observations -> raw provenance page
POST /searches/{searchId}/results/{resultId}/download -> exact-claim admission
```

Metadata exposes durable count and Unix-second created/updated/completed times,
with nullable active telemetry. Results contain materialized fields; raw evidence
has its own fixed observation-ID page. Unknown reported values remain null,
including counts/media values. Its first/last seen and occurrence count belong
to the selected session. Missing membership returns 404; busy/closing uses the
common 503/error contract. Download admission supports unknown size as waiting
for metadata; known zero stays a known empty file. Creation returns its owned
receipt without a second postcommit read.

The WebUI keeps one bounded session page, one result page and at most one selected
50-row observation page. It uses the server's global order, opaque cursors and
exact ID strings. First/Next replaces rows rather than accumulating caches.
Evidence loads on demand with explicit retry. Client validation and fixtures
adopt the same OpenAPI contract.

Diagnostic capture reads one newest-first metadata page (at most 64 sessions),
then at most 128 source-descending summaries per selected session. It reuses the
canonical session and result builders, never hydrates observations, and caps the
retained search-item JSON at the smaller of 1 MiB and the requested bundle budget.
Result omissions and continuation are explicit; the session collection has no
exact global total. The inline bundle contract is `emulebb.diagnostic-bundle.v7`;
search items contain `session` metadata and a bounded `results` collection. The
Python diagnostic collector consumes that same contract. Existing final bundle
encoding applies its exact overall byte cap afterward.

Kad completion resolves only incoming vote hashes through the indexed
`(session_id, ed2k_hash)` result projection. Its copied hash and size sort key
share a composite foreign key to the permanent claim. Header transitions return
persisted result cardinality and accepted vote hashes from the same transaction;
publication and diagnostics no longer inspect cached results for those facts.
The point probe must use no full scan and fewer than 100 SQLite VM steps even
with 100,000 conflicting-size claims for one hash or an absent session/hash.

Runtime search records contain only execution metadata and progress. Result
summaries and observation histories are never retained there. Ingestion prepares
only the incoming packet's fields/votes; SQL combines them with persisted state.
After commit, publication updates activity metadata. Terminal transitions remove
runtime records, while SQLite retains the session for browsing and downloads.
Startup interrupts collecting sessions durably and starts with an empty runtime
map. The bulk metadata hydration API and full-history data types are removed;
all consumers and fixtures use canonical point reads or bounded pages.

### Delivery and remaining acceptance

Storage tests cover first/late pages, all twelve sorts in both directions,
100,000 equal-key results, Unicode/binary order, unknown/zero/full-u64 sizes,
long anchor keys, byte-bound continuation, rollback, terminal freeze, independent
session/global counts, cascade deletion and interrupted startup. The production
late-page statements must use no full scan or temporary sort and fewer than 1,000
SQLite VM steps; the anchor point read must stay below 100 steps. Owner tests
cover retained charges, shared-budget refusal, closing, failed reads and explicit
success after repair. Native evidence reuses the existing Python metadata
fixtures, launchers and OpenAPI campaign.

The sorted-resource cut passes **293 metadata**, **660 Core**, **166 REST**,
**207 selected Python**, **58 WebUI unit** and **32 browser tests**, plus the UI
production build. Rust test compilation has no warnings. Evidence is in
`reports/settings-request-round-1/search-sorted-pages-{metadata,core,rest,python,webui}.log`.
The daemon and embedded WebUI build passed with zero warnings on Rust
`a00d9508`; evidence is `logs/builds/20261118T140114Z-build-clients/build-result.json`.
The native campaign passed on that executable with Harness `2aba4fc8`: **86
routes exercised, no failures**, seeded metadata/result/observation reads,
network-only live results and full-width search identities. Evidence is
`reports/rust-rest-openapi-ci/20261118T140557Z/report.json`; teardown was graceful.
This qualifies the sorted-resource checkpoint, not the pending cache removal or
combined library/job scale qualification.
The bounded diagnostic cut passes **167 REST** and **292 selected Python**
tests, including the persisted 260-result/128-summary capture and aggregate
item-byte budget checks. Evidence is
`reports/settings-request-round-1/search-diagnostic-{rest,python}.log`.
The daemon/WebUI build passed with zero warnings on Rust `e1c4ced6`
(`logs/builds/20261118T141959Z-build-clients/build-result.json`). Native
qualification with Harness `2418cead` passed 86 routes and validated the inline
bundle against OpenAPI, including equality with canonical session/result reads
(`reports/rust-rest-openapi-ci/20261118T142253Z/report.json`); teardown was graceful.
The WebUI diagnostic consumer is aligned with the published `v7` bundle in Rust
`0d5b0a42`. Its real REST client accepts the raw artifact, and the browser test
checks downloaded JSON content rather than only the filename. Harness
`c5ee9980` adds a current-contract consistency check comparing the producer and
WebUI identifiers with OpenAPI, preventing matching stale client fixtures from
concealing drift. **60 WebUI unit, 32 browser and 119 OpenAPI harness tests**
pass, including type checking and the production WebUI build. UI evidence is
`reports/settings-request-round-1/diagnostic-v7-webui.log`; the packaged
daemon/WebUI build has zero warnings:
`logs/builds/20261118T181705Z-build-clients/build-result.json`.
Backend code is unchanged by this client cut; existing native bundle
qualification remains the producer evidence, not a claim of a new live-browser
backend campaign.
The indexed completion cut passes **294 Metadata**, **660 Core**, **167 REST**
and **207 selected Python** tests, with no Rust compilation warnings. Evidence
is `reports/settings-request-round-1/search-membership-{metadata,core,rest,python}.log`.
The daemon/WebUI build passed with zero warnings on Rust `07e2b8ef`
(`logs/builds/20261118T143915Z-build-clients/build-result.json`). Native
qualification with Harness `45892855` passed 86 routes, retained search browsing
and canonical diagnostic capture
(`reports/rust-rest-openapi-ci/20261118T144212Z/report.json`); teardown was graceful.
The active-only runtime cut passes **294 Metadata**, **661 Core** and **167 REST**
tests without compilation warnings. It includes startup with 100,000 retained
sessions, durable interruption, an empty runtime map after paging, terminal
eviction, disconnect publication, restart/download selection and canonical
diagnostic capture. Evidence is
`reports/settings-request-round-1/search-runtime-{metadata,core,rest}.log`.
The daemon/WebUI build passed with zero warnings on Rust `3cc0bf93`
(`logs/builds/20261118T150810Z-build-clients/build-result.json`). The unchanged
Python harness qualified 86 native routes and retained search/diagnostic reads
(`reports/rust-rest-openapi-ci/20261118T151111Z/report.json`); teardown was graceful.
The Stop lifecycle cut passes **295 Metadata**, **665 Core**, **168 REST**,
**207 selected Python**, **59 WebUI unit** and **32 browser tests**, including
rollback, caller disconnect, repeated stops, terminal preservation, late-ingress
freeze and the Stop control. Rust compilation has no warnings. Evidence is
`reports/settings-request-round-1/search-stop-{metadata,core,rest,python,webui}.log`.
The daemon/WebUI build passed with zero warnings on Rust `c9235a4b`
(`logs/builds/20261118T155327Z-build-clients/build-result.json`). Native
qualification with Harness `e03d7afb` passed 87 routes and the positive
full-width-ID Stop proof; teardown was graceful
(`reports/rust-rest-openapi-ci/20261118T155620Z/report.json`).

The linked-creation cut passes **297 Metadata**, **667 Core**, **169 REST**,
**207 selected Python**, **60 WebUI unit** and **32 browser tests** without Rust
compilation warnings. It covers independent criteria/results, child preservation
across deletion/reopen, stale execution specifications after unlink, creation
rollback, disconnect ownership, exact IDs and selection outside an empty list
page (`reports/settings-request-round-1/search-parent-{metadata,core,rest,python,webui}.log`).
The daemon/WebUI build passed with zero warnings on Rust `0ef97f28`
(`logs/builds/20261118T163030Z-build-clients/build-result.json`). Native
qualification with Harness `4d1a626d` passed 87 routes and the positive
full-width-ID linked-creation/unlink/nonallocation proof; teardown was graceful
(`reports/rust-rest-openapi-ci/20261118T163329Z/report.json`).

Remaining work includes combined library/job memory qualification. Query-scale
evidence alone does not qualify app-wide resident memory or the complete
100k-library/job operating model. Settings/runtime,
CLI/Docker, library and remaining foundation gates retain their scope below.
Live Kad AICH seeding evidence uses a process-local FIFO cache capped at 512
result entries and a conservative 4 MiB accounting budget. Accounting includes
both key copies, vote/node overhead and 64 KiB reserved for bounded FIFO capacity
and collection heads. Empty evidence is not retained. Replacement and explicit
session removal release charges; eviction discards the oldest cached entries.
Download selection still examines at most four retained sessions and 64 distinct
actual responders for one hash. Cache eviction affects optional live seeding;
retained search knowledge and download integrity verification remain authoritative.
There is no saved cache setting. Combined memory qualification must measure this
cache alongside active downloads and the other resident state.
The bounded-cache cut passes **664 Core tests** without compilation warnings,
including 100,000 insertions, maximum vote payloads, FIFO eviction, replacement,
removal/clear accounting, responder deduplication and corroborated-AICH download
seeding (`reports/settings-request-round-1/search-aich-cache-core.log`). The
daemon/WebUI build passed with zero warnings on Rust `8d0bafdc`
(`logs/builds/20261118T152320Z-build-clients/build-result.json`); native
qualification passed 86 routes with graceful teardown
(`reports/rust-rest-openapi-ci/20261118T152617Z/report.json`). Accounting limits
alone do not establish full-daemon resident-memory qualification.

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

The accepted 2b/2c download cut uses `POST /downloads` with `source` equal to
`{type: "ed2k-link", link}` or `{type: "content", hash, name, sizeBytes?}`.
Content size is optional nullable u64; reuse the server-side eD2K parser,
including AICH/source hints. Optional fields default to `category:null`,
`intent:started` and `redownload:false`. A new job returns 201; an active
duplicate returns 200 unchanged, while conflicting known sizes return 409.
Redownload never duplicates active work. Present or unavailable local content
requires explicit choice; confirmed absence can be downloaded normally.
Initial source hints and filename observations commit atomically with a new
job, including stopped jobs. Active duplicates do not merge that initial peer
state. After native admission the owner completes the transaction despite caller
disconnect; creation does not allocate or hydrate execution storage.

Download resources use positive decimal i64-string `id`, separate 32-hex `hash`,
canonical user-visible filename `name`, nullable `sizeBytes`/`progress`, desired
`intent` (`started`/`stopped`) and observed execution `state`: `queued`,
`waiting-metadata`, `downloading`, `stopping`, `stopped`, `verifying`, `delivering`,
`completed`, `removing`, `failed`. A draining owned operation need not falsely
report stopped. Use `createdAt`, `updatedAt` and nullable `completedAt` in Unix
seconds. `PATCH /downloads/{id}` edits name/category or unknown-to-known size.
Name changes require an unfinished job before an active fixed delivery attempt;
otherwise return 409. Category changes are metadata and never move files.
Equal known size is a no-op; a contradictory known size returns 409. Intent is
controlled through the action endpoints.

`GET /downloads` returns a thin `data` array with `meta.nextCursor` and
`meta.hasMore`, default limit 100 and maximum 200, in fixed newest numeric-ID
order. Use bounded opaque cursors and `view=unfinished` by default, with
`completed`/`all` and category filtering. Pages are compact and byte-bounded;
exact totals are later optional work. `GET /downloads/{id}` returns the selected
job, including actual `delivery.path` and ownership. Sources and comments use
separate paginated `/downloads/{id}/sources` and `/downloads/{id}/comments`
resources. No top-level list/detail hydrates all source history, and no list
path may materialize the whole collection. A source exposes at most 16 recent
filename observations, newest first, with `reportedFileNamesHasMore` whenever
older or oversized observations are omitted. The page byte budget also applies
to this nested window; do not silently rewrite observed names.
Part details are independently paginated. Their `start`/`end` are zero-based
inclusive byte offsets and `sizeBytes = end - start + 1`. `DownloadPart.complete`
means successful part verification, independently of byte presence or zero gaps.
`presentBytes` reports checkpointed internal byte presence. Derive only the
requested geometry window for known-size queued jobs; unknown geometry and
retired internal piece data return an empty part collection. Do not hydrate an
execution or probe the completed output merely to browse parts.

Use one bounded action endpoint per download operation:

```text
POST /downloads/start
POST /downloads/stop
POST /downloads/verify
POST /downloads/remove
```

Action bodies contain 1-100 distinct IDs, including one-element lists for single
jobs; remove also requires `deleteData`. Every accepted batch returns HTTP 207
with a `data` array in request order: `{id, status, httpStatus, error?}`. Item
`status` is `accepted`, `unchanged` or `failed`, with a concrete HTTP outcome
such as 200/202/404/409/503. Failed items require the standard
`error:{code,message,details}`; accepted/unchanged items omit it. Malformed
whole requests return 400; shared-capacity refusal before admission returns 503
without modifying jobs. Once admitted, the existing owner completes every item
despite caller disconnect. Per-job failures do not roll back unrelated successes
or lose later items in a request-owned loop. Native bulk operations initially
accept bounded explicit selections; no all-matching asynchronous framework.

Verification preserves start/stop intent and initiates no network downloading.
Check retained partial data for unfinished jobs and the recorded output file
for completed jobs. A stopped job remains stopped; a started unfinished job
returns to normal scheduling after verification, subject to its existing failure
and admission conditions. Verification does not clear an unfinished job's
storage-failure requirement for explicit start. Missing/damaged completed output
is reported separately from historical completion and never reopens the job;
re-download remains explicit. Do not search other library copies for replacement
data or introduce automatic relocation/repair behavior.

Use live indexed keyset cursors, stable tie-breakers and optional exact totals.
Document weak traversal consistency under concurrent changes; do not retain
per-client collection snapshots. Never clone/filter/sort a full durable
collection before slicing a response. Runtime queues need bounded query/index
structures too. Separate thin list summaries from expensive details/evidence.

Upload-list browsing order awaits an operator decision: fixed entry-admission
order with live scheduler rank in detail is recommended for simple indexed
paging; the alternative retains global live-rank ordering in list pages.
Neither option changes upload scheduling, ranking or credit rules. Do not cut
the list contract until that decision is settled.

The WebUI is an operations console using bounded pages, not continuous scrolling
or unbounded accumulated row caches. Use server-side search/filter/sort, default
download view unfinished with explicit Completed/All. Fetch for the active view.
Keep lightweight native SSE change/reset notifications, coalesce refreshes and
use polling as fallback rather than redundant broad snapshot polling. Snapshot
is a bounded dashboard summary; its underlying work must also be bounded.
Its download portion is `downloads:{unfinished,completed}`, counting unremoved
jobs by historical completion without embedding job rows. Existing-stream
`download.changed`/`download.removed` events carry `downloadId`, not full rows
or hash identity. `sync.reset` sends clients back to bounded current pages.

Native SSE IDs are opaque `epoch:revision` tokens. Event bodies carry that
epoch, numeric revision `id`, and `downloadId` for change/removal notifications.
Subscribe and capture the reset baseline under the same publication lock.
Initial connections and reconnects reset to that baseline; replay is not promised.
On lag, replace the receiver before sending reset so buffered older events cannot
follow it. Retain at most 1,024 scalar identity notifications, never job rows.
Revision exhaustion changes epoch and emits reset before numbering restarts.
Reset reasons are `initial`, `reconnect`, `lagged`, and `epoch-changed`; only lag
includes a `missed` count. Publish explicit mutations within their admitted owners,
including after caller cancellation. Clients coalesce invalidations into bounded
page refreshes rather than constructing a full collection from event payloads.

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
are not silently repopulated. For initialized-empty Kad contacts, suppress hidden
built-in/public fallback seeds; explicit operator-configured bootstrap endpoints
remain usable as distinct operator input.

Begin shutdown, seal reload/regular admission and stop/join the monitor, then
call the final Kad checkpoint directly before bounded network cleanup can
discard its DHT runtime. Outside that cleanup timeout, drain the persistence
owner, join the reload worker without abort, seal/drain local finalizers, then
drain root SQL and eligibility reads before connection/profile-lease release.
Attempt every stage even after a failure; the [#155 lifecycle contract](../active/items/RUST-REF-016.md#planned-category-publication-continuation-phase-2a)
owns retained tokens, cooperative stop, error reporting and the limits of the
scoped checkpoint evidence; this does not imply full phase-2a qualification.

### Docker and deployment

Use separate `/config/emulebb-rust` profile, `/data/incoming` delivered files and
`/data/temp` partial storage. The operator requires **automatic completion of
interrupted first-run setup**. Provision only a genuinely fresh profile; never
replay setup into an existing final profile or overwrite subsequent user edits.
This is an accepted allocation target, not current package/runtime proof.

The planned package-private initializer uses these boundaries:

1. Acquire a parent installation lock. Persist and sync an ownership journal
   identifying the intended private stage and final destination before creating
   that stage. Unknown ownership must not authorize cleanup or replay.
2. Create private fresh staging on the same filesystem as the final profile.
   Run the canonical offline per-key settings service under one profile lease;
   do not spawn competing writers, bypass validation or add package-specific SQL.
   Under that lease the private helper inspects typed default/custom markers and
   applies a packaged path only to a default-marked leaf through the same setter.
   Preserve every custom leaf, including operator edits inside private staging.
   Resume can skip already committed steps without comparing previous values,
   guessing defaults or changing public CLI get's resolved-value-only output.
   Interrupted setup automatically resumes from its durable owned state. Resolve
   persisted profile-relative data against the final profile namespace, never
   serialize staging absolute paths into product settings or root metadata.
3. Close owned database handles and sync completed stage data before publication.
   Publish using a strict same-filesystem **atomic no-replace** operation, then
   sync the parent directory. If another final profile wins a race, treat it as
   existing user state; never replace or replay settings into it.
4. Resume interrupted owned work automatically at the next launch. If the strict
   atomic operation is unsupported or durability cannot be established, fail
   visibly and retain the owned stage/journal for retry. Never substitute a
   check-then-move, copy or overwrite fallback. Once final publication exists,
   subsequent launches preserve it even if interruption left a journal behind.

Reuse the pinned `rustix::fs::renameat_with` / `RenameFlags::NOREPLACE` primitive
already used in `emulebb-ed2k`'s `ed2k_transfer/fs_durability.rs`. GNU/BusyBox
`mv` behavior with unsafe fallback is not qualification of strict publication.
The package-private helper adds no public daemon commands, flags or environment
settings bridge. The daemon itself runs with only `--profile`.

Configure P2P interfaces through saved settings. The daemon atomically publishes
the typed ephemeral `.emulebb-rest-listener.json` receipt after binding its
control listener. It contains the actual bound address, probe host/port and an
ephemeral instance ID; it contains no credential. Wildcard listeners use the
corresponding loopback probe. This is runtime output, not another configuration
authority or a hand-written TOML parser. The Docker health helper reads it with
the standard JSON parser and requires HTTP 204 plus a matching
`X-Emulebb-Instance` response header. Normal shutdown removes the receipt;
missing, malformed and stale receipts fail health checks. Both image variants
include `jq` for this package-private reader. Update
launchers, Compose/VPN examples, both container variants, package smoke tests and
harness callers. Preserve legitimate harness route/interface scenario inputs
and apply them through canonical profile setup.

Reuse the existing package/container Python tests for failure cuts before
ownership/stage creation, between per-key commits, before/after atomic rename
and at parent-directory sync. Include automatic resume, final-profile user edits,
concurrent publication, unsupported no-replace behavior and proof that no staging
absolute path leaks into published state. Both Ubuntu and Alpine variants need
actual proof; none is claimed by this design.

The listener/health slice is qualified on Rust `3fb53b64` and Harness
`b23dcdbb`. `[rest].bind_addr` in the profile bootstrap TOML is the listener's
configuration authority. The Docker service uses that configuration, including
the canonical fresh-profile wildcard default, and bind-error guidance points to
the same TOML key. Python launchers already prepare this file and launch with
profile selection. Current LAN-input rules remain covered without preserving
retired-name lists or checks. This is the listener cut, not completion of the
remaining runtime-input/settings/provisioning work.

Scoped checks passed **127 daemon** and **147 selected Python tests**. Daemon
evidence is `reports/settings-request-round-1/toml-rest-listener-daemon.log`.
The regular daemon/WebUI build passed with zero warnings:
`logs/builds/20261118T183015Z-build-clients/build-result.json`.
The native campaign passed on exact Rust
`3fb53b6467f21fa24812fb3e431411f3f518bc49` with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T183316Z/report.json`.
Its `listenerReceiptPhase` proves the configured nondefault port, matching live
instance and removal on shutdown; its settings CLI and 100k retained-job phases
also pass, with 87 native routes exercised and zero failures. The
existing Docker image smoke now exercises missing/malformed/stale receipts with
the real packaged helper when run. Python mocks prove that smoke rejects false
positives and cleans up; they do not prove actual image execution. Actual
Ubuntu/Alpine images, interrupted provisioning and the remaining deployment cut
are still unqualified.

## Ordered implementation and acceptance

| Phase | Required outcome |
| --- | --- |
| 1. Contract baseline | Reconcile policy and this specification, typed settings catalog, exact route/schema inventories, error/lifecycle contracts and query/index designs. Refresh source ownership, fixtures and baseline measurements. |
| 2. Persistence/domain services | Complete the shared-owner/Kad prerequisites, then the vertical cuts 2a-2d below. Keep remaining statistics/search-claim work with its existing owners and replace unbounded startup/list/recovery paths. |
| 2a. Categories | Immutable public name IDs, internal allocated SQL keys, nullable temp/destination paths and nullable name-based job assignment; deletion clears matching assignments. Cut affected REST/OpenAPI/UI/fixture consumers together. |
| 2b. Durable job identity | Never-reused job IDs, distinct protocol hash, nullable known size, one nonterminal job per hash and retained terminal/history records. Make every child, delivery/recovery reference and cleanup authority refer to its actual job. Separate verified delivery from destructive ownership and publish retirement/journal state coherently. Couple with 2c wherever separate commits would permit unsafe multiple attempts. |
| 2c. Job storage and execution | Establish a job-specific piece/storage namespace, first-start fixed temp placement and fixed delivery-attempt destination before enabling multiple historical/re-download attempts. A hash-based old-attempt cleanup must never reach a new job's data. Preserve freshly verified matching delivery across fingerprint drift without duplicates and provide safe retryable cleanup when atomic directory rename is unsupported. Include scheduling/restart/recovery and directly affected consumers. |
| 2d. Library policy and indexed reads | Durable hash sharing/upload policy, immutable tags, locations and verification caches plus incremental indexed library queries. Cover all accepted filters/sorts, stable keyset traversal and 100k behavior with the relevant live statistics owner. A full projection rebuild or output-only limit is not bounded-read evidence. |
| 3. Settings/CLI/provisioning | Default/custom resolution, revisions and application status, offline get/set/reset, fresh-only Docker setup and canonical harness profile preparation. |
| 4. REST/OpenAPI/WebUI | Routes, DTOs, validators, OpenAPI and consumers together; bounded action/query paths, substring/statistic sorting, shared change tracking and paginated active-view UI. |
| 5. Integrated checkpoint | Package/harness repair, failure/recovery and combined-scale qualification, independent review/repairs, clean granular commits and pushes. Stop for operator review, no PR. |

These are ordered vertical allocations, not claims of completed implementation.
Keep 2b/2c in one coordinated cut where necessary: never expose a temporary
hash-based re-download path before job-specific storage and cleanup are safe.
Statistics accounting, independent search claims and canonical settings remain
their existing owned later pieces, not implicitly complete after 2d. Preserve
current settings ownership until the direct canonical 59-field cut; do not add
transitional old/new field maps or parallel setting authorities.

Every vertical slice includes its directly affected REST/OpenAPI/UI/fixture
consumers and focused checks. Avoid temporary compatibility adapters. The parent
resolves routine technical choices; material product/scope changes return to the
operator.

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

This round has no response-time acceptance threshold. Record timings as
diagnostics; prioritize functional correctness, recovery, stability and bounded
resources while retaining the required checks below.

- Default/custom startup resolution with changed running defaults, equal-value
  and reset behavior, revision conflicts, atomic candidate failure, committed
  but failed application, restart-pending reporting and offline lease races.
- Creation/re-download races, nullable metadata, immutable IDs, no historical
  resurrection, start/stop intent, bounded active work and retained history.
- Adaptive admission and fixed burst semantics, rare-part capture, endgame
  duplication/cancellation, shortest-remaining ordinary admission, useful-source
  discovery without per-waiting-job workers, safe yielding, pressure recovery,
  preflight disk waiting versus execution failure, and scan/download contention.
  Prove the closed lifecycle/reason contract and bounded resource summary.
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
- Qualify two capacity tiers: **50,000 library contents plus 100,000 retained
  download jobs at 512 MiB**, and **100,000 library contents plus 100,000 retained
  download jobs at 1 GiB**. Both use mixed completed/queued/stopped jobs and
  bounded active work. These are measured qualification targets, not enforced
  file-count limits or guarantees before the full campaigns pass. Measure startup,
  first/late pages, substring search, every statistic sort, mutations, shutdown,
  memory and CPU. Inspect query plans and transient allocations, not only output
  sizes. Each tier uses its enforced **total container memory limit, no swap
  and 1 CPU**, with 100,000 retained jobs and a realistic
  incomplete queue spanning the accepted 10-to-1,000 workload. Measure the whole
  daemon, including startup and background activity, not just resident manifests.
  Concurrency adapts; this target does not promise sixteen simultaneous payload
  executions. Preserve long-path and Unicode coverage in both library sizes.
  Qualify additional capacity separately. Physical reference
  devices remain distinct pending evidence; no idle-only or component-budget
  result proves the constrained-container gate.

Inspect correctness, contracts, failure recovery, interactions, maintainability
and resource use, together where practical. Further review addresses concrete
risks or material findings rather than a fixed round count. Repair material
findings and refresh affected checks. Run applicable gates available without a PR; retain PR-only/physical
device evidence as explicitly pending.

### Retained-download scale checkpoint (2026-11-18)

The existing native REST/OpenAPI campaign now includes a metadata-only fixture
with **100,000 retained jobs**: 99,000 completed records, 900 stopped jobs and
100 queued jobs. It uses the existing profile, daemon launch/shutdown, schema
and metadata helpers. Fixture construction streams one atomic transaction and
grants no output deletion authority; it creates no completed payload files.

Qualification exposed a status bug: a busy metadata connection caused the
dashboard to report the bounded live cohort as if it represented all retained
jobs. Rust `7d3b464c` removes that fallback and routes count reads through the
existing bounded metadata worker, retaining the response charge and propagating
failures through the native error contract. Network/lifecycle status remains
independent of SQLite, including VPN monitoring. Rust `11400e31` updates the
regular diagnostic summary to use the same authoritative count path.

Rust `5e662b40` uses fresh schema **102** and replaces the dashboard row scan
with the same singleton `download_job_counts` summary used for collection
counts. Its `unfinished`, `completed`, `started`, `delete_requested_unfinished`
and `delete_requested_completed` counters update atomically with job mutations.
`started` means started unfinished intent, excluding admitted destructive
deletion; it is not resident-job or payload-execution concurrency. Existing
dashboard membership rules and public response shapes remain unchanged.
Insert/update/delete triggers maintain the counters, including intent changes,
logical removal and pending deletion. No periodic rebuild, extra writer,
migration or compatibility path is added.

The counter cut passes **298 metadata, 668 core, 169 REST and 1,458 transfer
tests**, including the connection-contention regression. The existing mixed
100k SQL test now verifies both count queries use a primary-key seek with no
full scan or sort and fewer than 80 VM steps. Lifecycle tests check counter
results against an independent row-scan oracle and cover transaction rollback.
Python fixture/campaign checks pass **64 tests** (34 metadata and 30 campaign
tests). These cover atomic fixture
rollback, valid short pages, restart, and rejection of incomplete/duplicate
pages with the intended failure reason. The first native attempts exposed two
harness assumptions about the public status shape and the difference between
active and unfinished jobs; the corrected harness is `1396e0f4`.

The final daemon/WebUI build has zero warnings:
`logs/builds/20261118T180054Z-build-clients/build-result.json`.
The native campaign passes on Rust `5e662b40`, with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T180347Z/report.json`.
Its `retainedDownloadScalePhase` proves complete newest-ID traversal of all
100,000 jobs (500 pages), 99,000 completed jobs (495 pages) and 1,000 unfinished
jobs (5 pages), with matching content hashes, scoped view membership and
preserved counts after clean restart. Dashboard counts are 100 active downloads
and 100,000 retained downloads. Unit logs include
`reports/settings-request-round-1/fixed-dashboard-counts-{metadata,core,rest,ed2k}.log`.

This is retained-job correctness evidence. Physical-library contents are not
seeded by this fixture. The combined checkpoint below supplies separate
physical-library and resource evidence; this fixture alone cannot qualify the
enforced 512 MiB/one-CPU container or physical-device gates.
The fixed-work counter lookup is qualified; no response-time guarantee is set.
Canonical runtime settings and the other foundation cuts retain their scope.

### Combined physical-library and retained-job baseline (2026-11-18)

Harness `6b9cb34d` extends the existing shared-library I/O campaign with the same
100,000-job fixture, full download-page traversal and process measurements across
four planned daemon lifetimes. Snapshot checks use the current metadata schema
rather than an invented partial test schema. Harness `df0364a1` reads public job
counts from the existing snapshot resource. Its affected suite passes 50 tests;
the preceding combined harness changes pass 113 selected tests.

Builder `f6f8c48` locks the required process-sampling dependency and the existing
browser harness version in managed Python. Dependency-input fingerprints isolate
workstream environments from canonical Git-hook environments. The scoped runtime
suite passes 39 tests, with evidence under
`reports/builder-unit/5f3f39c4a4a0`. This tooling behavior is on the feature branch;
it is not yet integrated into the canonical startup policy.

The Windows combined-profile attempt on Rust `3fb53b64` **failed qualification**.
Its evidence is
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T191708Z-8064.json`.
The existing physical fixture contains 100,000 files and 10,485,760,000 bytes.
The post-scan database has 100,000 active memberships and verified contents,
1,000 long-path sources, 200,000 known contents, no scan failures and no invalid
active hash-integrity rows. The 100,000 download jobs retain the expected mix.
All download views traverse completely: 500 all-job pages, 495 completed-job
pages and five unfinished-job pages, with matching hashes and view membership.

Two findings prevent acceptance. A pending follow-up reload reuses all files and
replaces the first scan's progress counters before the harness evaluates them;
initial scan accounting needs evidence tied to the correct reload. During the
watcher-create check, `GET /shared-files?limit=1` exceeds its procedural request
timeout. Emergency shutdown then requires the forced fallback. Preserve the
failure evidence and investigate the blocked read and teardown; increasing a
timeout alone does not establish correct bounded work or safe shutdown.

The observed lifetime peak working set is 362,397,696 bytes (about 345.6 MiB),
sampled peak private memory is 410,181,632 bytes (about 391.2 MiB), and cumulative
process CPU is 541.656 seconds over the failed 945.913-second campaign. These
are partial Windows measurements, not enforced container memory or CPU limits.
That attempt did not qualify watcher lifecycle, clean restarts or the full
combined campaign. The enforced 512 MiB/one-CPU container and physical-device gates
also remain open. The next bounded slice is the watcher/read/teardown failure
and correct reload accounting, reusing this campaign and fixture.

Rust `88111e7e` removes the library-wide joins from unfiltered collection totals:
the refreshed physical catalog is already the eligible-content set. Filtered
counts retain their predicates. The existing 100k regression checks the actual
count statement uses fewer than 20 SQLite VM steps, with no full row scan or
sort; all 298 metadata tests pass. No public response or schema changes.
The daemon/WebUI build passes with zero warnings
(`logs/builds/20261118T194203Z-build-clients/build-result.json`), and native
REST/OpenAPI conformance passes with graceful teardown
(`reports/rust-rest-openapi-ci/20261118T194502Z/report.json`).

Harness `e67076cf` retains a completed reload observation separately from final
worker quiescence; 51 focused tests pass. The second combined campaign still
**fails qualification**:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T194817Z-14056.json`.
Its full download traversal passes again, but the same watcher-time library
request times out and shutdown requires forced cleanup. The count optimization
does not resolve that failure. Initial progress accounting also remains
unproven: polling can miss the completed reload before a subsequent run resets
its counters. Preserving an observation when available is insufficient for
reliable completion evidence. Keep the strict failed verdicts.

The existing campaign now supports `run --watcher-replay-from RUN_ID` through
the same Builder lock and source-admission checks (Builder `d851f07`, Harness
`6950cbec` and `0f77f21e`). Replay validates the owned source receipt, physical
fixture, current metadata schema, foreign keys and download counts, and copies
the database with SQLite backup without changing the original. It reuses the
configured roots and explicitly excludes initial-payload-hashing qualification.
The helper suite passes 57 tests; the Builder routing/lock suites pass 115 tests
(`reports/builder-unit/515cd462ab6e`). No additional runner or product recovery
path is introduced.

Replay also exposed a populated-root replacement timeout before watcher work:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T201041Z-20328.json`.
Derived publication was interrupted by shutdown, which exited with a reported
persistence failure. That root-update finding remains open; focused watcher
replay requests a reload without unnecessarily replacing existing roots.

Rust `55857bc4` fixes an independently demonstrated catalog invalidation defect.
Single-path and full-root admission preserve identical verification rows rather
than replacing them, so unchanged scans do not invalidate the entire physical
projection. An explicit trigger conflict clause preserves deduplication when
changed evidence is already pending. The extended 100k regression fails before
the repair by detecting an unwanted projection rebuild, then passes afterward;
all 298 metadata tests pass. Retained proof:
`reports/settings-request-round-1/root-admission-red.log` and
`reports/settings-request-round-1/root-admission-metadata.log`.
The build has zero warnings
(`logs/builds/20261118T202735Z-build-clients/build-result.json`), and native
REST/OpenAPI conformance passes with graceful teardown
(`reports/rust-rest-openapi-ci/20261118T203919Z/report.json`).

Transaction-stage diagnostics identified the additional connection contention:
a 101,000-path root transaction held the connection for about 17 seconds; the
library read resumed and refreshed/counting completed in milliseconds after
acquisition. Rust `f67545b2` reuses prepared statements in the root batch and
shared delivery-exclusion checks, preserving every identity/fingerprint check.
Measured root batches fell to approximately six seconds without changing the
request timeout. Its watcher replay passed all four mutations and retained-job
checks, but still needed forced cleanup while a catalog rebuild was running:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T210906Z-16844.json`.

Rust `fff62fce` makes background offer-catalog rebuilding observe shutdown
between bounded pages, join its blocking worker and discard an incomplete
candidate without publishing it. Durable membership transactions still finish;
foreground reload publication remains required. The regression verifies that
cancellation leaves the active catalog generation unchanged and a subsequent
foreground rebuild succeeds. Validation passes **298 metadata, 668 core,
1,458 transfer and 58 harness tests**. Relevant logs are
`reports/settings-request-round-1/root-batch-metadata.log`,
`reports/settings-request-round-1/catalog-cancellation-core.log` and
`reports/settings-request-round-1/catalog-cancellation-ed2k.log`.

The focused watcher replay now **passes** on Rust `fff62fce` and Harness
`8287894c`:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T213354Z-17328.json`.
It proves create/modify/rename/delete convergence, preserved 100,000-job rows and
public counts, zero REST/watcher errors and REST shutdown with exit code zero.
Replay is explicitly bounded to this lifecycle and cleanup; it excludes initial
payload hashing, the full restart/mutation campaign and enforced container
limits. The measured lifetime peak working set is 408,838,144 bytes (about
390 MiB), not a total-memory container qualification. Build evidence has zero
warnings (`logs/builds/20261118T213022Z-build-clients/build-result.json`);
native REST/OpenAPI conformance passes with graceful teardown
(`reports/rust-rest-openapi-ci/20261118T214356Z/report.json`).

### Full combined Windows campaign (2026-11-18)

The existing full I/O campaign **passes** on Rust `0833fb58` and Harness
`3c3af739`, using a fresh profile with 100,000 physical library files and
100,000 retained download jobs:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T215835Z-19680.json`.
All three scan phases, all four watcher actions and all global checks pass.
The download fixture remains 99,000 completed jobs, 900 stopped jobs and
100 started jobs throughout four daemon lifetimes. All/completed/unfinished
traversal verifies 100,000/99,000/1,000 rows across 500/495/5 bounded pages.
Both complete-library restart checks reach 100,000 validated shares. All four
shutdown receipts record REST shutdown and exit code zero; there are zero REST
or watcher errors.

Rust now emits path-free numeric completion facts atomically with the completed
reload state. The harness streams the first matching event after each phase's
log offset and separately waits for worker quiescence. This removes reliance on
polling a transient completed state. Stale and partially written records are
excluded; invalid counters fail verification. The retained events prove:

| Phase | Hashed | Reused | Payload bytes read |
| --- | ---: | ---: | ---: |
| Initial | 100,000 | 0 | 10,485,760,000 |
| Unchanged reload | 0 | 100,000 | 0 |
| One-percent mutation | 1,000 | 99,000 | 104,857,600 |

The daemon/WebUI build has zero warnings
(`logs/builds/20261118T215441Z-build-clients/build-result.json`).
Harness `ffa668b2` additionally makes all four graceful-zero-exit receipts an
explicit full-campaign acceptance gate; the existing passing run's four receipts
satisfy it. Its focused suite passes 68 tests, including rejection of forced,
missing, nonzero and malformed exit receipts. That gate change does not alter
the daemon or scenario inputs; the recorded campaign source identity remains
`3c3af739`.

Measured peak lifetime working set is 408,326,144 bytes (about 389.4 MiB);
sampled peak private memory is 420,933,632 bytes (about 401.4 MiB). The campaign
takes 1,671.882 seconds. These are Windows measurements with metadata-only
download history, not enforced container memory/CPU limits or simultaneous
payload-transfer qualification. No latency SLO or relaxed timeout was used.
The enforced 512 MiB/one-CPU container, remaining library query/sort
qualification and the unfinished public-foundation cuts
retain their scope. A sustained soak remains deferred below.

The supported `linux-containers --workstream public-foundation-round-1
--wsl-distro Ubuntu` preflight passes on 2026-11-19. WSL Docker reports AMD64
and ARM64 support and successfully executes the ARM64 probe. Evidence:
`reports/linux-containers/preflight.json` and
`reports/settings-request-round-1/container-preflight.log`.
This architecture-only preflight establishes the available container lane;
it does not qualify the scale workload.

The opt-in `linux-containers --resource-budget` preflight now verifies those
limits with the campaign's actual kernel observer. Harness `8b7b8316` checks
that the unified cgroup contains the controller, samples limits/OOM counters
before and after the campaign, and fails a measured run if its scope, limits or
OOM counters change. Missing
namespace evidence leaves the run unqualified for the container budget. The
observed budget covers the campaign controller and its ordinary process tree;
it does not place the controller outside the measured envelope.

Builder `f449487` reuses frozen Harness snapshots and owned-container cleanup
for the real probe. Its result passes with memory limit **536,870,912 bytes**,
swap disabled, CPU quota/period **100,000/100,000 microseconds**, unchanged scope
and limits, no OOM events, and confirmed container removal:
`reports/linux-containers/budget/9f51d39d17504c4ab05c468013ddfd9c/report.json`.
All 88 focused harness tests and scoped Builder tests pass; evidence is retained
in `reports/settings-request-round-1/cgroup-budget-harness.log`,
`reports/builder-unit/2ad0bd27ceb7` and
`reports/settings-request-round-1/cgroup-budget-native.log`.
The probe explicitly records `workloadQualified:false`. Running the full
physical-library/retained-job campaign inside this budget remains open.

The GNU/AMD64 package prerequisite now passes on Rust `928ffe12`, Builder
`0969bec` and Harness `3cbacb58`. The strict Clippy and packet-diagnostics
compile gates pass; the release binary builds; all **3,308 workspace tests**
and **three VPN egress tests** pass. The single ignored workspace entry is an
isolated subprocess fixture invoked by its ownership regression tests. Evidence:
`reports/rust-linux/gnu-amd64/e533c662023b4d8e848391ceff1c5b18/`.
Windows scoped evidence also passes: 668 Core, 1,458 eD2k and 298 metadata tests,
retained in `reports/settings-request-round-1/linux-quality-core-final.log`,
`owner-receipts-ed2k.log` and `linux-native-profile-metadata.log`. The latter two
filenames share that reports directory. Scoped Builder checks pass in
`reports/builder-unit/2e90ef167383`.

The source-verified GNU archive and DEB are local validation artifacts under
`packages/rust-linux/0.1.0-beta.2/gnu-amd64/`. The archive's non-root lifecycle
smoke passes with the current separate download-detail and bounded part
resources, including verified partial progress, same-profile restart, resumed
completion and retained history:
`reports/rust-linux/gnu-amd64/c0e1d1b651fc42e386fcb3b4db269615/package-smoke.json`.
All 76 scoped package-smoke Python tests pass in
`reports/settings-request-round-1/package-download-resources-python.log`.
These artifacts are neither published releases nor constrained-scale evidence.

The owner receipt helper now releases transient workspace and command guards
before exposing completion, while independently charged result backing remains
owned by its consumer. The same helper covers metadata reads, cleanup,
job lifecycle/progress, delivery, payload/availability evidence and path/content
mutations. Existing receipt-ordering and storage regressions remain required.
Local-ingest preparation follows that same guarantee on Rust `733e5d16`:
publication retains its preparation proof through the final projection, then
hashing admission and transient workspace release before completion. All 1,458
Windows eD2k tests pass, including ingest cancellation, held-preparation capacity
and publication coverage:
`reports/settings-request-round-1/ingest-receipt-ed2k-final.log`.
The native package evidence above still belongs specifically to `928ffe12`.
Fresh Linux package qualification passes on the ingest change; constrained
workload acceptance remains incomplete. Builder and Harness provide
the persisted wrapper around the existing combined campaign. It verifies the
current archive checksum/source/SBOM, snapshots exact independent Rust/Harness
Git sources, and uses a labelled local Docker volume for native profile and
fixture storage. The non-root container enforces the selected capacity tier's
memory limit, disabled swap, one CPU
and a private cgroup. Kernel measurement includes archive extraction, fixture
preparation and all campaign phases. Acceptance requires the full physical
library/history report, its measured budget, unchanged sources and confirmed
owned-container removal. Physical SSD speed and cold-cache behavior are not
claimed when Docker's backing topology is opaque.

The supported entrypoints, run from Builder with the existing workstream, are:

```text
python -m emule_workspace test rust-library-container --workstream public-foundation-round-1 --archive <current-gnu-amd64-archive> --library-files 50000
python -m emule_workspace test rust-library-container --workstream public-foundation-round-1 --archive <current-gnu-amd64-archive> --library-files 100000
python -m emule_workspace cleanup-rust-library-container --workstream public-foundation-round-1 --receipt <campaign-report.json>
```

Native profiles and fixture data remain on the recorded volume after success or
failure. Cleanup checks the managed receipt, actual volume labels, local driver
and absence of remote mount options or attached containers before removal, under
the normal workspace lock. Reports remain in the output tree. The runtime image
includes the existing campaign's Python validation/measurement and Linux disk
inventory dependencies. Scoped Builder checks pass in
`reports/builder-unit/a10e14ab2c79`; all 168 selected harness tests pass in
`reports/settings-request-round-1/container-library-harness.log`. These scoped
checks verify orchestration and failure handling, not the full workload itself.

The fresh GNU/AMD64 package gates and non-root smoke pass on Rust `733e5d16`:
`reports/rust-linux/gnu-amd64/3e887912411743e390e43a38ef4f4d5a/` and
`reports/rust-linux/gnu-amd64/6faf822a05d1474a8dff0e6e1be201a9/package-smoke.json`.
The first full constrained execution on Builder `9302058` and Harness `9a1f5686`
**fails qualification**. It prepares all 100,000 physical files, validates
10,485,760,000 bytes, starts the 100k retained-job profile and enumerates the
full library. During the initial scan the kernel kills the daemon at the
512 MiB process-tree limit. The observer records one OOM kill, unchanged scope
and limits, swap disabled and CPU quota/period 100,000/100,000. Receipt and failed
campaign evidence are retained under
`reports/linux-containers/library/ecb456c5b4bc4b98b437f4811f632558/`; its labelled
native volume retains the profile and fixture. This is not a passing scale result.

That run has no usable daemon RSS samples, so it does not establish whether
daemon allocations or controller memory dominate the failure. Harness `fc0dd988`
now preserves CPU/RSS readings when optional metrics are unavailable, records
metric errors, leaves unavailable private/I/O measurements null, and records
controller RSS before/after fixture preparation and alongside daemon samples.
All 94 selected campaign tests pass in
`reports/settings-request-round-1/container-memory-observability-python.log`.
These fixes do not retroactively add measurements to the failed run.

Harness `c939b02f` reduces the existing fixture validator's transient allocation
cost without changing its generated paths, sizes, Unicode/long-path coverage or
acceptance criteria. It verifies each complete native relative path against its
generated index, tracks expected-file presence in a compact byte array, retains
only unexpected paths, and aggregates geometry bounds incrementally. A 100k
metadata-only inventory regression measures 160,907,569 traced allocation bytes
before the change and enforces a limit below 16 MiB afterward. Malformed-index,
misplaced, missing, unexpected, wrong-size and duplicate-walk cases preserve
their exact rejection/count behavior. All 101 selected campaign tests pass:
`reports/settings-request-round-1/fixture-inventory-memory-baseline.log` and
`reports/settings-request-round-1/fixture-inventory-memory-final.log`.
This is a Python allocation measurement, not a daemon RSS measurement or a
passing full-scale result.

The repeat on the same Rust revision, Builder `9302058` and Harness `c939b02f`
also **fails qualification** under the unchanged 512 MiB/one-CPU process-tree
budget. Evidence is retained under
`reports/linux-containers/library/15768d47ab30409abdf8ac72b714f99e/`.
All 100,000 physical files and 10,485,760,000 bytes validate. The observer now
retains 442 samples: sampled daemon RSS peaks at 446,324,736 bytes and controller
RSS at 44,404,736 bytes. The kernel records one OOM kill and a 536,891,392-byte
cgroup peak; these sampled process peaks are not simultaneous totals or private
allocation measurements. Optional I/O readings are unavailable and remain null.
The owned container is removed; the labelled volume retains its profile and
fixture.

Live counters reach 99,800 exhaustive-scan hashes after the separately hashed
200-file startup cohort. This gap is intentional, not missing long-path files;
the completed reload merges both cohorts. No completion event precedes the
daemon's exit. Inspection narrows the remaining investigation to final root
membership persistence and complete-catalog refresh, without yet attributing
the OOM to either operation. Root persistence streams SQLite point updates from
the retained scan inventory; refresh builds a replacement catalog while the
current catalog remains available. Preserve transaction/publication fences and
the full acceptance criteria when reducing peak allocation. After two failed
full runs, investigate this path before another full campaign; do not raise the
budget or repeat the unchanged approach.

Rust `efa3c50d` removes a concrete scan/admission allocation overlap. Root scan
snapshots retain only the path and fingerprint needed for later admission,
without duplicate planning keys or disk identifiers. Membership input is
consumed row by row inside the existing SQLite transaction instead of building
another full-library vector. Both reload paths consume reused-file planning
records before finalization. Publication fences and transaction semantics are
unchanged; no public schema changes. Structured log markers distinguish root
commit from complete-catalog rebuilding in subsequent diagnostic evidence.

Scoped validation passes 298 metadata tests, 668 core tests and 127 daemon tests
(plus the intentionally ignored ownership subprocess fixture exercised by its
parent tests). A late invalid member rolls back earlier streamed admission and
session verification. Scan coverage checks that compact root records preserve
the original path and fingerprint. Core/daemon evidence is in
`reports/settings-request-round-1/root-admission-core.log` and
`reports/settings-request-round-1/root-admission-daemon.log`; branch quality
checks pass in `reports/local-check/emulebb-rust/20261119T044347Z-a6814be6/`.
This proves the scoped correctness checks, not resolution of the constrained
OOM.

Fresh Linux GNU/AMD64 qualification passes on Rust `efa3c50d`: strict Clippy,
packet-diagnostics compilation, release build, **3,308 workspace tests** and
**three VPN egress tests**. Logs are retained under
`reports/rust-linux/gnu-amd64/abef0e7e10cf439fa4bd7d85b650d200/`.
The source-verified archive SHA-256 is
`b32aca50c61c54569745ed8fe131c484cecc78bb66450476020155c72b2497c9`.
Non-root partial-download/restart/resume/completion smoke passes in
`reports/rust-linux/gnu-amd64/2b42c7609ae64983bec70fee23dfbab0/package-smoke.json`.
These are local qualification artifacts, not published releases.

Harness `5cb091ca` extends the existing log summary with fixed finalization
event counters and the last event reached. It reads logs line by line and
retains no log text or private paths in that summary. All 102 scoped campaign
tests pass in `reports/settings-request-round-1/root-finalization-harness.log`
and the required push checks. An unchanged-budget full campaign on this archive
remains required before claiming the constrained OOM is resolved.

That campaign, on Rust `efa3c50d`, Harness `5cb091ca`, Builder `9302058` and
Tooling `9d25c202`, **fails qualification**. Evidence is retained under
`reports/linux-containers/library/b4656cfbe2a746c2bb32059d177ebada/`.
The budget and full workload remain unchanged. The kernel records one OOM kill
and a 536,883,200-byte cgroup peak; the daemon exits with code -9. All 100,000
physical files validate. The owned container is removed and the labelled native
volume retains its profile and fixture.

The new markers narrow the failure: root commit finishes, complete-catalog
rebuilding starts, and a full reload completion event is emitted before the
kill. Its numeric counters report 100,000 successful hashes, 10,485,760,000
payload bytes read and zero hashing failures. The harness has not observed a
settled initial phase before the process exits, so this is not a passing initial
phase or full campaign. The completed reload distinguishes this result from the
earlier finalization hypothesis; investigate the brief interval following
publication rather than assume root persistence or catalog rebuilding failed.

Across 441 retained samples, daemon RSS peaks at 397,762,560 bytes and controller
RSS at 44,085,248 bytes. The daemon's sampled peak is lower than the preceding
run, but sampling can miss a short allocation peak and does not establish the
OOM's allocating operation. No REST or watcher errors precede exit. Keep the
same budget and acceptance criteria; do not repeat another full campaign
without narrower allocation evidence or a justified repair.

Rust `9d5cbe9d` repairs a verified duplicate-scan scheduling path. An explicit
root command already reserves and arms its reload before acknowledging commit.
Its health notification now requests only watch refresh; the health worker does
not also interpret that event as root recovery and queue another inventory.
Category changes without an owned scan still request one. Periodic offline-root
recovery retains its scan behavior. Coalescing watch notifications cannot erase
a pending scan request.

All **670 core tests** pass in
`reports/settings-request-round-1/root-scan-owner-core.log`. The regression holds
reload execution at a gate, lets the committed root command hand off its scan,
processes the health event and requires no second pending scan. It also verifies
that an unowned category scan remains schedulable. Existing unavailable-root
withdrawal/rejoin coverage passes. Branch quality checks pass in
`reports/local-check/emulebb-rust/20261119T053148Z-77a6c745/`. This confirms the
duplicate scheduling defect and repair; its causal contribution to the OOM is
not yet proven.

Fresh Linux GNU/AMD64 qualification passes on `9d5cbe9d`: strict Clippy,
packet-diagnostics compilation, release build, **3,310 workspace tests** and
**three VPN egress tests**, with logs under
`reports/rust-linux/gnu-amd64/dc5b5b895abc45e09ec57aadfc7768d8/`.
The clean-source archive SHA-256 is
`ede02a46c700319588c9f4d23289c7a199ed0e21440e91646eb751ee4c27dfd6`.
Non-root partial-download/restart/resume/completion smoke passes in
`reports/rust-linux/gnu-amd64/633503b8e61e4060a2d22fd1add8f273/package-smoke.json`.
Artifacts remain local and unpublished. Unchanged-budget full campaign
qualification remains required.

The unchanged-budget campaign on Rust `9d5cbe9d`, Harness `5cb091ca`, Builder
`9302058` and Tooling `3463be8f` **passes its initial physical-library phase**:
100,000 successful hashes, 10,485,760,000 bytes read, settled idle state, exact
active DB counts, zero integrity/scan failures and 1,000 long-path sources.
The same profile retains 100,000 jobs. All/completed/unfinished traversal passes
at 500/495/5 pages, and the populated-root update succeeds. Evidence is retained
under `reports/linux-containers/library/d29f96e722a64ad18d9ad73037c9e0cd/`.

The **full campaign still fails qualification**: an OOM kill occurs during a
later catalog rebuild in the watcher phase, resetting a shared-file probe.
Elapsed time is 1,011.89 seconds; the kernel records one OOM kill and a
537,075,712-byte cgroup peak with unchanged limits. The owned container is
removed; its labelled native volume retains the fixture/profile. Initial-phase
sampled daemon/controller peaks are 337,403,904/44,167,168 bytes. Whole-campaign
sampled peaks are 413,048,832/126,410,752 bytes; these are not simultaneous totals.
Download traversal's sampled controller peak remains 43,872,256 bytes. The later
controller increase therefore needs investigation in watcher polling rather
than an assumption that download traversal retains all job rows.

Harness `9522a32e` deterministically closes the campaign's read-only SQLite
connections, including exceptions. SQLite connection context managers alone
commit/roll back; they do not close connections. Active-source selection uses
an indexed membership `EXISTS` test instead of a wide deduplicating join,
preserving one row per path across overlapping roots. The existing 102 scoped
tests pass, including overlapping-root counts, absence of a temporary
deduplication tree in the query plan, and explicit close checks after successful
and failing reads. Evidence:
`reports/settings-request-round-1/watcher-reader-resources-python.log` and
`reports/local-check/emulebb-build-tests/20261119T061033Z-989a1ee7/`.
Rust and its qualified archive are unchanged. The impact of this reader-resource
repair on the later constrained peak remains unproven; reuse that archive for
the next unchanged-budget campaign rather than rebuilding product binaries.

The repeat on the same Rust archive and Harness `9522a32e` keeps sampled
controller RSS below 45,887,488 bytes. Initial physical-library acceptance and
all three retained-job traversals pass again, but the full campaign still
fails with an OOM kill during watcher creation. Sampled daemon RSS peaks at
408,104,960 bytes; the unchanged cgroup records one OOM kill and a
537,018,368-byte peak. Elapsed time is 906.681 seconds. Receipt, process samples
and phase evidence are retained under
`reports/linux-containers/library/8aae0f242d7b456d84fb313676accbe3/`; owned-container
removal is confirmed and its native volume is retained. The reader repair
reduces observed controller overhead; it does not qualify the daemon's later
populated-library work.

Rust `e73fc37d` removes the populated reload planner's full persisted
path/fingerprint map. Each scanned path reads its current persisted fingerprint
through the unique native-path index. Missing-source diagnostics retain only a
compact snapshot of numeric path IDs and binary hashes; their seen/kept sets
also use those compact identities. No duplicate set of full path strings or
second collection of persisted fingerprints is retained. Fingerprint reuse,
identity-alias fallback, changed files and missing-source counts remain covered
by the core/transfer suites. No persistent schema or public surface changes.

Scoped validation passes **298 metadata, 670 core and 1,458 transfer tests** in
`reports/settings-request-round-1/indexed-reload-{metadata,core,ed2k}.log`.
The existing 100k metadata fixture additionally proves a late-path seek with no
full scan in its query plan and a pruning snapshot backing allocation below
4 MiB. Branch quality checks pass in
`reports/local-check/emulebb-rust/20261119T064728Z-dfdc7a81/`.
Fresh Linux package and unchanged-budget full campaign evidence remain required
before claiming that the populated-library OOM is resolved.

Rust `169691c6` removes the reload target's unused hash-vector field and its
constructor plumbing. Fresh Linux GNU/AMD64 qualification passes on that revision:
strict Clippy, packet-diagnostics compilation, release build, **3,310 workspace
tests** and **three VPN egress tests**. Logs:
`reports/rust-linux/gnu-amd64/259c372a62264db39cda4625f73bcf8f/`.
The clean-source archive SHA-256 is
`03688335f6cd54dd42d582df35526e531bc75e6311e2e64508e10960a3f9a0ae`.
Non-root partial-download/restart/resume/completion smoke passes in
`reports/rust-linux/gnu-amd64/f7ace5145ac34e2f837d5815c29e2be5/package-smoke.json`.
These are local, unpublished artifacts. The full unchanged-budget campaign is
still required to qualify the populated-library repair.

The full campaign on Rust `169691c6`, Harness `9522a32e`, Builder `9302058` and
Tooling `726e8261` **still fails qualification**. Evidence is retained under
`reports/linux-containers/library/d4b19e6433b64f8789abb87d758390c0/`.
Initial physical-library acceptance passes. A second reload plans and reuses all
100,000 files without payload reads, commits memberships and completes catalog
rebuilding. An OOM kill later resets a watcher-phase shared-file probe before
watcher convergence is recorded. Elapsed time is 1,441.758 seconds; the unchanged
cgroup records one OOM kill and a 536,977,408-byte peak. Sampled daemon/controller
RSS peaks are 465,154,048/45,481,984 bytes, not simultaneous totals. Owned-container
removal is confirmed; the labelled native volume retains the fixture/profile.

A diagnostic extension of the existing 100k metadata test checks per-connection
SQLite page-cache growth through `SQLITE_DBSTATUS_CACHE_USED`; it passes a bound
below 8 MiB when constructing the library projection. The diagnostic patch and
298-test result are retained in
`reports/settings-request-round-1/projection-cache-probe.patch` and
`reports/settings-request-round-1/projection-cache-baseline.log`.
This was a diagnostic probe, not a retained product/source change. The checked
dependency build uses ordinary bundled SQLite; the memory-temp-store flag found
during investigation belongs to its SQLCipher-only branch. No production pragma
was changed. This rules out that default-mode assumption, not every transient
SQLite allocation or the watcher read path.

Allocation-stack investigation reuses the retained initial-phase
proof and existing copied-profile watcher replay. Keep profiler dependencies and
launch control in the persisted harness/Builder lane, preserve the failed source
profile, and retain source/archive identities and trace evidence. Any additional
memory required by profiling is diagnostic-only: it cannot satisfy either
capacity-tier workload gate or set `workloadQualified` true.

Harness `b802a96b` and Builder `ab68276` provide the bounded allocation replay:

```text
python -m emule_workspace test rust-library-heap-profile --workstream public-foundation-round-1 --archive <current-gnu-amd64-archive> --receipt <retained-campaign-report.json>
```

It requires the exact inactive source/archive and verifies its labelled local
volume. The existing replay copies the database into a new run; the failed
source database and logs are preserved. The synthetic fixture is reused under
the existing replay's probe cleanup/mutation rules. Heaptrack profiles only the
first daemon lifetime, through warm baseline and watcher creation. Resource
sampling observes the daemon child, not the profiler wrapper. Raw traces stay
on native storage and interpreted allocation stacks are retained with the
diagnostic reports. The validation image adds heaptrack only for this lane.

Profiling uses a separate **1 GiB**, no-swap, one-CPU process-tree allowance.
Reports always retain `workloadQualified:false` and failed workload acceptance;
diagnostic completion cannot satisfy either capacity-tier gate. No product
arguments, settings, schema or runtime binary change. Scoped harness checks pass
115 tests in `reports/settings-request-round-1/heap-replay-harness.log`.
Required combined push checks pass in
`reports/local-check/emulebb-build-tests/20261119T080541Z-ee0c9177/` and
`reports/local-check/emulebb-build/20261119T080727Z-a02496ae/`;
Builder source-snapshot checks also pass in `reports/builder-unit/277bd7e12169/`.
The live-wire byte-report fixture now supplies current search-result IDs and a
deterministic clock, preserving its completed/partial-byte assertions.

The first allocation replay is terminal in
`reports/linux-containers/library-heap/7e98565889934ebd9211e9b63d3852e0/`.
It fails on a request timeout before watcher creation, but retains a successfully
interpreted 23,118,438-byte trace (`daemon.zst.analysis.txt`). Heaptrack reports
245.63 MB peak live heap, 491.02 MB peak RSS including instrumentation overhead,
and 297,387,451 allocation calls over 577.55 seconds. The diagnostic cgroup
records no OOM events; both owned containers are absent. This is useful partial
allocation evidence, not completed watcher coverage or workload qualification.
It does not establish that remaining memory costs are unavoidable.

The operator approved the two capacity tiers above on 2026-11-19. Harness
`9c72fc6b` and Builder `03b8656` extend the existing fixture/campaign and admission
to carry an explicit matched library-size/memory pair. `--library-files 50000`
selects 512 MiB; `--library-files 100000` selects 1 GiB and is the default.
Both keep 100,000 retained jobs. Fixture preparation, baseline hashing, four
watcher phases, no-change and mutation reloads, restart/storage integrity and
the whole process-tree budget are measured by the same campaign. Both sizes
retain 1,000 long paths and all 16 Unicode cases. Mutation samples remain 1%
of the library, preserving the file-size distribution.

Reports name the target explicitly. Admission rejects an incorrect fixture or
job count, mismatched target/limits, incomplete phases, OOM evidence, changed
source or missing owned-container cleanup. Diagnostics without an explicit
workload target cannot claim enforced workload limits even at a matching cap.
Scoped Harness checks pass 126 tests plus 33 focused budget/preflight checks;
required Harness push checks also pass in
`reports/local-check/emulebb-build-tests/20261119T083225Z-e243ff02/`.
Builder CLI/container checks pass in `reports/builder-unit/562bc95bd462/` and
`reports/local-check/emulebb-build/20261119T083346Z-0620987d/`.
The Rust source/archive are unchanged. Full tier qualification remains pending.
Earlier failed 100k/512 MiB runs remain diagnostic evidence;
they do not reduce the 100k support requirement at the 1 GiB tier. Investigate
concrete allocation waste without making a major rewrite solely to force that
larger workload into 512 MiB.

Compiler investigation uses Builder's diagnostic-only Linux collection command;
its receipt explicitly records `qualityGatePassed:false` and
`packageProduced:false`. Acceptance continues to require the ordinary strict
gates. The canonical workspace test command now collects failures across crates
without changing the failing exit status, avoiding successive hidden failures.

### Populated-root update replay (2026-11-18)

The focused replay passes on Rust `9316bc39` and Harness `eb3c975e`:
`reports/workstreams/public-foundation-round-1/shared-library-io/rust-shared-library-io-20261118T224537Z-4724.json`.
It copies the preceding successful campaign's database into a new owned profile
and preserves the matching physical fixture generation. The warm baseline
reuses all 100,000 files without reading payload bytes. After bounded download
traversal, replacing the populated root set with the same canonical root
succeeds in 0.022 seconds. All four watcher actions converge, 100,000 retained
download rows and public counts remain correct, REST/watcher errors are zero,
and REST shutdown exits zero. Total replay duration is 564.116 seconds.

The earlier unchanged-root timeout is not reproduced on these revisions;
no additional root-update behavior change is justified by this evidence.
The harness now requires this unchanged-root update in both campaign modes.
This replay qualifies that operation and the watcher lifecycle, not removal or
replacement with a different populated root, initial hashing, a fresh full
campaign on these revisions, payload-download concurrency or enforced container
limits. Build evidence has zero warnings:
`logs/builds/20261118T224149Z-build-clients/build-result.json`.

### Upload detail read checkpoint (2026-11-19)

Rust `23ac0696` selects the requested active or waiting upload before hydrating
its serving view. The queue iterator retains only the selected snapshot rather
than allocating a snapshot vector for every session. List and detail use the
same snapshot builder and ordering; absent clients and wrong-queue lookups
return no entry. Management actions that read upload detail also use this path.
Selection still scans the in-memory queue and computes the selected waiter's
rank; this is bounded intermediate allocation, not constant-time lookup or
completed upload-list pagination.

Validation passes all 1,458 transfer and 668 core tests. Evidence:
`reports/settings-request-round-1/upload-detail-ed2k.log` and
`reports/settings-request-round-1/upload-detail-core.log`.
The daemon/WebUI build has zero warnings
(`logs/builds/20261118T230427Z-build-clients/build-result.json`). Native
REST/OpenAPI conformance passes with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T230723Z/report.json`.
No DB, settings, CLI or public response shape changes in this slice.

### Live upload UUID contract checkpoint (2026-11-19)

Rust `aec534d0` implements lifetime UUID identity for upload entries; `b0e9c61d`
updates missing-resource test fixtures. A UUID is allocated only when a queue
entry is created. Reasks, peer rekeys and waiting/granted/uploading transitions
retain the entry's UUID. Removal ends that lifetime, and readmission allocates
a fresh UUID. The queue stores the compact UUID value in memory, with no
database allocation or connection history. Detail and management actions select
that identity before hydrating a file view. Protocol peer identity and credits
remain separate.

Native upload responses expose `id`; `/uploads/{id}` and `/upload-queue/{id}`
use lowercase hyphenated UUIDs. The embedded WebUI, OpenAPI path/response schemas,
native conformance fixtures and affected Android/reask harness callers use the
same contract. Harness `caaf4520` binds concrete UUID fixture paths, including
round-trip template verification. The populated native friend-control proof
passes all six required active-upload, waiting-upload and download-source routes,
including durable/cache failure consistency and successful retries.

Validation passes 1,458 transfer, 668 core and 169 REST tests; 119 static OpenAPI,
132 Android, 72 other affected caller and four fixture-path Python tests;
60 WebUI unit and 32 browser tests; and strict documentation checks. Evidence
is retained under `reports/settings-request-round-1/upload-id-*.log`.
The daemon/WebUI build has zero warnings
(`logs/builds/20261118T233227Z-build-clients/build-result.json`). Native
conformance passes all 87 safe routes with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T233725Z/report.json`.

Upload-list indexing, thin list shape and bounded keyset traversal remain open;
UUID identity alone does not qualify those reads. No schema, settings or CLI
changes are introduced by this checkpoint.

### Tag WebUI checkpoint (2026-11-19)

Rust `659d9f56` delivers global tag management under Sharing and hash-level
assignment controls in file details. Global management uses `/library/tags`
for browsing, creation and confirmed deletion. Names remain immutable and use
the same case-insensitive identity and ASCII validation rules as categories.
File details read `/library/files/{hash}/tags` and send explicit one-hash
selections to the existing bulk add/remove endpoints. Removing an assignment
does not delete the global tag; tag creation remains an explicit global action.

Both controls reuse one bounded tag-page loader, cursor controls and public-name
validation. They retain one 100-row page per resource, replace rows during
traversal and support explicit refresh. Successful mutations refresh only the
tag resource and return to its first page. Failed writes retain the proposed
name and current page; HTTP 207 item failures surface without retrying accepted
work. A content change resets cursor/input scope, and late responses cannot
overwrite the newly selected content. There is no new polling loop or
accumulated row cache.

All 72 WebUI unit tests and 32 browser tests pass, including tag lifecycle,
pagination, hash-selection and partial-batch regressions:
`reports/settings-request-round-1/content-tags-webui-final.log`.
The staged daemon/WebUI build has zero warnings:
`logs/builds/20261119T000950Z-build-clients/build-result.json`.
Backend API, DB, settings and CLI are unchanged. Multi-file selection and
library filtering remain part of the library-browser cut; this checkpoint
qualifies global tag management and selected-content assignment controls.

### Deferred follow-up

A sustained mixed-workload soak is follow-up work, not a prerequisite for this
delivery checkpoint. No soak duration is set for this round. Reuse the existing
Python harness and monitoring when that follow-up is scheduled. Current scoped
tests do not establish year-long endurance; report the evidence at its actual
scope without delaying functional delivery for a long-running campaign.

Preserve evidence, branch heads and exact
companion revisions for iterative review. Report completed phases, pending work,
failed/unavailable gates and risks honestly. A launched process or pushed partial
implementation does not establish the required acceptance checks.

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
  Live upload and upload-queue entries use opaque UUID strings. Retain an ID
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

### Observation reporter checkpoint

Search and download filename observations use `reporterEndpoint` in JSON and
`reporter_endpoint` in Rust/SQL. This identifies the captured reporting endpoint;
advertised download-peer identity remains separate. Unknown reporting endpoints
are null. Kad results retain the queried contact's IPv4 UDP endpoint, including
results without AICH metadata. AICH corroboration retains reporter-IP/version
rules. The independent corpus decodes server AICH's wire Base32 representation
into the typed 20-byte root.

### Search session identity checkpoint

The positive `search_sessions.id` AUTOINCREMENT primary key is the public session
identity, rendered as an exact decimal string. SQL owns allocation; creation
accepts no caller-selected ID. Queue admission precedes allocation and
publication follows commit. Updates require an existing session. Deletion and
clear do not reset allocation; exhaustion fails without wrapping. OpenAPI paths,
summaries, details and result references share `SearchId`. The current native
campaign proves exact IDs above JavaScript's safe-integer range, retrieval and
non-reuse after deletion.

### Independent claim ingestion checkpoint

Fresh schema **91** stores permanent `content_claims` keyed by ED2K hash plus
nullable unsigned size, with never-reused positive identities. Unknown size,
known zero and conflicting known sizes remain distinct. Remote evidence creates
no accepted library identity. Independent `content_claim_observations` retain
typed metadata variants by origin and reporting endpoint, with first/last-seen
Unix seconds and a saturating positive occurrence count. SHA-256 fingerprints
use the canonical typed metadata representation; timestamps and counts are not
variant identity. Unknown reporters aggregate explicitly as null.

The shared profile persistence owner ingests raw decoded occurrences before
session filtering or presentation aggregation. Connected-server pages emit
before terminal completion, preserving already decoded evidence across later
interruption. Global UDP and Kad use the same ingress. Network handoff channels
are bounded at 16 items. SQL batches accept at most 128 events and 256 KiB of
conservative charge, with 64 KiB per event. Provenance keyset pages return at most
100 variants and 256 KiB. Admission capacity waits retry only an unadmitted Busy
outcome; uncertain commit faults ingress. Admitted work finishes after caller
disconnect. Final completion settles status/integrity votes without replaying
results. Terminal sessions reject new membership/progress while their late raw
observations can enrich the independent corpus.
Forwarding drains until the decoder closes its channel even when cancellation
settles the request first. Queued requests hold weak channel handles; executing
decoders upgrade them, so disconnected queued requests cannot strand a drain.

Rust `6baabe7e` implements storage; `0e944e0d` integrates ingestion and `2334e5f0`
closes the cancellation drain gap. Checks pass **261 metadata**, **643 core**,
**1,458 eD2K** and **174 existing Python harness**
tests. New coverage includes null/zero/conflicting/full unsigned sizes,
repetition/variant aggregation, rollback, reopen, byte-bounded keysets, caller
disconnect, 750 forwarded occurrences after request settlement through small bounded
channels, queued cancellation channel closure, raw AICH
conversion, session filters, frozen terminal membership and session deletion.
Evidence: `reports/settings-request-round-1/content-observations-*.log`.
The zero-warning daemon/WebUI build is recorded at
`logs/builds/20261118T063735Z-build-clients/build-result.json`.
The native REST campaign passes with graceful teardown on exact Rust
`2334e5f09e8ec86e640440212933f4df4d8bc85a`:
`reports/rust-rest-openapi-ci/20261118T064046Z/report.json`.

This does not complete the search cut. Session membership still needs global
claim/observation references, nullable-size public projections and claim-ID
actions. Kad's upstream unknown-size admission, bounded session/history reads,
canonical separate REST/OpenAPI/WebUI resources and shared-owner session
lifecycle/snapshot replacement remain open. This evidence does not qualify the
combined-scale or total-memory gates. Settings/runtime, library and remaining
foundation allocations retain their existing acceptance gates.

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

The listener/health slice is implemented in Rust `075ea97a` and Harness
`bab926fc`. Scoped checks passed **127 daemon**, **159 REST** and **55 Python**
tests, plus Bash syntax validation and normal commit/push gates. Logs:
`reports/settings-request-round-1/listener-{daemon,rest,python}.log`.
The regular daemon/WebUI build passed with zero warnings:
`logs/builds/20261118T035145Z-build-clients/build-result.json`.
The native campaign passed on exact Rust
`075ea97a1df3d04520d295788b10a562c6c6d75a` with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T035534Z/report.json`.
Its `listenerReceiptPhase` proves the configured nondefault port, matching live
instance and removal on shutdown; its settings CLI phase also passes. The
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
- One profile with **100,000 library contents plus 100,000 retained download
  jobs**, mixed completed/queued/stopped and bounded active work. Measure startup,
  first/late pages, substring search, every statistic sort, mutations, shutdown,
  memory and CPU. Inspect query plans and transient allocations, not only output
  sizes. Qualify normal operation under an enforced **512 MiB total container
  memory limit and 1 CPU**, with 100,000+ retained records and a realistic
  incomplete queue spanning the accepted 10-to-1,000 workload. Measure the whole
  daemon, including startup and background activity, not just resident manifests.
  Concurrency adapts; this target does not promise sixteen simultaneous payload
  executions. Qualify higher-capacity operation separately. Physical reference
  devices remain distinct pending evidence; no idle-only or component-budget
  result proves the constrained-container gate.

Inspect correctness, contracts, failure recovery, interactions, maintainability
and resource use, together where practical. Further review addresses concrete
risks or material findings rather than a fixed round count. Repair material
findings and refresh affected checks. Run applicable gates available without a PR; retain PR-only/physical
device evidence as explicitly pending.

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

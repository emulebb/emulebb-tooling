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
- Application-allocated public IDs, including jobs, roots, servers,
  searches and results, are immutable never-reused decimal strings. Content is
  publicly addressed by its eD2K hash; immutable tag and category names are their
  public IDs. Natural
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
default, owner, platform applicability and application mode. The accepted 59-leaf
engineering catalog is in SETTINGS-TARGET/SETTINGS-INVENTORY; implementation and
qualification remain pending. Derive consumers
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

Downloads have independent durable job IDs and only one unremoved unfinished
job per hash.
Keep compact completed jobs until explicit removal, separate piece/source cleanup
from terminal history, and retain prior-download knowledge independently of job
removal. No download-priority control, including category defaults.

Use only start/stop. Stop preserves the job and partial data; sharing remains
independent. Preserve intent across restart and resume eligible work gradually.
New jobs start by default with an explicit stopped-on-add option. Bound active
work using `maxConcurrentDownloads` with a built-in bounded exploration buffer.
The accepted engineering default is 8 active jobs with a built-in exploration
buffer 2. The global connection cap remains 500; lowering job admission drains
existing work rather than silently stopping jobs. Connection and source caps
have separate meanings. Queued/history rows do not
each require live workers, timers or source machinery.

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

The accepted 2b/2c download cut uses `POST /downloads` with `source` equal to
`{type: "ed2k-link", link}` or `{type: "content", hash, name, sizeBytes?}`.
Content size is optional nullable u64; reuse the server-side eD2K parser,
including AICH/source hints. Optional fields default to `category:null`,
`intent:started` and `redownload:false`. A new job returns 201; an active
duplicate returns 200 unchanged, while conflicting known sizes return 409.
Redownload never duplicates active work. Present or unavailable local content
requires explicit choice; confirmed absence can be downloaded normally.

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
path may materialize the whole collection.

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

Configure P2P interfaces through saved settings. A planned typed ephemeral
receipt from the actual bound listener supplies the health-check endpoint; it
is runtime output, not another configuration authority or a hand-written TOML
parser. Missing/stale receipt handling must fail health checks honestly. Update
launchers, Compose/VPN examples, both container variants, package smoke tests and
harness callers. Preserve legitimate harness route/interface scenario inputs
and apply them through canonical profile setup.

Reuse the existing package/container Python tests for failure cuts before
ownership/stage creation, between per-key commits, before/after atomic rename
and at parent-directory sync. Include automatic resume, final-profile user edits,
concurrent publication, unsupported no-replace behavior and proof that no staging
absolute path leaks into published state. Both Ubuntu and Alpine variants need
actual proof; none is claimed by this design.

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

---
id: RUST-REF-016
workflow: github
product: emulebb-rust
phase: Phase 1
github_issue: https://github.com/emulebb/emulebb-rust/issues/155
title: Move blocking SQLite work behind bounded async persistence
status: OPEN
priority: Major
category: refactor
labels: [rust, tokio, sqlite, async, persistence, performance]
milestone: post-beta-polish
created: 2026-10-23
source: 2026-10-23 Rust async and portability audit
---

> Workflow status is tracked in GitHub: https://github.com/emulebb/emulebb-rust/issues/155. This local document is retained as the durable engineering spec and evidence record.

# RUST-REF-016 - Move blocking SQLite work behind bounded async persistence

## Owned-ingest checkpoint (2026-11-16)

The clean bundle Rust `be881243`, tests `c1ad2912`, tooling `d73eca60` and
Builder `e93fca5` passed the native Windows/host full supported Rust suite:
2,938 passed, zero failed, one ignored subprocess helper, 56 suites and zero
warnings. This is not platform-matrix qualification. Receipt:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/owned-ingest-rust-acceptance-round-1/rust-unit.log`.
Focused gates passed with zero warnings: metadata 126 unit plus 3 ownership,
ED2K 1,350 unit and Core 561 unit plus all Core integrations. Retained logs:

- `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/owned-ingest-metadata-round-2/rust-unit.log`.
- `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/owned-ingest-ed2k-round-2/rust-unit.log`.
- `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/owned-ingest-core-round-1/rust-unit.log`.

One existing tracked `JoinSet` blocking unit owns hashing/media preparation,
conditional SQL and old/new-hash publication through requester cancellation.
Core index metadata and explicit-root memberships commit in the same transaction;
the narrow progress observer retains no Core. One prepared job takes one of the
registry's four slots and zero ordinary 8-MiB bytes. Its separate 64-MiB
representation lease includes a 4-MiB publication workspace and checked path/text
costs. The registry's combined charged representation allowance is at most
72 MiB; the Core owner's 8 MiB and bounded read workspace are additional.
Parser allocations, SQL allocator costs and RSS are excluded, so this is not
a complete 64-MiB ingest-memory claim.

Coverage includes the existing 256-GiB cap enforced before allocation and a
Windows sparse-file regression; fallback with real rollback and a binding race
from another connection; cancellation during preparation/after commit and drain;
old/new copies, live partial state and short root-epoch retry without rehashing.
Delivery/journals remain outside this owned-ingest proof. Pinned Symphonia
options do not establish parser allocation bounds, and broader scan/resource
qualification remains open. The native Windows/host suite above is not
Android-device qualification. Neither
phase 2a nor round one is complete.

The subsequent regular Windows runtime build passed in 188 seconds with zero
warnings; receipt:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261116T094710Z-build-clients/build-result.json`.
The registered campaign passed for Rust `be881243`, tests `c1ad2912`, tooling
`611d756a` and Builder `e93fca5`; report:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261116T095105Z/report.json`.
It exercised 83/105 main operations: 40 successes, 43 expected errors, 22 explicit
unsafe skips and a passing SSE check. The six-route friend phase passed. Kad
proved actual SQL HTTP 500 failure with unchanged state, retry, reopen and same-profile restart
with stable identity/contacts. The category phase passed, including unique-
complete-hash withdrawal, independent-copy preservation and unchanged fixture
bytes. Overall teardown was graceful. This qualifies this scoped Windows
runtime bundle, not all 105 operations, Android device behavior, delivery repair,
combined scale or the entire foundation.

## Prepared-ingest provider checkpoint (2026-11-16)

The five-file allocation-provider slice is qualified by focused checks: exact-
capacity packed leaves, moved root buffers, flat hash decoding, streaming stored-
identity comparisons and streaming alias IDs. Public APIs, SQL and fallback
semantics are unchanged. Metadata passed 123 unit plus 3 ownership checks with
zero warnings, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/prepared-ingest-metadata-round-1/rust-unit.log`.
ED2K passed 1,340 units with zero warnings, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/prepared-ingest-ed2k-round-1/rust-unit.log`.
Independent Terra review found no material defect. The maximum-geometry fixture
is not an exact part multiple: the terminal empty-MD4 branch is unchanged and
is not newly proved by this fixture.

At the existing 256-GiB geometry, the conditional representation capacities are
32,284,688 bytes during hashing and 36,055,288 during conversion. These are
provider payload-capacity calculations, not an actual 256-GiB read, full-ingest
allocation bound, media-parser bound or RSS result. The total prepared-job
64-MiB allowance and cancellation/publication integration were pending at this
provider checkpoint; the subsequent owned-ingest checkpoint above records their
scoped implementation and tests. Pinned Symphonia options do not
establish a parser allocation bound; qualification remains open without feature
removal. This is a provider checkpoint, not complete ingest or round-one proof.

## Registered category checkpoint (2026-11-16)

The supported registered campaign **passed** for this exact staged source bundle:

- Rust: `22573afd8cc4d8d8850e537d91f030be2eb5fbd0`.
- Tests: `c1ad2912e0a9717958e3592f99f7c0e2ff54dfeb`.
- Tooling: `5be25fc44d4faf7bbd5313070fb67c992d0b1233`.
- Builder: `e93fca5abc195cc203ba28d0d935db500f056334`.

Regular Windows runtime rebuild: 182 seconds, zero warnings, receipt
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261116T074842Z-build-clients/build-result.json`.
Passing report:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261116T075302Z/report.json`.
Main conformance covered 83/105 operations, 40 successes, 43 expected errors and
22 explicit unsafe skips, with SSE passing. Friend fault/retry covered all six
delegated frontdoors returning HTTP 500 `PERSISTENCE_FAILED`, with unchanged
cache/database on failure and three reopened
database `quick_check` results of `ok`. Kad exercised real SQL HTTP 500 failure
with unchanged state, retry, graceful reopen/restart and stable identity/contacts,
including one actual routing reply; no Kad `quick_check` result is claimed.

The new category phase proved the name grammar, case-insensitive lookup,
immutable public name identity, nullable assignments, deletion, and same-name
recreation without relinking cleared assignments, including restart. Removing
the category destination withdrew its unique complete hash while retaining an
independent complete copy; all fixture bytes remained unchanged. All owned
daemons ended gracefully. These results qualify this staged category contract
and scoped lifecycle, not the entirety of phase 2a or round one.

The original campaign failure is retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261116T073121Z/report.json`.
It exposed three private bootstrap phase values and four stale live-consumer
probes in the main phase; subsequent phases did not run. The direct correction
uses the five public coarse phase literals and a producer regression. Core round
10 then passed 560 units plus all Core integrations with zero warnings; Python
round 6 passed 46 live-conformance/CI-owner checks. Earlier current-contract
140 checks and UI 53 unit/32 Playwright/typecheck/build evidence remain unchanged.

Full supported Rust acceptance round 6 passed 2,921, zero failed, one ignored
subprocess helper and zero warnings on the preceding working material. Its
104 recorded source-file hashes matched the five granular Rust commits ending at
`eb5b551251f10c9b985ad648bf16345b2b7a4726`; receipt:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/category-foundation-rust-acceptance-round-6/committed-source-material.json`.
That full-suite result precedes the phase correction; the later focused checks
and exact staged campaign above qualify that correction without attributing
the earlier full suite to a later source head.

The sealed-arm failure, concurrent drain wake-up and separate control/join-handle
review repairs are implemented and tested. A real Core Kad fixture proved the
snapshot row and revision before a held reload-execution gate was released;
this is not proof against blocked slow filesystem I/O. At this runtime bundle,
prepared-ingest accounting remained planned; the later owned-ingest checkpoint
above records its scoped progress. Broader hash/scan bounds and jobs,
settings, CLI, REST redesign and combined-scale work remain outstanding. No
100k runtime, 365-day or full-platform qualification, complete-goal claim, PR or
merge follows. An ensuing evidence-only tooling head is not this tested bundle.

## Registered shared-owner runtime checkpoint (2026-11-16)

The [#233 registered runtime checkpoint](RUST-FEAT-062.md#registered-kad-runtime-checkpoint-2026-11-16)
records the exact staged Rust `d5c2cfbe` / tests `0531be83` / tooling `eac34a72` /
Builder `e93fca5` bundle, supported build receipt and passing REST CI report.
It covers main conformance/SSE, all six delegated friend fault/retry frontdoors,
and real Kad import SQLite fault/retry followed by graceful reopen and same-profile
restart with stable identity and contacts. All owned daemons ended gracefully.
The three friend databases passed `quick_check`; the Kad phase records distinct
reopen/restart assertions and does not record that integrity check.
This is scoped shared-owner runtime proof, not global all-SQL conversion,
measured RSS, sustained upload progress or full-foundation qualification.

## Typed Kad owner extension checkpoint (2026-11-15)

The [#233 schema 72 checkpoint](RUST-FEAT-062.md#schema-72-and-typed-owner-checkpoint-2026-11-15)
records `b08709a1` typed load/initialize byte leases and `ca5e6993` durable generated
Kad identity, with focused metadata/Core/Python proof. These extend the existing
owner rather than introduce a new lane. At this storage checkpoint production
DHT binding and the runtime lifecycle were still in progress. The registered
local peer proof below remains attributed to its exact older staged source
`b509524f`; no later
schema/runtime qualification or global all-SQL conversion is implied.

The [Kad local-suite checkpoint](RUST-FEAT-062.md#runtime-coupling-local-suite-checkpoint-2026-11-16)
records final green uncommitted-material Rust/Python/WebUI suites and the
resource, startup-handoff and daemon SQL-failure cleanup/drain repairs. Earlier
failed/interrupted rounds remain retained. Those suites were local working-material
evidence; the registered checkpoint above now supplies exact staged acceptance
for the new Kad fault/restart phase. Do not claim global async conversion,
measured RSS, sustained upload progress or full-scope delivery from these counts.

## Registered conformance and local peer checkpoint (2026-11-15)

The first registered campaign at Rust `45ca468b` **failed**. Its retained report
is `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261115T205632Z/report.json`.
The main conformance phase exercised 83 of 105 operations with 43 expected errors,
22 unsafe skips and no failed routes; the separate SSE check passed. The local
peer phase proved all 6 required friend-mutation frontdoors and retry behavior,
but two peers exited nonzero during teardown. The campaign correctly remained
failed instead of treating successful HTTP assertions as complete acceptance.

The defect was ordinary handled SQLite request failures being retained as a
sticky owner-drain failure. Rust `b509524f` separates completed request errors
from worker/uncertain-commit faults without weakening the harness. The focused
Core selection passed 510 checks and all selected integrations. The registered
regular runtime was rebuilt in 187 seconds with zero warnings; its build log is
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261115T210559Z-build-clients`.

The rerun **passed**, with exact frozen companions Rust `b509524f`, tests
`a96b5859`, tooling `26492515` and Builder `e93fca5`. Retained report:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/rust-rest-openapi-ci/20261115T210858Z/report.json`.
It exercised 83 of 105 main operations, including 43 expected-error responses;
22 unsafe operations remained explicitly skipped, no route failed, and SSE
passed. The local loopback-only peer phase covered 6/6 active-upload, waiting-
queue and download-source add/remove-friend frontdoors: injected failures
returned HTTP 500 `PERSISTENCE_FAILED`, cache and reopened database stayed
unchanged, and subsequent add/remove retries succeeded. All three databases
reopened with integrity `ok`, fault triggers were removed and every owned
process exited zero. The original failed evidence remains retained.

Logs include bounded forced-download-task-abort warnings during teardown; they
are not claims of leaked processes. This proof does not establish upload-byte
progress under SQLite contention, a full platform matrix, combined 100k scale,
365-day endurance or complete Kad/settings delivery. No PR/merge/publication is
authorized before operator review.

## Scoped friend-owner checkpoint (2026-11-15)

Rust `ea0f9653` implements ordered friend mutations through the allocated owner,
including the direct and delegated REST friend frontdoors. Its scope is converted
friend writes and their commit/cache-publication boundary, not global FIFO or
conversion of every SQLite path. GET reads the cached friend view and reports
an unavailable state after an unresolved owner fault. Kad runtime commands and
canonical settings integration still need to reuse this owner.

The parent recorded 509 Core checks, 155 REST checks and 3 integration checks
passed. Earlier metadata 108 proof belongs to the separate schema 71 repository
checkpoint; it is not new friend-runtime evidence. Selected-artifact OpenAPI
validation passed 130 existing Python checks, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/current-openapi-ea0f9653-9f7040ed/junit.xml`.
The frozen pushed source set was Rust `ea0f9653`, tests `fcf6dbb3`, tooling
`9f7040ed` and Builder `e93fca5`.

The diagnostics runtime build completed in 225 seconds with zero warnings,
with its log under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/logs/builds/20261115T203327Z-build-clients`.
Compilation is not a runtime contention campaign. Actual upload progress under
SQLite contention, combined-scale proof and full-scope qualification remain
pending. No PR/merge/publication is authorized before operator review.

## Allocated foundation owner: 155-A (2026-11-15)

The parent has explicitly allocated the accepted 155-A owner and friend-CRUD
slice under [public-foundation round one](../../design/PUBLIC-FOUNDATION.md).
The contract was accepted before implementation; the scoped checkpoint above
records current implementation evidence without claiming global completion.
The allocation baseline was Rust `82181294`, fresh schema 71. The slice adds no schema change, new CLI option,
environment input or public tuning knob. Earlier schema 68 acceptance is a
historical review baseline, not a downgrade instruction. Keep WAL/FULL durability,
profile ownership, typed current-model validation and existing busy behavior.

### One owner and composition

Compose one shared profile/runtime persistence owner with one fixed blocking
SQLite worker and one tracked asynchronous coordinator. Cloneable handles share
that owner; they never create workers, queues or coordinators per request or
clone. Commands are a closed typed FIFO. Friend CRUD is the first canonical
integration; later Kad, settings and other converted paths reuse the same owner.
Do not create a rival actor, per-request spawn-blocking lane or unbounded task
fan-out. FIFO and responsiveness claims cover converted paths only; synchronous
unconverted paths still exist and must not be described as globally fixed.

Offline synchronous metadata constructors continue to work without a Tokio
runtime. Runtime composition explicitly starts and owns the coordinator/worker;
there is no hidden runtime requirement during schema/profile construction.
The ownership graph must contain no strong Core-to-Owner-to-Core cycle and no
Store-to-Owner-to-Store cycle. Finalization retains only the necessary independent
cache/state handles or typed completion data, not a strong Core back-reference.

### Admission and resource accounting

Use conservative internal limits of **64 admitted operations** and **8 MiB
(8,388,608 bytes) of admitted owned payload**. These are implementation limits,
not user settings. Eight MiB is chosen to accommodate a full bounded 12,000-
contact routing snapshot plus temporary conversion costs; tests must measure the
actual representation cost rather than assume source-wire size equals owned
memory. Changing this engineering budget requires measured review, not a second
public authority.

Admission is nonblocking: reserve both operation and byte quotas before cloning
or materializing owner-held request data. Account for owned backing storage,
variable-length fields, bounded replies and temporary conversion allocations.
Use checked sizing arithmetic and a conservative documented cost model; do not
admit a zero-cost command that later allocates an unbounded result. Converted
reads need bounded query/results or an explicit pre-allocation size decision.
Do not silently truncate data. The 8 MiB limit bounds retained product-payload
capacity, including the charged owner-held buffers/conversions; it is not a
measured RSS bound. Transport/TLS memory, rejected oversized transport frames,
SQLite internals, allocator bookkeeping and thread stacks are excluded. Keep
those costs explicit and measure them separately; do not report total process
memory as bounded to 8 MiB. Retain quota through the actual worker allocation
peak, not only through request handoff.

Retain the operation and byte permits through required SQL completion, outcome
handling and cache publication, including required finalizers. A queue slot is
not released merely when dequeued or committed. Request cancellation must not
turn a bounded queue into unbounded detached tasks or release retained payload
while a worker/finalizer still owns it. Saturation, closing and oversized work
are explicit typed outcomes; no invisible waiting queue or admission bypass.

### Ordering, cancellation and shutdown

The close/admit boundary is atomic: after close wins no new operation is
accepted; work accepted before close remains owned and drains. Capture normalized
friend intent without holding global CoreState across admission, SQL wait or
publication. Ordering spans durable commit and the matching authoritative cache
publication; a later command cannot observe or publish half of its predecessor's
result. The planned category continuation below separates bounded filesystem
publication from this immediate SQL/cache order without stalling unrelated domains.
Caller cancellation before admission changes nothing. After admission, the
operation owner retains SQL completion, cache publication and required follow-up
handoff independently of request disconnect/cancellation. Required work and
finalizers survive caller abort under that same tracked owner, which participates
in terminal drain. Success cannot precede acceptance of a required handoff.
A successful completion is reported after the required publication, not merely
after enqueue or SQL commit.

Release the SQLite connection mutex before any CoreState/cache finalizer. Never
hold that mutex while acquiring CoreState: remaining synchronous callers can
otherwise invert the lock order. Keep commit/publication ownership explicit;
SQL failures do not publish uncommitted cache state. Errors after a successful
commit must retain the fact of commit and cannot pretend the write rolled back.
Known-committed handoff failure is an explicit outcome, not successful completion
or a claim of rollback. Reuse existing owners, finalizers and reservations rather
than per-endpoint actors/tasks. Request disconnect does not invoke explicit
business cancellation such as stopping or removing a download.

Audit settings application, download create/delete/delivery, asynchronous
imports and other mutation lifecycles as their existing phases implement them.
Do not declare unreviewed paths safe or faulty, broaden the current checkpoint,
or create a separate inventory/status ledger for this rule. Extend the existing
Rust/Python owners for cancellation before SQL, after commit and during
publication/handoff; concurrent or cancelled drains; SQL fault/retry and
saturation. Tests must check retained intent and required completion, not only
whether the disconnected caller receives a result.

#### Confirmed follow-up ownership gaps (2026-11-16)

The independent Terra cancellation audit confirmed these pending boundaries;
they are not fixed or qualified by the prepared-provider/category checkpoints:

- `store.rs::store_manifest_unlocked`: SQL through manifest/checkpoint cache,
  followed by `core/transfer_state_api.rs::set_transfer_control_state` attempt
  cancellation, Core view and publication, needs retained completion ownership.
- `metadata.rs::update_shared_file_metadata`: SQL through catalog/upload-queue
  publication has the same ownership gap.
- Owned ingest now covers its verified-content/media SQL and publication. The
  subsequent `core/delivery.rs` call to
  `metadata.rs::register_delivered_local_content`, then path admission and
  retirement, still needs retained completion ownership.
- `metadata.rs::remove_completed_transfer_row`: request-retirement SQL, catalog
  publication, finish SQL and cache eviction need tracked completion together.
- `app_api.rs::update_app_settings` already uses an owned task that survives
  requester abort. The gap is shutdown: `friend_api.rs::drain_persistence` does
  not track/seal that task, rather than ordinary request cancellation.
- Pre-existing phase-2d monitor gaps: `auto_share` registers its map entry before
  awaited admission, so failed admission plus the same fingerprint can suppress
  retry. `auto_unshare` removes its entry before awaited withdrawal, losing retry
  intent on failure/cancellation. Reuse canonical path lookup, tracked withdrawal
  and conditional map removal/reconciliation; a delayed Remove must fingerprint/
  compare-and-set guard a newer recreated path. Full reload/overflow reconciliation
  can repair state; watcher restart alone is not proof. Add no Core capture.

Route repairs through the existing `LocalMutationRegistry`, per-hash manifest
owners, settings rewrite and existing delivery/retirement journals as appropriate.
Journal recovery alone is not proof of same-process completion after caller
abort. Reuse existing ED2K tests and Core `transfer_lifecycle`, `deliver_runtime`
and settings test owners with gates after SQL and at publication/handoff,
requester abort, cancelled/concurrent drains and reopen. These follow-ups remain
unimplemented; add no generic actor or per-endpoint task framework.

Shutdown explicitly closes admission, drains accepted required operations and
finalizers, joins the fixed worker and tracked coordinator, then releases the
connection/profile lease. Drain failure is reported honestly. No owner lifetime
may rely on a dropped caller's future, a transient runtime handle or an Arc cycle.
The parent serializes the shared Core, schema and daemon-drain composition seams.

Expose Busy/Closing as retryable native HTTP 503 outcomes when the phase-four REST
mapping is implemented. This owner slice first establishes typed errors and
required completion semantics; it is not permission to change unrelated status
contracts or weaken accepted durability. Oversized work must fail explicitly
before copying and be distinguishable from transient saturation.

### Planned category publication continuation (phase 2a)

This parent-approved allocation now has the scoped registered category proof
above. The contract below also retains outstanding prepared/hash/scan resource
obligations; it is not a claim of complete phase-2a implementation, measured RSS
or 100k qualification. Earlier friend/Kad evidence remains attributed to its
own source bundle.

#### Current draft feedback (2026-11-16)

These retained local-draft observations precede the registered checkpoint above;
their failure and repair history is not the latest acceptance verdict.

The settled public contract uses immutable ASCII category names as IDs,
name-addressed category routes and one nullable `category` download field,
with numeric SQL keys internal. Parent-recorded focused checks on working
material passed: metadata round 7 had 120 unit plus 3 ownership checks; ED2K
round 4 had 1,339 unit checks, including observed-root exact paths, old-location
tombstones, independent copies, unchanged last-scan state and stale-epoch
rollback. WebUI round 4 passed 53 unit and 32 Playwright checks, typecheck and
production build, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/category-foundation-webui-round-4/webui.log`.
Current-contract/campaign-unit Python round 4 passed 140, retained at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/category-foundation-python-round-4/junit.xml`.
Static round 2 passed 129 before the later documentation-only OpenAPI port-literal
correction; that is not a final selected-contract verdict.

Earlier Core round 4 passed 540 units plus all Core integrations. Subsequent
lifecycle rounds 5 and 6 failed root-SQL fixture assertions, with round 6 at
546 passed and one aggregate-root/explicit-origin accessor failure. Round 7
was interrupted after six failures and a real test-only deadlock; retain its
incomplete failure log at
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/category-foundation-core-round-7/rust-unit.log`.
Round 8 compiled with zero warnings and reached 550 passed plus one
verified-parent fixture failure; five delivery regressions were fixed, but
integrations did not run. Retained log:
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/category-foundation-core-round-8/rust-unit.log`.
Core round 9 subsequently passed 555 units and all Core integrations, including
detached-scan checks. This precedes the latest cancellation-handoff refinement;
the related handoff gap remains open. Full-acceptance rounds 1-3 retain,
respectively, an import compilation failure, one invalid-name fixture failure,
and two actual detached-scan failures. None is a final successful acceptance run.
That internal review queued sealed-arm success-gap, concurrent join-handle
drain-waker and control-to-join-handle strong-back-reference repairs; the
registered checkpoint above records their subsequent implementation and tests.

Monitor async stop/join, retained root-I/O/root-SQL slots, cancellation fixes,
root-admission sealing and owned explicit-root compare-and-set/multiple-root
continuation were still draft at this local checkpoint. The registered result
above supersedes that pending lifecycle verdict. Prepared verification was still
planned at this local checkpoint; the owned-ingest checkpoint records its later
scoped implementation, without broad scan or scale qualification.

The coalesced reload handoff and terminal ordering use the following contract.
Reuse the existing reload worker with one retained task slot.
Its narrow control holds only pending state, reservation count, seal state and
`Notify`, without a Core or join handle. Reserve a `RootCommand` token in
`submit_reserved`'s `make_command`, after the existing owner quota is acquired;
the command holds only that token. Successful SQL plus authoritative cache
publication arms the accepted scan intent before the mutation receipt; failed
compare-and-set or rollback drops it. Caller cancellation cannot lose the
accepted handoff. The worker waits while reservations remain and exits when
idle; permit only one immediately-exiting predecessor handoff. Add no actor,
queue or per-request task, and never let a scan rearm a stopped monitor.

Terminal order is: begin shutdown; seal reload and regular admission; stop/join
the monitor; call the final Kad checkpoint directly; perform bounded network
cleanup. Final Kad reads DHT state only and need not wait for local finalizers.
After that stage and outside the network timeout, drain the persistence owner
so accepted root-command tokens resolve; join the retained reload task in place
without abort, using cooperative stop; seal/drain the local registry; drain root
SQL work; drain eligibility reads. Attempt every stage and retain errors before
releasing the connection/profile lease. Scan/hash allocation bounds remain planned.

Keep category SQL and immediate authoritative category/assignment caches ordered
through the existing worker/coordinator. Retain each admitted category receipt
until its required publication succeeds or returns an explicit failure. Permit
one active tracked category continuation, with later category work in an
admitted, slot-bounded parked FIFO. Unrelated friend/Kad domains may proceed
subject to normal shared admission; no global metadata FIFO may wait behind a
100k filesystem scan. The existing sharing/health owner performs bounded
filesystem slices off the SQL worker. Add no persistence actor, detached task
per request, unbounded continuation queue or lock held across filesystem work.
Keep coordinator-to-health ownership weak (a `Weak` sender). Monitor stop/join
and cancellation-safe fixed slots for Core-owning async handles have scoped
checkpoint evidence above. Track actual late filesystem probes and
snapshots separately from root SQL jobs retaining `MetadataStore`; those SQL
jobs must settle before profile release. A single tracked actual late probe
suffices. No broad Core extraction or new strong coordinator/health retention
cycle is required by this refinement.

Shared-directory GET is a lightweight cached configuration/last-observed-health
read. The existing monitor's two-second interval and explicit scans update those
observations; they are not a freshness deadline or instantaneous filesystem
truth. New unverified roots report `accessible=false`. Do not initiate a physical
probe per GET; root mutations or health work requiring filesystem access use
the retained blocking-I/O boundary. This adds no DTO/freshness field or setting.

Missing/stopped sharing ownership or shutdown interruption yields a distinct
internal known-committed publication failure (`CommittedPublicationFailed`),
not unknown commit or global authoritative-cache corruption. Keep the eligibility
safety fence active and the immediate authoritative category/assignment caches
coherent. Retain the fact of durable commit; unrelated admission, the final Kad
checkpoint and owner drain stay available. The planned mapping is HTTP 503
`PERSISTENCE_COMMITTED` with `details.committed=true`: durable commit is known,
but downstream sharing publication is not guaranteed. The category caller must not receive
success before required publication. Caller abort does not detach or abandon
the continuation. Public error mapping must preserve these distinctions.

Late category-health filesystem work retains its actual byte lease until its
buffers are dropped, including after the initiating continuation stops waiting.
Core baseline payload, final Kad reservation and that late-I/O payload share the
Core owner's 8 MiB product-payload budget; prove their checked combined bound and actual
residual capacity. Do not release quota while blocking work still owns memory
or describe this budget as process RSS.

The minimal indexed prerequisite extends existing `shared_file_memberships`
with derived `known_file_id`. Its composite `(path_id, known_file_id)` foreign
key references `local_file_instances`' matching unique key with `ON UPDATE`
and `ON DELETE CASCADE`; a covering `(root_id, known_file_id, path_id)` index
supports grouped keyset traversal. This remains derived membership, not a new
index authority or table. Enumerate removed memberships too, process each
affected content once, and bound each query/allocation rather than materialize
the full library or all-copy manifests/source lists.

Bound complete/partial copy selection independently and preserve their separate
serving eligibility. An active-hash watch prevents unrelated content changes
from starving progress. A root eligibility epoch covers every root/accessibility
writer. Actual cached ranked server-offer batches and Kad/direct complete-file
serving must revalidate eligibility while category publication is pending or
failed; unchanged cached offers are not sufficient. Independent partial sources
must remain usable where their own policy permits.

Run bounded indexed eligibility reads through the existing `MetadataStore`
outside ordinary persistence admission. Use an explicit separate bounded read
workspace/concurrency limit and track the store/profile-lease lifetime; add no
reserved read actor. Combine complete-file eligibility with independent live
partial-source authority rather than treating one as a substitute for the other.

At allocation no existing ED2K mutation tracker supplied the local-eligibility
lifetime boundary. The small finalizer registry tracks existing
blocking local-eligibility SQL and synchronous-publication units using an owned
`JoinSet::spawn_blocking`. Bound it to **4 admitted units and 8 MiB ordinary
retained payload**, reserving before clone/spawn. The single prepared-ingest job
shares those slots with its separately charged allowance below. It has no queue,
dispatcher, new actor or per-request async task, and uses the same database mutex.
This separate allowance is additional to the Core owner's 64 slots/8 MiB and
the separately bounded read workspace; the combined payload allowance increases
and must not be reported as the Core's 8 MiB limit or a process RSS bound.

The actual blocking unit owns bounded input, the existing owned per-hash guards
and stripe guard, payload lease, SQL/cache handles and response sender. Perform
fallible projection work before commit in the same transaction, release the DB
connection, then finish bounded synchronous cache/catalog publication while
preserving live partial state, uncheckpointed progress and independent complete
copies. Caller abort loses the response only; the admitted unit completes.
Reap completed handles; atomically seal admission and join outside the registry
lock. Retain panic and known-committed publication failures for honest drain
reporting. Drain in the post-final-Kad sequence above before profile-lease
release. Saturation is transient busy; internal required work
must retry without losing its intent. This tracks existing
blocking calls, not a second persistence service or new test framework.

Prepared verification uses **one separately accounted 64-MiB representation
lease**, including its 4-MiB publication workspace and checked path/text costs.
It takes one of the four local-registry slots and zero ordinary 8-MiB bytes:
the registry's combined charged representation allowance is at most 72 MiB.
Core's 8 MiB and bounded read workspace remain additional. Preserve existing
256-GiB support; parser/SQL allocator costs and RSS are outside this allowance.
The provider checkpoint above establishes exact-capacity packed leaves and
streaming stored-identity/alias handling for its scoped representation.
Complete parser/pipeline allocation qualification remains open. Maximum geometry
is 28,257 parts and 1,497,588 leaves, or 29,951,760 packed leaf bytes. Conditional
provider payload capacities are 32,284,688 hashing bytes and 36,055,288
conversion bytes; neither
is a complete ingest/media/publication or process-memory bound.

The prepared job's real lease follows the actual hashing closure and its
result through tracked SQL/cache publication even when the caller cancels. The
progress observer retains only its required progress authority, not Core.
Its publication workspace is included in the prepared allowance, not charged
again as ordinary registry bytes; other local mutations retain their own charges.
Do not describe these allowances as the Core's 8 MiB or total RSS.
Immutable registration must not silently rebind paths or mutate the transfer's
AICH cache authority. These changes add no public setting, queue, actor or
file-size limit. Broader ingestion/scan resource and runtime qualification
remains open.

Preserve the existing direct `TcpStream::write_all` path. Encode at most the
existing 200 server items into an owned bounded packet, then perform a final
eligibility epoch check and admit that packet under the short publication/root
lock. Release the lock before socket I/O. A root change before admission
invalidates the packet and requires retry; a root change after admission may
allow that one already in-flight bounded packet to finish. Every subsequent
batch must recheck eligibility. Add no writer actor/channel or lock spanning
the write. These packet and read boundaries remain planned and unqualified.

Reuse existing Rust/Python owners to prove same-category order, unrelated
friend/Kad progress, receipt/cancellation/shutdown outcomes, removed-membership
coverage, bounded first/late keyset pages and allocation peaks, and eligibility
at real offer/serving frontdoors. No such new acceptance proof is claimed here.

### Required acceptance before reuse

Use the existing Rust/Python test owners and supported orchestration. Prove:

- exact slot/byte reservation and checked sizing, refusal before clone, full
  contact-snapshot representation cost and temporary-conversion allowance;
- slow connection acquisition/commit with unrelated runtime progress, FIFO
  ordering through publication and no SQL/CoreState lock inversion;
- saturation and atomic close/admit interleavings;
- caller abort after admission or commit without abandoned finalizers, prematurely released
  permits, lost writes or unbounded tasks;
- failed writes and same-key friend mutations without cache/durable divergence;
- explicit close/drain/join, reopen and profile-lease release ordering;
- one owner across clones, no retention cycle, and offline constructors without
  an async runtime.

Record focused evidence and exact source revisions in this item. Two inspection
rounds and applicable integration gates remain required. Runtime Kad checkpoint
wiring must wait for this owner; no separate temporary worker is authorized.


## Allocated delivery/job-storage repair (phases 2b/2c)

The operator's unchanged `2026-11-15-android-duplicate-download-delivery-bug.md`
report is retained in the requested operator audit folder. It records repeated
completed copies and unsupported atomic directory cleanup on Android; the
installed build differs from reviewed source `be881243`. Fingerprint drift's
device cause remains unknown. File close, playback and media-indexer activity
are not established causes. This repair is authorized within the common
job-storage/delivery/journal phases and is **not fixed** by the ingest checkpoint.
No device installation, profile reset/migration or Android-specific bypass is
authorized by this allocation.

Source inspection at `be881243` confirms `deliver.rs` finds matching bytes but
resets an owned delivery to Pending and recopies after fingerprint drift;
`metadata.rs::register_delivered_local_content` separately refuses the prior
fingerprint. Separate verification from destructive ownership: a stable freshly
hash-matching recorded output may remain Delivered + Unowned, refreshing its
verification fingerprint conditionally on the same job/path. Matching bytes
never grant delete/overwrite authority. Materialization, promotion, retry and
restart must change coherently; pending cleanup must not recopy a successful
delivery. Deliberately revise the existing byte-identical replacement regression
to require verified unowned delivery without duplicate copying or destructive
authority.

`fs_durability` classifies `EINVAL`, `ENOSYS` and `EOPNOTSUPP` as
`AtomicMoveUnsupported`; current internal cleanup cannot progress without
directory rename.
Provide common capability/authority-preserving cleanup through exact job storage
and existing journals, preserving foreign replacements, markers, symlinks and
collisions. If safety cannot be proved, retain pending cleanup; never substitute
an unchecked rename or recursive deletion.

`metadata.rs::remove_completed_transfer_row` commits retirement/journal state
but changes only a local manifest clone before cleanup. Failed cleanup can leave
the cache stale, making a later refusal to enter retirement a plausible cause
of the observed error; deterministic reproduction is still required. Publish
committed retirement coherently and retain same-process retry ownership through
pending cleanup and reopen, without triggering delivery again.

Extend existing Rust delivery/retirement owners and the Python platform harness
for baseline/verification diagnostics distinguishing device/inode, size, mtime
and ctime at capture/verification; metadata drift, byte-identical replacement
and actual mutation; unsupported rename; same-process retry, reopen and crash
cuts; job/path compare-and-set races; and genuine foreign ownership, markers,
symlinks and collision protection. Distinguish observed filesystem drift from an inferred
device trigger. This allocation preserves the fresh-profile/no-shim scope and
adds no device/runtime qualification claim.

## Summary

Remove synchronous SQLite waits and durable flushes from Tokio worker threads
and global async state locks. Introduce bounded persistence ownership that keeps
the network runtime responsive while preserving crash consistency and explicit
backpressure.

## Allocated Safety Slice: Peer-Credit Settlement

The parent allocated the bounded `peer-credit-settlement` workstream after
source review at Rust `23e685b87bb76db21489c9b1cc725dd0da4241c1`.
Failed single-peer settlement currently removes parked deltas before fallible
SQL without restoring them. Restore by saturating merge under the existing
flush gate, retain additions parked during SQL, and propagate the original
error. Reuse the batch-flush restoration rule.

Preserve current schema 69, WAL/FULL durability, storage ownership, secure-ident
anti-theft behavior and existing ordering. No persistence actor, queue, shutdown
or Kad snapshot change belongs to this repair. The earlier schema-68 reference
below records the 155-A review baseline, not a schema downgrade instruction.

Required regression proof covers a real SQLite abort with durable rows
unchanged and parked credit retained, additions merged without overwrite or
overflow, exactly-once retry and reopen, plus existing secure-ident wipe tests.
The failed-settlement parked-credit restore and exactly-once SQL retry were
delivered in PR [#335](https://github.com/emulebb/emulebb-rust/pull/335), merged
to Rust `main` at `0840e9005fd2ab28e9cbe262054dd692262e5698`. Its exact
pre-merge source passed all six stages in the full local owner check
(`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/local-check/emulebb-rust/20261115T075009Z-41880a82`),
including Windows, Linux and Android; all 30 hosted checks and four workflows
passed. The broader bounded persistence conversion remains incomplete; the newer
scoped friend-owner checkpoint above records the implemented 155-A slice.

Review confirmed a separate remaining secure-ident boundary: the flush gate
ends before the subsequent `pin_verified_secure_ident`, and additions do not
take that gate. Concurrent pre-bind deltas can therefore flush after the first
bind wipes unsecured credit. The settlement restore does not fix this ordering
gap. A separate coherent bind/add linearization repair needs deterministic
interleaving proof. The analogous absolute-seed path currently has only test
callers; this review establishes no production race for that path.

## Historical accepted 155-A review (2026-11-12)

The parent accepted [one bounded persistence owner plus friend CRUD](https://github.com/emulebb/emulebb-rust/issues/155#issuecomment-6830001541)
after source review at Rust `080a5dea70186da31dab958757b5b8c0fd883f82`.
The allocation above now authorizes implementation under the round-one mandate.
This older review remains evidence; contract acceptance is not implementation
or global completion.

- Compose one fixed worker and typed FIFO for migrated friend operations.
  Bound admitted slots and owned payload bytes through completion; report
  saturation/closing explicitly rather than spawning unbounded work. Cloning
  a handle does not create another owner.
- At this historical review the baseline was schema 68. The current allocation
  preserves actual schema 71, WAL/FULL durability, existing SQLite busy behavior,
  secrets and the OS-backed profile lease. Offline synchronous constructors
  remain usable without a Tokio runtime. No schema change is part of 155-A.
- Capture normalized friend input and release global CoreState before
  admission/wait. Ordering spans durable commit **and** cache publication;
  caller cancellation cannot release that order or strand committed DB/cache
  state. Required success follows publication, not enqueue alone.
- Release the SQLite connection mutex before any cache/CoreState finalizer.
  Legacy synchronous DB-under-CoreState callers still exist; the new lane must
  not introduce a lock-order deadlock with them. Migrated-only FIFO does not
  imply global FIFO or complete removal of blocking persistence.
- Shutdown closes admission, drains accepted required writes and finalizers,
  joins the worker before connection/profile-lease release and reports failed
  drains honestly.
- Use meaningful saturation, slow-commit/connection-contention, failed-write,
  same-key concurrency, cancellation and drain/reopen regressions. Measure
  queue, connection wait and execute/commit behavior; source inspection alone
  establishes no responsiveness or performance result.

Reserve the metadata executor/exports and composition seam, friend APIs and
their ordering boundary, daemon drain seam and existing friends REST error
mapping/tests. The parent serializes shared Core/schema/shutdown edits.
[#233](RUST-FEAT-062.md) must reuse this owner for its later typed,
generation-safe Kad snapshots and met-file removal. No production or schema
implementation is claimed by this accepted slice.

## Current State

The metadata layer shares a synchronous `rusqlite::Connection` behind
`std::sync::Mutex`, uses `synchronous=FULL`, and allows a five-second busy
timeout. Core API methods and search paths call that storage directly from async
contexts, sometimes while holding the global core state or search-index lock.
Upload request handling also performs synchronous counter and metadata writes
before continuing peer work. A busy database or durable flush can therefore
block a Tokio worker and serialize unrelated network, REST, or scheduler work.

`RUST-REF-008` already owns large-library ingestion batching. This item owns the
broader runtime boundary for interactive reads, compound writes, counters, and
hot peer paths.

## Why This Matters

Blocking a cooperative executor on database mutex acquisition, query work, or
filesystem synchronization converts storage latency into protocol latency.
Adding more `spawn_blocking` calls ad hoc would hide ownership, permit
unbounded work, and make ordering harder to reason about.

## Representative Sites

- `crates/emulebb-metadata/src/store.rs` connection ownership and pragmas.
- `crates/emulebb-core/src/category_runtime.rs`, `server_api.rs`,
  `friend_api.rs`, `app_api.rs`, and `search_api.rs` async callers.
- `crates/emulebb-metadata/src/transfer_store.rs` transfer metadata and counter
  updates.
- `crates/emulebb-ed2k/src/ed2k_transfer/upload.rs` upload accounting called
  from the peer payload path.

## Intended Shape

- Own SQLite writes in a dedicated bounded persistence executor or actor with
  typed commands, explicit queue capacity, and measured latency.
- Use set-oriented transactions for compound state changes and bounded
  batching/coalescing for lossy counters where the durability contract permits.
- Run blocking reads through a bounded read lane or dedicated read connections;
  never hold a Tokio mutex guard while waiting for SQLite.
- Define per-command completion semantics so callers know whether they require
  durable commit, ordered enqueue, a snapshot read, or best-effort accounting.
- Surface overload and database unavailability as typed errors or controlled
  backpressure rather than unbounded task creation.

## Accepted Sharing-Path Follow-up (2026-11-06)

This owns approved follow-up 3 from the async-I/O review. It remains in the
post-beta backlog; the update does not promote it into a blocker for the
validated stock-import workflow. Main `e3372aba` and the import/root branch at
`43855fba` were reviewed before recording the following sites.

`shared_file_api.rs` still calls `index.upsert_file` synchronously after
offloaded ingest and calls `index.replace_shared_directory_roots` while holding
the async index guard. Ignore-rule list/add/remove/toggle paths also call the
synchronous metadata layer directly. The async guard does not make the SQLite
query, connection-mutex wait, busy wait, or durable commit asynchronous.

Route these live operations through the same bounded persistence owner as the
other runtime callers. Capture owned arguments, release global state/index
guards before queueing or awaiting storage, and publish the result according to
the command's required durable-commit semantics. Serialize logical root edits
or use configuration revisions so removing a guard does not introduce lost
updates. Do not replace a bounded owner with independent unbounded
`spawn_blocking` calls at each handler.

Keep SQLite synchronous inside that worker. The current `Arc<Mutex<Connection>>`
serializes users of each shared connection even with WAL: a five-second SQLite
busy timeout does not bound time waiting for the Rust connection mutex. Expose
both queue/connection wait and execution/commit latency. A read-lane or
connection-pool expansion needs measured justification and explicit snapshot
consistency; it is not a prerequisite to isolating blocking work.

Whole-file ingest, its local-content/AICH persistence, media extraction, root
membership updates, and paged catalog reads already use blocking boundaries in
important paths. Preserve and consolidate that good behavior. Exclusive offline
imports may keep bounded synchronous transactions because they serve no live
network/API workload.

RUST-REF-018 owns filesystem probes and root state lock scope. RUST-REF-008 owns
the compiled ignore-policy cache and eliminating per-file query/compile work;
its rule edits/invalidation use this persistence boundary. RUST-REF-019 owns
CPU-only bursts. These items must not introduce competing SQLite actors.

Additional representative sites:

- `crates/emulebb-core/src/shared_file_api.rs`: final index upsert, root
  replacement, ignore-rule operations, and current cached progress accessor.
- `crates/emulebb-index/src/lib.rs`: synchronous metadata adapter methods.
- `crates/emulebb-ed2k/src/ed2k_transfer/ingest.rs`: already-offloaded durable
  local-content/AICH writes to preserve.

Additional acceptance criteria:

- [ ] Live root edits, post-ingest index updates, and ignore-rule operations use
      the bounded storage boundary without global async guards across waits.
- [ ] Injected SQLite mutex contention, busy waits, and slow FULL commits leave
      unrelated REST requests, peer timers, and cached progress responsive.
- [ ] Queue saturation and shutdown preserve required commit guarantees and do
      not silently lose root edits or mark uncommitted content durable.

## Scope Constraints

- Preserve `synchronous=FULL` where the durability contract requires it; improve
  scheduling and transaction shape rather than weakening correctness.
- Keep password/secret handling and profile isolation unchanged; encryption
  feature work is not part of this scheduling change.
- Preserve stock eMule wire timing rules and packet behavior.
- Keep large-library batching performance work in `RUST-REF-008` and category
  deletion atomicity in `RUST-BUG-131`; share one persistence architecture.

## Acceptance Criteria

- [ ] No synchronous SQLite operation runs on a Tokio worker thread while
      holding global core, search, or peer-session async state.
- [ ] Persistence queues and blocking read concurrency are explicitly bounded
      and expose queue depth, wait time, execution time, and failure counters.
- [ ] Compound operations use one transaction and publish in-memory state only
      after the required commit succeeds.
- [ ] Upload accounting cannot delay payload service on a database busy timeout;
      its durability and coalescing policy is explicit and tested.
- [ ] Shutdown drains or rejects persistence commands according to documented
      command guarantees without silently losing required writes.
- [ ] Database contention tests prove REST, search, and peer timers remain
      responsive under the configured busy timeout and durable flush latency.

## Validation

- Tokio paused-time and multi-thread contention tests with injected slow SQLite
  operations and queue saturation.
- Crash/restart tests for commands that promise durable completion.
- Upload/search/API latency regressions under forced database contention.
- Current-schema rejection, metadata durability, REST, eD2K, Kad, and
  large-library validation lanes. Product code gains no migrations or reset path.

## Audit Release Placement

This remains parallel follow-up work and does not independently block Beta 3.
Its existing Client, Indexer, or Arr phase ownership remains unchanged;
non-gating Beta 3 placement does not bypass the separate whole-phase gates.

## Audit Reconciliation (2026-11-09)

The complete audit collection was reconciled against current source and
owning issues. The following are retained findings, corrected assumptions,
or required evidence for this owner; inspection does not replace runtime proof.

- `emulebb-rust-prompt_audit_findings_persistence.md` section 2.4 (existing): Do not add speculative pools or independent actors. Existing REF016 owns queue/wait/commit semantics and read-lane justification.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section scale-proof (existing): The aMule scaling wave is inspiration, not evidence of the same defect in Rust. Existing storage-domain, scan-I/O, async SQLite/filesystem/CPU and upload-performance items own the remaining work.
- `emulebb-rust-prompt_audit_findings_product_direction_amule_future_parity.md` section A3-kad-cache-load (existing): Kad cache hydration calls SQLite synchronously during core construction. Existing async SQLite persistence work is the nearest owner; the review did not measure startup blocking or establish a new release defect.

### Scoped Follow-up Acceptance

- [ ] Preserve FULL durability and measure connection/queue latency; keep one storage owner.
- [ ] Use bounded representative benchmarks and latency evidence.
- [ ] Reuse existing 100k fixture and cross-platform owners.
- [ ] Required Beta 3 Windows/Linux evidence is selected under #142; optional platforms remain parallel.
- [ ] Measure representative cache startup and executor responsiveness.
- [ ] Offload substantial work through the bounded persistence owner if required.
- [ ] Preserve startup consistency and the existing cache model.

## Retained Public Issue Context

The following pre-intake context is retained for provenance. The release
placement and scope stated in this item govern current execution.

**Reviewable branch spec:** https://github.com/emulebb/emulebb-tooling/blob/fix/stock-hash-share-tree/docs/products/emulebb-rust/active/items/RUST-REF-016.md

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

## Foundation specification

[PUBLIC-FOUNDATION](../../design/PUBLIC-FOUNDATION.md) owns the current contracts,
ordered delivery plan and required proof. It contains no checkpoint chronology
or superseded component-status claims. Keep implementation evidence and open
qualification concerns in owning items such as this one. The specification's
required-proof checklist and deferred-soak boundary were preserved verbatim
during consolidation; documentation checks passed in
`reports/settings-request-round-1/foundation-spec-consolidation-docs.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.

## Admission-time package resource observations (2026-11-23)

The existing sixteen-peer package smoke now samples daemon resource counters
before admission, after each accepted start and throughout completion polling.
Process sampling uses the same observation path. The result records admission
sample count separately and retains maxima across all phases, preventing an
early overlap peak from disappearing before the final start. Each independently
served payload is 4 MiB, paced at 64 KiB/s to make overlap observable.

All 100 package-smoke Python tests passed through Builder. The existing
multi-job regression now models overlap that ends before the final start,
requiring the early peak to be retained while still awaiting every delivery.
Runtime evidence for this extended fixture is pending. Its minimum overlap
assertion remains two charged owners; this change neither promises sixteen
simultaneous executions nor closes constrained active-transfer pressure proof.

## Canonical network-setting startup guidance (2026-11-23)

Rust `080441ec` reports P2P binding failures with `network.p2p.bindIp` and
`network.p2p.bindInterface`, matching the current settings catalog. Ambiguous
default routes direct the operator to the offline command
`emulebb-rust --profile <PATH> settings set network.p2p.bindInterface <NAME>`
while the daemon is stopped. Existing route/interface regression assertions
cover this guidance. Builder's `test rust-unit --package emulebb-daemon` passed
112 tests; its one ignored ownership child is an isolated subprocess fixture
invoked by the passing parent tests. Normal commit checks also passed.
This diagnostics-only cut does not replace the archive-specific capacity
evidence below.

## Qualified capacity campaigns and library reads (2026-11-23)

The existing shared-library I/O campaign now streams all ten library sorts in
both directions through their terminal pages, plus case-insensitive literal
substring probes covering case, punctuation, Unicode and a nonmatching wildcard
lookalike. It checks strict sort/hash advancement, exact baseline counts and
shared-row eligibility. Only current-page data and compact first/last summaries
are retained; the existing process sampler and total campaign deadline apply.
This unchanged baseline exercises equal-key upload-statistic cohorts, not live
upload counter changes. The global acceptance gate requires these reads.

All 137 focused Python tests passed through Builder's `test python` operation
with `test_rust_shared_library_io.py` and `test_rust_rest_contract.py`. Failure
cases include truncated traversal, duplicate/reversed rows, nonmatching results,
stalled continuation and invalid counters. The required push checks also passed
after the focused nine-test query repair: Harness `1297a1ca` uses a three-character
literal wildcard-lookalike probe and preserves descending order with default
sorting. An earlier campaign correctly returned HTTP 400 for the harness's
two-character probe; its failure remains preserved under
`reports/linux-containers/library/1799bf0c9415496d867ada16fbdea4e0/`.

Both complete constrained campaigns passed against Rust `f36ea7d7`, Harness
`1297a1ca`, Builder `54bfc7d` and Tooling `de594433`. Each used one CPU, no swap,
physical library contents and 100,000 retained jobs. Every sort/direction
traversal returned the exact baseline count with strict key/hash advancement.
All five substring probes matched their expected counts: 1,000, 2, 1, 0 and 1.
Watcher lifecycle, mutations, restart hydration, retained-job traversal and
graceful shutdown also passed. Both reported zero OOM, OOM-kill or group-kill
events. Evidence below is relative to `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

| Library files | Memory limit | Campaign seconds | Pages per sort/direction | Kernel peak bytes | Read-phase daemon RSS peak bytes |
| --- | --- | --- | --- | --- | --- |
| 50,000 | 512 MiB | 858.902 | 250 | 536,883,200 | 146,833,408 |
| 100,000 | 1 GiB | 1,627.230 | 500 | 1,073,770,496 | 349,229,056 |

The capacity reports are:

- `reports/linux-containers/library/5d2b1525dd2f4daf97d6ea9048209856/report.json`
  and its `campaign/rust-shared-library-io-20261122T224635Z-1.json` detail.
- `reports/linux-containers/library/3fd2500cbfbe4b41972b7d09f22b4e7a/report.json`
  and its `campaign/rust-shared-library-io-20261122T230254Z-1.json` detail.

The exact GNU archive SHA-256 is
`6a0de0ecf00524a4aeb63544c6844a2d1b91ec2d0a0648c17215b0a39360346e`.
Its full Linux gate passed Clippy, packet diagnostics, 3,542 workspace tests,
three VPN egress tests and release compilation. The WebUI build and non-root
package lifecycle/download smoke passed. Evidence is
`reports/rust-linux/gnu-amd64/ae887898f593407ebd3a222c1d62385c/` and
`reports/rust-linux/gnu-amd64/874ed5e8faa54b1b934c7bf9750a654d/package-smoke.json`.

These measurements qualify this archive and campaign workload. Kernel peaks
include controller memory and file cache and can slightly exceed nominal limits
through kernel accounting; they do not measure daemon RSS or spare capacity.
Read-phase RSS is sampled, not an overall daemon ceiling. Retained jobs remain
metadata-only: 99,000 completed, 900 stopped and 100 started/waiting. Live upload
statistics, active-transfer pressure, full adaptive/burst behavior and coupled
scan/download contention remain separate required proof. Package smoke verifies
sixteen distinct payload deliveries but only requires two overlapping charged
owners; it does not qualify sixteen simultaneous executions or maximum geometry.

## Canonical status and cached scan observations (2026-11-22)

Native status exposes lifecycle, statistics, server/Kad/network state and real
runtime diagnostics. Status, stats and diagnostics read `Core.library_scan()`;
they do not clone configured root collections to obtain progress. The WebUI
uses the lifecycle object and current scan/diagnostics DTOs directly.

`sharedFilesComplete` now means scan quiescence: no running pass, pending
follow-up or active hashing. The response regression covers discovery and
pending work with zero active hashers, preventing premature completion.
Root `scanRequired` flags separately report known incompleteness.

All 182 REST tests, 304 scoped Python route/schema/conformance tests, 94 WebUI
unit tests, 35 browser tests and the UI production build passed. Core code is
unchanged by this cut. Evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/status-canonical-scan-{rest,python}.log` and
`reports/settings-request-round-1/status-canonical-lifecycle-webui.log`.
All four local-client checks, including both native scenarios, also passed
against the verified Windows rebuild on Rust `f36ea7d7` and Harness `346c3db5`.
Wire evidence is
`reports/settings-request-round-1/status-canonical-native-qualified-runtime.log`,
the sibling JUnit XML and retained input/profile descriptors. This completes
this status cut. Capacity/read evidence appears above; active-memory
qualification remains open.

## Fractional or unknown Kad bootstrap progress (2026-11-22)

Kad bootstrap progress now follows the foundation rule: `0.0` while stopped,
`1.0` when ready and `null` while joining. A changing network has no measurable
completion fraction; REST preserves unknown progress rather than fabricating
a numeric value. Core's DTO uses an optional floating-point value; OpenAPI
declares a nullable number bounded by zero and one, and the WebUI type accepts
null. This changes runtime telemetry only.

All 753 Core tests, 182 REST tests, 306 scoped Python tests, 94 WebUI unit tests,
35 browser tests and the UI production build passed. REST covers ready, joining
and stopped serialization; schema tests exercise numeric boundaries and null.
The existing native fixture additionally requires null after its one-peer
partial bootstrap. All four fixture tests passed against the verified Windows
rebuild on Rust `0740f76b` and Harness `346c3db5`, including both native scenarios.
Evidence is `reports/settings-request-round-1/kad-progress-native-qualified-runtime.log`,
the sibling JUnit XML and retained scenario input/profile descriptors.
Evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/kad-progress-fraction-{core,rest,python,webui}.log`.

## Current native local-client fixture (2026-11-22)

The existing `test_emulebb_rust_local_client.py` now uses revisioned settings
saved/effective/application data, root resources and paginated library rows,
204 metadata edits, separate search headers/results and immutable server IDs.
It tests disabling separately from deletion and creates stopped jobs from an
explicit content source. Passive-index search preloading and unused fixture
manifest helpers were removed. Existing profile, publication, paging, local-peer
and runtime-stage helpers are reused.

All four tests passed together: two fast tests and both native scenarios.
The Windows Rust/WebUI build passed without warnings on Rust `7bf86227`;
evidence is `logs/builds/20261122T210356Z-build-clients/build-result.json` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. Final scenario evidence is
`reports/settings-request-round-1/native-client-qualified-runtime.log`, its
`native-client-qualified-junit.xml` sibling and retained scenario profiles.
The input descriptors attest the verified runtime and fixture SHA-256
`9be4ac1f9b29cff7d7a49aa1bc4ec504d1f766a6e32b0e744a78503527194a91`.

The declared local Kad peer uses plaintext transport and produces real routing
replies. With one contact and the daemon's current ten-contact readiness rule,
this qualifies partial bootstrap telemetry, not a fully populated Kad network.
Server-bind evidence exercises configured binding and REST lifecycle, not
observed socket-source-IP proof. No daemon transport/default was changed.

Runtime all-sort/substring, active-payload pressure and maximum geometry
qualification remain open.

## Current physical-library capacity tiers (2026-11-22)

Both existing full physical-library campaigns passed on Rust `7bf86227`,
Harness `44e9c8fa`, Builder `54bfc7d` and Tooling `2b0d9aa0`, using GNU archive
SHA-256 `853d916638b32cba251327be30d4a94c3e7d48e718c1ba29f2c713a92588d06f`.

| Physical library | Retained jobs | Enforced memory | Campaign seconds | Cgroup peak bytes |
| --- | ---: | ---: | ---: | ---: |
| 50,000 files / 5,242,880,000 bytes | 100,000 | 512 MiB | 938.140 | 536,920,064 |
| 100,000 files / 10,485,760,000 bytes | 100,000 | 1 GiB | 1,744.145 | 1,073,782,784 |

Both enforced one CPU and no swap, with zero OOM, OOM-kill or group-kill events.
All campaign acceptance checks passed: initial payload hashing, exact physical
fixtures, optional watcher lifecycle, populated-root update, mutations, retained
download counts/traversal, warm/final restarts and graceful shutdowns. Each
fixture includes 1,000 long-path files and 16 Unicode-path files. The measured
cgroup peak covers the campaign process tree and filesystem cache; it is not
daemon RSS or evidence of spare RAM. Native fixture volumes remain retained.

Evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- 512 MiB: `reports/linux-containers/library/2940043ebc4d47cba53f95b732ce6e9d/report.json`,
  with `campaign/rust-shared-library-io-20261122T200935Z-1.json` beneath that run.
- 1 GiB: `reports/linux-containers/library/609abb5e77d341ce9bc20d304609a76e/report.json`,
  with `campaign/rust-shared-library-io-20261122T202719Z-1.json` beneath that run.

The retained-job workload is explicitly metadata-only: 99,000 completed,
900 stopped and 100 started/waiting jobs. It does not prove combined active
payload pressure or maximum geometry. The campaign currently probes library
counts rather than every public library sort, late page and substring query;
that runtime read qualification remains required. The native local-client
integration fixture also still needs its settings/library/search calls updated
to the current contract. These are open acceptance work, not waived gates.

## Current GNU package checkpoint (2026-11-22)

Rust `7bf86227`, Harness `44e9c8fa`, Builder `54bfc7d` and Tooling `5e8e9b1f`
passed the full GNU amd64 package gate. This follows the server REST/catalog,
status/snapshot, discovery-import and runtime read changes above. The first
attempt stopped at Clippy; unused endpoint-token validators were removed and
a redundant test field initializer corrected before the passing rerun.

Passing evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/rust-linux/gnu-amd64/56f566942afe4601a7e45a5eae9fdb15/`:
  Clippy, packet diagnostics, release build, 3,542 workspace tests and three
  explicit VPN egress tests. The initial lint failure is retained separately in
  `reports/rust-linux/gnu-amd64/3f06f78f955740a7b6399d1c0af3fee4/clippy.log`.
- `reports/rust-linux/gnu-amd64/6fd830e14b034920976a58357dc4ab11/package-smoke.json`:
  non-root packaged lifecycle, CLI/profile behavior, WebUI/backend checks,
  verified partial stop/restart/delivery, and 16 independent real-payload peers.
  All 16 added outputs verified; 17 retained completed jobs including the initial
  transfer. One recorded start-admission retry among 17 requests; no hidden
  daemon retry. All auxiliary source processes exited successfully.
- GNU archive SHA-256:
  `853d916638b32cba251327be30d4a94c3e7d48e718c1ba29f2c713a92588d06f`.

The 112 resource samples peaked at eight charged active downloads, 15 waiting,
zero sampled preparation/burst and 8,152 resident manifest bytes. This is ordinary
payload qualification, not maximum geometry, sixteen simultaneous executions,
safe-update pressure or constrained-container memory proof. Both capacity tiers
must be rerun on this archive; older tier results are not transferred. The full
goal remains open, including maximum-geometry/adaptive/contention proof and the
remaining current-surface/platform/fixture acceptance work.

## Borrowed server feedback and case-insensitive retirement (2026-11-22)

Feedback endpoint resolution and discovered-server intake now use selected
endpoint reads rather than cloning the full rich catalog. Resolved-IP fallback
borrows cached rows and preserves deterministic endpoint ordering. Reverse-DNS
candidate collection borrows records and retains compact IPv4 candidates only;
it still includes configured endpoints, live dynamic-host facts, Kad contacts
and upload peers.

The new deletion regression found that the exact-string disabled set disagreed
with SQLite's ASCII case-insensitive server identity: deleting `seed.example`
could leave configured `Seed.Example` eligible for reconnect or delayed feedback.
The internal endpoint set now uses that same case-insensitive identity rule.
Server records retain their display spelling. The regression verifies that
deletion excludes the configured endpoint, delayed metadata cannot recreate it,
and explicit re-import receives a fresh ID and restores eligibility.

All 753 Core tests passed without compiler warnings; evidence under
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/server-feedback-borrowed-core.log`.
The preceding focused run passed 58 server tests. Daemon startup popularity
selection remains a full-list caller; the active connection directory and DNS
candidate storage still scale with server count. No constant-memory claim or
server-count limit is introduced. Current-artifact integrated qualification
remains required before full-goal acceptance.

## Server point reads and connection-plan merge (2026-11-22)

Single-endpoint Core reads now clone only their selected cached/configured row,
then apply controls, connection presentation and hostname facts. Connection-plan
publication compares its replacement with a borrowed watch value instead of
cloning the previous directory. Merging saved metadata uses an endpoint-to-index
map rather than repeatedly scanning the growing entry vector. Reported metadata
supersedes configured observations while preserving configured host spelling.
There is no server-count cap or omitted connection entry.

All 753 Core tests and 182 REST tests passed. The added regression covers
case-insensitive endpoint identity, cached reported-name precedence, configured
host spelling, operator controls and missing endpoints. Evidence under
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/server-plan-merge-{core,rest}.log`.
The active connection directory still retains entries proportional to its server
count; this is not constant-memory catalog selection. Feedback endpoint
resolution and hostname-candidate collection still have full-list callers and
remain concrete follow-on work before closing the catalog-memory audit.

## Dashboard server resources separated from summaries (2026-11-22)

Dashboard snapshots carry server connection status and the catalog count.
Catalog rows are browsed through `GET /servers`; the WebUI Network view owns
an independent cursor page and its metrics use the status count. Overview and
the connection toolbar use status facts directly. OpenAPI, WebUI types and
browser fixtures use this shape. REST has no remaining calls to the full-list
`Core.servers()` reader.

The retained-frame capacity regression now exercises real byte-short server
pages, retains cloned response frames until Native's shared allowance refuses
another request, then verifies recovery after final drop. Snapshot regressions
verify summary counts and separate paginated catalog access.

Validation passed: all 182 REST tests, 94 WebUI unit tests, 35 browser tests,
WebUI typecheck/production build and 303 Python route/schema/conformance tests.
Evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/snapshot-server-resource-{rest,webui,python}.log`.
Runtime connection-plan construction and final current-artifact qualification
remain open. This is a public-surface checkpoint, not full-goal acceptance.

## Bounded server connection status (2026-11-22)

REST status and server connection acknowledgements now use an admitted metadata
summary: a live-row count and at most one indexed endpoint lookup in one read
transaction. They no longer clone the configured/cached catalog. Core projects
only that current row and live connection details; disabled resources count,
deleted resources do not. Missing current endpoints remain null, and storage or
admission failures propagate through the normal HTTP error path. Existing status
fields and queued-connect acknowledgement semantics are preserved.

Validation passed: 374 Metadata tests, 140 focused Native server tests, all
752 Core tests and all 182 REST tests. The metadata regression injects an
unrelated oversized row to prove a summary does not materialize other records;
Core verifies retained projection charge and release without hydrating its
server cache. Evidence under `EMULEBB_WORKSPACE_OUTPUT_ROOT`:
`reports/settings-request-round-1/server-status-summary-{metadata,native,core,rest}.log`.
Snapshot's embedded catalog and runtime connection-plan construction remain
unfinished; this checkpoint does not claim those paths are bounded.

## Bounded diagnostic server prefix (2026-11-22)

Diagnostic operational snapshots now traverse admitted server-resource pages
instead of loading and sorting the entire catalog. The section keeps at most
512 records in immutable-ID order and at most 1 MiB of encoded item backing
(or the smaller requested bundle budget). Each read page is released before
the next; the existing single-capture permit owns the bounded diagnostic JSON.
Count-limit and byte-budget omissions are reported separately. This limits
diagnostic capture, not the stored catalog or its paginated REST access.

All 182 REST tests passed (178 unit and four integration), including a 513-server
regression covering multiple pages, the record limit and byte-budget omissions.
Evidence: `reports/settings-request-round-1/diagnostic-server-pages-rest.log`
under `EMULEBB_WORKSPACE_OUTPUT_ROOT`. Full-catalog reads in aggregate status,
snapshot and runtime planning remain separate unfinished work; this checkpoint
does not claim their memory use is bounded.

## Small, retained discovery imports (2026-11-22)

Direct read-only HTTP measurements on 2026-11-22 returned:

| Source | File bytes |
| --- | ---: |
| https://upd.emule-security.org/server.met | 3,390 |
| https://upd.emule-security.org/nodes.dat | 5,962 |
| https://emuling.gitlab.io/server.met | 1,692 |
| https://www.gruk.org/server.met | 1,964 |

The primary documents advertised 20 servers and 175 version-2 contacts. Their
SHA-256 digests were respectively
`8457474eb14dcc4b609ef30afae4c4101175085488b974acc241cd1872b31c3f`
and `93933d8b06e8b9f516ebe3fcae181a8e9ee4a00ee05bd5c5e6d6beba9fdd9cde`.
No downloaded source files were retained. These are observations of mutable
providers, not a guarantee of their future size.

The operator selected one 8 KiB ceiling for both file types and both automatic
and manual intake, retaining Core's 8 MiB pool. The existing ingress ticket now
serves both discovery types. Server imports reserve body/frame backing before
fetch, parse the bounded document on the SQL owner, commit accepted records in
one transaction and retain only IDs for subsequent bounded point publication.
The whole accepted document finishes after caller disconnect without retaining
the full Core. Shared per-record merging preserves identity, controls and health.

Unusable endpoints are skipped. Corrupt variable tag framing stops server intake
at its valid prefix; fixed-layout nodes intake retains complete declared records
and ignores an incomplete tail. Neither guesses new offsets. Zero usable records
return HTTP 400; a successful HTTP response waits for persistence/publication.
The REST regression reuses the existing Core loopback discovery fixture and
checks both zero-result routes through redirects plus visible partial intake.
The SQL regression proves an injected second-row failure rolls back the accepted
set and initialization. The quota-pressure proof still fills the actual shared
allowance; live-change tests no longer assume a tiny request saturates it.

Passes: **752 Core, 373 metadata, 181 REST and 112 daemon tests**, with the daemon
child-only ownership entry intentionally ignored and invoked by parent tests.
Also **four server.met and twelve nodes.dat parser tests pass**. Logs below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/discovery-small-import-core-full.log`
- `reports/settings-request-round-1/discovery-small-import-metadata.log`
- `reports/settings-request-round-1/discovery-small-import-rest.log`
- `reports/settings-request-round-1/discovery-small-import-daemon.log`
- `reports/settings-request-round-1/discovery-small-import-ed2k.log`
- `reports/settings-request-round-1/discovery-small-import-kad.log`

Whole-import ownership is implemented. Server aggregate construction and
current-source packaged/runtime qualification remain open. Passing endgame
fixtures in this run do not establish a causal repair for their earlier
intermittent admission failure.

## Canonical creation callers and reported bootstrap names (2026-11-22)

The remaining server creation helper, its DTO and validator are removed.
All Core, REST and daemon fixtures now use canonical explicit creation and
separate reported observations where required. Fresh-profile bootstrap leaves
an unreported name empty; endpoint display remains a separate presentation
concern. Its existing seed test asserts the empty observation.

The snapshot frame-retention proof now builds a large response from sixteen
valid 65,535-byte reported names. No single fixture record bypasses the canonical
row allowance. The reader-fault test injects an oversized stored row directly
through its existing SQLite test seam and verifies bounded read failure and
released backing. It does not add a product mutation bypass.

Validation passes: **750 Core tests, 180 REST tests and 112 daemon tests**.
The daemon's child-only profile-ownership entry remains intentionally ignored;
its parent ownership tests pass. The final full Core run passes after the
reader fixture repair. Logs below `EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/server-create-removal-core-final.log`
- `reports/settings-request-round-1/server-create-removal-rest.log`
- `reports/settings-request-round-1/server-create-removal-daemon.log`

Creation-helper cleanup is complete. Whole-import bounded admission/ownership,
server aggregate construction and current-source runtime qualification remain
open. These passing endgame fixtures still do not establish a causal repair
for the earlier intermittent admission failure.

## Retained single-record server imports (2026-11-22)

Manual server.met imports now merge each observed endpoint/name through the
canonical persistence owner. SQL preserves the live ID, operator controls and
health columns; an absent name tag preserves the known name. A previously
deleted endpoint receives a fresh ID and initial controls. The bounded row is
validated inside the write transaction before commit, so a failed projection
rolls back both the import and discovery initialization. Cache publication
changes only the reported name, preserving current health and controls.

The new disconnect regression holds a committed record import before cache
publication, disconnects its caller and changes cached health. Publication
finishes without retaining the full Core, preserves the disabled/high/static
controls and newer health, and releases its reservation. Malformed payload and
persistence errors propagate rather than becoming a zero-import result; REST
uses the shared persistence error mapping.

**372 metadata tests, 750 Core tests and 180 REST tests pass**, including both
nonterminal Windows endgame fixtures in this Core run. This passing run is not
a causal repair for their earlier intermittent admission failure. Logs below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/server-import-metadata.log`
- `reports/settings-request-round-1/server-import-core.log`
- `reports/settings-request-round-1/server-import-rest.log`

This proves retained ownership for one admitted record, not whole-payload
ownership. Payload fetching/parsing still needs bounded ingress and full import
ownership. The unused-by-production creation helper still has test callers to
convert before removal; startup bootstrap and aggregate server construction
retain their separate remaining work.

## Canonical server controls and restart proof (2026-11-22)

Endpoint-addressed edit and disable-as-delete methods are removed. Internal
callers and tests use retained ID-addressed update/delete operations. The
runtime control overlay uses `MetadataServerUpdate` directly, with no name
field or separate public edit DTO. Tests disable explicitly and delete
explicitly. The live-plan test persists its server resource before mutating it;
configured protocol endpoints alone do not manufacture a saved resource ID.

The profile integration test creates through the canonical owner and verifies
identity, edited controls and disabling across restart, then deletion across a
further reopen. **93 focused server tests and the full Core suite of 749 tests
pass**, including this profile test and the Windows endgame fixtures. Logs below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/server-canonical-controls-core.log`
- `reports/settings-request-round-1/server-canonical-controls-core-full.log`

This passing endgame run does not establish a causal repair for the previously
captured intermittent admission failure. Explicit creation/import separation
and aggregate server construction remain open; operator edits now have only
the canonical retained mutation path.

## Server resource REST/OpenAPI/WebUI cutover (2026-11-22)

Native server list/detail reads now use admitted persisted-ID reads and a
separately admitted presentation projection. They do not build the complete
configured/runtime server list. Pages default to 100, cap at 200, may end early
on byte allowance and expose optional exact totals. Ascending-ID cursors remain
usable after anchor deletion. Resource responses include immutable decimal IDs;
per-server connect resolves that ID rather than accepting a protocol endpoint.

Creation uses the retained canonical owner, returns 201 with `data.id` and
`Location`, and reports 409 `SERVER_EXISTS` without changing an existing live
endpoint. PATCH saves selected operator controls and DELETE retires the resource;
both return 204. Names are observation-only. The WebUI fetches one cursor page,
selects/actions by ID and provides no name input. Its filter is explicitly local
to the displayed page. The native Python conformance owner supplies server-ID
fixtures; the separate MFC contract and smoke fixtures were left untouched.

Checks pass: **176 REST unit tests plus four integration tests; 179 native
Python route/conformance tests; 93 WebUI unit tests and 35 browser tests**, with
TypeScript checking and the production UI build. Logs below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/server-resource-rest.log`
- `reports/settings-request-round-1/server-resource-python.log`
- `reports/settings-request-round-1/server-resource-webui.log`

These checks do not replace current-source packaged/runtime qualification or
the full Core gate. Internal endpoint-based creation/edit/import helpers and
manual-name overlays still need removal/replacement; snapshot, status,
diagnostics and connection-plan aggregate construction remain separate bounded
ownership work. The intermittent Windows endgame admission failure remains open.

## Reported server names: canonical edits (2026-11-22)

The subsequent bounded endgame investigation added error-chain context at
upload serving-entry resolution, reader admission and verified-fragment reads,
with nested job-resolution/local-serving-view context. The captured busy error
can otherwise originate from several admitted read/publication paths. Reads
explicitly prohibit waiting for capacity while holding job/content guards;
do not add an indiscriminate retry loop to these paths. The four focused
endgame fixtures pass with these diagnostics in
`reports/settings-request-round-1/endgame-upload-admission-context.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. No capacity, retry or disconnect behavior was
changed, and the intermittent full-run failure remains unresolved.

Explicit creation now uses `MetadataServerCreate`: address, port, priority,
static status and enabled status only. Rich network/import records remain
separate. The DB returns the committed initial snapshot, avoiding a second
post-commit read for retained cache publication. Core checks projected read size
and reserves command memory before cloning the creation input. Creation starts
without reported names or telemetry; a subsequent import supplies observations
while preserving the ID. Duplicate, rollback, disconnect, feedback ordering and
oversize proofs remain covered. **367 metadata unit tests, three ownership
tests and seven focused Core server tests pass**. Logs:
`reports/settings-request-round-1/server-create-input-metadata.log` and
`reports/settings-request-round-1/server-create-input-core.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. This focused pass does not supersede the full
Core endgame failure recorded below.

Canonical ID-addressed metadata/Core edits accept only priority, static status
and enabled status. Reported names are preserved by the selective SQL write and
cache publication. The feedback/publication regression now supplies a network
name while an operator control edit is held at publication; both the observed
name and edited priority survive. REST/OpenAPI/WebUI creation and editing still
require their coordinated cutover; this prerequisite does not claim that cutover.

Validation: **366 metadata unit tests and three profile-ownership tests pass**.
All **seven canonical Core server tests pass** within the broader Core run.
That run finishes **714 passed, one failed**: the existing Windows nonterminal
endgame fixture reports an early seed EOF at 1,290,240 of 9,400,064 prefix bytes.
Importantly, this capture includes a preceding seeder listener error:
`local mutation capacity is busy`. Investigate the bounded mutation-admission
path before another unchanged endgame rerun; this is evidence, not a proven fix.
The retained log is
`reports/settings-request-round-1/server-reported-name-core.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. Full Core acceptance remains blocked.

## Ordinary parallel payload proof (2026-11-22)

Harness `92469fe1` extends the existing native package smoke with sixteen distinct
1 MiB payloads, sixteen independent Rust seeders and the existing receiver. Peer
leases remain genuine: one shared source is not presented as sixteen independent
uploaders. Existing profile, launch, publication, delivery and process-sampling
helpers own the fixture. Auxiliary processes drain through `ExitStack`, including
startup/shutdown failure cases. The original verified-part restart proof remains.

The GNU/amd64 runtime report passes against Rust `264b9fe9`, Builder `54bfc7d`
and Tooling `332df28a`:
`reports/rust-linux/gnu-amd64/29c8907ac3b44894a756f47c0c4a610f/package-smoke.json`
below `EMULEBB_WORKSPACE_OUTPUT_ROOT`. It verifies all **16 delivered byte hashes
and library locations**, retains **17 completed jobs** including the original
restart case, and records **112 resource samples**. Sampled maxima are **8 charged
active owners**, target 16, zero sampled preparations and **8,152 resident-cache
bytes**. Receiver sampled peak working set is **53,829,632 bytes**. All fifteen
auxiliary source exits are zero; the original peers also shut down gracefully.

Start controls use one ID per request. Under the operator-approved test-client
policy, 17 requests include **one recorded 503 `DOWNLOAD_UNAVAILABLE` retry after
0.25 seconds**. Each job has at most five attempts with recorded backoffs; other
errors and execution/storage failures do not enter that path. The existing waiter
requires `None` until completion, covered by a regression that fails on premature
one-sample completion. **100 focused Python tests pass.**

This proves ordinary real-payload operation, not sixteen simultaneous executions,
maximum manifest geometry, a total RAM limit or combined-scale active-payload
qualification. Those proofs remain open. Its archive SHA-256 is
`b766339a268a79f2d5ad2f7ddc18e12f751a55c96a35fa9d01de325588c19754`;
capacity evidence below remains pinned to its separately recorded archive.

The server-name decision is settled: retain only reported names and expose no
name editing. Its DB/service, REST/OpenAPI, WebUI and caller cutover remains to
be implemented with the stable resource-ID work.

## Focused Windows endgame diagnostics (2026-11-22)

Builder `54bfc7d` extends the existing `test rust-unit` command with diagnostic
`--filter` and `--nocapture` options. Default full-suite selection is unchanged;
filters remain literal test-name substrings, with the existing lock, source-cache
checks, owned scratch and runtime-artifact cleanup. Seven scoped Builder tests
pass, including diagnostic/default success and failure cleanup.

The supported filtered Windows run passes all four endgame fixtures against
Rust `264b9fe9`; its evidence is
`reports/settings-request-round-1/endgame-focused-windows.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. Connection-abort messages also occur in this
successful run and do not establish the intermittent fault's cause. No transfer
behavior, timeout or assertion is changed; the fault remains open. Further
investigation should distinguish fixture interference or a specific close cause
rather than repeating unchanged runs until green. Filtered evidence does not
replace required full-suite validation.

Inspection of the retained failing process finds four distinct endgame fixture
directories, ruling out a directory collision in that run. Metadata fixtures use
separate in-memory SQLite connections. A broader supported Windows run of
`tests::download_` also passes **61 tests** with visible Native tracing; evidence
is `reports/settings-request-round-1/endgame-download-family-windows.log` below
the output root. Neither focused concurrency scenario reproduces the failure.
No directory allocator, timeout, transfer policy or retry behavior is changed on
this evidence. Preserve the open fault and stop unchanged reruns; active-payload
memory qualification is a separate outstanding acceptance task.

## Current GNU and capacity proof (2026-11-22)

Rust `264b9fe9`, Harness `cce2809f`, Tooling `cc33be1c` and Builder `98fa3d2`
pass the current schema-117 GNU/amd64 package gate: Clippy, packet-diagnostics
compilation, release build, **3,529 workspace tests plus 3 VPN-egress tests**, and
non-root package smoke validation. The only source repair is a borrowed-slice
expectation in a metadata test, preserving its assertion without cloning. Its
scoped Windows gate passes **369 metadata tests**.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/rust-linux/gnu-amd64/b5b4c405d9224f1ebca48c2086959f56/`, with runtime smoke
in `reports/rust-linux/gnu-amd64/0be5de6d92e542bf8265a1f984dda248/package-smoke.json`.
The archive SHA-256 is
`f696b41bae72e09168d8030eb774cb6396589e410c22d01b9ea5f3e261f10e79`.
The earlier Clippy failure remains recorded under
`reports/rust-linux/gnu-amd64/009efefb708c4c9a8970df89a589ed1e/`.

That archive passes the full **50,000 physical files plus 100,000 retained jobs
at 512 MiB, 1 CPU and no swap** campaign, including initial payload hashing,
watcher lifecycle, rescans, mutations and restarts. Its report is
`reports/linux-containers/library/35a6d8e76fd242bcbd3c0e3df98a92bc/report.json`.
Kernel checks prove unchanged limits, the same process-tree scope and no OOM
events. The recorded cgroup peak is **536,899,584 bytes**; this includes the
campaign process tree and does not establish spare daemon RAM. The container is
removed and its owned native volume is retained for evidence.

The same archive also passes **100,000 physical files plus 100,000 retained jobs
at 1 GiB, 1 CPU and no swap**, with Tooling `1e101261` and the same Rust, Harness
and Builder revisions. Its report is
`reports/linux-containers/library/f066678e7de64723a9e68f724e6af798/report.json`.
All global acceptance checks pass, including watcher policy, populated-root
updates, long paths, mutations, warm/final restarts, retained-job counts and
graceful shutdowns. Kernel checks show unchanged limits, the same process-tree
scope and no OOM events. The recorded cgroup peak is **1,073,762,304 bytes**;
it does not establish spare daemon RAM. The container is removed and its native
volume is retained.

Retained download history is explicitly **metadata-only** in both tiers. These
campaigns do not qualify the active-payload worst case or endurance.
The intermittent Windows endgame concern and server public cutover remain open;
the Linux nonterminal endgame and Unix filesystem-grouping tests pass.

## Current Windows runtime and REST proof (2026-11-22)

Rust `9196c5a3`, Harness `cce2809f` and Builder `98fa3d2` build and stage the
current schema-117 Windows daemon and WebUI with **zero warnings**. The build
receipt is `logs/builds/20261122T131530Z-build-clients/build-result.json` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.

The first current-binary REST gate exposed missing generic probe definitions for
the canonical library point routes. Harness now supplies a valid upload-priority
PATCH body and expects 404 for its intentionally absent detail/PATCH hash.
Dedicated fixture edits continue to require 204 and verify retained values.
**77 focused Python tests pass.**

The refreshed live report,
`reports/rust-rest-openapi-ci/20261122T132203Z/report.json`, passes with graceful
teardown: **114 declared operations, 89 safe operations exercised, 38 successful
responses and 51 expected errors**, with no failed routes. The 25 operations
excluded from generic safe sampling are not all thereby qualified. Dedicated
settings/lease, category/library policy and tags, friend and Kad persistence
phases pass. Metadata-only traversal covers **100,000 retained jobs** (99,000
completed, 100 queued, 900 stopped), all/completed/unfinished pages and restart
counts. This establishes neither physical-library capacity nor a memory limit.
Current constrained-container and platform qualification remains pending.

A further visible-output Core run passes 750 tests and preserves a successful
comparison trace in `reports/settings-request-round-1/endgame-visible-core.log`.
It does not reproduce or resolve the intermittent endgame failure described below.

## Endgame close diagnostics (2026-11-22)

Rust `9196c5a3` retains exact prefix-forwarding offsets and distinguishes
receiver EOF/reset from receiver-read and upstream-write failures in the existing
loopback fixture. Native debug events identify receiver EOF, read errors,
response deadlines and scheduling cancellation. Upload close events preserve
policy/cancellation reasons; listener errors include their complete error chain.
A test-only subscriber captures the relevant Native targets in libtest output.
Transfer policy, timeouts, geometry and acceptance assertions are unchanged.

The first diagnostic gate reproduced the intermittent failure in
`nonterminal_verified_part_drains_redundant_endgame_peer`: seed EOF followed
**1,290,240 of 9,400,064 prefix bytes**, while the receiver-forwarding task was
still pending at that observation. This does not establish which side initiated
closure. It disproves treating the previous periodic progress marker as a fixed
4 MiB close boundary. The failure remains an open qualification concern; neither
additional logging nor a later passing run establishes a repair.

After adding test log capture, the scoped gates pass **750 Windows Core and
1,535 Native tests**, without compiler warnings. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/endgame-close-core.log` (reproduction),
`endgame-close-trace-core.log` and `endgame-close-trace-native.log` in that same
directory. Further diagnosis must use the captured close reason before changing
transfer behavior. Full current-platform/resource qualification remains pending.

## Scan calendar contract (2026-11-22)

Rust `af8f2b37` exposes scan/pass and active-file `startedAt`/`updatedAt`, plus
recent-file `finishedAt`, as Unix seconds. Monotonic clocks continue to own rate,
duration and completion ordering; `durationMs` retains its elapsed-time unit.
OpenAPI and embedded WebUI types use the same field names and units. Coordinator
state now supplies the running/pending pair under one lock, preventing mixed
observations from reporting false idle during a worker/pending transition.

Harness `1a864dde` removes calendar-change completion fences from the existing
real-media and WebUI proofs. They observe accepted actions, coherent quiescence
and catalog facts. Structured completion evidence continues to use existing log
offsets; calendar values may stay equal or move backward. No completion token,
revision comparison, additional worker or retry loop is added.

Scoped gates pass **750 Windows Core, 179 REST, 499 Python, 93 WebUI unit and
35 browser tests**, without Rust compiler warnings. Coverage includes calendar
serialization against a seconds clock, preserved monotonic precision, same-second
completion, completion before the first poll and backward-moving calendar facts.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/scan-calendar-core.log`,
`scan-calendar-rest.log`, `scan-calendar-python.log` and `scan-calendar-webui.log`
in that same directory. Schema 117 is unchanged. Current Linux and resource
evidence is recorded above at its actual scope. Server public-resource
cutover and remaining active-payload qualification remain open.

## Scan follow-up progress and device grouping (2026-11-22)

Rust `5c827531` preserves the active scanning/planning/hashing phase when more
scan requests coalesce into the existing pending follow-up. Its counters and
calendar values remain attached to the current pass; idle requests still show
queued work. There is no new scan queue, completion token or scheduling policy.

Unix scheduling groups now reuse the existing filesystem device identity
helper, including nearest-existing-ancestor handling. Resolution remains once
per configured root. Windows physical-disk resolution is unchanged. A Unix
filesystem device is a scheduling proxy and does not identify shared hardware
behind partitions or virtual volumes.

**749 Core tests pass on Windows**, without compiler warnings, including a
regression exercising repeated follow-up requests during all three active
phases and final draining. Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/scan-followup-core.log`. The Unix-only
regression was **not executed by the Windows gate**; its GNU result is recorded
above. Remaining server contract integration,
aggregate ownership and current resource qualification
remain open. Server names are reported observations, with no editing surface.

## Retained server resource mutations (2026-11-22)

Rust `72558714` routes canonical server create/edit/delete through the existing
profile persistence actor and SQL worker. The command keeps its input and
publication allowance until SQL, derived cache and connection-plan publication
finish, including after caller cancellation. Its publication context retains
only shared server/network handles, not the full Core. Creation preserves typed
endpoint conflicts; selected-field edits preserve current cached health data.
Projected record backing is checked before commit so an edit cannot create a
resource the bounded point reader cannot return.

A shared server mutation fence covers that SQL/cache window and existing
feedback/discovery writers. It prevents stale feedback snapshots from overtaking
a committed edit. Connection initialization occurs after the existing add path
releases the fence. Delayed feedback also cannot recreate a deleted resource
from startup connection configuration. This protects current resource lifecycle;
it adds no profile migration, retired-input path, worker or retry loop.

**748 Core and 179 REST tests pass**, without compiler warnings. Eight new
regressions cover all three canceled mutation callers, charge release, no
retained Core, selected-field health preservation, SQL rollback, typed conflicts,
oversized-input/record refusal, feedback ordering, and late feedback after
deletion. Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/server-owner-core-fenced.log` and
`server-owner-rest.log` in the same directory. The first run found a private
test-fixture accessor, corrected using the established shared in-memory database
fixture. The intermediate owner run passed before adding the shared fence.

This is a service checkpoint. REST/OpenAPI/WebUI and native callers still need
the coordinated ID/pagination/deletion cut, including retirement of endpoint-based
entrypoints. Aggregate server list/connection-plan construction ownership and
current runtime/resource qualification remain open. Existing feedback SQL still
uses its current persistence path under the fence; do not claim every server
writer has moved to the actor. The settled name contract retains only network/
import observations; the coordinated cut must remove name mutation inputs.

## Atomic server resource storage prerequisite (2026-11-22)

Rust `07ff665a` makes server upsert return the stable ID from the SQL write,
only after its transaction commits. ID-addressed edits update only selected
operator fields, preserving endpoint identity and network observations. Deletion
atomically disables and retires the resource; repeated deletion and edits of a
missing ID do not create rows. Importing the endpoint again allocates a new ID.
The fresh schema remains **117**; no schema shape or public route changes here.

Scoped gates pass **366 metadata, 740 Core and 112 daemon tests**, without
compiler warnings. One daemon subprocess fixture remains intentionally ignored
by the unit entrypoint, pending its registered full-matrix execution. Coverage
includes update/delete failure rollback, field preservation, case-insensitive
identity receipts, disabled-resource retention and re-import identity.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/server-mutations-metadata.log`,
`server-mutations-emulebb-core.log` and `server-mutations-emulebb-daemon.log`
in that same directory.

Rust `9e762739` adds explicit creation separately from import merging. A SQLite
immediate transaction spans the live-endpoint uniqueness check, insertion and
discovery initialization; conflict returns the typed `ServerEndpointConflict`
without updating or enabling the existing server. **369 metadata tests pass**
without compiler warnings, including simultaneous creators, preservation of a
disabled resource, fresh identity after deletion, and initialization-failure
rollback. Evidence is
`reports/settings-request-round-1/server-create-metadata-second.log` below the
same output root. The first attempt found a test closure-lifetime error, fixed
before the passing run. Schema 117 and the HTTP surface remain unchanged.

Next, switch REST/OpenAPI/WebUI and native callers together. The operator settled
duplicate explicit `POST /servers`: return 409 without changing the existing
resource. Imports retain their separate merge semantics and stable live IDs.
This decision is saved in the authoritative specification; the public creation
path still needs integration and validation. Reuse the existing persistence
actor and SQL worker, retaining only the server publication context rather than
the full Core. The network configuration is already held by `Arc`, and external
reachability provides a cheap cloned reader.

## Native library comparison reads (2026-11-22)

Harness `0f01dd7e` updates the existing soak-control comparison utilities to
stream canonical shared hash pages and separate cached locations. Hash-only
comparison does not load copies. Path/root comparisons include every present
copy, fingerprint paths immediately, and keep content totals distinct from copy
totals. They do not recreate physical REST records. MFC collection reads retain
their own offset contract. The shared library iterator accepts page sizes from
1 through 200; the comparison command defaults to 200 without clamping inputs.
Sharing policy remains independent of upload queue priority; offline database
priority manipulation is outside the utility's command surface.

**128 scoped Python checks pass**, including two hashes with multiple copies,
location-page continuation, excluded non-present copies, root grouping,
hash-only reads, MFC offset reads and current page bounds. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-soak-control-second-python.log`.
This is caller validation, not a running persisted-profile soak or current
resource qualification. The native local-client fixture conversion remains open.

## Canonical library resources checkpoint (2026-11-22)

Rust `f1b38386` and Harness `1f0203de` switch REST/OpenAPI and the embedded WebUI to
thin `/library/files` pages, admitted hash detail and separate cached locations.
Metadata PATCH returns 204 after retained ownership completes; it does not
perform a post-commit read. Publication visibility is on demand. The snapshot
has no library array. One public `uploadPriority` mode round-trips automatic
selection; sharing eligibility remains independent. Fresh schema is **117**.
Diagnostic bundle **v8** contains a bounded `libraryFiles` page rather than a
physical shared-file projection; this does not close aggregate ownership work.

Scoped current-source evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT`:

- `reports/settings-request-round-1/library-api-cut-rest-third.log`:
  **175 REST unit and 4 real-file integration tests pass**, without compiler
  warnings. Fixtures compare native paths by filesystem identity and settle
  setup scanning before testing idle reads; capacity refusal remains supported.
- `reports/settings-request-round-1/library-api-cut-webui-order.log`:
  type checking/build, **93 unit and 35 browser tests pass** with the final
  `order` query parameter and one public upload-priority mode.
- `reports/settings-request-round-1/library-api-cut-scale-python.log`:
  **412 Python checks pass**, including the existing scale caller, bounded
  traversal and selected OpenAPI/response checks. Scale totals come from page
  metadata; sampled physical paths come from separate cached location pages.
- `reports/settings-request-round-1/library-api-cut-consumer-python.log`:
  **106 Python checks pass** for the consumer/WebUI proof helpers, including a
  thin-row/detail/location restart regression. This is not a live consumer run.
- `reports/settings-request-round-1/library-api-cut-docs.log`: documentation
  publication checks pass after the specification update.
- `reports/settings-request-round-1/library-api-cut-emulebb-metadata.log`,
  `library-api-cut-emulebb-ed2k.log` and `library-api-cut-emulebb-core.log` in the
  same directory: **363 metadata, 1,535 Native and 740 Core tests pass**, without
  compiler warnings. Core includes the automatic-priority round-trip and
  endgame/preparation fixtures. Those fixtures passing at this revision does
  not establish the cause or repair of their earlier intermittent failures.
- `reports/settings-request-round-1/library-api-cut-upload-python.log`:
  **23 upload-proof helper checks pass** using canonical hash detail.
- `reports/settings-request-round-1/library-api-cut-package-python.log`:
  **79 package-smoke helper checks pass**. Completed delivery requires matching
  job identity, canonical detail and a present cached location for the delivered
  path before the existing on-disk size/SHA-256 proof.
- `reports/settings-request-round-1/library-api-cut-cross-client-second-python.log`:
  **103 cross-client/reask checks pass** after the Rust callers use bounded
  library pages and selected detail. Reask withdrawal checks point-detail
  presence/sharing eligibility, so retained copyless knowledge is not mistaken
  for shared content. MFC continues to use its own native contract.
- `reports/settings-request-round-1/library-api-cut-android-peer-python.log`:
  **82 Android peer helper checks pass**, preserving collision, output-byte,
  restart and cleanup assertions through separate cached-location reads.
- `reports/settings-request-round-1/library-api-cut-android-sharing-second-python.log`:
  **145 public-sharing helper checks pass**. Approved-copy validation joins thin
  hash rows to paginated cached locations, checks every observed present copy
  against operator scope, and reports whether all approved instances are
  indexed. It keeps distinct-content ambiguity visible and tests 221 hash rows
  across pages. These Python checks launch no public-network campaign or APK.
- `reports/settings-request-round-1/library-api-cut-daemon.log`:
  **112 daemon/import tests pass**, without compiler warnings; one subprocess
  fixture remains intentionally ignored by this unit entrypoint and needs its
  registered full-matrix execution before final qualification.

Remaining before library integration closes: convert the other native harness
callers, run applicable current-binary proofs, and reconcile the current
caller/docs inventories. The earlier schema-114 scale results
are not current-source qualification. Server resources, scan progress/calendar,
aggregate ownership and intermittent endgame/preparation failures remain open.
No PR or merge is authorized.

The remaining caller inventory includes native local-client tests;
MFC-only callers are not a Rust removal target.
Do not add a common projection that reconstructs physical flat records from
the canonical hash/detail/location resources.

## Bounded library hash-detail prerequisite (2026-11-22)

Rust `c5877019` adds metadata/Native/Core point-detail reads for client hashes,
including copyless content. A shared point-query helper reads summary facts and
explicit local priority/comment/rating in one transaction. It checks borrowed
text lengths before decoding, retains only a fixed-size AICH root, and does not
read jobs, path lists or hashsets. Passive-only evidence remains outside library
membership. Thin collection rows do not acquire detail fields.

The existing admitted Native read owner supplies captured upload counters and
retains the result. Core checks profile coherence before and after the read,
then separately admits detail conversion, link construction and JSON backing.
Its 2 MiB detail allowance covers maximum-length name/comment and escaped link
text within the existing shared transient budget; no new cache, worker or user
setting is introduced. Unknown accepted size yields a null link. Accepted size
uses the existing delimiter-safe eD2K/AICH link formatter.

Scoped gates passed **363 metadata, 1,537 Native and 740 Core tests**, without
compiler warnings. Coverage includes copyless explicit fields/current counters,
no payload admission, conversion/serialization charge release, absent hashes,
coherence faults, accepted-size links, oversized-comment refusal, maximum-length
name/comment and fixed AICH identity. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-hash-detail-metadata.log`,
`library-hash-detail-native.log` and `library-hash-detail-core.log` in that same
directory. Normal Rust commit checks passed.

The Core gate is green at this revision, including endgame and preparation
fixtures. Their earlier intermittent failures remain unresolved qualification
concerns; this pass does not explain or repair them. Fresh schema stays **116**.
This is the bounded service prerequisite, not the public REST/OpenAPI/WebUI
cutover. Next switch those callers together, preserve on-demand publication
visibility and remove the shared-file collection/detail/scalar read surface.
Server resources, scan progress/calendar work, aggregate construction ownership
and final platform/pressure gates also remain open. No PR is authorized.

## Retained Core metadata edit publication (2026-11-22)

Rust `075ee6fb` extends the existing profile persistence owner across hash
metadata edits and their Kad/eD2K scheduling effects. Its admitted command
supports copyless client hashes, clones bounded text only after admission and
keeps ownership after caller cancellation. The SQL transaction computes scalar
change receipts and deletes the persisted Kad notes clock atomically with an
actual comment/rating change. Unknown hashes remain absent; identical notes and
ordinary priority-only edits do not reset the notes clock. Native retains its
existing SQL/cache/catalog publication ownership.

Core then dirties the live notes schedule and queues affected server offers.
The established catalog publisher now has a small reusable retained context;
its worker, debounce and rate limits are preserved, without capturing the whole
Core/persistence owner in the edit command. The existing HTTP edit path uses this
service. The canonical library route/DTO/OpenAPI/WebUI cutover remains the next
delivery slice; no transitional routes or compatibility handling were added.
Fresh schema remains **116**.

Passed gates: **362 metadata, 1,537 Native and 179 REST tests**, with no compiler
warnings. The new Core regression cancels the caller after Native publication
but before Core scheduling, then proves the ordered owner finishes both network
effects and releases capacity. Existing rating/publish-status reoffer tests also
pass. Metadata covers unchanged-note/priority behavior and rolls back the entire
edit when a synthetic persisted-clock deletion fails. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/retained-library-edit-metadata-final.log`,
`retained-library-edit-native.log` and `retained-library-edit-rest.log` in that
same directory. The first metadata compile found a missing timestamp argument
in the new test setup; that was corrected before the passing gate.

**The full Core gate is not green:** `retained-library-edit-core-final.log`
records **703 passed, one failed**, the previously observed
`nonterminal_original_copy_drains_replacement_endgame_peer` prefix setup. The
first run (`retained-library-edit-core.log`) also exposed two reoffer regressions
in the initial demand-signal-only implementation; the retained publisher context
repairs those. That first run separately timed out waiting for the existing
download-preparation fixture's completed shares. Its cause remains unproven;
passing on the subsequent relevant-code run is not a repair of that timeout.

A bounded read-only endgame investigation establishes that the periodic
4,229,120-byte progress message is not the closing offset. Receiver EOF/reset
drops the relay's upstream writer, so the later seed EOF alone cannot identify
which side closed first. The incomplete/no-terminal-error downloader report
also represents both peer closure and its own receive timeout. Existing upload
byte-cap, replacement-only rotation and resident-cache code do not establish a
4 MiB cutoff. Next diagnostic proof must retain the exact forwarded count, the
receiver's timeout/closure reason and the seed handler's full terminal result.
Do not change geometry, timeout or acceptance without that evidence. This
failure remains a final qualification blocker, not a claimed green rerun.

Normal Rust commit checks passed. Canonical library/server cuts, scan progress
and calendar work, aggregate construction ownership and final platform/pressure
qualification remain open. Earlier binary/package/resource receipts retain
their recorded source revisions. No PR or merge is authorized before review.

## Remote Kad notes are independent evidence (2026-11-22)

Rust `7aec1fba` removes passive Kad note autofill from local comment/rating. The
existing bounded observation owner now retains remote note text, reported rating
and claimed publisher ID as corpus observations. It does not hydrate a selected
manifest to store a note, create accepted library content or attach observations
to a search session. Unknown name, size and responder endpoint remain null;
the query's size filter is not treated as reported content size. Exact repeated
notes increase occurrence counts, while different publishers/comments remain
distinct semantic observations.

Fresh schema **116** extends the existing observation table/model with nullable
comment and publisher identity. Ingestion accounting and borrowed-row byte checks
include note text before cloning. Corpus and session readers retain bounded
pages. The existing REST observation projection/OpenAPI and on-demand WebUI
metadata details expose `comment` and `publisherId`; the publisher is a claimed
32-character lowercase hex identity, separate from the responder endpoint.
Passive observations still have no implicit search-session membership. This is
no new indexer search mode, notes endpoint, worker or settings surface.

Scoped gates passed **361 metadata, 739 Core, 179 REST, 93 WebUI unit, 35 browser
and 177 Python tests**, with no final Rust compiler warnings. Core covers empty
and explicitly edited local fields while retaining remote notes, duplicate
occurrences, independent publishers and an unrelated non-library hash. Metadata
covers roundtrip/deduplication and oversized-note rollback. REST/SPA/Python cover
the typed remote-note fields and strict publisher identity. Harness `3e487a5c`
extends the existing OpenAPI suite. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/remote-note-evidence-metadata.log`,
`remote-note-evidence-core-final.log`, `remote-note-evidence-rest.log`,
`remote-note-evidence-webui.log` and `remote-note-evidence-python.log` in that
same directory.

The initial Core run passed the new notes regression but failed the existing
`nonterminal_original_copy_drains_replacement_endgame_peer` fixture when its seed
closed after a partial prefix. The final gate passed without changing its
geometry, timeout or acceptance conditions. The fixture now reports the actual
downloader outcome if its relay fails. **The early close's cause is unresolved**;
keep it in final endgame qualification rather than treating a rerun as a repair.
The original failure is retained in `remote-note-evidence-core.log`.

This delivers explicit-user-only local notes and separate remote retention.
Core-owned metadata publication side effects, canonical library/server resource
cutovers, scan progress/calendar work, aggregate ownership and final platform/
pressure qualification remain open. Earlier Native/package/live/resource receipts
retain their original source revisions. No PR is authorized before review.

## Copyless Native metadata mutation service (2026-11-22)

Rust `7aeee57c` exposes the runtime's canonical `update_library_file_metadata`
operation through the existing retained content mutation owner. It accepts a
client-library hash without requiring a current job, local copy or serving-view
lookup. Unknown hashes return false without implicit creation; successful edits
return true. Existing Core/Native consumers use that operation. The service does
not allocate payload storage or grant upload eligibility for copyless content.

The existing owner retains SQL, active-cache and catalog publication through
caller cancellation. Two new Native regressions cover copyless edits after
normal job removal and cancellation after commit but before publication; drain
waits until the held producer finishes and the cache/catalog contain the edit.
Native, Core and REST gates passed **1,537, 740 and 178 tests**, respectively,
with no compiler warnings. Logs below `EMULEBB_WORKSPACE_OUTPUT_ROOT` are
`reports/settings-request-round-1/hash-metadata-service-native.log`,
`hash-metadata-service-core.log` and `hash-metadata-service-rest-final.log` in
that directory. Normal commit/push checks passed.

The first REST run found the snapshot shape fixture competing with its own
background root scan and receiving the valid shared-capacity refusal. That
fixture now waits for its setup scan to settle before making its single snapshot
request. The independent retained-frame capacity/refusal/recovery test remains
unchanged and passed. No backend retry or capacity relaxation was added.

This closes the Native mutation frontdoor, not the public library editing
contract or Core's Kad/eD2K scheduling side effects. Those still need the retained
Core service and coordinated REST/OpenAPI/WebUI cutover. The operator also chose
**explicit user edits only** for local comment/rating: passive Kad autofill must
be removed and remote notes kept separate as network evidence. That behavior
change is the next slice and is not claimed implemented by this checkpoint.
The database remains schema 115. Earlier platform/resource receipts retain their
recorded source revisions, and the no-PR boundary remains unchanged.

## One persisted hash-presentation owner (2026-11-22)

Rust `4b481e2d` gives upload priority, automatic-priority mode, local comment and
rating one persisted owner on `known_files`. Fresh schema **115** removes the
duplicate columns from download jobs and verified local content. Catalog,
publication, payload, execution and manifest reads project the same hash values.
Progress checkpoints reconcile their in-memory snapshot against this owner and
do not write presentation fields. Verified-content registration preserves an
existing client hash's metadata; first acceptance may initialize it from intake.

The metadata mutation requires client library membership and can update a hash
without any available copy or remaining job. It does not implicitly create
unknown content. If an unfinished job exists, its exact execution token is
returned for the existing cache publication path. The unused complete-copy-only
mutation was removed. Harness `e31d487d` seeds these fields on the hash and reads
them from that owner, preserving existing metadata when seeding another job.

Scoped gates passed **360 metadata, 1,535 Native, 740 Core, 178 REST and 70 Python
tests**, with no Rust compiler warnings. A new persisted regression edits a
copyless hash, removes its job, edits again, reopens the database and admits a
new job while retaining the same values. Existing stale-progress protection,
execution observation fences, catalog and upload-priority tests passed. Evidence
below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/hash-metadata-owner-metadata-final.log`,
`hash-metadata-owner-native.log`, `hash-metadata-owner-core.log`,
`hash-metadata-owner-rest.log` and `hash-metadata-owner-python.log` in that same
directory. Normal commit/push checks passed in both repos.

This closes persisted ownership, not the canonical public editing contract.
Core's current shared-file edit frontdoor still requires an available share;
unavailable-hash edits and canonical library detail remain the next coordinated
Core/REST/OpenAPI/WebUI slice. Two native import tests were deselected in the
Python gate: the stage must be rebuilt for schema 115 before rerunning them.
Earlier package, live and resource receipts retain their recorded revisions.
All three operator decisions are now accepted: persistent hash metadata,
separate server deletion/disabling and progress-only scans without completion
tokens. The goal remains active and the no-PR review boundary is unchanged.

## Library reads respect profile coherence (2026-11-22)

Rust `45d8f3cd` applies the existing profile-coherence checks to library summary
pages, exact summaries and location pages. Each checks before Native admission
and after its database await, including absent-hash results. An unreconciled
profile therefore returns the common `CommitUnknown` persistence failure rather
than ordinary library data or an authoritative-looking not-found result. This
matches the existing download/server read pattern and adds no recovery worker,
settings, schema or wire shape.

The Core and REST gates passed **740 and 178 tests**, respectively, with no
compiler warnings. The new regression injects an actual postcommit worker fault,
then proves collection and known/absent point/location reads preserve that
failure and retain no transient read capacity. It tests an already-faulted
profile; it does not independently orchestrate a fault during an in-flight SQL
read. Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-coherence-core.log` and
`library-coherence-rest.log`. Normal commit/push checks passed.

This closes a prerequisite read-failure gap. Canonical library REST/OpenAPI/WebUI
cutover, server resources, aggregate construction and active payload pressure
remain open. Prior Windows live and GNU/resource receipts remain qualified to
their recorded source revisions, not this later change. Operator choices and
the no-PR boundary are unchanged.

## Current Windows REST/OpenAPI campaign (2026-11-22)

The existing Builder `test rust-rest-openapi --workstream
public-foundation-round-1` campaign passed against the verified Windows release
stage for Rust `130ca0b2`, with Harness `0c39dc1a`. Its receipt is
`reports/rust-rest-openapi-ci/20261122T044049Z/report.json` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`; the parent log is
`reports/settings-request-round-1/schema114-current-rest-openapi.log`.

Registry/OpenAPI agreement covers **116 routes**. Conformance exercised the
**91 safe operations**: 38 successes and 53 expected errors, with no failed
routes. The 25 unsafe operations were not indiscriminately executed. Dedicated
local phases separately passed all six required peer/friend frontdoors,
category persistence and hash-wide sharing/wire eligibility, search identity and
parent-child lifecycle, Kad import/retry/reopen, canonical single-key settings
CLI, listener identity/removal and retained-download views/restart counts.
Top-level teardown was graceful.

These are local-only fixtures. The retained-download phase explicitly records
metadata-only history, with neither memory-limit nor physical-library
qualification. This receipt does not establish public-network interoperability,
rendered WebUI behavior, active payload pressure or physical-device behavior.
It verifies the current integrated surface, while the planned canonical library
and server cuts and scan completion contract remain unfinished. The three
operator choices and the no-PR review boundary remain unchanged.

## Native Windows profile-import qualification (2026-11-22)

The current Windows release client and embedded WebUI built successfully from
Rust `130ca0b2`, with zero warnings. Build evidence is
`reports/settings-request-round-1/schema114-windows-build.log` and
`logs/builds/20261122T042947Z-build-clients/build-result.json` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.

Enabling the existing native import regressions found a root fixture that used
a nonexistent conflict constraint and a hashes-only importer that selected the
operator executable instead of its managed source's verified runtime. Harness
`0c39dc1a` uses fresh root IDs after retiring the previous fixture resources and
uses the existing verified-stage owner for managed imports. Canonical source
imports retain their explicitly staged operator runtime. Unknown source layouts
fail before export or execution; managed-stage admission has no operator fallback.
The affected fixtures use the selected Rust source, current root timestamps and
the canonical settings singleton. No product alias or compatibility path was added.

The four existing profile/import Python suites passed **79 tests**, including
the two previously deselected native profile tests and two native corrupt-AICH
cases. Coverage includes fresh import, preserved upload counters on enrichment,
optional AICH rejection with MD4 reuse, relocated files and immutable replacement
root IDs with watching off. Synthetic fixtures were kept under the workspace
output root using pytest's `--basetemp`. Evidence is
`reports/settings-request-round-1/schema114-native-import-python-final.log`.
Normal commit and push checks also passed.

One Docker/WSL integration test was skipped because `EMULEBB_IMPORT_TEST_IMAGE`
was not configured; cross-platform import is therefore not qualified here.
This is import/build evidence, not a fresh full Windows REST/OpenAPI campaign or
physical-device proof. Aggregate construction, canonical library/server resource
cutovers and active payload pressure remain open, together with the pending
operator choices. Existing GNU/resource receipts retain their recorded revisions.

## Snapshot wire ownership (2026-11-22)

Rust `130ca0b2` encodes the existing snapshot envelope from a typed borrowed
projection. Upload/queue rows and download counts retain their admitted input
backing through encoding instead of being copied into another JSON value tree.
The existing retained-read encoder admits exact output bytes before allocation;
the HTTP body and all frame clones keep that output charge until final drop.
Capacity refusal uses the common persistence error contract. No route, field,
setting or database shape changed.

The complete REST gate passed **174 unit and four integration tests**, without
compiler warnings. A new response-level regression retains cloned snapshot
frames until shared capacity refuses another request with 503/PERSISTENCE_BUSY,
then proves capacity recovers after final drop. Existing snapshot shape and
collection assertions remain green. Evidence is
`reports/settings-request-round-1/snapshot-wire-rest.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`; normal commit/push checks passed.

This closes snapshot transfer-row duplication and encoded-body ownership, not
aggregate construction. Server reads still build the full cached catalog, and
library projection and diagnostic selected metadata need their coordinated
bounded construction work. The preceding package and physical-library receipts
remain attributed to `d603eb42`; they were not rerun for this change. Operator
choices and the no-PR boundary remain unchanged.

## Schema-114 GNU package and constrained library campaigns (2026-11-22)

Rust `d603eb42`, Harness `7da4dd8d`, Tooling `83d5f29c` and Builder `98fa3d2c`
passed the full GNU amd64 package gate and both agreed physical-library tiers.
The archive SHA-256 is
`9445c9902fe417b8f97b5d9c2ba37908ddc99025299d373a0e94b83485fceb22`.
All evidence paths below are relative to `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

The package gate passed strict Clippy, packet diagnostics, release compilation,
**3,505 workspace tests and three VPN-egress tests**. One intentionally ignored
ownership-child fixture is exercised by its parent tests. The archive and DEB
were built locally; no release was published. The non-root native package smoke
passed a 12 MiB local transfer, preserved its verified 9,728,000-byte prefix over
a stopped-job restart, completed delivery with the expected SHA-256, retained
the completed job and shut down gracefully. It does not prove rendered WebUI
behavior. Receipts are `reports/settings-request-round-1/foundation-gnu-schema114-full.log`,
`reports/rust-linux/gnu-amd64/b5879ba8ed2944cabaf2f85db004fdcc/` and
`reports/rust-linux/gnu-amd64/57b927673ff3409e90ed16d05efface9/package-smoke.json`.

| Physical library | Retained jobs | Enforced memory | Campaign receipt |
| --- | --- | --- | --- |
| 50,000 files / 5,242,880,000 bytes | 100,000 | 512 MiB | `reports/linux-containers/library/d65ce811618c49d7b894d5486476f94b/report.json` |
| 100,000 files / 10,485,760,000 bytes | 100,000 | 1 GiB | `reports/linux-containers/library/4a9beb312ba0467ea691a83ad0679d42/report.json` |

Both receipts report `passed` and `workloadQualified: true`, with one CPU,
no swap, unchanged resource limits and no OOM events. Both include 1,000
long-path files. The campaigns cover initial payload hashing, catalog recovery
over restarts, root updates, opt-in watching and filesystem mutations. The 100k
campaign's global checks also confirm preserved retained-job counts, graceful
shutdowns and no REST/watcher errors. Owned execution containers were removed.
Kernel campaign-tree memory peaks include filesystem cache and controller
charges; they are not daemon RSS or proof of the resident-cache ceiling.

Retained history contains 99,000 completed jobs, 900 stopped jobs and 100 started
intents. Its explicit qualification scope is **metadata-only download history**,
not concurrent payload execution. These passes establish the current campaign
baseline; canonical library/server resource cutovers, their expanded query and
mutation qualification, aggregate response ownership, active payload/session
pressure and remaining platform gates are still open. They do not complete the
foundation goal or authorize a PR. The three pending operator choices are
unchanged.

## Monotonic scan progress measurements (2026-11-22)

Rust `d603eb42` separates scan elapsed-time anchors from calendar presentation.
Aggregate, active-file and per-disk rates use monotonic elapsed time; completion
durations use the same clock. Recent results merge by monotonic completion
order, and bootstrap progress retains its matching earliest start anchor and
calendar fact. Merged rates are refreshed after counters combine. Successful
completion calculates its average from the confirmed final byte count,
consistently with the reported completed bytes.

The anchors stay private and are excluded from JSON. This prerequisite does not
change public timestamp keys/units, add a token, change SQLite, introduce new
workers or alter the existing bounded progress lists. The scan calendar API cut
is deferred until the operator answers the completion-token question now recorded
in [PUBLIC-FOUNDATION](../../design/PUBLIC-FOUNDATION.md).

Scoped gates passed **739 Core and 177 REST executions**, with zero Rust compiler
warnings. New cases exercise backward/forward calendar changes with fixed
monotonic elapsed time, aggregate/active/disk rate agreement, precise completion
duration, final-byte average consistency, merged start/completion ordering and
absence of private anchors in JSON. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/scan-monotonic-core.log` and
`scan-monotonic-rest.log`.

This closes internal scan-clock separation. Scan completion tracking/calendar
projection, canonical library/server resources, aggregate ownership and final
platform/resource qualification remain open. The schema remains 114; the other
pending operator decisions and the no-PR review boundary remain unchanged.

## Global publish diagnostics and fresh-catalog proof (2026-11-22)

Rust `76d4a6e8` exposes global eD2K attempt/success/update times and Kad update
time as nullable integer Unix seconds. Idle diagnostics report null; epoch zero
is valid. The canonical OpenAPI document now names both diagnostic models and
declares all their existing fields, rather than leaving the objects untyped.
Their counters and publication behavior remain unchanged.

Harness `7da4dd8d` requires a known empty eD2K catalog before its disposable WebUI
sharing proof mutates roots. It then requires the exact positive fixture count,
complete publication, zero pending entries, a known success time and no error.
Publication no longer depends on a strictly greater calendar timestamp. New
cases prove same-second and epoch-zero success and refuse nonempty/unknown
baselines, partial catalogs, invalid success facts and failed publication.

Scoped gates passed **737 Core, 177 REST and 343 Python executions**, with no
Rust compiler warnings. Core covers idle nulls, epoch zero and real seconds-based
update clocks for both diagnostic owners. Python extends existing OpenAPI field
constraints and WebUI-proof unit coverage. The live publication campaign was not
rerun here; these are scoped unit/contract results. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/global-publish-seconds-core.log`,
`global-publish-seconds-rest.log` and `global-publish-seconds-python.log`.

Global publication calendar fields are closed. Library scan progress still
needs its calendar/elapsed-time separation and ordering work. Canonical resource
cutovers, aggregate response ownership and final platform/resource qualification
remain open, with schema 114 and the pending operator choices unchanged.

## Process samples and per-file publication time (2026-11-22)

Rust `38e8a713` exposes process `sampledAt` and per-file publication
`lastSuccessAt` as nullable integer Unix seconds. The process sampler retains
monotonic CPU intervals and their millisecond precision. Kad publication
tracking stores seconds; eD2K's protocol-side millisecond evidence is converted
at the public projection boundary. Unknown times stay null, while epoch zero
remains a confirmed time and survives a later failed publication attempt.
The WebUI formats those seconds in sample labels and publication tooltips.

The canonical OpenAPI document and Harness `e14f455b` adopt those fields together.
The Android physical-resource reader consumes the current key and accepts epoch
zero as a valid timestamp while retaining positive RSS, finite CPU and settled
interval requirements. This change does not run or qualify a physical device.

Scoped gates passed **736 Core, 177 REST, 93 UI unit, 35 browser and 479 Python
executions**, with no Rust compiler warnings. Evidence covers publication-state
serialization, retained success after failure, epoch-zero sampling/publication,
seconds-formatted browser tooltips, unchanged millisecond CPU intervals,
OpenAPI integer/null constraints and Android reader warmup/multicore handling.
The existing contract-serialization fixture needed its renamed Rust fields;
Core's final rerun passed without changing the already validated WebUI inputs.

Logs below `EMULEBB_WORKSPACE_OUTPUT_ROOT` are
`reports/settings-request-round-1/resource-publication-seconds-core-final.log`,
`resource-publication-seconds-rest.log`,
`resource-publication-seconds-webui.log` and
`resource-publication-seconds-python.log`.

Global eD2K/Kad publish diagnostics and library scan progress still expose
millisecond calendar fields. Scan progress also uses wall-clock values for
rates and recent ordering; its conversion needs a coordinated runtime-clock
change. These remain open alongside public resource cutovers, aggregate response
ownership and final platform/resource qualification. The database remains schema
114 and the pending operator choices remain unchanged.

## Native calendar DTOs and capture time (2026-11-22)

Rust `6c35e587` serializes the DateTime-backed Core REST models as integer Unix
seconds, including nullable hostname resolution and Kad node creation/last-seen
facts. Missing optional hostname values retain their default/omission semantics;
epoch zero remains a valid time. The explicit server response mapper uses the
same seconds representation. Diagnostic `capturedAt` is an integer, validated by
the WebUI's typed capture client. Downloads use that capture time in their file
name without substituting a client clock. The WebUI formats Kad/log times from
seconds and uses only the canonical log `timestamp` field.

The canonical OpenAPI document defines integer seconds for those fields, optional
`EnvelopeMeta.generatedAt` and log timestamps. Harness `c2bb4a9e` extends the
existing response-schema suite with nullable/nonnegative/integer constraints.
Current fixtures and the embedded UI adopt the same shapes together.

Scoped gates passed **735 Core, 177 REST, 93 WebUI unit, 35 browser and 213 Python
contract executions**, with no Rust compiler warnings. Cases prove nullable and
epoch-zero hostname serialization/deserialization, the explicit current-server
mapper, actual HTTP capture time, bounded capture bytes, Kad browser date
rendering, diagnostic download content/naming and current OpenAPI validation.
The production WebUI build also passed. No database shape changed from schema
114, and no full platform/live/resource campaign is claimed by these checks.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/public-calendar-seconds-core.log`,
`public-calendar-seconds-rest.log`, `public-calendar-seconds-webui.log` and
`public-calendar-seconds-python.log`.

This closes the DateTime-backed native calendar group. Explicitly named
millisecond calendar fields in public diagnostics, canonical library/server
cutovers, aggregate response ownership and final qualification remain open.
The pending operator choices are unchanged. Durations retain their documented
precision, and previous package/resource receipts keep their own revisions.

## Persisted calendar timestamp consolidation (2026-11-22)

Rust `b3ca4c69` introduces fresh schema 114 and closes the remaining peer/Kad
calendar storage conversion. Peer first/last-seen times and the exact 150-day
credit expiry use seconds. Kad bootstrap updates, received publish observations
and outbound schedule times use seconds throughout their metadata writers and
readers. The index snapshot bridge preserves encoded tags while reducing stored
observation time to seconds. Live scheduling remains monotonic; restart restores
elapsed seconds and treats future wall times as zero elapsed time. The separate
metadata millisecond clock and superseded snapshot-column alternatives are
removed. Duration fields and native filesystem fingerprints keep their units.

Harness `d5ca37f4` updates bootstrap seeding and fixes both source-statistics
queries to consume the canonical size/verification columns. The source diagnostic
regression now creates the actual compiled schema rather than a hand-written
subset, and checks seconds-based filtering while retaining native mtime
precision. That stronger fixture exposed the adjacent summary query's column
mismatch, which was repaired before the final passing run.

Scoped checks passed **359 metadata, 86 index, 1,535 Native, 734 Core and 197
Python executions**, with no Rust compiler warnings. New cases cover exact
credit-expiry boundaries, real peer calendar bounds, snapshot subsecond
reduction with unchanged wire tags, future/normal wall-clock reconstruction and
current-schema source diagnostics. Existing publish admission/Busy rollback,
snapshot expiry, credit settlement and reopen checks passed. One Native
settlement test's direct SQL needed the current timestamp columns; its final
rerun passed. No acceptance checks were relaxed.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/peer-kad-seconds-metadata.log`,
`peer-kad-seconds-index.log`, `peer-kad-seconds-native-final.log`,
`peer-kad-seconds-core.log` and `peer-kad-seconds-python-final.log`.

This closes persisted calendar timestamp units, not the complete public time
contract. Public diagnostic/DTO timestamps still require coordinated review and
conversion. Canonical library/server resources, aggregate response ownership,
native import qualification and final platform/resource campaigns remain open.
Earlier package and constrained-container receipts do not qualify schema 114.
The pending operator choices in the authoritative foundation are unchanged.

## Library calendar timestamps and scan completion (2026-11-22)

Rust `cb06ca76` introduces fresh schema 113. Library content/origin/name
observations, local verification, root creation/deletion/scanning, memberships,
ignore rules and source-scan failures persist explicit Unix-second calendar
columns. Native filesystem fingerprints retain their full precision. Download
storage owners share the metadata seconds clock instead of deriving another
clock through milliseconds. Core root DTOs consume seconds directly, preserving
the existing public `lastScannedAt` shape.

Root recovery now detects scan completion through the active root ID and its
committed `scan_revision`, independently of calendar time. The revision advances
atomically with scan memberships and loss acknowledgement. A new root at the
same path starts at zero and cannot count as a completed scan. Revision
exhaustion fails and rolls back the scan instead of wrapping, saturating or
falsely acknowledging progress. This is internal state, not a new API field,
setting, timer or automatic scan policy.

Harness `a46bcb2d` updates the existing metadata/physical-library helpers and
soak-control SQL consumers. Scoped gates passed **358 metadata, 1,535 Native,
733 Core and 297 Python executions**, with zero Rust compiler warnings. New
checks cover library calendar bounds, preserved fingerprint evidence, identical
scan timestamps with distinct completion revisions, reopen, replacement-root
identity and revision-exhaustion rollback. Existing root recovery, watcher loss,
indexed library queries, transfer admission and current-schema helper suites
continue to pass. Two native import tests were deselected by the standard
Python lane and are not qualified here.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-seconds-metadata.log`,
`library-seconds-native.log`, `library-seconds-core.log` and
`library-seconds-python-final.log`. The initial Python run caught two invalid
clock-helper references introduced during the fixture edit; both were corrected
before the passing rerun. Rust inputs did not change after their passing gates.

Peer-credit and Kad calendar storage remain to consolidate. Public library/
server cutovers, aggregate response ownership and final platform/resource gates
remain open. This checkpoint does not rerun the physical 512-MiB/1-GiB campaigns
or a sustained soak; prior package receipts do not qualify schema 113.

## Profile, identity and friend calendar timestamps (2026-11-22)

Rust `8156fc82` introduces fresh schema 112. Schema-marker/profile creation,
local-identity creation/update and friend first-seen/last-seen/deletion use Unix
seconds in explicit `_s` columns. Identity updates preserve creation time. The
friend recovery postcondition compares the same seconds stored by the write
owner. Core restores friend times using the seconds constructor and serializes
`lastSeen` as nullable integer Unix seconds. OpenAPI and the WebUI adopt that
shape together; the UI formats known times and leaves unknown times blank.

Harness `778bf132` extends the existing metadata seed helpers, durable friend
campaign reads and response-schema suite. No replacement launcher or parallel
schema definition was introduced. Scoped checks passed **355 metadata, 733 Core,
177 REST, 93 WebUI unit, 34 browser and 256 Python executions**, with no Rust
compiler warnings. New evidence covers profile/identity calendar bounds,
creation-time preservation, friend persistence/recovery and JSON round-trips,
nullable/epoch-zero values, subsecond reduction, schema integer constraints and
actual browser display. The standard Python lane deselected two native profile
import tests; this checkpoint does not claim their execution or current native
import qualification.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/profile-seconds-metadata-final.log`,
`profile-seconds-core.log`, `profile-seconds-rest.log`,
`profile-seconds-webui.log` and `profile-seconds-python.log`.
Other timestamp domains and final combined platform/resource qualification
remain open. Library and server public cutovers still depend on the two
operator choices recorded in the authoritative foundation. Existing platform
receipts retain their original revisions and do not qualify schema 112.

## Server calendar timestamps (2026-11-22)

Rust `87b22226` introduces fresh schema 111: server `first_seen_at_s`,
`last_seen_at_s` and `deleted_at_s` use Unix seconds. Bootstrap and ordinary
upsert use the same seconds clock, preserve first-seen time on updates and keep
ping durations in milliseconds. Live-row indexes, admitted page/exact reads and
protocol catalog loading use the current columns. Harness `42ae73b1` updates
the existing seed and discovery-snapshot helpers to that same schema.

Scoped gates passed **354 metadata, 732 Core and 43 Python metadata executions**,
with no Rust compiler warnings. New cases check real calendar-time bounds,
first-seen preservation on update and unchanged ping precision. Existing
retirement, re-import, identity and bounded-read checks continue to pass. Logs
below `EMULEBB_WORKSPACE_OUTPUT_ROOT` are
`reports/settings-request-round-1/server-seconds-metadata.log`,
`server-seconds-core.log` and `server-seconds-python.log`.

This closes only server calendar-time storage. Other persisted/public calendar
timestamp domains still require consolidation. Server mutations and the public
caller cut, canonical library resources, aggregate response ownership and
current platform/resource qualification remain open. Earlier platform receipts
do not qualify schema 111. The two operator choices recorded in the foundation
remain pending; this slice does not select either behavior.

## Server identity and bounded metadata prerequisites (2026-11-22)

Rust `046b83a1` introduces the fresh schema-110 server identity foundation.
Positive SQLite AUTOINCREMENT IDs survive metadata updates and reopen and are
never reassigned after deletion. Live address/port uniqueness uses ASCII
case-insensitive address matching. Retired rows do not block a fresh identity at
the same endpoint and cannot be resurrected by upsert. The existing Python
server seed helper uses the same live-row upsert semantics and preserves the
allocation high-water mark when clearing fixture data. No migration, alias or
endpoint-to-ID compatibility path was added.

New metadata readers select one exact ID or an ascending keyset page of at most
200 rows, default 100, with optional totals. A 1-MiB allowance includes text/port
conversion headroom; SQLite checks text length before cloning. Byte-short pages
preserve continuation without truncating strings. Disabled rows remain visible,
retired rows are hidden and removed ID boundaries still continue. A live-ID
partial index avoids walking retired history. Existing protocol catalog loading
shares the row decoder; auxiliary ports retain first-observed order with bounded
duplicate lookup work.

Scoped gates passed **353 metadata, 729 Core and 42 existing Python fixture
executions**. Rust warning scans were empty. Cases cover stable IDs, hard-delete
high-water retention, retired-endpoint re-import, hostname case, distinct ports,
reopen, disabled/retired visibility, byte-short traversal, oversized rows and
invalid queries. The 100,000-row case includes 50,000 retired rows and proves a
late indexed seek without a temporary sort in fewer than 10,000 SQLite VM steps.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/server-identity-metadata-verified.log`,
`server-identity-core-accepted.log` and `server-identity-python-verified.log`.
An intermediate broad SQL edit also changed friend re-add behavior; the existing
FIFO regression caught it, the unrelated edit was restored, and Core passed.
No friend-domain change remains in the final diff.

This is the database/read-model prerequisite. The coordinated
server REST/OpenAPI/WebUI caller cut, aggregate snapshot/diagnostic ownership,
persisted-calendar timestamp consolidation and resource qualification remain
open. The server deletion choice and the separate library hash-metadata choice
remain pending in the authoritative foundation. Existing platform receipts keep
their own source/schema revisions and do not qualify schema 110.

## Admitted server catalog reads (2026-11-22)

Rust `7d3736bf` routes server pages and exact-ID reads through the existing
Native metadata worker. Validation precedes admission. Results retain the
1-MiB read allowance under the shared transient-work budget until conversion or
final drop; missing exact IDs release their allowance. No new worker pool,
saved setting, endpoint or alternate server catalogue was introduced.

Core exposes the retained persisted records without walking or populating its
runtime server cache. It checks persistence coherence before and after the
await. Invalid queries remain typed validation failures, oversized rows become
PERSISTENCE_TOO_LARGE, admission/closing errors retain their classification and
SQL failures remain storage errors instead of empty results or missing IDs.
Connection presentation and the coordinated HTTP model remain separate work.

The complete scoped gates passed **1,535 Native and 732 Core executions**, with
zero compiler warnings. Existing compact-result and cancelled-receiver/drain
coverage now includes server pages. New cases prove shared-budget saturation,
validation before saturated admission, release on missing/closed reads, persisted
ID authority with an empty runtime cache, no resident download hydration,
retained conversion/exact JSON backing, ordered page continuation, oversized-row
handling and SQL failure classification. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/server-admission-native-final.log` and
`server-admission-core.log`.

This closes server read admission. Server mutation ownership, public caller
adoption, aggregate response ownership, timestamp consolidation and platform/
resource qualification remain open. This is not profile-fault-policy proof.

## Current REST error catalogue (2026-11-22)

The closed OpenAPI error enum now includes the current cursor, overlapping-root,
managed-root, local-content-choice and internal-error responses emitted by native
handlers. The previous catalogue omitted these outcomes even though controller
regressions exercised them. Local-content choice requires typed
`details.availability` with the actual present/unavailable/absent values. No
endpoint behavior, error-code translation, alias or compatibility path was added.

The existing Python response suite validates each affected operation/status
combination, including both upload collections and diagnostic SERVICE_BUSY.
Missing or invalid local-content availability is rejected. Together with the
existing route suite, **165 tests passed**; evidence is
`reports/settings-request-round-1/current-error-contract-python.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. These schema checks complement the controller
regressions; they do not expand the earlier live campaign's selected outcomes.

## Current GNU/Linux qualification (2026-11-22)

Rust `f6a9a206`, Harness `439304ec` and the selected tooling contract passed the
supported amd64/GNU full package gate: strict Clippy, packet-diagnostics
compilation, **3,479 workspace test executions**, three VPN-egress tests, release
build, GNU archive/DEB packaging and native non-root lifecycle smoke. The one
ignored test entry is the ownership-test subprocess fixture; its parent ownership
regressions invoke it explicitly and passed. This is not an omitted qualification
case. Smoke delivered and verified 12 MiB, preserved its verified prefix across a
stop/restart, retained completed history and shut down gracefully.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/foundation-current-gnu-full.log`,
`reports/rust-linux/gnu-amd64/2671accd66d74fdbbd8d8b694158b51c/` and
`reports/rust-linux/gnu-amd64/919b64e498124598bb721949bc77444a/package-smoke.json`.
The archive SHA-256 is
`5ac2bb9f318ff164df2d41ec3a91235f5f6f810200140927a219b319664ffa4f`.
This qualifies the current GNU source checkpoint, not the physical-library/memory
tiers, Android APK/device behavior, sustained soak or other platform gates.

## Diagnostic encoding and response ownership (2026-11-22)

Rust `f6a9a206` measures escaped UTF-8 JSON with serde's writer before allocating
wire backing. Both search-item fitting and whole-bundle trimming use this
allocation-free count. Final encoding allocates one exact boxed slice after the
payload fits its requested byte cap; `budget.encodedBytes` includes its own
serialized decimal width. Mandatory core data still fails explicitly if it
cannot fit, and optional omission accounting retains the v7 contract.

One diagnostic capture or retained capture body is admitted per REST listener.
The standard owned semaphore permit moves into the body owner and survives
body-frame clones; concurrent captures return existing HTTP 503/SERVICE_BUSY
without waiting. Failure releases admission. This separates the explicitly
requested diagnostic output allowance from Native metadata work and leaves
ordinary status reads available while a client retains a bundle. No setting,
byte-range change, format revision or daemon-side output file was introduced.

The complete REST gate passed **173 unit + 4 integration tests**, without
compiler warnings. New cases cover escaped/control/multibyte text, decimal-size
boundaries, frame-clone retention, status reads during retention, release after
the final clone, and repeated captures after a persistence failure. Existing
exact byte-budget, mandatory-core and omission tests remain green. Evidence is
`reports/settings-request-round-1/diagnostic-capture-rest.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. The existing Python route/response schema suites
also passed **151 tests** (`diagnostic-capture-python.log` in the same directory).
The last full Windows/live receipt belongs to Rust `e651b35b`; it is not proof
for this later source revision.

This closes diagnostic encoding and concurrent body ownership. Aggregate
snapshot/diagnostic construction, underlying full reads and combined physical
library/memory qualification remain open; selected metadata trees are not
claimed to fit the final encoded-byte allowance.

## Typed library summary reads (2026-11-21)

Rust `bfdd3824` adds typed Core summaries and an admitted exact-hash read over
the indexed metadata model. Collection and exact reads expose identical scalar
facts, including unavailable/copyless client hashes, accepted nullable size,
sharing policy and real session/lifetime statistics. Exact reads do not warm
unrelated filename keys or inspect physical files. Core conversion and JSON
encoding retain the existing admission charge until backing is dropped.
Storage failures retain their storage classification instead of becoming
invalid-user-input responses.

Library filters now accept immutable public tag names, resolved case-insensitively
inside SQLite. A valid absent tag returns an empty page without creating a tag,
matching the existing download-category filter behavior. Numeric tag keys remain
internal; no per-row Rust lookup or extra persistence owner was added.

Scoped checks passed **345 metadata and 729 Core executions** without compiler
warnings, including the Native dispatcher used by the Core reads. New cases
prove exact/copyless/passive boundaries, no unrelated name warming, equality of
collection/exact facts, positive current-field JSON serialization, unknown/zero
timestamp distinctions and exact retained charges through conversion/encoding/drop.
Evidence is `reports/settings-request-round-1/library-summary-{metadata,core}.log`
below `EMULEBB_WORKSPACE_OUTPUT_ROOT`; normal commit/push hooks passed.

The canonical REST/OpenAPI/WebUI cut remains open. The operator accepted detail-only reads for the link and local comment/rating.
Persistent hash ownership of upload priority/local comment/rating remains pending
in the authoritative foundation. No transitional REST routes were added.

## Cached locations REST/WebUI integration (2026-11-21)

Rust `c90e5eb7` exposes `GET /library/files/{hash}/locations` through the existing
admitted metadata worker. The hash-scoped cursor selects at most 200 cached
copies, with a default of 100 and a 1-MiB result allowance. Results retain their
allowance through Core conversion, JSON serialization and HTTP body delivery.
The response is a thin data array of paths and cached presence; it neither
probes files nor grants upload permission. Accepted copyless hashes return an
empty page; unknown/passive-only hashes return 404. The selected-file WebUI
inspector fetches one location page and resets paging on hash selection.

Scoped checks passed **727 Core, 174 REST, 93 WebUI unit and 33 browser tests**,
plus **131 existing Python route/schema and 30 conformance-runner tests**.
Rust compiler warning scans were empty. A three-copy REST fixture traverses
every page with sharing disabled, then deletes the physical files and proves
that reads still return cached observations. Core checks unchanged resident
execution use and exact retained charges through encoding/drop. Browser fixtures
now use canonical lowercase hashes. The existing Python populated sharing phase
also checks both physical copy paths through the new route.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-locations-core.log`,
`library-locations-rest-final.log`, `library-locations-webui-final.log` and
`library-locations-python-{openapi,ci}.log` in the same directory. Normal commit
hooks passed. The regular Windows release build passed without compiler warnings
on Rust `c90e5eb7`; its full live REST/OpenAPI campaign passed with Harness
`a61955ff`. All 91 selected operations passed their success or expected-error
contracts. The populated category phase proved both real cached copies present;
settings CLI, category/friend/Kad persistence and retained-download scale phases
passed, with graceful teardown. Evidence is
`reports/rust-rest-openapi-ci/20261121T204225Z/report.json` and
`reports/settings-request-round-1/library-locations-{windows-build,live-identity}.log`.

The generic unknown-hash probe requires 404, while the populated phase requires
200 and both copies. That phase compares filesystem identity rather than Windows
extended-length path spelling; failure reports preserve returned observations.
No daemon path conversion or endpoint expectation was weakened. This closes the
locations resource, not global library browsing, visibility or statistic sorting.

## Stable client library names (2026-11-21)

Rust `53b3fb31` implements the operator's first client-accepted display-name
decision using retained library membership. Download admission, verified local
acceptance and client-origin indexing select the client name before membership
is established, replacing a passive-only label. Subsequent observations, copies
and jobs preserve it, even after the final job and origin rows are removed.
Job presentation and actual location filenames remain independent. No schema
change, additional authority or name-reconciliation machinery was introduced.

Scoped validation passed **335 metadata and 1,522 Native tests** without
compiler warnings. The acceptance-failure regression proves the name and
membership roll back together, then exercises real job retirement and a new
attempt with different presentation. Existing verified-copy and origin tests
cover passive promotion and later local names. Evidence is
`reports/settings-request-round-1/library-first-name-{metadata-final,native}.log`.
Normal commit/push hooks passed. The preceding release/live receipt proves the
locations integration on `c90e5eb7`; final package, current-source live and tier
qualification after remaining library-query integration stay open.

## Retained client library identity (2026-11-21)

Rust `5cd0ad7a` introduces fresh schema **109** with `library_files`, the retained
client-membership relation keyed by content ID. Accepting a download, verified
local content or client-origin knowledge records membership in the same
transaction. Retiring the final job, copy, root or origin preserves it.
Passive-only knowledge does not establish membership. Tags now reference this
relation through a foreign key; policy, tag reads/writes, cached locations and
client-session counter publication use the same boundary.

The metadata locations reader returns an empty page for an unfinished accepted
download. It gains no verified identity, size or serving authority
merely from membership. Tests run the real removal/retirement/finalization path,
then prove that the hash, tags and policy survive without authorizing payloads.
Injected acceptance failure rolls back membership, content creation and the job.
Passive demand retains its lifetime accounting but creates no client-session
counter; explicit client acceptance changes that classification atomically.

Scoped gates passed **334 metadata, 1,522 Native, 726 Core and 171 REST**
executions without compiler warnings. The existing Python metadata suite passed
**41 tests**, including current-source schema/fixture construction. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-identity-{metadata-final,native-final,core-final,rest}.log`
and `library-identity-python-metadata.log` in that directory. Counter and policy
fixtures now declare client origins; dedicated passive-observation coverage
remains. Ordering, cancellation, admission and failure assertions are preserved.
Normal Rust commit hooks passed. No migration, alias or retired-input handling
was introduced. Final package and constrained-tier qualification remain open.

The bounded specialist question about live statistic publication is resolved in
the foundation specification: publish to indexed TEMP read state under existing
ownership, keeping durable checkpoints batched. Bounded publication is implemented
below; the indexed backend query is implemented as well. REST/OpenAPI/WebUI
collection integration remains open. The first client-accepted library display-name
decision is implemented above; later copies retain actual filenames in locations.

## Real-peer endgame contention checkpoint (2026-11-21)

Rust `1d92d229` adds nonterminal verified-part contention for both winner roles
and fixes the redundant-peer read gap exposed by that fixture. Each source has
only its first verified part; the final part remains missing. After verification,
one latched per-peer signal wakes the losing reader at the existing safe read
boundary. The registry retains every live lease owner through takeover and removes
only the exact dropped owner. No task or future is allocated per block to wait for
completion, and no state is retained for historical jobs. The source fixture
disables upload-session rotation so its resumable prefix can exceed the independent
90%-of-file session policy; product defaults are unchanged.

Validation passed 1,515 Native and 726 Core executions without warnings, including
all four real-peer winner/completion combinations. The nonterminal cases verify
the exact first-part payload, single accepted-byte accounting, an incomplete final
manifest, receiver-side socket closure without reconnect and restored connection
and temporary-work accounting before the normal peer timeout. Regular Windows
release/WebUI build passed with zero warnings. Evidence is
`reports/settings-request-round-1/endgame-nonterminal-native-final.log`,
`endgame-nonterminal-core-final.log` and `endgame-nonterminal-windows-build.log`
under the same directory below `EMULEBB_WORKSPACE_OUTPUT_ROOT`.

The prior baseline reached duplicate-tail contention but exceeded its drain
deadline after the winner was released. Earlier diagnostic attempts located slow
prefix setup separately from that drain assertion. Detailed scope and remaining
interop proof belong to [RUST-FEAT-038](RUST-FEAT-038.md). Decoder consumption of
the partial frame, explicit wire cancellation, daemon output delivery, sustained
rare-job displacement and final platform/memory campaigns remain unqualified.
No schema, settings or public API changed; no PR or merge is authorized.

Rust `5b03afb7` extends the existing Core loopback transfer fixtures with two
real Native peers and a resumed payload obtained over TCP. Both the original
and replacement endgame lease win in separate cases. The losing connection
receives a partial data frame before the winner completes the payload; the
fixture requires receiver-side socket closure without reconnect, exact verified
payload bytes, a single accepted-byte charge, empty outstanding requests and
connection/temporary-work accounting restored to baseline. Real lease age and
rate conditions are exercised rather than fabricated manifest progress.

The regular locked Core gate passed 724 executions without warnings in
`reports/settings-request-round-1/endgame-two-peer-core-final.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. Formatting, diff checks and commit hooks passed.
The test-only dependency uses the existing pinned Tokio codec; no package version,
product behavior, public contract or schema changed.

This proves final-tail contention and whole-payload socket drain. It does not
prove nonterminal duplicate-block cancellation, decoder consumption of the partial
frame, an explicit wire cancel message, daemon output delivery, sustained rare-job
displacement or final platform/memory campaigns. Those requirements remain open.

## Upload queue REST/WebUI integration (2026-11-21)

Rust `f000fb0f` connects the live Native selector to cursor-based queue browsing,
snapshot previews and diagnostic prefixes. REST returns a data array and cursor
metadata, optional exact `meta.total`, and HTTP 409/`CONFLICT` for a departed
anchor. Score diagnostics are detail-only. The WebUI fetches its visible page,
uses the existing cursor controls and refreshes from the first page after expiry.
Hostname enrichment reads scalar peer addresses without constructing upload rows
or file captions. The scheduler helper identified by GNU Clippy was moved
unchanged before its inline test module; the fresh full GNU gate passed below.

The existing temporary-work ledger admits the Native page before queue locking
and retains input/output through asynchronous caption projection. Native
projection is byte-bounded; Core bounds owned rows with JSON escaping headroom.
Encoded responses retain their charge through the standard Bytes owner until
HTTP delivery/drop. The schema and settings surface are unchanged. Tests cover
cancellation drop order, complete traversal with large multibyte peer labels,
memory ownership through JSON encoding, unchanged resident-cache use, cursor
scope/expiry, and UI refresh without retaining previous pages.

Scoped gates passed 1,522 Native, 726 Core and 170 REST executions; final compiler
warning scans were empty. The WebUI passed 92 unit and 32 browser tests, type
checking and production build. Harness `98e1c0a1` passed 220 selected Python
checks: 131 route/schema, 30 conformance-runner, 39 cross-client fixture and 20
response-schema tests. Strict download field checks and fixtures were aligned
with the already-required `waitingReason` field. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/upload-queue-final-emulebb-{ed2k,core,rest}.log`,
`upload-queue-integration-webui.log`, `upload-queue-python-openapi-final.log` and
`upload-queue-python-{ci,reask,responses}.log` in the same directory. A final,
equivalent positive IPv4 projection passed the existing product-policy hook.

The regular Windows release/WebUI build passed with zero warnings in
`logs/builds/20261121T175221Z-build-clients/build-result.json`. Live REST/OpenAPI
conformance passed on exact Rust `f000fb0ff2705a50e6d1d2a5373ad1d6969bf692`,
with graceful teardown, in
`reports/rust-rest-openapi-ci/20261121T175848Z/report.json`. This includes the
existing populated upload resources, persistence and retained-download scale
phases; it does not qualify a physical library or a constrained-memory tier.

The full GNU amd64 package gate passed on the same Rust revision: strict Clippy,
packet diagnostics, 3,438 workspace tests and three VPN-egress tests. Evidence is
`reports/rust-linux/gnu-amd64/0bf3b4df84da4d9683c0d97b34b74d71/`.
The non-root package lifecycle passed in
`reports/rust-linux/gnu-amd64/18231a3914684074a608f6aeb60b85a5/package-smoke.json`.
It verifies a real 12 MiB download and delivery, a 9,728,000-byte verified prefix
preserved across restart and explicit start, retained completed history and
three graceful shutdowns. It checks packaged WebUI assets and backend resources,
not rendered browser operation. The bundled PCP/NAT-PMP C build emitted warnings;
this is not a zero-warning Linux result. The local archive SHA-256 is
`09d398d531daae5c4cfee539f2871ec3d30bbbb9dc7ae9da794833d4b887a9a6`.

Remaining platform and physical-library campaigns remain open.
Snapshot/diagnostic selection is bounded; this does not claim
complete aggregate-response accounting or final upload DTO cleanup. No PR or
merge is authorized.

### Physical library and retained-history checkpoint (2026-11-21)

The existing container campaign passed on Rust `f000fb0f`, Harness `98e1c0a1`,
Tooling `d374d6de` and Builder `98fa3d2`: 50,000 physical files (5,242,880,000
bytes), 100,000 retained jobs, 512 MiB total container memory, no swap and one
CPU. Evidence is
`reports/linux-containers/library/76bee0996e7f4344919d9b8225723735/report.json`
below `EMULEBB_WORKSPACE_OUTPUT_ROOT`, with its linked campaign report.
The fixture includes 1,000 long paths and Unicode paths. All four opt-in watcher
bursts passed exact-content and root-acknowledgement checks. No-change reloads
read no payload; the 1% mutation rehashed exactly 500 files. Retained completed,
queued and stopped jobs survived restarts; all 100,000 job rows were traversed.
Kernel OOM and OOM-kill deltas were zero. Recorded cgroup peak was 536,932,352
bytes, slightly above the 536,870,912-byte enforced limit; it is whole-campaign
memory, not daemon RSS or a resident-cache measurement.

This is scoped capacity evidence, not complete tier acceptance. The campaign's
download history is metadata-only. Active-payload pressure, large-library
substring queries and every statistic sort remain unqualified. Current library
browsing still uses the path-ordered `/shared-files` surface; the accepted
canonical library resource, visibility filters, thin DTOs and statistic sorts
remain implementation work. Extend the existing campaign for those requirements
before claiming the full tier, and qualify the 100k-file/1-GiB tier separately.

## Indexed hash-level library queries (2026-11-21)

Rust `3901716f` adds the admitted Native library-page read. It supports Present,
Shared, Unavailable and All Known, filename substring, root, tag and sharing
filters, optional exact totals, and both directions of name/size plus all eight
statistic sorts. Rows contain one client hash, its stable display name, accepted
nullable size, cached presence, sharing policy and scalar statistics. Passive-only
observations, paths, job arrays, hashsets and tag arrays stay outside the page.
Limit defaults to 100 and cannot exceed 200; byte-short pages retain a cursor.

SQLite owns the disposable summary projection. Missing/changed Unicode name keys
warm one bounded label at a time; idle reads rewrite neither names nor projections.
Presence changes reconcile only affected content in the existing physical-index
refresh. Statistic indexes have a presence prefix, letting Present skip retained
copyless jobs. All Known uses SQLite's ordered merge of the two indexed cohorts
instead of another index set or a full collection sort. Generated non-null keys
permit tuple seeks for nullable sizes/timestamps; zero remains distinct from
unknown. The scale test exposed a 701k-step expression-index cursor walk, which
the generated columns eliminated without weakening the work bound.

Hash anchors remain usable outside the current filters. Missing anchors fail
before cold projection warming, so invalid cursors do not repeatedly warm and
roll back the index. Pages are live and make no multi-request snapshot guarantee.
The Native result retains 2 MiB of work/result allowance until drop, including
folding headroom; the decoded page remains bounded to 1 MiB. Durable statistics
updates also invalidate SQL-owned keys, so inactive imported/seeded lifetime
facts publish without allocating runtime accounting rows. Runtime captures and
durable pending keys share the existing bounded publication path.

Scoped gates passed **343 metadata, 1,528 Native and 727 Core executions** without
compiler warnings. The 100k query fixture places 99,900 unavailable hashes before
100 cached present copies; every sort/view/direction late-page combination uses
fewer than 10,000 SQLite VM steps and no temporary sort. Smaller fixtures cover
Unicode/literal matching, filter conjunctions, zero/unknown values, one-row and
byte-short traversal, anchors outside filter membership and cold refusal.
Native coverage proves global live/inactive lifetime ranking, unchanged durable
pending bytes, no execution hydration/runtime statistics allocation for inactive
rows, and exact retained charges through drop. The final cursor-refusal change
reran metadata coverage; its successful-query paths are unchanged.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-query-metadata-verified.log`,
`library-query-native.log` and `library-query-core.log` in that directory. Normal
commit/push hooks passed. REST/OpenAPI/WebUI collection integration and the
extended physical tier campaigns remain open; this backend fixture does not
qualify constrained-container RAM or a final package.

## Bounded live statistic publication (2026-11-21)

Rust `146262e9` publishes captured statistics into a connection-local SQL read
model through the existing admitted metadata owner. It moves the dirty-key set
instead of cloning the complete ledger, copies at most 128 fixed-size captures
at a time, and releases the capture mutex before SQL. Publication shares the
credit-settlement gate, so effective lifetime values are committed totals plus
still-parked deltas. Session values are absolute current-process captures.
Reading does not checkpoint credit or file totals and hydrates no execution.
The scalar read retains a 64-KiB allowance until its result is dropped.

Each SQL chunk is atomic. Failure or unwinding restores all detached keys,
including keys whose earlier chunks published successfully; absolute retry
does not add those values twice. Captures during publication remain dirty for
the next read. Checkpoint drain marks affected hashes for recomputation after
commit or restoration. Durable peer/file writes retain their existing batched
transaction and reject out-of-range arithmetic atomically. No additional runtime
counter map, per-payload SQL write, durable schema, settings or REST shape was
introduced.

The SQL population includes every retained client hash, including inactive
zero-valued rows, and excludes passive-only observations. Eight indexes cover
session/lifetime bytes, demand and accepted stints, plus both activity timestamps,
with deterministic hash ties. A 100,000-hash fixture proves indexed first pages
in both directions and late-page seeks without a temporary sort; nullable
timestamps retain their meaning. Repeating identical captures performs no
writes. Clones share publication, and reopening resets session values while
retaining checkpointed lifetime facts.

Scoped gates passed **336 metadata, 1,527 Native and 727 Core executions**,
without compiler warnings. Native cases prove nonzero durable baselines plus
uncheckpointed captures, equality after checkpoint, retained result charges,
capture/publication/checkpoint races, overflow recovery, unwinding, and failure
after the first of multiple chunks. The existing capture/removal/rebuild/reopen
test retains all byte, request and stint assertions through admitted publication.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-statistics-publication-metadata.log`,
`library-statistics-publication-native-verified.log` and
`library-statistics-publication-core.log` in that directory. Normal commit/push
hooks passed.

The indexed backend collection/query integration is implemented above. Native
REST/OpenAPI/WebUI collection DTOs and combined-scale qualification remain open.
The in-memory SQL fixtures are not constrained-container or final-package
qualification claims.

## Library filename-search contract (2026-11-21)

Rust `2143a89c` applies the agreed filename-only literal substring rule through
the existing indexed catalog, REST validation and WebUI. A supplied query must
contain at least three Unicode characters after trimming. Validate before
lowercasing because lowercasing can expand a character. SQL matches only the
stored filename search key; parent directories, content hashes and wildcard
syntax do not participate. The WebUI labels this scope and prevents short
submissions. OpenAPI documents the same constraint. No schema change is needed.

Scoped checks passed 327 metadata, 171 REST, 92 WebUI unit, 32 browser and 131
existing Python OpenAPI executions. Metadata and REST compiler warning scans
were empty. The existing 100k catalog fixture verifies filename scope without
allocating a full result collection. The REST integration uses an actual Unicode
filename and verifies uppercase and mid-word matches. Evidence below
`EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/library-filename-metadata.log`,
`library-filename-rest-final.log`, `library-filename-webui.log`,
`library-filename-python-openapi.log` and `library-filename-docs.log` in that
same directory. Normal Rust commit hooks passed.

This closes only search semantics on the current collection. Canonical library
routes, visibility filters, thin summaries, locations and statistic sorting
still require integration; full constrained-tier qualification remains open.

## Upload management read prerequisites (2026-11-21)

Rust `dd34104e` provides Native active and waiting management pages. Waiting
pages preserve scheduler rank; active pages use immutable entry-ID order.
Selection keeps a page-sized heap plus lookahead, copies only selected entries
and omits requester bitmaps. A departed anchor requires refresh. Byte-short pages
retain continuation, so every entry remains reachable. Active results retain a
1-MiB allowance until drop; selection bounds cloned backing to 512 KiB.

Selected-client reads also omit requester bitmaps and no longer run protocol
maintenance. Waiting reads apply the ordinary timeout without physically
retiring state. Full management ranks are independent of the protocol's u16
rank representation, with a 65,536-entry regression. Snapshot facts now include
real elapsed seconds: waiting stops at first accepted payload, while upload
duration is null until that stint starts. Scheduling, credits and wire ranks
retain their existing owners.

Scoped validation passed **1,533 Native and 729 Core executions** without
warnings. Cases cover complete ID/rank traversal, byte limits without truncated
software text, optional totals, departed/expired anchors, no read-driven queue
cleanup, accurate durations, bitmap omission and retained-charge release.
Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/upload-management-native-final.log` and
`upload-management-core.log`; normal commit/push hooks passed.

Rust `e651b35b` completes the upload DTO/REST/WebUI cut. Both lanes expose
bounded cursor pages and optional totals. Detail reads retain their bodies and
actual scheduler diagnostics; nullable identity/file facts remain unknown rather
than becoming fabricated values. Rates use bytes per second and durations use
elapsed seconds. Controls read fixed scalar identity independently of captions
and read-body admission. A borrowed envelope encoder admits exact wire backing
without another full projection allowance and retains it through HTTP body drop.
The snapshot completes unrelated metadata work before retaining upload pages;
this prevents its own reservations from exhausting the existing budget. Diagnostic
capture uses the same bounded active-page reader and reports a 200-row limit.

Scoped gates passed **1,534 Native, 729 Core and 173 REST executions**, with no
Rust compiler warnings, plus **93 WebUI unit, 33 browser and 224 Python harness
tests**. Type checking and production bundling passed. REST cases cover both
collection envelopes, optional totals, limit boundaries, cross-collection cursors
and missing anchors. WebUI cases cover independent paging, cursor refresh,
selection races, elapsed units and totals differing from page lengths. An existing
Core recovery test now waits for both publication and the completion checkpoint
within its original timeout, preserving all data and recovery assertions.

Evidence below `EMULEBB_WORKSPACE_OUTPUT_ROOT` is
`reports/settings-request-round-1/upload-wire-native.log`,
`upload-wire-core-current.log`, `upload-wire-rest-accepted.log`,
`upload-wire-webui-current.log` and `upload-wire-python.log`.
The regular Windows release build passed without warnings on Rust `e651b35b`
with Harness `439304ec` and Tooling `8edaf975`. The full existing live REST/OpenAPI
campaign passed: all 91 selected operations across the 116-route inventory met
their success/expected-error contracts, with no failed routes. Its six real peer
friend-control front doors, category/Kad persistence, offline settings CLI,
listener receipt and retained-download history phases passed, with graceful
teardown. This includes actual active and waiting upload identities under the
new schemas. Evidence is
`logs/builds/20261121T231839Z-build-clients/build-result.json` and
`reports/rust-rest-openapi-ci/20261121T232156Z/report.json`; the executable SHA-256
is `dfb3deb50e47504f5a5b20eb493b306ce79180b891b1b7fb9ac212b40c41e4a7`.

Combined physical-library/memory qualification and aggregate snapshot/diagnostic
ownership remain open. The history phase explicitly does not qualify physical
library size or a memory limit; sustained soak remains deferred.

Rust `0ce94c98` replaces serving-view hydration in upload list/detail captions
with a scalar metadata read through the existing bounded Native worker. It seeks
the requested hash and counts whole verified ranges in SQL, including a short
final part, without loading hashsets, paths, manifests or local part arrays.
Cached content/job names and geometry are display facts independent of current
physical-copy availability; this read grants no protocol serving authority.
Unknown or observation-only hashes have no caption. Complete cached local content
takes precedence over a download record. Schema and REST response fields are
unchanged.

The read bounds names to the existing 64-KiB allowance and retains a 256-KiB
temporary-work charge with its result. Native regression proves large geometry
does not allocate storage or hydrate the resident cache, and that dropping the
result releases its charge. SQL tests cover disjoint/partial/short-final ranges,
cached content without paths/hashsets, UTF-8 byte bounds without truncation and
indexed plans without collection scans or temporary sorts. These replace the
former Core in-memory part-count calculation test. Gates passed 326 Metadata,
1,516 Native, 725 Core and 169 REST executions without warnings. Evidence is
`reports/settings-request-round-1/upload-caption-metadata-validated.log` and
`upload-caption-{native,core,rest}.log` in the same directory below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.

That checkpoint closed per-file serving-state hydration in management reads.
It did not qualify queue-wide memory use or final platform/physical-library
campaigns. Subsequent cursor/ownership integration is recorded above.

The attempted full GNU/Linux package gate at Rust `0ce94c98` stopped in strict
Clippy: `download_scheduler.rs` declares `collect_ready` after its test module.
Evidence is `reports/rust-linux/gnu-amd64/003ba42ed6fa48babc1bd62ac52df32f/clippy.log`
and `reports/settings-request-round-1/foundation-current-gnu-full.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`. This run produced no qualified package or smoke
result. The integration moved the helper unchanged; rerunning the full gate and
final Linux qualification remain open.

Rust `d0876435` selects active upload sessions before constructing management
snapshots. Active list/status reads no longer clone waiting-client bitmaps or
compute ranks for waiting entries. Selection still scans/reaps the runtime queue;
the retained result is bounded by the existing active-slot policy. Core upload
projection now lives in `upload_api.rs`. The existing admission fixture verifies
that active identities, phase/rank fields and ordering match the combined view.
Scoped gates passed 1,514 Native, 722 Core and 169 REST executions without
warnings; logs are `reports/settings-request-round-1/active-upload-read-*.log`
below `EMULEBB_WORKSPACE_OUTPUT_ROOT`. No public response shape changed. That
checkpoint did not address thin file metadata or bounded waiting-queue pages.

Rust `85e113f4` computes one waiting client's rank with an allocation-free linear
count instead of sorting a full queue copy. It shares the scheduler's unchanged
score/sequence ordering and preserves stable waiting-order ties at sequence
saturation. The regression compares counted ranks with scheduler ordering at
multiple ages and verifies equal-score ties and absent clients. Full Native
recheck passed 1,514 tests without warnings in
`reports/settings-request-round-1/upload-rank-count-native-recheck.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`.

The preceding run passed the rank regression but failed
`live_plan_replacement_discards_stale_events_and_polls_added_server`: its responder
received a status request where it expected a description request, followed by an
event timeout. The unchanged full-suite recheck passed; the unexpected packet is
unexplained and remains a final-qualification concern. No UDP production code or
acceptance assertion was changed to obtain the passing recheck.

Those prerequisites preceded upload-list pagination. The operator selected
departed-anchor expiry: when the last
returned entry leaves the waiting queue, the caller must refresh from the first
page. Do not continue from its saved rank. The accepted contract is recorded in
[PUBLIC-FOUNDATION](../../design/PUBLIC-FOUNDATION.md). Schema, REST and settings contracts
are unchanged by this checkpoint. No PR or merge is authorized.

## Closed waiting reasons checkpoint (2026-11-21)

Rust `81a4c52e` adds required nullable `waitingReason` to download summaries,
details and creation responses, using only `network`, `sources` or `resources`
while queued and null in other lifecycle states. OpenAPI constraints and the
WebUI discriminated union enforce the same combinations. Browse/detail/create
share the projection. Network policy and explicit binding availability take
precedence over ready preparation evidence. Prepared sources retain only a
scalar deadline on their existing ownership entry; expiry, cancellation,
generation rebind, promotion and drop invalidate that evidence. No source-hint
scan, per-history-job status cache, new worker or persisted field is added.
Schema 108 and settings/CLI contracts are unchanged.

Validation passed: 722 Core and 169 REST executions without warnings; 20 existing
Python OpenAPI-response tests, including every lifecycle/reason combination;
91 WebUI unit and 32 stateful browser tests, type checking and production build.
The existing two-peer preparation fixture proves queued `resources` projections
before payload allocation. A separate test proves a missing explicit interface
reports `network` even with VPN policy off. Windows release build passed with
zero warnings. Logs are `reports/settings-request-round-1/waiting-reasons-*.log`
below `EMULEBB_WORKSPACE_OUTPUT_ROOT`. Live REST conformance passed in
`reports/rust-rest-openapi-ci/20261121T135424Z/report.json`, including 100,000
metadata-only retained jobs, restart-preserved counts and graceful teardown.
Upload-queue pagination, real-payload scheduling/endgame qualification and final
physical-library/platform campaigns remain open. No PR or merge is authorized.

## Download resource summary checkpoint (2026-11-21)

Rust `ee90d905` and `215c75d2` introduce fresh schema 108 and the canonical
`stats.downloadResources` summary across stats/status/snapshot and the WebUI.
Active execution and preparation counts include draining owners. Waiting work
uses a transaction-maintained scalar, excluding stopped, failed, metadata-only,
verified-delivery, removed and terminal jobs; sorted unique selected IDs are
checked by primary key in the same read transaction. Cohort membership, not
retained history, bounds request memory and lookup work. The existing Native
metadata worker accounts for the request backing; no new pool or task per
waiting job is introduced. Concurrency reports automatic/fixed configuration,
current ordinary target and active owners above it. Native resident-cache usage,
soft target and hard ceiling are explicitly separate from total process RAM.

Scoped validation passed: 322 Metadata, 1,513 Native, 719 Core, 169 REST and
112 daemon test executions; the daemon's ignored child-process entry point is
invoked through its parent ownership test. No Rust warnings were reported.
Existing Python suites passed 18 Rust OpenAPI response, 30 REST campaign,
119 shared-library and 145 shared smoke tests. WebUI passed 88 unit and 32
stateful browser tests, type checking and production build. Windows release
build passed with zero warnings.

Evidence: `reports/settings-request-round-1/resource-summary-*.log` below
`EMULEBB_WORKSPACE_OUTPUT_ROOT`; live conformance passed in
`reports/rust-rest-openapi-ci/20261121T132251Z/report.json`, including 100,000
metadata-only retained jobs, 100 waiting jobs, preserved restart counts and
graceful teardown. This does not qualify physical libraries, real payload
displacement/endgame contention, current Linux packages or final 512-MiB/1-GiB
campaigns. Upload-queue pagination remains an unfinished foundation slice.
No PR or merge is authorized.

## Current download provider

Rust `cb35ecac` on the existing foundation branch provides:

- Atomic new-job admission with initial source/name evidence, unchanged active
  duplicates, and no eager piece-map or storage allocation.
  The existing bounded Core owner retains admission, category resolution and
  scheduler notification after caller disconnect. Shared owner refusal occurs
  before durable creation; duplicate responses project stored fields.
- Idempotent native start/stop with job/generation fences and fixed storage.
- A bounded Core owner for start/stop/verify/remove batches. Shared refusal changes no
  jobs; admitted work completes all request-order items after caller disconnect,
  including execution cancellation/wake-up. Results retain their byte charge
  until released. Long verification batches remain quota-bound and profile-owned
  while unrelated commands continue; owner close drains their actual tasks.
- Thin source pages with at most sixteen recent reported names, explicit omission
  flags, a shared 512-KiB name allowance inside the 1-MiB page budget, and indexed
  exact source lookup. Live source scalars do not clone peer part bitmaps.
- Fresh schema 85 with a partial comment/rating index on source job/row ID.
  Comment pages seek this index directly, load neither source-name windows nor
  execution geometry, and preserve continuation across metadata and Core byte
  limits. Generation checks reject stale callbacks/reads.
- Compact detail with recorded delivery path/ownership and bounded storage
  failure information. Reads neither probe files nor grant ownership.
- Part pages derive only the requested expected-geometry window and seek its
  checkpoint rows through the existing primary key. Queued jobs do not hydrate
  execution, full byte presence does not imply verification, and retired
  internal data exposes no synthetic piece inventory. Creation/list/detail share
  one canonical summary projection.
- Atomic name/category/unknown-to-known-size updates in one SQLite transaction.
  Native reader-pinned cache replacements reserve memory before commit; the
  existing Core owner retains publication through caller cancellation. Stale
  progress refreshes authoritative presentation instead of restoring old names.
  Size discovery replans preparation without starting stopped jobs or allocating
  storage. Invalid combinations, delivery-fixed names, and admission refusal
  leave all requested fields unchanged.
- A native completed-output verification provider, separate from partial-piece
  rechecking. It streams the recorded output even after internal retirement,
  forces a fresh hash, reports missing/damaged output, and neither searches other
  copies nor changes history, ownership or intent. Unsupported stable identity
  evidence remains an error.
- Core verification reserves at most two rechecks, excludes scheduler selection,
  cancels/drains the previous execution, and rereads its resulting generation.
  Partial checks reopen only proven existing storage without allocation or
  adoption. Started/stopped intent and storage-failure markers are preserved;
  missing/damaged completed output is reported without reopening history.
  Both successful and failed partial checks release the exact quiesced view,
  including stopped/faulted jobs whose generation need not advance.
- Native job-control receipts follow captured-input and temporary-workspace
  release. Returned data retains its separate charge, so an immediate subsequent
  command cannot race a completed command's workspace. A deterministic regression
  checks capture lifetime, retained-result charge and immediate capacity reuse.
- Fixed persisted download dashboard counters and bounded ID-only notifications.
  Creation, PATCH and controls publish within their admitted owners, including
  after caller cancellation. Subscription/baseline capture is serialized with
  publication; reconnect/lag resets use a new receiver and coherent epoch/revision.
  The 1,024-entry broadcast retains no job rows, and sequence rollover changes
  epoch before numbering restarts. The master specification defines the wire
  contract and client refresh behavior.

Supported gates passed **1,441 ED2K tests and 592 Core unit tests plus all enabled
integration suites**, with no failed or ignored tests. Exact inputs and logs are
under `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/download-verify-core-round-5/`
(`ed2k.log`, `core.log`, `source-freeze.json`). Native produced no warnings; Core
retains fourteen warnings for the remaining consumer cleanup. Normal hooks
passed for the separate native storage/view-lifetime commit `b5bb160f` and Core
verification commit `d55ec249`. Their combined validated source was restored and
hash-checked between commits.

Unchanged metadata/schema gates remain valid: **227 metadata unit plus 3 ownership
tests** under `reports/download-patch-round-1/metadata.log`, and **31 Python
schema/writer tests** under `reports/download-comments-round-1/python-metadata.log`.
Creation-owner cancellation/refusal evidence is retained under
`reports/download-create-owner-round-1/core.log`. Completed-output regressions
under `reports/completed-verification-round-3/` cover retired pieces, same-size
corruption with restored modification time, missing output across restart,
unrelated good copies, and stale/unfinished-job refusal.

Current verification regressions cover scheduler exclusion and actual execution
retirement, cancellation/capacity refusal, continued unrelated commands after
caller abort, ordered mixed outcomes, real stopped and failed-storage payloads,
completed-output failure/history separation, and a 20-job batch larger than the
resident cohort. Native checks also prove that verification cannot allocate or
adopt unknown storage and that releasing stopped/faulted views preserves their
durable state. A bounded independent read-only review found no actionable
ownership/draining/lock-order defect; actual runtime tests provide the evidence
above.

The comment regressions cover sparse evidence among 100,000 source rows with
query-plan proof, rating-only rows, generation fencing, retained native charges,
and metadata/Core byte-boundary continuation without dropped rows or hydration.
Browse regressions add maximum supported file geometry without manifest-cache
population, inclusive tail offsets, presence versus verification, recorded
unowned delivery, removed/unknown jobs, and bounded failure projection without
automatic recovery or timestamp conversion.
Core owner disconnect/capacity evidence is retained separately under
`reports/download-control-owner-round-1/core.log`.

These commits are local and await the coherent REST/application checkpoint
before push. Canonical REST/OpenAPI and caller integration, the accepted adaptive
scarcity/endgame scheduler, final settings/CLI
and Docker wiring, actual held-I/O/resource qualification and combined-scale
checks remain open. The existing fixed live cohort does not qualify the
adaptive target. Python REST producer evidence must be refreshed after
its consumers are converted; no whole-application or 512-MiB acceptance is
claimed. Sustained soak is follow-up under the master specification.

The current counter/notification integration passed **595 Core unit tests plus
all enabled integration suites** and **148 REST unit plus 3 integration tests**,
with zero failures or ignored tests. Evidence and exact source hashes are under
`reports/download-events-round-2/{core.log,rest.log,source-freeze.json}`. Core's
fourteen remaining consumer-cleanup warnings are unchanged; REST produced none.
Cancellation regressions now verify notification publication as well as durable
and cache publication. Further checks cover subscription/publication races,
bounded lag recovery, epoch rollover and HTTP identity-only create/remove frames.
Normal hooks passed for Core commit `937c3cac`; the held REST/SPA work was restored
and hash-checked against the same validated combined source.

The coupled REST consumer conversion remains uncommitted pending the remaining
Rust operator callers and Core consumer cleanup. Snapshot uses fixed persisted
download counters; diagnostic capture uses an indexed bounded download page.
Source browsing currently checks peer capability without performing a browse;
the operator decision to remove that operation or return HTTP 501 remains pending.
No complete application, client or combined-scale acceptance is claimed.

## Current WebUI and OpenAPI integration (2026-11-17)

The held UI reads one current download page (100 rows), with server-side
unfinished/completed/all and category filters, cursor-preserving refresh and
page replacement. Selection and actions use immutable job IDs. Details,
sources, parts and comments use separate bounded resources; no whole history
is hydrated. Root previews request twelve jobs, while global counts come from
the fixed persisted snapshot counters rather than preview length.

Creation submits one tagged source per link and confirms only explicit
`LOCAL_CONTENT_CHOICE_REQUIRED` responses before requesting redownload. Actions
use start/stop/verify/remove batches, with required removal data choice and
failed 207 items surfaced to the user. The existing unit and stateful browser
suites now produce the current requests. Regressions cover page replacement,
retained cursors after refresh, distinct same-hash job selection and late detail
responses. No adapter or indexer implementation is included.

The event consumer uses scalar identity notifications and `downloadEvents`
diagnostics with `downloads.sse` capability names. It retains the exact opaque
SSE cursor, including revisions above JavaScript's safe integer range. Refresh
coalescing is retained; initial reset fixtures use revision zero.

The supported WebUI lane passed **56 unit tests**, **32 browser tests**, TypeScript
checks and the production build. Core passed **595 unit tests and all enabled
integrations**; REST passed **148 unit and 3 integration tests**. Exact combined
sources and logs are retained below the output root at
`reports/download-webui-pages-round-3/{source-freeze.json,webui.log,core.log,rest.log}`.
Hashes were verified after validation and after restoring the held consumer work
around Core commit `cb35ecac`. Its normal hooks passed. The local Kad caller now
retries only typed transient capacity refusal within the existing deadline;
other errors fail immediately and both creations must still be new jobs.

OpenAPI now describes the independent parts array using `sizeBytes` and
checkpointed `presentBytes`, concrete verification/delivery details and nullable
storage failure details. The existing Python route/schema suite passed
**115 tests**, including nonempty part and detail payloads; the unchanged response
helper suite previously passed **4 tests**. The source reader handles shared Rust
allowlists without changing runtime validation.

The daemon package also passed **108 unit and 15 executed integration tests**;
its declared subprocess fixture is skipped as a standalone test and invoked by
its ownership parents. Log: `reports/download-webui-pages-round-3/daemon.log`.
Commit `beb532dd` fixes runtime construction and imports native identity evidence
from the existing opened-file helper. Its normal hooks passed, and held source
restoration was hash-verified. The Core and UI suites remain valid because these
daemon-only changes did not alter their inputs.

The registered release daemon and WebUI bundle built successfully through the
existing Builder owner. The selected-source live REST/OpenAPI campaign passed
with graceful teardown: **79 safe HTTP routes** plus the populated peer-control,
Kad persistence and category/restart phases. The category phase additionally
validated populated download detail, a nonempty checkpointed part page,
source/comment pages and real cursor continuation against the selected OpenAPI
document. Its allocated UUID storage identity survived restart, deleted categories
cleared assignments, and independent complete files remained byte-identical.
This does not claim coverage of every unsafe route in the generic probe budget.

Evidence: `reports/rust-rest-openapi-ci/20261117T170453Z/report.json` and
`reports/download-staged-contract-round-1/{build.log,campaign-populated-pages.log,harness-source-freeze.json}`.
The existing conformance, response-helper and campaign unit suites passed
**31, 4 and 22 tests**, respectively. Harness commits `611012f0` and `a1ddd98e`
passed normal hooks; held campaign source was restored and hash-verified before
its separate commit. The current diagnostics schema uses `downloadEvents`.

The category fixture reuses the proven loopback profile helper and starts the
bounded scheduler before proving allocation. It requires native download PATCH
204 replies, and retains durable job facts on failure. Existing persistence and
file-preservation assertions remain in force.

The next operator-caller slice is committed as Harness `9d22b10c` and
`c16686f4`. Consumer restart evidence retains the rendered workflow's job ID,
checks its hash, and reads fixed global counts rather than enumerating history.
The handoff proof uses the current Stopped control. The local upload helper uses
single-source creation, explicit start batches and the captured job detail;
its `--start-stopped` option has no aliases. Completion requires retained
terminal state, payload verification and delivery state, with exact output size
and SHA-256 when requested. A library hash resource is read directly.

Shared part accounting streams pages of at most 200 rows and retains scalar
cursors/totals, separating bytes present from verified bytes. It refuses repeated
parts and same-hash job substitution. Retired internal pieces do not erase the
durable payload-verification fact or fabricate internal byte presence. Existing
consumer, WebUI-proof, shared-client and upload-helper unit suites passed
**17, 46, 31 and 21 tests**, respectively; both commits passed normal hooks.
These are caller/unit results, not a new live upload, memory-scale or sustained
soak qualification. The earlier source-bound staged REST result remains valid
for its unchanged product inputs.

Harness `e36f2732` converts the wire campaign to captured job IDs, fixed global
counts and bounded source-count lower bounds. Payload verification and delivery
are distinct from piece presence; source growth does not prove source-exchange
packets. The wire suite passed **16 tests**; the shared Rust-client suite passed
**47 tests with one platform-specific skip**.

Harness `17915ec1` converts both VPN smoke callers and their existing common
completion helper. The proof follows the captured job ID and verifies only its
recorded output path, retaining final-rehash log requirements. A failed job
requires operator action. The helper, OpenVPN and Gluetun suites passed
**8, 5 and 8 tests**, respectively. Normal commit hooks passed for both slices.
These are local caller tests; no public-network or VPN campaign was launched.

Harness `5ad74924` converts direct-smoke creation, probes and completion to
captured jobs and recorded output paths; all **21 tests** passed. Harness
`9a12d230` converts the Rust side of bilateral reask proofs, while preserving
the active MFC API. Source absence walks bounded cursor pages and checks the
captured job identity first; all **40 tests** passed. Normal hooks passed for
both commits. No public-network or bilateral live campaign was executed.

Harness `3eeb4156` aligns soak-control SQLite diagnostics with the current
schema. It removes candidate table/column fallbacks, reads fixed persisted job
counts and current source/hash tables, and gathers counters inside one read-only
transaction. Existing source coverage diagnostics now use the durable job
counters too. All **108 soak-control tests** passed, including a database built
from the selected canonical Rust schema whose bytes remain unchanged by the
read. Normal hooks passed. This qualifies diagnostic queries, not the remaining
public-search/download callers or a sustained soak.

Harness `5b391fde` replaces history-scanning download diagnostics with
`public-download-debug-summary --download-id ID`: one exact job read and one
source window (at most 200), with lower-bound count labeling. The shared ID
validator is reused. **114 soak-control and 31 shared-client tests** passed.

Harness `14e079a4` converts the public search-to-download proof to current
`displayName`/`sizeBytes` results, stopped content-job creation, captured job IDs
and explicit start batches. It requires successful per-item receipts, streams
part totals, and samples bounded source windows. Presence, part verification,
whole-payload verification and delivery remain distinct. Completed internal
piece retirement preserves the payload fact; the proof checks the recorded
output size. Failed jobs require operator action. All **119 soak-control tests**
passed, including current creation/start sequencing, stalled candidates,
privacy, substituted-job refusal, failed start items and completion semantics.
Normal hooks passed for both commits. No public download or soak was launched.

Harness `51ee6e36` qualifies the existing local-client integration scenario
against the verified registered runtime bundle, using the selected Rust OpenAPI
and its existing conformance loader. Category names and current job IDs replace
the removed download surface. The scenario proves separate parts/source/comment
pages, atomic metadata PATCH 204, same-job restart persistence, explicit
start/stop receipts and removal while preserving library files. It reuses
`LocalKadPeer` for a real local bootstrap exchange; discovery is explicitly
initialized locally and no Cargo launch fallback remains in this scenario.
The **native integration passed**, and its **two fast tests passed**. Evidence
is retained under `reports/local-client-foundation-round-6/`: JUnit result,
daemon log/profile and stage descriptor with the exact harness SHA-256. The
retained hash matches the committed source. Normal hooks passed. The separate
native server-bind scenario was not run; this is not combined-scale or RSS
qualification.

Rust `dda78579` removes unused Core hydration fields, cancellation/default-state
helpers, the single-category-assignment command path, and transfer PATCH/details
DTO builders. Category omission/null tests use `DownloadUpdate`; the verified
data lifecycle test now reads the current paged parts provider. The removed
parts-view tests belonged to the removed DTO; current metadata part-page tests
retain the presence-versus-verification invariant.

Supported gates passed **593 Core unit plus all 35 enabled integrations**, and
**148 REST unit plus three integration tests**, with zero warnings. Exact source
hashes and logs are retained under `reports/core-consumer-cleanup-round-2/`
(`source-freeze.json`, `core.log`, `rest.log`). Normal hooks passed. The held
REST/WebUI work was restored and its complete recorded hashes checked after the
separate Core commit. No source-bound release bundle was rebuilt in this slice;
the earlier staged live proof remains attributed to its exact older inputs.

Rust `5af2e531` commits the durable download REST resources, opaque bounded
pages, job-ID controls, ID-only events and directly coupled validators/DTOs.
Rust `5c689f76` commits the WebUI job-ID consumers, bounded active-view pages
and independent evidence collections. Both normal commit hooks passed; their
source hashes match the previously qualified REST/WebUI inputs. The Rust
worktree is clean.

The supported registered bundle build passed with **zero warnings**; evidence:
`logs/builds/20261117T183841Z-build-clients/build-result.json` and
`reports/download-committed-baseline-round-1/build.log`. The rebuilt committed
source then passed the loopback REST/OpenAPI campaign with graceful teardown:
`reports/rust-rest-openapi-ci/20261117T184140Z/report.json`. This qualifies the
current committed download slice, not every route against populated state or
the complete foundation. Prior Core/REST and unchanged WebUI test evidence
remains as recorded above.

The Rust download checkpoint is pushed through `5c689f76`; the harness is
pushed through `a21722cc`, on their existing foundation feature branches. The
required harness push gate exposed three Android listener fixture expectations
for an unsupported API error code. The fixture-only correction uses current
`INVALID_ARGUMENT`; all **81 Android tests** passed. The complete required
affected-file push suite then passed **1,205 tests**, with one POSIX-only skip
and four unselected native tests. Evidence:
`reports/local-check/emulebb-build-tests/20261117T184932Z-4454ede5/02.log`.
Rust push checks passed under
`reports/local-check/emulebb-rust/20261117T184408Z-c329caeb/`.

### Library policy persistence baseline

Rust `13cffee3` starts phase 2d with fresh schema **85**. Known hashes own the
default-enabled sharing flag; immutable case-insensitive tag names have internal
SQL keys and indexed many-to-many known-file associations. Explicit writes never
create content/tags implicitly, deletion cascades assignments only, and tag pages
retain at most 200 rows. Policy and associations survive copyless knowledge,
reobservation and reopening. Revision changes roll back with failed writes.

Supported gates passed **234 metadata unit plus three ownership tests**,
**593 Core unit plus all 35 enabled integrations**, and **31 existing Python
metadata helper tests**. Rust produced zero warnings. Logs and exact product
source hashes are retained under `reports/library-policy-metadata-round-2/`.
Normal commit hooks passed. These are persistence/provider results; protocol
request admission, publication filtering, REST/OpenAPI/WebUI and large-library
query qualification are still pending. The previous staged daemon/campaign
remains attributed to schema 84 and its exact recorded commit.

Rust `8013b41e` wires tag creation/read/delete, bounded global/per-file tag
pages and explicit assignment batches through the existing profile coordinator
and blocking SQL worker. It adds no thread, second actor or full tag catalog
cache. Validation precedes admission; shared-capacity refusal precedes mutation.
A conservative 64-KiB response reservation remains charged through projection
and serialization, within the existing 8-MiB profile-owner budget. Admitted
batches complete after caller disconnect; per-item SQL constraint failures do
not skip later hashes. Public tag projections expose names, not SQL IDs.

The supported Core gate passed **598 unit plus all 35 enabled integration
tests**, with zero warnings. New regressions cover retained response charge,
pre-mutation queue refusal, complete work after disconnect, ordered mixed
outcomes and invalid-selection refusal without implicit creation. Exact source
hashes and logs are under `reports/library-tags-owner-round-1/`. Normal commit
hooks passed. REST/OpenAPI/WebUI exposure and sharing-flag protocol enforcement
remain pending; this provider gate does not qualify fatal I/O/commit ambiguity
or 100k/resource behavior.

The operator selected bulk-only tag assignment actions; the authoritative
foundation specification records the accepted endpoints and explicit selection
bounds. No parallel per-file write surface or implicit tag creation is planned.

The full foundation checkpoint remains open. Sustained soak execution is
follow-up work. The current build, loopback campaign and focused gates do not
establish 512-MiB/combined-scale acceptance or the remaining settings, library
and scheduling work. Source browsing still awaits the operator's
remove-versus-501 decision. No PR or merge is authorized.

## Download-engine behavioral feedback (2026-11-16)

The ninth supported ED2K package run compiled the test target without warnings
and executed 1,370 unit tests: **983 passed, 387 failed, zero ignored**. Retained
log: `EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/download-job-ed2k-diagnostic-round-9/rust-unit.log`.
Of the failures, 385 report the same catalog-page-size mismatch, one rejects
incompatible native identity evidence in a fixture, and one has an incorrect
maximum-geometry count. This is the first behavioral feedback for this coupled
job-runtime conversion, not an accepted engine checkpoint. No full application,
platform or combined scale qualification follows from it.

The subsequent complete runs improved to **1,346 passed / 26 failed** (round
10), **1,359 passed / 14 failed** (round 11), and **1,371 passed / 2 failed**
(round 12); all had zero ignored tests and no warnings. Logs remain under
`reports/download-job-ed2k-behavior-round-10`,
`reports/download-job-ed2k-behavior-round-11` and
`reports/download-job-ed2k-behavior-round-12`.
The existing maximum-geometry stream fixture now passes its unchanged 6-MiB
representation assertion; resident admission, result lifetimes and total RSS
are not established by that fixture. Round 12 exposed the missing completed-job
payload catalog source and a name guard that confused payload verification with
terminal job completion.

Round 16 passed **1,376 engine tests**, with zero failures, ignored tests or
warnings (47.23 seconds). The name guard and bounded completed-payload hydration,
rebuild and serving admission now pass their regressions. Source hashes for all
106 pending engine paths and the complete log are retained under
`reports/download-job-ed2k-behavior-round-16` (`sources.json`, `rust-unit.log`).
This is component evidence, not an accepted complete engine/domain cut: ordinary
content mutation publication still selects only local/partial sources and can
withdraw a valid internal-payload offer until refresh. The existing owner must
close that common publication path without unaccounted filesystem work or nested
capacity deadlock. The new cancellation fixture holds a scheduling gate rather
than blocked OS I/O; actual held-I/O, projection/result lifetimes and the remaining
storage obligations below are still unqualified. Core/REST and full application
readiness do not follow from this test pass.

Round 23 closes that mutation publication gap and passes **1,383 engine tests**
with zero failures, ignored tests or warnings (44.61 seconds). Local copies,
verified internal payloads and partial pieces now share coherent publication
across path mutations, finalizers, atomic ingest and category replacement.
The existing registry keeps four units/eight MiB and three filesystem-eligible
units/two MiB; phase transitions drop large buffers and guards before waiting,
and actual lease release wakes capacity waiters independently of task joining.
Payload-result charges follow consumer ownership. The parent verified all 107
pending engine hashes against `reports/download-job-ed2k-behavior-round-23`
(`sources.json`, `rust-unit.log`). Targeted review found retained native-path
backing could exceed the reduced phase charge. Round 24 repairs that finding
with one shared native-path allocation whose existing-capacity lease follows
reservation, scheduled queue, consumer and requeue through acknowledgment.
The maximum-path held-capacity regression passes; the complete gate passes
**1,384 tests**, zero failures, ignored tests or warnings. Evidence and 107-source
receipt: `reports/download-job-ed2k-behavior-round-24`. Final reinspection accepted
that repair and its three matching source hashes. Rust `c23896ee` commits the
107-source coupled job-native engine cut; normal commit/push hooks passed and
the feature checkpoint is pushed. Actual blocked-OS-I/O cancellation,
broader diagnostic-result and resident lifetimes, complete catalog accounting,
Core/REST integration and combined 100k qualification remain unfinished.

Rust `1921823d` retains compact job-read backing through worker reaping, caller
consumption and owned native-path projections using the existing capacity
control. JSON encoding counts output without allocating, admits simultaneous
input/output backing, then writes into fixed-size storage; sixfold escaping and
stateful serializer growth cannot silently exceed admission. The supported gate
passed **1,394 tests**, zero failures/ignored tests, under
`reports/download-job-read-leases-round-2` (`rust-unit.log`,
`source-receipt.json`). Parent inspection found and repaired the initial uncapped
encoder; the prior 1,388-test run is retained in round 1. The commit hook then
required rustfmt's closure-block formatting in source-hint tests; normal hooks
passed after that formatter-only repair. Full execution hydration, resident pins
and other broad memory/storage obligations remain outside this compact-read cut.

Repair catalog callers through bounded keyset pages into the existing indexed
projection, preserving publication fences and partial/hint precedence. Do not
raise the provider cap or rebuild full intermediate vectors. Byte-capped pages
can be shorter than their requested row count: merge using returned frontiers,
advance over rejected stale candidates and prove exhaustion with empty input.
Full-projection lifetime/accounting remains part of the unqualified runtime work.

The fixture review retained current protocol, source-isolation, corruption and
independent-copy assertions. Its exact 59-path receipt is under
`reports/download-job-fixture-conversion-review/sources.json`; the seven-file
before/after comparison is under `reports/download-job-seven-fixture-review`.
Two substantive obligations remain open: wire content-only Delivered recovery
through dedicated verification/ownership-refresh publication, and add a current
staged-attempt/removal/journal test for the intersection no longer covered by the
retired hidden-row fixture. Generic checkpoints must not regain ownership, and
removed jobs must not be resurrected by stale delivery callbacks.

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

### Remaining retained-runtime implementation order

The Metadata provider is qualified separately in
[RUST-CI-044](RUST-CI-044.md#typed-mutation-and-execution-stream-provider-checkpoint-2026-11-16).
That checkpoint does not qualify these runtime ownership boundaries:

1. Keep the existing registry's byte charge alive for the actual returned
   representation, not merely until its task is reaped. Diagnostic receipts
   retain that charge through consumption/serialization, including temporary
   conversion buffers. Selected execution hydration instead builds privately,
   validates the complete stream and current token, then moves into an admitted
   bounded resident. Eviction cannot release resident capacity while readers
   still own its allocation. Do not introduce another pool, queue or actor.
2. Retain bounded payload writes and streaming part verification through the
   existing registry, with the captured token and storage authority through
   checkpoint/cache publication. Stop may invalidate logical execution before
   old filesystem work finishes; restarting that same storage must wait for its
   admitted writers. Unrelated jobs do not wait on that filesystem guard.
3. Retain final rehash and delivery as existing long-filesystem units, using the
   existing prepared representation allowance and cleanup sublimit. Replace the
   remaining whole-manifest delivery checkpoint with a typed transaction that
   checks the captured committed journal snapshot. Preserve per-piece dirty
   acknowledgement, post-commit authority reconciliation and Delivered state
   through verification drift and cleanup retries.
4. Persist output reservation barriers under the existing eligibility fence,
   then process bounded candidate pages and filesystem probes outside SQLite.
   Existing indexes support lexical `(platform, file_name_search_key, id)` and
   native identity `(identity, size_bytes, path_id)` keysets. Read actual primary
   and secondary identity branches separately and deduplicate only the bounded
   current page. Condition each withdrawal on captured job/reservation/path/
   content/fingerprint/root state, bind actual paired identity after exclusive
   creation, and finish required withdrawals before writing bytes. Interruption
   leaves durable pending authority rather than permission to copy again.

These are allocated implementation boundaries, not executed proof. The proposed
6-MiB hydration charge still needs maximum supported geometry/capacity evidence.
At Rust `1921823d`, inspection found that at 28,257 parts, current MD4/AICH character backing
alone needs 20,345,040 bytes for ten residents; even one resident plus existing
hydration/AICH workspaces exceeds the shared 8-MiB allowance. These are arithmetic
lower bounds, not allocator measurements. Exact-source inspection receipt:
`reports/download-job-resident-hydration-round-1/source-receipt.json`.
The [foundation specification](../../design/PUBLIC-FOUNDATION.md#resource-admission-and-discovery)
owns current admission and resident-budget policy: adaptive automatic concurrency,
an optional `maxConcurrentDownloads` ordinary ceiling with a fixed 25% rare-
opportunity burst, a 64-MiB soft resident target, and an initial 128-MiB hard
resident ceiling. Sixteen active plus two preparation slots is a qualification
baseline, not a permanent product count limit. The separate 8-MiB native
transient budget is unchanged. No automatic growth beyond the resident ceiling,
new saved memory setting, pool or actor is introduced; this does not bound total
daemon RSS. The accepted scarcity, completion, endgame and observability policy
is specified there; the fixed-cohort implementation and its existing tests do
not yet deliver or qualify that policy.
Evicted backing remains charged until its final reader drops. Implementation
and qualification remain pending; the accepted budget alone is not gate proof.
Resident groundwork is committed at Rust `615ae950`. The retained evidence is
**210 metadata checks** (207 units and 3 ownership tests, round ten) and
**1,421 ED2K tests** (round eleven), with no failures, ignored tests or warnings.
Source receipt and logs:
`reports/download-job-resident-hydration-round-11/{source-freeze.json,ed2k.log}`;
metadata proof remains in `reports/download-job-resident-hydration-round-10/metadata.log`
with unchanged provider bytes. The normal commit hook passed after formatter-only
repairs to two files; the receipt distinguishes tested and formatted hashes.
The maximum-geometry fixture measured 5,307,260 retained bytes per entry;
eighteen entries require 95,530,680 bytes, or 120,696,504 bytes including four
6-MiB replacement reservations from the existing mutation slots. Round six
passed 1,412 tests and failed the new 64-MiB capacity assertion, justifying the
operator-authorized fixed **128-MiB** cap. The passing capacity regression retains
all eighteen entries and old reader pins while publishing four replacements.
This measures backing capacities, not allocator metadata or total daemon RSS.

The following scoped changes close Native resident-accounting prerequisites.
Core adaptive admission and actual payload/session qualification remain open:

- Rust `cc263416` replaces the weak slot/count registry with direct byte
  reservations. Each backing owns its budget/control identity and job ID;
  immutable readers release their charge only with their last backing owner.
  No per-job slot allocation, weak-node table or Native resident-count limit
  remains. Regressions admit 96 distinct small reservations, retain independent
  reader versions, and reject mutable credits from another job or budget in
  both unique and reader-pinned cases. The 128-MiB ceiling is unchanged.
- Rust `34a59a82` closes the owned-unwrap credit gap in
  `resident.rs::try_edit_owned`: every successful unwrap restores mutable
  allowance before exposing a draft. Refusal returns an intact immutable pin.
  Deterministic tests release a reader after observing shared ownership, then
  prove restoration, pressure refusal, readmission and complete charge release.
  The Windows eD2K suite passes 1,460 executions in
  `reports/settings-request-round-1/resident-owned-frontier-ed2k.log`.
- Rust `181f3c40` moves ordinary persistence into `store_publication.rs` and
  transfers the caller's exact I/O guard through its SQL/cache/checkpoint worker.
  Reserve replacement credit and revision headroom before SQL; conversion and
  backing settlement must succeed before commit. Existing immutable readers keep
  their charges until release. Cache-only publication also settles to actual
  retained backing. Deterministic tests prove precommit pressure/revision refusal,
  metadata rollback on preparation failure, competing-writer exclusion after
  caller cancellation, retained old reader pins and final backing-charge release.
  Rust `7a6d5e89` prepares this handoff with retainable scoped guards: the exact
  mutex and registry key live through the last guard owner. It also fixes private
  hydration to acquire content before category, matching store/cache publication.
  A deterministic test proves a category writer can finish while hydration waits
  on held content. Guard tests prove retained exclusion, unrelated-key progress
  and exact registry retirement; the existing 100,000-key churn test also passes.
  Windows validation passes 1,462 eD2K and 688 Core executions in
  `reports/settings-request-round-1/retained-io-lock-order-ed2k.log` and
  `retained-io-lock-order-core.log` in that directory. The ordinary-store handoff
  is now wired by `181f3c40`. Progress SQL preserves authoritative shared
  comment/rating/upload-priority fields rather than restoring a stale snapshot.
  Verification and salvage publish catalog geometry only after successful
  persistence, and the final SQL fence supplies current presentation and AICH
  authority even when the caller retains an older proposal. Regressions prove a
  refused whole-piece store cannot advertise uncommitted ranges and a stale
  catalog refresh cannot undo an operator edit.
  Windows validation passes 1,466 eD2K, 312 metadata and 688 Core executions in
  `reports/settings-request-round-1/ordinary-store-catalog-ed2k.log`,
  `ordinary-store-catalog-metadata-final.log` and `ordinary-store-catalog-core.log`
  in that directory. After the eD2K run, only two metadata-test callback signatures
  and their formatting changed; metadata/Core checks and the mandatory commit
  hook cover those repairs. No production bytes changed after that eD2K proof.
  The cancellation proof covers SQL/cache/checkpoints; catalog refresh remains a
  caller-owned follow-on. Ordinary blocking stores retain the profile lease but
  are outside the local-mutation registry drain. Hosted owners must drain their
  Tokio runtime, as required by the hosted shutdown contract; final-source
  shutdown qualification remains required.
- Rust `144081e7` replaces checkpoint dirty-piece tree nodes with a geometry-sized
  bitmap. Exact word backing is admitted to the existing resident budget before
  allocation and remains charged through the checkpoint owner's lifetime, even
  when acknowledgment clears every bit. Maximum supported geometry needs 3,536
  bytes. Duplicate marks and acknowledgments allocate nothing. All supported part
  positions remain representable; no new file/job/library limit is introduced.
  Ordinary stores prepare replacement bitmaps before SQL. Piece checkpoints
  prepare missing bookkeeping before their SQL commit. Cache-only publication
  validates the live execution, admits backing and checks revision headroom
  before publishing cache and dirty state under their existing locks. A stale
  stopped callback cannot recreate either half. Checkpoint state is no longer
  freely cloneable into uncharged bitmap backing.
  Windows passes all 1,468 eD2K and 688 Core executions in
  `reports/settings-request-round-1/checkpoint-bitmap-ed2k-final.log` and
  `checkpoint-bitmap-core.log` in that directory. New regressions cover every
  maximum-geometry part, duplicate marks/acknowledgments, retained empty backing,
  final release and bitmap-credit refusal before SQL/cache mutation. The existing
  stopped-callback regression caught premature preflight insertion; the validated
  common publication path repairs it and the full rerun passes unchanged.
  Slot/map/cache/checkpoint-table allocations remain outside the bitmap proof.
- Rust `c910046c` replaces the in-memory checkpoint HashMap with resident-charged
  sorted entry storage. Lookups use binary search; membership insertion/removal
  shifts entries only for selected execution bookkeeping. The fixed backing
  allowance and actual Vec capacity remain charged, including unused capacity.
  Growth reserves peak old-plus-new backing before moving entries and frees the
  old buffer before returning its credit. Failed admission preserves the table.
  Ordinary SQL owners claim insertion space before commit. Concurrent accepted
  claims reserve enough capacity for every owner; cancellation releases its
  claim without an async lock. Claimed publication performs no new admission or
  storage allocation. Last removal frees an empty buffer when no claim needs it;
  rollback-only spare remains fully charged until the next edit or table drop.
  Checkpoint bitmaps retain their independent charges. Native token ordering is
  derived from job ID and generation; SQLite and public ID shapes are unchanged.
  Windows passes 1,472 eD2K and 688 Core executions in
  `reports/settings-request-round-1/checkpoint-table-ed2k.log` and
  `checkpoint-table-core.log` in that directory. Regressions cover 64 storage-only
  entries, retained spare capacity, final release, competing claims plus rollback
  at a full budget, old-plus-new peak refusal and actual ordinary-store refusal
  before SQL/cache/checkpoint publication. Existing caller-cancellation and
  competing-writer tests also pass with the claimed table. This does not qualify
  more than eighteen selected jobs or close manifest-cache/slot accounting on
  that source revision.
- Rust `ea8d4477` applies the same resident-charged table to the manifest cache.
  Ordinary stores retain cache and checkpoint insertion claims before SQL.
  Selected hydration claims its activation space before the observed-availability
  publication callback. Identity refresh and cache-only progress also claim
  before activation. Cache readers, eligibility projection and category/scalar
  publication share this one cache; fixture construction admits the same storage
  instead of inserting through an uncharged test map. No new worker or budget is
  introduced, and no public contract or schema changes.
  Windows passes 1,475 eD2K and 688 Core executions in
  `reports/settings-request-round-1/resident-cache-ed2k.log` and
  `resident-cache-core.log` in that directory. New regressions isolate cache
  growth refusal before SQL with checkpoint space already reserved, refuse
  selected-hydration activation at a full budget, and prove eviction releases
  entry storage while old reader backing remains charged through rehydration.
  Full owner release returns every charge. Existing competing-writer,
  cancellation, stopped-callback, dirty-progress and scalar-patch tests pass.
  The slot registry and category-batch reservation plan remain outside this proof.
- Rust `cc263416` also prepares category replacements at their actual retained
  size, with charged plan-vector backing. Core/root preparation and DB queue
  waiting hold only the existing category fence. After dequeue, the blocking DB
  owner acquires the cache, prepares every selected immutable replacement before
  SQL, and retains that exact cut through commit and synchronous publication.
  Readers and writers cannot invalidate the prepared cut. Budget refusal occurs
  before durable mutation; publication requires no new admission or allocation.
  Scalar download patches keep their single-member mutable credit and existing
  lifecycle/I/O/content/category fences.
  The 32-member category regression proves small replacements use less than one
  MiB together, preserves old reader values, parks an arriving reader and ordinary
  writer across the SQL cut, and finishes publication at a full resident budget
  after observer cancellation. The writer subsequently retains the new category
  and its own progress. Windows passes 1,477 eD2K and 688 Core executions in
  `reports/settings-request-round-1/category-byte-admission-ed2k.log` and
  `category-byte-admission-core.log` in that directory.
  A bounded independent source review found no reachable lock/queue cycle:
  category SQL/publication must remain independent of Core replies, root-epoch
  waits and catalog locks while the cache is held. Hydration/AICH metadata
  callbacks use preheld cache guards; ordinary upsert, ingest and control finish
  metadata calls before reacquiring cache. Preserve that order. Metadata
  contention, SQLite waits, category/root updates and fsync can temporarily stall
  the global cache during this administrative operation. No latency target is
  claimed; no new worker, budget or retry machinery is introduced.

Rust `a9dfbdf3` closes Core's unsuccessful-hydration retirement gap before raising
admission ceilings. `ensure_job` can establish a Native storage session before
resident hydration refuses; returning directly from that outcome abandoned
temporary ownership across repeated queue selections. Empty/failed hydration now
uses the same retirement as a settled network worker: cancel producers, retire
UDP state, checkpoint/release the Native execution, and release source-file
ownership before dropping the attempt guard. Successful hydration keeps its
execution. Busy/Closing deferral and an empty outcome preserve healthy started
intent; genuine preparation storage errors retain their explicit-start failure.
If cancellation wins an allocation reply, both the guard and canceled attempt
record the Native generation for retirement while callback authority stays
revoked. The guard's immutable content identity is available without a hydrated
Transfer value.

Windows passes 690 Core executions in
`reports/settings-request-round-1/selection-hydration-retirement-core-final.log`.
Outcome-boundary tests use real begun Native storage/cache state, then exercise
empty, Busy, Closing, storage-failure and successful hydration results. They prove
generation retirement, removal of old cached views, preserved runnable/manual-
fault policy, retained attempt ownership through cleanup and successful execution
continuity. The cancellation rebind test checks recorded generation, revoked
selection and eventual slot release. These are retirement-policy tests, not
actual memory-pressure or higher-concurrency payload qualification; Native's
existing admission-pressure proofs retain their own source evidence.

Rust `64917f38` implements the ordinary adaptive admission layer. Memory-only
host/cgroup sampling shares the scheduler clock and uses the existing blocking
pool. Scalar Native samples expose charged resident/transient bytes, available
mutation units and connection usage without taking a cache or SQL lock. Finished
mutation tasks are reaped before sampling capacity. The initial active baseline
can grow beyond 16, one saturated sample at a time, within host/connection bounds
and any positive configured limit. Pressure drains admission without cancelling
owned work. Preparation and active work share the overall capacity; resident
construction keeps update headroom and actual producers still reserve bytes.

Windows passes 697 Core and 1,477 Native executions without warnings in
`reports/settings-request-round-1/adaptive-admission-core.log` and
`adaptive-admission-ed2k.log`. New checks exercise growth, configured ceilings,
shared capacity, resident/connection/I/O exhaustion and gradual recovery.
Builder `98fa3d2` permits resolving newly added registry dependencies through its
existing explicit lock-authoring flag; ordinary validation remains locked.
Its scoped tests and mandatory push checks pass.

Rust `770b1484` repairs a test-only strict Clippy assertion; 312 Windows metadata
executions pass in `reports/settings-request-round-1/adaptive-gate-metadata.log`.
Its GNU AMD64 gate passes strict workspace Clippy, packet-diagnostics, release
build, 3,349 workspace executions and three VPN egress tests. Evidence is under
`reports/rust-linux/gnu-amd64/81a2037abd804dacb0331eef1295eb76/`.
Non-root runtime smoke passes in
`reports/rust-linux/gnu-amd64/4d8e5014a8564f269dd2e6cf99501fbd/package-smoke.json`,
including a 12-MiB local download, partial restart, exact output hash, retained
completion, library registration and graceful shutdown. Public discovery is
disabled; this is not public-network or higher-concurrency qualification.

Rust `949b9e26` makes the three file-request encoders consume only geometry and
streamed verified bits. Payload startup calls the same encoders, with no extra
bitmap allocation. Probes can therefore use compact database status without
constructing a resident execution manifest or duplicating protocol encoding.
Absent bits never imply verified data; the exact-multiple EOF slice is complete.
Windows passes 1,480 Native executions without warnings in
`reports/settings-request-round-1/compact-request-status-ed2k.log`. The new
regressions assert wire bytes, byte-boundary/EOF behavior, absent status and
geometry-bounded consumption/output. Existing listener/download cases still pass.
GNU package evidence above retains its exact earlier source revision.

Rust `82487d53` adds the Native availability-probe component for directly
dialable peers, sharing normal transport, negotiated request encoders and
secure-ident handlers. Two shared try-only preparation permits and global
connection/rate admission precede socket creation. A total deadline and finite
packet allowance retire stalled/flooding peers. No job generation, resident
manifest, temporary storage, upload-queue request, hashset or payload request is
created. Replies retain the actual HELLO identity and validated data-part status;
filename-only completeness applies only to one-part files. Hints alone cannot
establish useful-part availability.

Windows passes 1,489 Native executions without warnings in
`reports/settings-request-round-1/peer-availability-probe-ed2k-final.log`,
including socket-level no-payload/storage, refusal, cancellation/deadline and
control-flood cases, plus malformed/conflicting metadata and EOF normalization.
GNU workspace/all-target diagnostic collection builds successfully and reports
no Rust warnings/errors in
`reports/rust-linux/gnu-amd64/47e6530a8f1c41a4a8522e5c59648b1c/`.
Its receipt remains diagnostic-only (`qualityGatePassed:false`,
`packageProduced:false`), not strict package or runtime proof. Core has not yet
adopted the probe. The next integration must persist observations under current
job generation/intent authority before ready admission; callback-only sources
and bounded shared discovery remain part of that work. No public REST/config or
schema change is made by the component.

Rust `5f31a6c5` adds the durable Native observation boundary in fresh schema 107.
The compact `download_job_source_availability` record cascades with its source,
stores packed data-part status plus observed identity/generation/session/time,
and is read through byte-bounded retained keyset pages over observed rows.
Discovery hints cannot establish readiness. Transactional writes and reads fence
current runnable intent, generation, geometry and source identity; queries also
fence runtime session and the caller's explicit freshness interval. Geometry is
derived from saved size/part size before execution preparation, without requiring
the execution part count to be initialized. No migration path is introduced.

Source/name/status deltas now reserve only transient work; only an explicit
rename reserves resident write credit for cached publication. The existing owned
blocking delta retains its guard and capacity through SQL after observer loss.
Windows passes 316 metadata, 1,491 Native and 697 Core executions without warnings:
`reports/settings-request-round-1/source-observations-metadata-geometry.log`,
`source-observations-ed2k-cohort.log` and `source-observations-core.log`.
The tests prove sparse observed-row seeks among 100k hints, byte-bounded complete
paging, stale identity/session/generation/intent fences, rollback/cascade,
cancellation completion and writes at exactly 128 MiB of charged resident
backing. Reopening requires new observation evidence. These are scoped Windows
results; earlier platform and capacity receipts retain their actual revisions.
Core's direct preparation below consumes these observation APIs. Callback
preparation and complete ready-job ordering remain open.

Rust `af4bef8f` retains an owned prepared peer across Native probe/payload
handoff. Its socket, connection/preparation permits, observed HELLO/SUI state and
at most two metadata answers have one non-cloneable owner. Dropping it closes
the socket before releasing permits. Promotion releases preparation capacity,
checks job/content identity and uses the normal download session on that socket.
Already-received metadata passes through normal AICH/name/part-status handlers
before additional startup requests, including for a cached hashset. Temporary
probe buffers can be dropped; the prepared owner satisfies `Send + 'static`.

Windows passes 1,493 Native and 697 Core executions without warnings in
`reports/settings-request-round-1/prepared-peer-handoff-ed2k-owned.log` and
`prepared-peer-handoff-core.log`. The socket case persists real observed status
and downloads 128 KiB on the original TCP connection, without repeated HELLO,
file request or redial; live part availability is preserved. Drop, identity
refusal, input lifetime and no-needed-parts-before-queue ordering also pass.
These are component proofs, not scheduler, large-file/AICH, callback-preparation
or pressure/higher-concurrency qualification. Core adoption below reuses this
connection admission and source lease/retry machinery. Schema 107
and public REST/settings contracts are unchanged in this checkpoint.

Rust `3306ca5b` adds the Core promotion/execution boundary. Preparation promotes
the same attempt guard before resident/storage hydration, preserving its nonce,
generation and cancellation. Refusal retains preparation ownership; existing
active work drains after a lower admission window. The direct-download driver
can consume a one-shot prepared future under its existing worker quota without
acquiring another connection permit or redialing that endpoint. Other sources
retain their normal retry behavior and common result handling.

Windows passes **702 Core executions**, without warnings, in
`reports/settings-request-round-1/core-prepared-execution.log`. Five new cases
cover promotion refusal/drain/cancellation, full connection-budget reuse,
endpoint deduplication, worker-panic drain and content-mismatch cleanup. Normal
commit/push hooks passed. The production consumer is described below; this
component gate alone does not qualify discovery. Schema, public contracts and
memory ceilings are unchanged.

Rust `15148425` provides the compact local status needed before probing a
known-size waiting job. One SQLite snapshot checks current generation, runnable
intent and healthy nonterminal storage, derives data-part geometry and reads
verified checkpoints through the existing job/piece primary key. It neither
hydrates a manifest nor opens piece files. Present but unverified bytes remain
false; geometry and verified extents are checked before use. The existing Native
read owner reserves 128 KiB before allocation and retains that transient charge
with the returned status. No schema or public API change is required.

Windows passes **319 metadata and 1,494 Native executions**, without warnings,
in `reports/settings-request-round-1/waiting-verified-parts-metadata-final.log`
and `waiting-verified-parts-ed2k.log`. Tests cover stale/stopped/unknown/retired
jobs, exact-multiple geometry, presence versus verification, extent corruption,
allocation bounds and a 256-GiB waiting job with no manifest, storage or resident
charge. The transient charge survives worker reaping and ends with result drop.
Normal hooks passed. Production direct preparation below consumes this read.

Rust `0181e102` connects direct preparation to production scheduling. Known-size
jobs enter the bounded preparation cohort before hydration. Discovery accepts
scalar job targets rather than hydrated transfer rows; remembered endpoints are
read and projected in charged pages. The common source registry retains lease,
dead-source and NNP/reask rules. Useful observed parts promote the same attempt
guard and connection into execution; endpoint authority follows the committed
hydration generation. Discovery can retain hints without construction headroom,
but avoids probing when the cohort cannot currently admit execution. The job
cursor stops at the last considered row when preparation capacity is exhausted.
Preparation observation authority grants no passive-request or payload authority.

Windows passes **704 Core executions**, without warnings, in
`reports/settings-request-round-1/core-source-preparation-final.log`. The regular
daemon/WebUI build passes with zero warnings in
`logs/builds/20261120T054316Z-build-clients/build-result.json`. The existing
Python REST/OpenAPI campaign passes with graceful teardown:
`reports/rust-rest-openapi-ci/20261120T055818Z/report.json`. Harness `08fc73e8`
contains the tested fixture bytes; its 30 Python tests and normal hooks pass.
Real local active/queued peers prove UUID/category temp storage materialization,
preservation after category deletion and identity persistence after shutdown.
The source-less category fixture proves a reserved SQLite pathname/UUID remains
unmaterialized across stop/restart; it does not confuse a plan with filesystem
ownership. Settings CLI, Kad, search, sharing and 100k retained-job checks pass.

This does not qualify full prepared multi-file payload completion,
callback preparation, global ready/scarcity ordering or pressure/capacity tiers.
Callback-only discoveries retain their existing execution route. The next
callback integration must keep the inbound dispatcher, connection guards and
callback claim in the listener task, pass bounded availability plus a one-shot
start receipt to Core, and fence that receipt to the exact preparation request
and successor job generation. Do not persist an inbound ephemeral port or a
server LowID as a directly dialable endpoint. A bounded read-only specialist
review resolved this ownership question and finished; the parent owns implementation.

Rust `79bfbc35` connects prepared sockets to the same Native A4AF file-switch
loop used by ordinary outbound connections. Connection profile, secure-ident
state and observed identity carry across files; file-specific state is reset by
the existing session constructor. Core passes the selected alternate plans and
consumes the normal per-file report, including earlier NNP/FNF outcomes when a
later file fails. The prepared primary's cached metadata is consumed once;
there is no extra HELLO, connection admission or redial.

Windows passes **1,495 Native and 704 Core executions**, without warnings, in
`reports/settings-request-round-1/prepared-a4af-ed2k-contract.log` and
`prepared-a4af-core.log`. Socket cases cover NNP-to-FNF switching, a later close
reported as accepted-but-incomplete, and a malformed later reply retaining the
earlier outcomes plus a terminal error. They check the observed identity on
each result and release of connection/preparation permits. Existing ordinary
A4AF, prepared single-file payload and other Native suites also pass. Normal
hooks passed. This is scoped Windows evidence, not multi-file payload/endgame,
pressure, final package/platform or memory-tier qualification. The earlier
daemon/WebUI/REST receipts remain evidence for their actual Rust `0181e102`.
Schema 107, settings and public REST contracts are unchanged.

Rust `ff351aec` fences inbound callback acknowledgment to the job token and hash
captured before peer I/O. Completion neither rereads a mutable queue head nor
consumes a replacement generation or a redownload job with the same hash.
Copies of the captured execution across matching callback routes are still
consumed together. Repeated acknowledgment cannot consume the next execution;
unacknowledged replacement work remains owned and returns to `NeedsDispatch`
when the listener claim finishes. No extra worker, database row or public field
is introduced.

Windows passes **1,497 Native executions**, without warnings, in
`reports/settings-request-round-1/callback-execution-ack-ed2k-final.log`.
Regressions cover generation/job-ID replacement and mixed-generation copies
across routes, alongside the existing listener, dispatch/drop and A4AF callback
cases. Normal hooks passed. This is the execution-acknowledgment prerequisite,
not deferred callback preparation: the Core-controlled handshake, exact preparation
request identity, one-shot Core start receipt and listener settlement remain
required. Earlier Core/build/REST receipts retain their actual revisions.
Schema 107, saved settings and public APIs are unchanged.

Rust `6385fa17` shares the bounded metadata exchange between outbound preparation
and listener-owned callback sockets. Accepted preparation uses compact job/part
reads, retains the existing preparation quota with its linear result and leaves
the socket in the listener. It performs no manifest/storage hydration, outbound
connection admission, upload-queue join or payload request. Cached metadata and
security state feed the normal session once consumed. Existing callback
executions preserve incomplete-close/timeout and A4AF-tail disposition; neither
is availability proof, and an interrupted framed read closes the socket.
Prepared sessions can send the negotiated standalone SX2 request omitted during
metadata-only preparation, with the actual sent flag preventing duplication.

Windows passes **1,498 Native and 704 Core executions**, without warnings, in
`reports/settings-request-round-1/accepted-probe-ed2k-closure.log` and
`accepted-probe-core.log`. The accepted-socket cases cover availability without
resident/storage growth, quota refusal before metadata I/O, wrong-content
refusal and quota release. The existing prepared payload case now verifies one
standalone SX2 request before queue entry and completion on the same socket.
Normal commit/push hooks passed.

The same clean Rust revision passes the strict **GNU AMD64** package lane:
workspace Clippy, packet-diagnostics, optimized release build, **3,384 workspace
tests plus 3 VPN egress tests**, and the non-root runtime smoke. The one ignored
workspace entry is the isolated subprocess fixture used by ownership regressions.
Rust gates pass; upstream C dependency warnings remain visible in the logs.
Build/test evidence is under `reports/rust-linux/gnu-amd64/e81ab868b66e47c387cd931bf4d17c1b/`.
Runtime evidence is
`reports/rust-linux/gnu-amd64/d2fe4b66e6c0410c9d28625c0ff70554/package-smoke.json`.
It records exact Rust `6385fa170d7442174bff85a38659c6df1497f53a` and Harness
`08fc73e865cb2e098d910b764743d5048ee31849`. A 12-MiB local direct download preserves
its verified first part across same-profile restart, resumes, delivers exact
SHA-256 bytes, registers the output, retains completion and shuts down gracefully
three times. Public discovery is disabled. The archive SHA-256 is
`3926fc3239da0bef41e14f0361685b3104d528052c034367ac98c774491011dd`.
This is local package evidence, not publication or rendered-WebUI proof.

Rust `849b58ef` adds the bounded Native callback admission handoff. Two pending
registrations carry opaque request identity, an absolute deadline and one-shot
start/skip/cancellation channels. The listener retains the socket, callback claim
and metadata while Core decides. Start verifies the authoritative current job
token and content before payload; exact request acknowledgment preserves newer
registrations. Preparation capacity follows the listener through cancellation,
is released before settlement notification, and leaves preparation accounting
when execution starts. No per-waiting-job tasks or new saved settings are added.

Windows passes **1,503 Native and 704 Core executions**, without warnings, in
`reports/settings-request-round-1/callback-admission-ed2k-receipts.log` and
`callback-admission-core.log`. Real-socket tests prove no early payload or storage
hydration, same-connection completion with a newer execution token, skip and
cancellation. Capacity and replacement-request fencing have unit coverage.
The commit is pushed and normal hooks pass. GNU evidence above remains scoped
to `6385fa17`; this newer handoff has not yet run that lane.

Rust `877534e7` removes the hydrated-transfer input from Kad buddy and direct
UDP callback dispatch. Shared scalar job/content authority constructs requests
for all three route families and preserves an optional preparation identity.
The real UDP test registers preparation for a fresh started job, dispatches the
exact callback frame with UDP reask disabled and proves no storage, resident
cache, transfer-row hydration or execution-generation change. All **704 Core
executions** pass without warnings in
`reports/settings-request-round-1/callback-scalar-core.log`. Normal hooks pass
and the commit is pushed. Rust `80a29803` extracts server dispatch into the shared
callback owner, retaining current server-route generation, HighID, cooldown and
dispatch-settlement rules. The real UDP test also proves exact global callback
bytes, suppression of an already-pending request and cancellation before
dispatch, with the same no-hydration assertions. The first run found the fixture
still used a documentation-only bind address; the corrected loopback fixture
passes all **704 Core executions**, without warnings, in
`reports/settings-request-round-1/callback-server-core-final.log`. Normal hooks
pass and the commit is pushed. This enables reuse by waiting preparation but
does not implement its scheduler producer.

Rust `70dafa72` wires preparation before hydration into Core selection for direct
UDP, Kad buddy/FINDSOURCE and server callbacks. The bounded producer retains only
metadata until needed parts and resource admission permit hydration, then sends
the rebound execution token to the existing listener. It supervises/drains
FINDSOURCE work and settles callback receipts on refusal, cancellation, shutdown
and the gap between hydration and first execution. Known-unavailable dispatch
does not consume the callback wait; joined/ambiguous dispatch and fast inbound
claims still wait for their exact receipt. Inbound ephemeral ports and server
LowIDs do not become direct endpoint hints.

Windows passes all **704 Core executions**, without warnings, in
`reports/settings-request-round-1/callback-producer-core-settlement.log`. The
existing UDP fixture covers pending producer cancellation and shutdown, no early
storage/resident/generation change, both Native preparation slots available
before return, and immediate completion without a route. The existing Kad swarm
two-file delivery case also passes. Normal hooks pass; the commit is pushed.
Native same-socket start/skip/cancel evidence remains separately scoped above;
full Core callback payload/pressure and current GNU/platform qualification remain
open.

An earlier run, `callback-producer-core-final.log`, failed the swarm delivery
deadline: one started job remained queued with zero geometry and no storage
fault while the second delivered. Later changed-source passes do not prove its
cause. Source review confirms a relevant ownership gap: unsuccessful hydration
drops the prepared peer and retires execution, but leaves the 20-minute source
reask stamp. Busy intentionally preserves healthy Started intent, so this local
refusal can lose useful capacity until another permitted network reask.

Rust `df7f02e8` retains the existing ready owner, guard and lease across temporary
local admission/hydration refusal. Begin/rebind is separate from remaining local
hydration and runs once; Busy retries only the refused local phase on the shared
clock. Source endpoint ownership follows that first rebind. Read loans and the
category gate do not cross waits. Direct admission is bounded by the configured
connect timeout (ten-second minimum) from availability; callbacks retain their
original ticket deadline. Cancellation, shutdown and expiry use normal producer
settlement and retirement. Local hydration no longer demands a second connection
slot for an already-owned socket. Cooldowns, discovery and network probes are
not reset or repeated.

Windows passes **707 Core executions**, without warnings, in
`reports/settings-request-round-1/prepared-hydration-core-baseline.log`. The new
injected post-begin Busy regression checks one generation, preserved/rebound
lease, released category gate, unchanged resident baseline and unmaterialized
storage, then recovery or cancellation/shutdown/expiry. The real local eMuleBB
seed test retains its prepared socket during the wait and delivers exact bytes
before the still-active 20-minute reask cooldown could permit another probe.
The completed job has no storage fault or additional selection generation.
The existing Kad swarm also passes. Initial test repairs corrected derived-part
versus materialization assumptions and use the actual thin-content resident
baseline. The fixture disables Kad via the existing canonical settings helper
and uses only loopback endpoints. Normal hooks pass; the commit is pushed.

This closes the demonstrated local-Busy handoff gap at Windows component/local
integration scope, without proving the cause of the earlier swarm failure.
Rust `a3295661` removes two needless return statements caught by strict Clippy;
the complete **GNU AMD64** lane then passes workspace Clippy, packet-diagnostics
checking, optimized release build, **3,392 workspace tests plus 3 VPN-egress
tests**, and non-root package smoke. The one ignored ownership entry is the
isolated subprocess fixture invoked by its regression parents. Upstream C
dependency warnings remain logged; strict Rust checks pass. Exact build/test
evidence is under
`reports/rust-linux/gnu-amd64/c81883508cab4490a8c0114fa2816962/`.

Runtime receipt:
`reports/rust-linux/gnu-amd64/9dc6e2deb84c490fa5b0e8c791e5b7ab/package-smoke.json`.
It records exact Rust `a32956617901ed30b887ca22665c442d70d408b3` and Harness
`08fc73e865cb2e098d910b764743d5048ee31849`. Real local-source delivery matches the
12-MiB payload SHA-256; verified bytes and part zero survive same-profile/binary
restart, explicit start completes delivery, and output registration/completed
history persist. Three shutdowns are graceful and public discovery is disabled.
Archive SHA-256:
`396e7812debddc448948c96dce4bbaae804473687eb84a95d5d09f7351015a6d`.
This is local qualification, not publication or rendered-WebUI evidence.

Current musl/Android/other platform gates, callback-payload/held-I/O pressure cases
and full scheduling qualification remain required. This checkpoint does not
qualify multi-file payload/endgame, adaptive pressure, either final memory tier,
musl, Android-target or other outstanding platforms. Schema 107, saved settings,
CLI and public REST contracts are unchanged.

Rust `75c4ed40` updates the existing within-file picker and actual block lease
path to rank measured scarcity first, then started/preferred work among equally
scarce parts, then bytes left to finish started work. Untouched ties are stable.
Unknown frequency is not rarity; verified and empty protocol slices are excluded.
Preferred-part affinity cannot bypass observed scarcity, including during the
ordinary-gap and endgame-takeover passes.

Windows passes **1,509 Native and 707 Core executions**, without warnings, in
`reports/settings-request-round-1/part-scarcity-ed2k-final.log` and
`part-scarcity-core.log`. A real block-reservation fixture verifies both rarity
before affinity and affinity among ties. Picker regressions cover unknown
frequency, started interior parts, untouched short-tail ties and empty slices.
Existing hashset/AICH wire and Core local-seed/Kad delivery cases pass. Normal
hooks pass and the commit is pushed. Schema 107, settings and public contracts
are unchanged; the preceding GNU receipt remains scoped to `a3295661`.

Rust `5c102cde` introduces bounded ordinary ready admission. Preparation and active
execution use separate task sets on the existing Tokio executor; guards account
for pending/ready preparations under the same two-slot allowance. Ready work
retains its connection until promotion or settled cancellation/expiry. Ordinary
selection uses remaining bytes and rotating creation-ID ties. Preparation is
independent of a full ordinary payload ceiling, while promotion still requires
ordinary capacity and respects drain limits. Shutdown settles preparation results
and ready owners before draining active execution.

All **708 Core executions** pass without warnings in
`reports/settings-request-round-1/ready-admission-core.log`. A two-seed fixture
holds the single ordinary slot, confirms two retained connections without storage
or generation allocation, then proves the smaller later-created job starts first,
both files deliver and disconnect releases their connections. Existing Busy
recovery and Kad swarm cases pass. Normal hooks pass; the commit is pushed.
No schema, setting or public REST shape changes are introduced. GNU qualification
above remains scoped to `a3295661`, preceding this ready-cohort change.

Rust `9c9f498d` completes exact source-lease settlement for Native no-socket probe
deferral. Monotonic lease identity and job-token fences prevent stale cleanup
from releasing a newer reservation or erasing its cooldown. Explicit capacity
refusal permits immediate reacquisition; real/ambiguous attempts retain their
reask stamps, and candidates and No-Needed-Parts holds survive settlement.
All **711 Core executions** pass without warnings in
`reports/settings-request-round-1/probe-deferral-core-final.log`, including a
real Native forced-capacity refusal, Core reacquisition/stale-release checks and
same-clock registry replacement. The initial full run exposed a test race in
the preceding ready-order fixture: two connections did not prove completed
metadata preparation. A test-only ready-cohort count now synchronizes that
fixture without weakening ordering, hydration or delivery assertions. Normal
hooks pass; the commit is pushed. Schema 107 and public contracts are unchanged.

Rust `de0738a6` adds measured direct-ready reporter scarcity. A bounded Native
metadata read streams all matching observations in one SQLite snapshot, unions
parts by selected identity versus other identities, and excludes verified parts
and protocol padding. Repeated endpoints do not multiply reporters. Current
generation, intent, runtime session and a 30-second freshness interval fence
proof. Two protocol-bounded bitsets and the existing 128-KiB transient read
reservation avoid manifest hydration, per-waiting-job state or a new worker pool.
Core refreshes proof before ready ranking and prioritizes rare opportunities
over remaining bytes; ordinary ties retain the rotating creation-ID policy.

**320 metadata, 1,509 Native and 712 Core executions** pass without warnings in
`reports/settings-request-round-1/reporter-scarcity-metadata.log`,
`reporter-scarcity-ed2k.log` and `reporter-scarcity-core.log`. Tests cover duplicate
identity endpoints, competing proof beyond one maximum-geometry diagnostic
page, verified/padding/stale/session/generation exclusion, full resident-budget
reads, reopened-session invalidation and real two-seed ready ordering with both
payload deliveries and disconnect cleanup. Normal hooks pass; the commit is
pushed. Schema 107 and public contracts are unchanged. Callback-only readiness
still lacks equivalent persisted evidence and receives no inferred rarity
advantage; active part-frequency identity deduplication is also not yet done.

Rust `54567712` includes live callback proof in ready scarcity without persisting
an inbound socket or LowID as a direct source. Core keeps the accepted identity,
shared bounded bitmap, size and captured time until admission. The common
metadata read checks current job authority/geometry, excludes verified parts and
other identities, and lets a live reply supersede older same-identity status.
Native checks the 30-second proof lifetime before work and again after receipt;
contention cannot renew it. Worker backing stays under the existing 128-KiB
transient reservation and Core releases its preparation bitmap at payload start
or cancellation. No table, setting, public shape or worker pool is added.

**321 metadata, 1,509 Native and 712 Core executions** pass without warnings in
`reports/settings-request-round-1/callback-scarcity-metadata.log`,
`callback-scarcity-ed2k-final.log` and `callback-scarcity-core-final.log`. The real
callback fixture checks accepted status rarity, expiry and zero inserted source
hints before retaining its start/skip/cancel and same-socket newer-token payload
checks. Metadata tests cover no-endpoint proof, geometry and authority fences,
and newer live status overriding an older reporter claim. An initial Native
compile rejected moving the borrowed bitmap; final Native/Core evidence follows
the bounded-copy correction. Normal hooks pass and the commit is pushed.

Rust `035de25c` aligns shared-peer eligibility and ordinary handoffs. The registry
leases the selected registered file while enforcing exclusive peer ownership;
source membership supplies no independent scheduling score or progress copy.
Other-file iteration borrows the source set, so Core filters lifecycle before
copying eligible plans and orders ordinary work by current remaining bytes,
then creation ID. NNP/FNF fallback picks one eligible ordinary transfer before
cloning it. Reask cooldowns, NNP holds, dead lists and explicit expiry pruning
keep their existing ownership.

All **713 Core executions** pass without warnings in
`reports/settings-request-round-1/shared-peer-alignment-core-final.log`.
Tests cover independent acquisition after release without concurrent engagement,
remaining bytes rather than total size, tie order and paused/completed exclusion;
existing ready/delivery, Busy, Kad, cooldown/NNP/FNF and disconnect checks pass.
The initial run identified an obsolete ranking assertion and a newly added
expiry check in the wrong layer. The final run keeps candidate expiry in pruning
and retains the cadence assertions. Normal hooks pass; the commit is pushed.
No Native, schema, setting or public API shape changes occur in this slice.

Rust `f3f7eacd` completes measured rarity ordering for eligible same-connection
handoff plans and deduplicates known reporter identities in active part counts.
Native sorts borrowed live observations, reuses one part bitset and counts each
known identity at most once per part; unidentified endpoints stay separate and
stale/no-status observations contribute nothing. Core releases its state lock
before bounded Native scarcity reads, uses the prepared peer's decoded HELLO
identity where available, and sorts rare handoffs ahead of remaining-byte and
creation-ID ties. No manifest hydration, peer acquisition, source truncation,
saved setting or public-shape change is introduced.

All **1,510 Native and 714 Core executions** pass without warnings in
`reports/settings-request-round-1/scarcity-consistency-ed2k-final.log` and
`scarcity-consistency-core-final.log`. Tests cover duplicate-identity bitmap
union, independent unidentified endpoints, stale/no-status and zero geometry,
real Native observation-backed handoff ranking and unchanged resident occupancy.
The reused size-aware Core fixture also keeps SQL geometry consistent with its
models; ordinary ordering and existing ready/callback/Busy/Kad cases pass.
An initial Native compile needed an explicit empty-vector assertion; final
evidence follows its correction. Normal hooks pass and the commit is pushed.

Rust `479a1c55` adds resource-safe rare-only burst promotion through the existing
attempt guard. Configured N remains the ordinary ceiling; active count cannot
exceed N + ceil(N/4). The adaptive window contributes a bounded extra allowance,
closes it under resident/work pressure and retains the shared active/preparing
cohort cap. Ordinary work cannot consume burst slots. Promotion keeps the same
owner, and lower limits drain actual owners without assuming pending work has
released capacity. Automatic mode derives its initial extra allowance from a
quarter of the current adaptive target, subject to actual Native admission.

Rust `cd210059` corrects the allowance to use hydration headroom for already-owned
ready sockets. Full connection capacity stops new probes, while a prepared
connection can reuse its existing slot; the shared cohort still caps count.
All **717 Core executions** pass without warnings in
`reports/settings-request-round-1/rare-burst-core.log` and the final
`rare-burst-owned-connection-core.log`. Tests cover N=1/4/5 rounding, ordinary
exclusion, pressure closure below the adaptive target, pending-owner drain and
connection reuse. The two-seed fixture holds the full count ceiling, frees one
slot, proves a real rare download starts above the ordinary limit, then frees
the other held owner and verifies both deliveries and disconnect cleanup.
Normal hooks pass; both commits are pushed. Public surfaces/schema are unchanged.

Rust `cfeb1a24` adds current-execution scheduling classification through the
existing Native blocking/read owner. A 1-MiB reservation covers bounded frequency
workspace; source references are checked against it before allocation and no
reporters are truncated. Reads borrow current cached manifests, reject stale
authority, try the job/cache gates without parking behind payload I/O, and return
only rarity, the shared block-leaser endgame classification and accepted-payload
counter/time. Waiting jobs never hydrate; temporary backing and resident read
loans outlive observer cancellation through the existing ownership machinery.

All **1,512 Native and 717 Core executions** pass without warnings in
`reports/settings-request-round-1/active-scheduling-ed2k-final.log` and
`active-scheduling-core-final.log`. New regressions cover cold/stale jobs, busy
job-I/O refusal, duplicate versus independent reporters, progress observations,
workspace refusal and final-verification protection at full 128-MiB resident
accounting occupancy. The initial full-residency fixture exceeded the per-request
reservation bound; the final run uses the suite's established fixed-size-credit
pattern without weakening the full-occupancy assertion. Normal hooks pass and
the commit is pushed. This is classification evidence, not completed displacement.

Rust `6de86094` wires rare-driven displacement. Core chooses the least recently
progressing ordinary owner, revalidates the ready opportunity after its Native
read, and rechecks the victim's token, accepted-byte version and protection.
One outstanding yield/drain blocks another displacement; the same control entry
remains active until actual producer/checkpoint retirement. A short admission
grace protects fresh readiness before live block acquisition is visible.
Native protects actual rare block leases and endgame, rather than letting a
queued rare-source bitmap protect a stalled slot indefinitely. Its runtime-only
yield signal leaves intent/resumable data intact, prevents new block claims,
and interrupts only the next framed read after accepted storage handlers settle.
Incomplete disposition closes that stream instead of reusing partial framing
or imposing an NNP hold. Idle/deferred Core execution observes the same signal.

All **1,513 Native and 718 Core executions** pass without warnings in
`reports/settings-request-round-1/safe-displacement-ed2k-final.log` and
`safe-displacement-core-acquisition.log`. Native tests cover stale/progress
rejection, rare acquisition versus queued availability, preserved Started intent,
and a real callback ending incomplete after only three bytes of its next frame.
The Core two-seed fixture supplies a controlled ordinary owner: it verifies the
yield request, retained count during Native retirement, actual guard release,
then rare admission and both real payload deliveries. An initial fixture omitted
persisted temp selection; final evidence uses the canonical selection path.
Normal hooks pass; the commit is pushed. This does not qualify sustained active
payload displacement, endgame contention, held filesystem I/O or either memory tier.

Next complete resource observability,
then payload/session qualification including structural snapshots, retained
session pins and held-I/O pressure. The new dependency still requires musl,
Android-target and other applicable platform qualification. GNU execution does
not prove adaptive pressure behavior or either memory-tier capacity campaign.
The accepted 64-MiB soft target, 128-MiB hard resident ceiling and
separate 8-MiB transient allowance stay unchanged; no new saved setting or second
worker pool is introduced. Owned unwrap, guard retention and private-hydration
lock ordering, ordinary SQL/cache/checkpoint publication, dirty membership and
checkpoint/cache-table backing, category batches and Native byte admission have
scoped evidence above; complete adaptive scheduling remains pending.
Earlier library/package receipts retain their
own source revisions.

Reads retain immutable pins; resident bytes survive cache eviction
and release through the existing admission wake control. MD4, peer/name,
delivery-evidence, AICH, content-metadata and ingest callbacks admit replacement
credit before SQL. Joint transient/resident admission avoids self-generated
retry wakes on rejection. AICH retires proposal geometry and transfers its
existing credit to publication instead of waiting with two full representations.
Routine contiguous incomplete appends publish one piece delta and dirty state
under the same lock boundary; their SQL acknowledgment compares selected pieces
without rewriting reader-pinned cache backing. Regressions cover unpinned
allocation reuse, immutable older readers, rejection before payload mutation,
and dirty acknowledgment after receipt/drain cancellation. Round eight's two
failed fixtures were corrected for prepublished progress and lazy payload
creation; round nine passes with exact pre-SQL progress validation and retained
cancellation assertions.

Hydration now separates diagnostic reads from selected activation. Before
inserting private streamed geometry, the existing owner holds category/content
and cache guards and validates the database observation and active generation
under a short SQLite writer fence. An already present dirty resident wins.
Regressions prove refusal after committed metadata changes, external writer
exclusion through publication, and preservation of newer cache-only progress.
The conservative observation can force retries after unrelated database writes;
its behavior under continuous indexing remains part of scale qualification.

Category publication now has a prepared native plan that retains the category
fence and reserves every affected execution before SQL. The blocking DB owner
publishes synchronously with admitted credit before replying; the async owner
can retain the same fence through Core state publication. Native tests prove
publication after SQL/observer cancellation under memory pressure, precommit
refusal without SQL changes, fence lifetime and multi-member removal while old
readers stay immutable. The owned Core category consumer integration now passes
the complete Core package, including category deletion and restart persistence;
REST publication remains outside that scoped result.

The full resident/retained-I/O scope is **not accepted yet**:
protocol sessions still retain old pins across appends, structural edits still
use full working snapshots, and actual held-I/O ownership remains unqualified.
The Core integration in local commit `78d127be` implements one SQLite-driven scheduler,
sixteen active slots and two metadata-preparation slots. Admission precedes
spawning; queued rows own neither workers nor timers. One retry clock drives
the selected cohort, and protocol callbacks wake their existing owner. Each
selection receives a fresh native execution generation; explicit healthy start
remains idempotent. Metadata preparation allocates no backing. UDP retirement
has an ordered completion receipt, and event handlers remain owned by their
consumer across disconnect. A storage-preparation failure persists an explicit-
start fault without replacing a foreign filesystem object.

Quiesced selection release now checkpoints only its job, transfers the exact
I/O guard into admitted native fencing/cache publication, and preserves started
intent and the fixed storage allocation. Tests cover partial-data reselection
and cancellation between SQL and cache publication without releasing that I/O
guard early. The scheduler yields after a completed network round with thirty
seconds of no received payload; it never times out in-flight I/O to rotate a
slot. The full Core package passes with this initial rotation policy.

Exact frozen-source evidence is retained under
`EMULEBB_WORKSPACE_OUTPUT_ROOT/reports/download-stop-progress-round-4/`.
The complete Core package passed: 570 unit tests and all integration targets,
including seven Kad swarm tests and actual download delivery. Native 1,433 tests
and metadata 215 unit plus three ownership tests passed. The rollback fixture's
test-only fault predicate was subsequently revised to avoid schema teardown;
metadata 215 plus three passed again under `reports/download-stop-progress-round-5/`.
Native/Core production inputs are unchanged by that fixture revision. These are local draft Core
integration results, not a pushed Core checkpoint. The category deletion fixture
now admits a download directly instead of starting an unrelated detached library
reload; native backpressure remains unchanged. Fourteen Core warnings remain for
removal with the remaining consumer refactor. Fairness under load, preparation
beyond unknown-size metadata discovery, final settings
binding, actual sixteen-plus-two load, held-I/O cancellation/drain, REST and
combined-scale qualification remain open. No total-RSS claim follows.

The acknowledged-progress stop defect is repaired in this frozen integration:
prefix appends flush before dirty publication; bitmap writes already did so.
The existing stop owner captures the exact bounded dirty delta and saves it
with the generation fence in one transaction through the shared progress
validator. Cache and dirty publication now share stop's content fence, and late
persisted acknowledgments cannot recreate stopped bookkeeping. Native progress
counts sparse bitmap bytes as well as prefixes. Tests prove exact prefix and
bitmap restoration after stop/restart, physical payload preservation, logical
stop while a later job I/O guard is held, rejection of late publication/handles,
and rollback of both progress and intent when the stop update fails. These
guard/gate tests do not establish actual held-OS-I/O qualification.

The separate persisted sparse-progress defect is corrected in local schema-83
provider `98f37249`: distinct prefix/presence scalars now maintain the job total
transactionally. [RUST-CI-044](RUST-CI-044.md) records the scoped native, metadata,
Core and existing Python-fixture evidence. Stop/restart tests now require the
persisted total to include sparse blocks as well as exact bitmap restoration.
The new provider and Core integration remain local pending the REST/application
consumer cut.

Require actual held-I/O cancellation/drain tests, query plans and parent/path
replacement races. The existing full catalog rebuild remains separate bounded
projection work; this conversion does not qualify it or total process RSS.

Connect logical removal to actual output cleanup through the job-native runtime
entry points `cleanup_removed_download_job(id)` and
`recover_removed_download_jobs_page(after, limit)`, using the existing retained
registry and shared cleanup-cap-one allowance. Compose internal retirement and
output reclamation inside one admitted attempt, rather than recursively taking
the public cleanup admission again. Capture compact token, delete intent,
recorded output ownership/path/fingerprint, delivery attempt, tombstone and
reservation authority before I/O. Tombstone phase advancement returns its actual
committed snapshot; successful, missing or safely preserved foreign objects
require explicit snapshot-checked settlement. Otherwise a helper can report
completion while stale journal authority still prevents final job removal.
Extend the existing delivery/reopen tests against this real path; no test-only
cleanup or synthetic job ownership may substitute for it.

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

## Tag REST contract qualification

Rust `47ee4f50` exposes immutable name resources, bounded global and
per-hash tag pages, and bulk-only assignment actions. Requests name one existing
tag and 1-100 distinct hashes; HTTP 207 preserves request order and reports each
hash independently. Creation returns 201 with Location, deletion returns an
empty 204, and assigning tags never creates content or tags implicitly. The
existing persistence owner and retained result charge remain authoritative.

The supported REST gate passed **152 unit and 3 integration tests**, with no
compiler warnings. The existing Python route/schema/response/conformance/smoke
suites passed **319 tests**. Evidence is retained below
`reports/library-tags-rest-round-1/{rest-2.log,python-3.log}`. OpenAPI now declares
the existing download PATCH 204 and the implemented 512-character cursor bound;
the shared conformance runner checks that 204 responses have empty wire bodies.
Harness `88764e74` extends the existing category restart campaign to exercise all
seven tag operations, unavailable-content retention, restart persistence, ordered
mixed outcomes, idempotent removal and deletion of assignments. The fresh regular
daemon and WebUI release build passed with zero warnings under
`logs/builds/20261117T195936Z-build-clients/build-result.json`. The source-bound
local campaign passed with graceful teardown: **83 generic route probes, zero
failed routes**, SSE, populated downloads, category storage/sharing, all seven
tag operations, real friend peers and Kad persistence. Its exact source revision
is `47ee4f5070f02323e37843c6ff3efd2dc11458f1`; retained runtime evidence is
`reports/rust-rest-openapi-ci/20261117T200236Z/report.json`, including the
`categoryPersistencePhase.libraryTags` assertions. Build/campaign console logs
are also under `reports/library-tags-rest-round-1/`.
Sharing enforcement, the bounded library browser, WebUI tags and combined scale
qualification remain open.

## Complete-file sharing admission foundation

Rust `5f871b55` applies the persisted hash sharing flag to the existing bounded
complete-copy eligibility batch. Independent verified internal download payloads
obey the same flag before physical probing can qualify them as a complete
source. Verified partial offers remain independent. This adds no schema version,
cache, thread or settings surface. Physical catalog/copy readers and internal
payload fingerprints remain unchanged: disabling sharing must not revoke an
already accepted physical snapshot or conceal content from library browsing.

Supported gates passed **234 metadata unit plus three profile-ownership tests**
and **1,442 eD2K unit tests**, with zero compiler warnings. Extended regressions
cover all-copy refusal/re-enable, retained physical catalog and copy metadata,
verified partial offers under a disabled flag, and internal-payload admission
without changing the captured physical snapshot. Evidence is retained below
`reports/library-sharing-admission-round-1/{metadata-2.log,ed2k-2.log}`.

This is the SQL/physical eligibility foundation, not complete live enforcement.
The normal clean-catalog admission shortcut still relies on its policy owner;
flag writes must use the existing content/stripe publication fence, update the
live catalog and publication demand, preserve accepted payload requests, and
cover normal waiter selection. Runtime mutation, REST/OpenAPI/WebUI exposure,
restart/wire proof and combined scale qualification remain open. The previously
staged daemon and native campaign remain attributed to Rust `47ee4f50`.

## Live sharing mutation and source-bound upload grants

Rust `aadd529a` extends the existing retained content-mutation owner with explicit
hash sharing writes. The owner reserves its existing workspace before admission,
commits under the content/stripe fence, publishes current eligibility and demand,
and retains admitted work after caller disconnect. Unknown hashes remain unknown;
unchanged writes are reported explicitly. A committed publication failure retains
the existing visible fault handling. Upload priority remains independent.

Complete publication selection, bounded local/internal hydration, reingestion and
manifest reobservation honor the persisted flag. Partial exchange remains eligible.
Clean admission checks the indexed live catalog; incomplete ownership/metadata
queries remain separate from payload admission. Materialized complete Kad/server
candidates cannot be admitted using a partial's eligibility. Ordinary waiter
selection borrows the current catalog without blocking or copying it; disabling
sharing performs no immediate queue sweep.

The listener acquires a source-bound verified reader for each granted payload
request. Existing complete readers may finish an already accepted request but
cannot authorize another one. When only a partial is eligible, a cached complete
reader is discarded and the exact partial job is opened instead of another
complete path. Physical fingerprints and payload snapshot equality remain intact.
No schema, setting, cache or persistence actor was added.

Supported gates passed **1,447 eD2K tests**, **598 Core unit plus 35 enabled
integration tests**, and **234 metadata unit plus three profile-ownership tests**,
with zero compiler warnings. New regressions prove disable/re-enable with retained
priority, idempotence and unknown hashes, accepted-reader continuity, cached-reader
refusal, cancellation-safe commit/publication/drain, restart/hydration, complete
copy plus independent partial, reingestion/progress, and normal waiter selection.
Existing callback, metadata, partial-offer and reader-cache tests also pass. Queue
algorithm fixtures now explicitly supply their synthetic catalog membership;
protocol-serving regressions use verified bytes. Evidence and exact source hashes:
`reports/library-sharing-runtime-round-1/{ed2k-3.log,core.log,metadata.log,source-freeze.json}`.
Normal commit checks passed under
`reports/local-check/emulebb-rust/20261117T204728Z-cdc7b83f/`.

Rust `4216e94a` also closes waiter admission after a committed publication fault.
The real root-epoch fence is held odd until the bounded publisher returns its
committed failure; the regression confirms the durable flag is disabled while
stale catalog entries cannot promote a waiter. Normal reconciliation alone does
not close the queue. The updated eD2K gate passed **1,447 tests** under
`reports/library-sharing-fault-round-1/ed2k.log`.

The later Core and REST/native checkpoints below extend this runtime proof.
WebUI library controls and combined scale qualification remain open.
The staged daemon and previous native tag campaign still belong to Rust `47ee4f50`;
these package gates do not claim a new staged campaign or complete foundation.

## Bounded sharing command qualification

Rust `d54cc252` connects explicit sharing batches to the existing profile owner
and retained native mutation path. The complete selection is validated before
admission: 1-100 distinct canonical hashes and an explicit enabled value. The
existing 64-slot/8-MiB owner reserves request backing and the common 64-KiB result
workspace before cloning inputs. Admitted batches finish every hash in request
order after caller disconnect, including later items after a known SQL failure.
Results distinguish changed, unchanged, missing and typed persistence failures;
committed publication failure and unknown outcomes retain their existing meaning.
The common retained library reply and hash validation also serve tags, with no
second worker, actor, mutation path or settings authority.

Supported gates passed **603 Core unit plus all 35 enabled integrations** and
**152 REST unit plus three integrations**, with zero compiler warnings. New
regressions prove retained result charge through projection/serialization,
ordered mixed outcomes and no implicit content creation, disconnect-independent
completion, pre-mutation shared-slot refusal, invalid selection refusal and
continuation after a per-item SQL failure. Evidence and exact source hashes:
`reports/library-sharing-owner-round-1/{core.log,rest.log,source-freeze.json}`.
Normal commit checks passed under
`reports/local-check/emulebb-rust/20261117T210730Z-e8108ab6/`.

This backend command proof is supplemented by the REST/native checkpoint below.
WebUI library controls and scale qualification remain open.

## Sharing REST and native wire qualification

Rust `73aa76ef` exposes `POST /library/files/sharing` with the qualified bulk
command. The response is HTTP 207 with ordered hash outcomes; input validation
and global admission errors happen before mutation. Sharing and tag actions use
one typed hash-outcome transport shape. Whole-request and per-item persistence
errors share their status, code and commit details through the existing mapper.
OpenAPI specifies the current boolean, common hash selection and fixed outcome
shapes without another mutation path or configuration authority.

The supported REST package gate passed **156 unit plus three integration tests**,
with zero compiler warnings. The normal affected-file push gate passed **349
Python tests**, including the current route/schema, response conformance,
observer/codec, shared smoke and campaign checks. Exact retained evidence:
`reports/library-sharing-rest-round-1/{rest.log,conformance.log,peer-wire.log}`
and `reports/local-check/emulebb-build-tests/20261117T214313Z-196d522e/02.log`.

The regular daemon and WebUI release build passed with zero warnings under
`logs/builds/20261117T213213Z-build-clients/build-result.json`. Harness `35e5b75a`
reuses the existing transport and HELLO encoder with explicit peer framing,
including valid eMule protocol packets. The existing restart campaign passed
with graceful teardown, **83 generic probes and zero failed routes**, SSE,
populated downloads, category storage/sharing, tags, friend peers and Kad.

The actual HTTP-to-wire proof keeps an established peer connection and cached
complete reader across disable/re-enable while two copies remain eligible. The
new disabled request receives an explicit no-file response; re-enable returns
the exact expected bytes. The same profile reopens with the flag still disabled,
refuses a new peer, then serves correct bytes after explicit re-enable. Mixed
ordered outcomes, idempotence, unavailable-content policy, unknown-hash absence,
tag retention and unchanged fixture bytes also passed. The report retains all
**28 wire frames** and each qualified sharing assertion:
`reports/rust-rest-openapi-ci/20261117T214032Z/report.json`,
`categoryPersistencePhase.librarySharing`. Its exact binary source is
`73aa76ef9f9cee73817b58b0954eded1928cb0b1`.

WebUI library controls, incremental indexed library reads and combined scale
qualification remain open; this does not close the full foundation scope.

## Incremental physical library index checkpoint (2026-11-17)

The physical catalog uses incremental per-content reconciliation under
schema 86. The
SQLite change index retains one latest revision per affected content identity,
including deletion tombstones, rather than accumulating events. Connections
track their own durable position and pending session verification changes;
another connection cannot consume their notifications. Root, copy, path and
delivery-exclusion changes update affected content. Tags, sharing policy and
statistics are read from their owners without rebuilding physical membership. Unchanged
verification fingerprints enqueue no work, including repeated observations
through the normal path-admission writer. Admission still reports success for
matching evidence without replacing the session row.

The existing 100k catalog fixture now protects unrelated projection rows against
deletes during one-content changes, exercises session withdrawal/restoration and
second-connection path changes, verifies policy/tag and unchanged-evidence writes
do not rebuild membership, and requires an indexed revision seek. Existing alias,
root withdrawal, sharing-policy and eligibility assertions remain active.

Scoped checks passed: metadata **234 unit + 3 profile-ownership tests**, Core
**603 unit + 35 integration tests**, and eD2K **1,447 tests**. The final
unchanged-evidence guard was followed by the complete metadata suite and normal
branch checks. Logs: `reports/library-incremental-index-round-1/`.
The regular daemon/WebUI build passed with **zero warnings**:
`logs/builds/20261117T220712Z-build-clients/build-result.json`.
The existing native REST/OpenAPI harness passed with graceful teardown against
exact Rust revision `825df4c8280be007dc45b005e52c77d27ea5adcc`:
`reports/rust-rest-openapi-ci/20261117T221004Z/report.json`.
The native report covers that exact revision; it does not qualify subsequent
source changes. Normal Rust commit/push hooks passed. All scoped commits remain
on the existing foundation branch, without a PR or merge.

The location-read checkpoint is Rust `e56a9a94`, including the admission
writer fix `4a987b63`. `library_locations` returns retained path observations
using content/path keyset seeks, at most 200 rows and a caller-reserved allowance
capped at 1 MiB. Lengths are checked before native-path decoding. A byte-limited
page resumes before the first omitted path. Reads expose cached verification,
root and exclusion facts without filesystem probes or granting serving authority.
Unknown and remote-observation-only hashes differ from verified library content
that has no remaining copies. Root withdrawal and identity exclusion retain
location knowledge.

The existing 100k fixture proves late-copy seeks and indexed path membership/root
lookups with multiple configured roots, without temporary sorting. Dedicated
checks cover row/byte limits, resumption, oversized native paths, process-local
verification, copyless content, passive observations and inaccessible/disabled
roots. The existing paired-identity exclusion fixture checks retained excluded
locations. The complete metadata suite passed **238 unit + 3 ownership tests**;
eD2K passed **1,447 tests** after both changes. Evidence:
`reports/library-location-reads-round-1/{metadata.log,ed2k.log}` and
`reports/library-incremental-index-round-1/verification-writer.log`.
The new locations reader is not yet exposed through REST. The Present-view
boundary (current roots versus verified copies outside them) awaits the operator;
locations deliberately expose separate facts so that decision is not guessed.

This qualifies the physical index maintenance slice. Canonical library visibility
views, display-name-only search, public locations, statistic sorts and WebUI controls
remain open, as do the remaining settings/CLI/Docker work and combined resource
qualification. This is not full library-read or foundation acceptance.

## Upload accounting and timestamp checkpoint

Current Rust revision `e53c07c2` counts one accepted upload stint when its first
verified payload is ready, using the existing upload-work lease. Repeated
packets share the acceptance marker; slot recycling or a file-hash switch starts
a fresh stint. Queue grants, empty/rejected ranges and failed verified reads do
not themselves count as accepted service. Accepted-session events join file-byte
and peer-credit deltas in the existing batch transaction and release flush.
Ordinary checkpoint failure rolls back the batch and restores its deltas,
including additions arriving before retry.

Fresh-profile schema **87** stores `last_upload_requested_at_s` and
`last_uploaded_at_s` as nullable Unix-second values. An absent event stays null;
an explicit epoch-zero event stays zero. A refused known-hash request records
demand without advancing actual-upload time. Positive transmitted payload-byte
events carry their capture time through the existing ledger, retaining the latest
time across coalescing, failure and retry. Metadata validation rejects negative
times and an actual-upload time without a byte event. Existing consumers,
publication calculations, MFC import models, corpus fixtures and Python metadata
helpers use the coordinated current shape. The profile-import exchange exports
`lastUploadRequestedAtSeconds`; its parsed MFC timestamp remains in seconds.

Scoped validation passed: metadata **239 unit + 3 ownership tests**, daemon
**123 tests** (its isolated ownership-child fixture is deliberately invoked by
parent tests), Core **603 unit + 35 integration tests**, and eD2K **1,449 tests**.
The selected Python suites passed **81 tests**, including the normal push gate.
Logs: `reports/library-upload-timestamps-round-1/`. Checks cover null/zero,
ordering, invalid events, transaction rollback, retry/reopen, publication
consumers, import/export units and the existing 100k metadata fixtures.

The regular daemon/WebUI build passed with **zero warnings**:
`logs/builds/20261117T231722Z-build-clients/build-result.json`.
Harness commit `1aaa5322` extends the existing native peer scenario. Exact Rust
revision `e53c07c290cc0c5cba47b338f21f4bd76514bee5` passed native REST/OpenAPI
validation with graceful teardown:
`reports/rust-rest-openapi-ci/20261117T232041Z/report.json`.
`categoryPersistencePhase.uploadAccounting` proves **six requests and two
accepted stints**; `uploadTimestamps` proves null initial times, Unix-second
request/upload values, persistence across restart and unchanged last actual
upload time during a refused request. Existing sharing, category, tag, download,
friend and Kad checks passed. Source commits are pushed on the existing feature
branches, without a PR or merge. This report covers its explicitly recorded
source revision; the subsequent process-accounting checkpoint is below.

This closes accepted-stint attribution, its batch retention and the upload-event
timestamp shape. Raw-request batching, process-session statistics independent of
catalog rebuilds, indexed statistic sorting and the canonical library REST/UI
surface remain open at that revision. Other persisted/public timestamp domains
still need their coordinated foundation cut, and combined resource qualification
remains open.

## Process-owned file statistics checkpoint

Rust `47c01eaa` retains per-hash session statistics in the existing accounting
ledger, independently of serving catalog membership. Clearing, replacing or
rebuilding a serving projection does not reset session totals or reconstruct
them from incoming projection data. Checkpoints drain dirty deltas without
draining process statistics. A new runtime starts session counters at zero and
merges committed lifetime facts. No database shape or settings were added.

Byte and accepted-stint events update the owner before a nonblocking catalog
projection attempt. Raw demand retains a known client's process request count
even if its SQL write fails; successful writes do not count the request twice.
The existing request statement now returns committed lifetime facts and bounded
client classification in one indexed statement, fully stepping its RETURNING
rows before exposing success. Passive-only and unknown demand do not allocate
permanent client session records. Request timestamps retain nullable Unix
seconds, including explicit epoch zero, through projection replacement.

Scoped checks passed: metadata **239 unit + 3 ownership tests**, Core **603 unit and
35 integration tests**, and eD2K **1,454 tests**. Evidence is under
`reports/library-session-accounting-round-1/`. The Core check precedes the final
private request-error capture and statement-completion changes; the final eD2K,
metadata, normal branch checks and regular build cover those changes. Tests
include catalog removal/rebuild, checkpoint/restart boundaries, held catalog
read locks, rejected request writes and epoch-zero preservation. Existing
admission/ingest fixtures now capture real events instead of injecting session
statistics into serving entries; their behavioral assertions remain intact.

The regular daemon/WebUI build passed with **zero warnings**:
`logs/builds/20261118T003547Z-build-clients/build-result.json`.
The existing Python native REST/OpenAPI campaign passed on exact revision
`47c01eaa` with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T003846Z/report.json`.
It retains the real-peer request/stint, timestamp/restart, sharing and other
existing contract checks. No new launcher or replacement harness was added.
Rust is committed and pushed on the existing feature branch; no PR or merge.

This closes process counter ownership across serving-cache changes, not the
entire accounting contract. Raw requests still perform synchronous SQL and are
not checkpoint-batched; failed request persistence is not restored by this
slice. Indexed statistic sorts, canonical library REST/WebUI and combined
resource qualification remain open. The Present and All Known membership
decisions are pending in the authoritative foundation specification. The next
independent accounting slice is raw-request batching through the existing owner.

## Upload demand ownership and checkpoint qualification

Rust `1123c6db` captures request counts and last-request
times in the existing credit/file ledger. Registered hashes need no SQLite call
on request capture. Requests, bytes, accepted stints and peer credits checkpoint
in one transaction; failure rolls the transaction back and restores all deltas,
including requests arriving before retry. Counters saturate within SQLite's
integer range, and nullable request times retain epoch zero and maximum event
time. No persistent schema change, settings, or additional accounting worker.

Cold hashes use a read-only indexed snapshot and capture in one admitted command
under the existing local-mutation registry. Its fixed 4 KiB temporary-work charge
fits the existing four-command/8 MiB owner; no filesystem admission is required.
Admission precedes capability clones and task spawning. The tracked command
captures counters and publication notification even after the peer drops its
receipt; a cancelled drain waiter does not release its charge or task ownership.
Closing/saturated admission captures nothing. Waiting for capacity holds only a
fixed hash and timestamp, with no SQL retry. Final drain joins admitted commands
before the accounting checkpoint. Unknown demand creates no metadata or
accounting record. Passive-only demand coalesces while dirty without permanently
allocating client session state. Selected physical-library rows merge committed scalar
totals with the process owner, so current reads do not wait for a checkpoint or
hydrate the full serving catalog. This does not yet implement canonical library
statistic sorting.

One reservation covers the scheduled and executing background flush. Concurrent
producers cannot enqueue duplicate flush tasks; dropping queued work releases
the reservation. Session release remains a best-effort flush. Final persistence
drain additionally attempts a required accounting checkpoint after network
teardown, before profile release. This covers refused-only demand without an
upload session to release. Required checkpoint failure returns an error and
retains failed deltas rather than silently claiming durable shutdown.

Scoped checks passed: eD2K **1,457 tests** and the selected existing Python suite
**22 tests**, under `reports/library-cold-demand-round-1/`. New tests hold the
actual command at its scheduling gate, cancel its real request caller and first
drain waiter, then prove retained charge, closed admission, joined capture,
notification and durable checkpoint. Saturated admission and unknown-hash
noncreation are also covered. Existing tests cover capture while a SQLite writer
and catalog reader are held, transaction rollback across peer/file accounting,
exactly-once retry, optional times and single-flight reservation release.
Metadata and Core sources are unchanged in this slice; prior **239 metadata unit
and 3 ownership tests** and **603 Core unit + 35 integration tests** remain valid
under `reports/library-request-batching-round-1/`. The regular build and native
campaign below cover the final integration. Normal commit/push gates passed.

The final regular daemon/WebUI build passed with **zero warnings**:
`logs/builds/20261118T012126Z-build-clients/build-result.json`.
Harness `80b66028` extends the existing Python peer scenario; its native
REST/OpenAPI campaign passed on exact Rust
`1123c6db375857cf190112ccaa46bd177a9fe623`, with graceful teardown:
`reports/rust-rest-openapi-ci/20261118T012424Z/report.json`.
`categoryPersistencePhase.uploadAccounting` proves **seven requests and two
accepted stints**, current in-session REST totals, policy refusal without extra
acceptance, refused-only demand surviving clean shutdown/reopen, and demand for
a retained hash without any copy under a current shared root. The unavailable
hash gains neither accepted-service counts nor payload authority. Existing
timestamp, sharing, category, tag, download, friend and Kad checks passed.
Rust and harness commits are pushed on their existing feature branches. No PR
or merge was created.

This qualifies admitted cold-demand retention as well as registered capture,
batch retention, live scalar reads and the final checkpoint; it does not close
this owner or the foundation goal. Canonical library views and indexed live-stat
sorting, the operator's library membership decisions, remaining settings/CLI/
Docker work and combined resource qualification remain open. Sustained soak
remains explicitly deferred follow-up.

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
